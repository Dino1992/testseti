from django.shortcuts import render, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.http.response import HttpResponse
from quiz.models import Theme, Answer, Question
import random

# Create your views here.


def themes_view(request):
    themes = Theme.objects.all()
    # Возвращаем HttpResponse со списком тем (см. quiz/templates/index.html)
    return render(request, 'index.html', {'themes': themes})


def init_session(request):
    """
    Функция, вызываемая при выборе какой-либо темы, инициализирует
    начальные значения в сессии.
    """
    # Здесь и далее `pk` = primary key или id
    # Получаем pk темы
    theme_pk = request.GET.get('theme_pk')
    if theme_pk is not None:
        try:
            # Получаем тему по pk
            theme = Theme.objects.get(pk=theme_pk)
        except ObjectDoesNotExist as ex:
            print(ex)
            return
        # Получаем список вопросов в виде листа, ...
        questions_list = list(theme.get_question())
        # ... перемешиваем спиок, ...
        random.shuffle(questions_list)
        # ... берем не более 15 первых вопросов.
        questions = questions_list[:15]
        # В сессии запоминаем порядок вопросов, а также создаем массив ответов
        # и индекс текущего вопроса
        request.session['questions'] = tuple(map(lambda t: t.pk, questions))
        request.session['answers'] = [None] * len(questions)
        request.session['question_idx'] = 0


def init_common_test_session(request):
    # Из всех вопросов выбираем не более 60 случайных
    questions_list = list(Question.objects.all())
    random.shuffle(questions_list)
    questions = questions_list[:60]
    # См. init_session(request)
    request.session['questions'] = tuple(map(lambda t: t.pk, questions))
    request.session['answers'] = [None] * len(questions)
    request.session['question_idx'] = 0


def finish_session(request):
    """
    Функция, вызываемая при завершении тестирования, подсчитывает количество
    правильных ответов и возвращает их и общее количество вопросов.
    """
    # Из сессии получаем список pk вопросов и ответов
    questions = request.session['questions']
    answers = request.session['answers']
    total_questions = len(questions)
    correct_answers = 0
    # Произвоим подсчет правильных ответов
    for question_pk, answer_pk in zip(questions, answers):
        # Получаем объект вопроса по pk
        question = Question.objects.get(pk=question_pk)
        # Пытаемся получить ответ по pk (answer_pk может быть None,
        # если пользователь не ответил на вопрос)
        answer = None
        try:
            answer = Answer.objects.get(pk=answer_pk)
        except ObjectDoesNotExist as ex:
            pass
        # проверяем корректность ответа
        if answer in question.get_answers() and answer.is_correct:
            correct_answers += 1
    return correct_answers, total_questions


def question_view(request):
    """
    Представление страницы с вопросами
    """

    # Проверяем, есть ли ответ на текущий вопрос, и если да, то запоминаем
    answer = request.GET.get('answer')
    question_idx = request.session.get('question_idx')
    session_answers = request.session.get('answers')
    if answer is not None \
            and question_idx is not None \
            and session_answers is not None:
        idx = int(question_idx)
        session_answers[idx] = int(answer)

    # Обрабатываем различные действия, которые могли произойти
    action = request.GET.get('action')
    if action == 'init':
        init_session(request)
    elif action == 'common_test':
        init_common_test_session(request)
    elif action == 'next':
        request.session['question_idx'] += 1
    elif action == 'prev':
        request.session['question_idx'] -= 1
    elif action == 'finish':
        correct_answers, total_questions = finish_session(request)
        return render(request, 'results.html',
                      {'correct_answers': correct_answers,
                       'incorrect_answers': total_questions - correct_answers})

    # Если тест еще не завершен, отображаем текущий вопрос и варианты ответа.
    # Если пользователь уже отвечал на вопрос, то ответ будет отмечен.
    questions = request.session.get('questions')
    question_idx = request.session.get('question_idx')
    answers = request.session.get('answers')
    question = Question.objects.get(pk=questions[question_idx])
    theme = question.theme
    return render(
        request, 'question.html',
        {'theme': theme,
         'question': question,
         'answers': question.get_answers(),
         'first_question': question_idx == 0,
         'last_question': (question_idx + 1) == len(questions),
         'choice': answers[question_idx]})


def test(request):
    for i in range(25):
        theme = Theme(name='Test #{}'.format(i))
        theme.save()
        for j in range(30):
            question = Question(text='Question #{}'.format(j), theme=theme)
            question.save()
            for k in range(4):
                answer = Answer(question=question,
                                text='Answer #{}'.format(k),
                                is_correct=(k == j % 4))
                answer.save()
    return HttpResponse('ok')
