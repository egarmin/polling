# from django.shortcuts import render

from rest_framework import viewsets
from rest_framework import permissions

# from django.contrib.auth.models import User, Group

from polling.app.api.serializer import PollSerializer, QuestionSerializer
from polling.app.polls.models import Poll, Question


class PollViewSet(viewsets.ModelViewSet):

    queryset = Poll.objects.filter(deleted=False).order_by('-created')

    serializer_class = PollSerializer
    # permission_classes = [permissions.IsAuthenticated]


class QuestionViewSet(viewsets.ModelViewSet):

    queryset = Question.objects.all()

    serializer_class = QuestionSerializer



