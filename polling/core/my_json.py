# -*- coding: utf-8 -*-

import json
import re
import simplejson
from decimal import Decimal

from django.db import models
from django.core.exceptions import ImproperlyConfigured
from django.core.serializers.json import DjangoJSONEncoder

try:
    from dateutil import parser as date_parser
except ImportError:
    raise ImproperlyConfigured(
        'The "dateutil" library is required and was not found.')


try:
    JSON_DECODE_ERROR = simplejson.JSONDecodeError  # simplejson
except AttributeError:
    JSON_DECODE_ERROR = ValueError  # other


TIME_RE = re.compile(r'^\d{2}:\d{2}:\d{2}')
DATE_RE = re.compile(r'^\d{4}-\d{2}-\d{2}(?!T)')
DATETIME_RE = re.compile(r'^\d{4}-\d{2}-\d{2}T')


class JSONDecoder(simplejson.JSONDecoder):
    """ Recursive JSON to Python deserialization. """

    _recursable_types = [str, list, dict]

    def _is_recursive(self, obj):
        return type(obj) in JSONDecoder._recursable_types

    def decode(self, obj, *args, **kwargs):
        if not kwargs.get('recurse', False):
            obj = super().decode(obj, *args, **kwargs)
        if isinstance(obj, list):
            for i in xrange(len(obj)):
                item = obj[i]
                if self._is_recursive(item):
                    obj[i] = self.decode(item, recurse=True)
        elif isinstance(obj, dict):
            for key, value in obj.items():
                if self._is_recursive(value):
                    obj[key] = self.decode(value, recurse=True)
        elif isinstance(obj, basestring):
            if TIME_RE.match(obj):
                try:
                    return date_parser.parse(obj).time()
                except ValueError:
                    pass
            if DATE_RE.match(obj):
                try:
                    return date_parser.parse(obj).date()
                except ValueError:
                    pass
            if DATETIME_RE.match(obj):
                try:
                    return date_parser.parse(obj)
                except ValueError:
                    pass
        return obj


class JSONField(models.TextField):
    """ Stores and loads valid JSON objects. """

    description = 'JSON object'

    def __init__(self, *args, **kwargs):
        self.default_error_messages = {
            'invalid': ('Enter a valid JSON object')
        }
        self._db_type = kwargs.pop('db_type', None)
        # self.simple_formfield = kwargs.pop('simple_formfield', False)

        encoder = kwargs.pop('encoder', DjangoJSONEncoder)
        decoder = kwargs.pop('decoder', JSONDecoder)
        encoder_kwargs = kwargs.pop('encoder_kwargs', {})
        decoder_kwargs = kwargs.pop('decoder_kwargs', {})
        if not encoder_kwargs and encoder:
            encoder_kwargs.update({'cls': encoder})
        if not decoder_kwargs and decoder:
            decoder_kwargs.update({'cls': decoder, 'parse_float': Decimal})
        self.encoder_kwargs = encoder_kwargs
        self.decoder_kwargs = decoder_kwargs

        kwargs['default'] = kwargs.get('default', '')
        kwargs['help_text'] = kwargs.get(
            'help_text', self.default_error_messages['invalid'])

        super().__init__(*args, **kwargs)

    def db_type(self, *args, **kwargs):
        if self._db_type:
            return self._db_type
        return super(JSONField, self).db_type(*args, **kwargs)
    
    def to_python(self, value):
        if value is None:  # allow blank objects
            return None
        if isinstance(value, basestring):
            try:
                value = json.loads(value, **self.decoder_kwargs)
            except JSON_DECODE_ERROR:
                pass
        return value

    def get_db_prep_value(self, value, *args, **kwargs):
        if self.null and value is None and not kwargs.get('force'):
            return None
        return json.dumps(value, **self.encoder_kwargs)

    def value_to_string(self, obj):
        return self.get_db_prep_value(self._get_val_from_obj(obj))

    def value_from_object(self, obj):
        return json.dumps(super().value_from_object(obj),
                          **self.encoder_kwargs)

    def formfield(self, **kwargs):
        defaults = {
            # 'simple': self.simple_formfield,
            # 'encoder_kwargs': self.encoder_kwargs,
            # 'decoder_kwargs': self.decoder_kwargs,
        }
        defaults.update(kwargs)
        return super().formfield(**defaults)

    def contribute_to_class(self, cls, name):
        super().contribute_to_class(cls, name)

        def get_json(model_instance):
            return self.get_db_prep_value(
                getattr(model_instance, self.attname, None), force=True)
        setattr(cls, 'get_%s_json' % self.name, get_json)

        def set_json(model_instance, value):
            return setattr(model_instance, self.attname, self.to_python(value))
        setattr(cls, 'set_%s_json' % self.name, set_json)

