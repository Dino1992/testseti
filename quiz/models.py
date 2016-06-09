from django.db import models

# Create your models here.


class Theme(models.Model):

    name = models.CharField(max_length=256)

    def get_question(self):
        return Question.objects.filter(theme=self)

    def get_question_count(self):
        return Question.objects.filter(theme=self).count()

    def __str__(self):
        return self.name


class Question(models.Model):

    theme = models.ForeignKey(Theme)
    text = models.CharField(max_length=256)

    def get_answers(self):
        return Answer.objects.filter(question=self)

    def __str__(self):
        return self.theme.name + ': ' + self.text


class Answer(models.Model):

    question = models.ForeignKey(Question)
    text = models.CharField(max_length=256)
    is_correct = models.BooleanField()

    def __str__(self):
        return self.text + (' (true)' if self.is_correct else '')
