
from django.db import models
from django.utils import timezone

from polling.core import JSONField


# Create your models here.



class Question(models.Model):

    TXT = 'txt'
    SIMPLE = 'simple'
    MULTI = 'multi'

    QUESTION_TYP_CHOICES = (
            (TXT, 'Your text'),
            (SIMPLE, 'The one option'),
            (MULTI, 'Several options'),
    )

    text = models.CharField(max_length=1024)

    typ = models.CharField(max_length=16, choices=QUESTION_TYP_CHOICES)

    options = JSONField(default="[]")



    class Meta:
        app_label = 'polls'
        verbose_name = 'Question'
        verbose_name_plural = 'Questions'

    def __str__(self):
        return  '%s (%s)' % (self.text, self.typ)


class Poll(models.Model):

    title = models.CharField(max_length=1024)

    deleted = models.BooleanField(default=False)
    
    created = models.DateTimeField(auto_now_add=True)

    finish_at = models.DateTimeField()

    questions = models.ManyToManyField(Question, related_name='polls')


    class Meta:
        app_label = 'polls'
        get_latest_by = 'created'
        ordering = ['-created']
        verbose_name = 'Poll'
        verbose_name_plural = 'Polls'

    def __str__(self):
        return self.title

    @property
    def is_alive(self):
         return self.finish_at > timezone.now()



