from django.conf.urls import url
import quiz.views

urlpatterns = [
    url(r'^$', quiz.views.themes_view),
    url(r'^question$', quiz.views.question_view),
    url(r'init', quiz.views.test)
]