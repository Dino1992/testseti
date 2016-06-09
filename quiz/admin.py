from django.contrib import admin
from nested_inline.admin import NestedStackedInline, NestedTabularInline, NestedModelAdmin
from quiz.models import Theme, Question, Answer

# Register your models here.


class AnswerAdmin(NestedStackedInline):

    model = Answer
    max_num = 4


class QuestionAdmin(NestedTabularInline):

    model = Question
    inlines = [
        AnswerAdmin
    ]


@admin.register(Theme)
class ThemeAdmin(NestedModelAdmin):

    inlines = [
        QuestionAdmin
    ]
