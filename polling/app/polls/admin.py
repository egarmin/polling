from django.contrib import admin

from polling.app.polls.models import Poll, Question

class PollAdmin(admin.ModelAdmin):

    list_display = (
        'title', 'created', 'finish_at', 'is_alive', 'deleted',)


class QuestionAdmin(admin.ModelAdmin):
    pass


admin.site.register(Poll, PollAdmin)
admin.site.register(Question, QuestionAdmin)
