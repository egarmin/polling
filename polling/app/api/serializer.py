
from rest_framework import serializers

from polling.app.polls.models import Poll, Question


class PollSerializer(serializers.HyperlinkedModelSerializer):
    
    class Meta:
        model = Poll
        fields = ['title', 'finish_at', 'questions']


class QuestionSerializer(serializers.HyperlinkedModelSerializer):
    
    class Meta:
        model = Question
        fields = ['text', 'typ', 'data']

