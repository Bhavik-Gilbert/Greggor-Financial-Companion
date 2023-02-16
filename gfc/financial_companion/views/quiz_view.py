from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django import forms
from django.contrib import messages
import random
from ..models import QuizQuestion, QuizScore, User


@login_required
def quiz_view(request: HttpRequest, question_total: int = 5) -> HttpResponse:
    """View to start quizzes"""

    user: User = request.user
    quiz_scores: list[QuizScore] = QuizScore.objects.filter(user=user)
    question_total = int(question_total)

    if request.method == "POST":
        if "start_quiz" in request.POST:
            return redirect("quiz_questions", question_total=question_total)

    top_quiz_scores: list[QuizScore] = []
    recent_quiz_scores: list[QuizScore] = []
    if len(quiz_scores) >= 5:
        recent_quiz_scores = quiz_scores[0:5]
        quiz_scores.sort(key=lambda score: score.get_score)
        top_quiz_scores = quiz_scores[0:5]

    elif len(quiz_scores) > 0:
        recent_quiz_scores = quiz_scores[0:len(quiz_scores)]
        quiz_scores.sort(key=lambda score: score.get_score)
        top_quiz_scores = quiz_scores[0:len(quiz_scores)]

    return render(request, "pages/quiz.html", {
        "top_quiz_scores": top_quiz_scores,
        "recent_quiz_scores": recent_quiz_scores,
        "question_total": question_total,
        "quiz_total_choices": [5, 10, 15, 20]
    })


@login_required
def quiz_question_view(request: HttpRequest,
                       question_total: int) -> HttpResponse:
    """View to partake in quizzes"""
    question_total = int(question_total)
    print(question_total)

    if QuizQuestion.objects.count() < question_total:
        messages.add_message(
            request,
            messages.WARNING,
            'Not enough questions in database to start quiz')
        return redirect("quiz")

    quiz_questions: list[QuizQuestion] = random.sample(
        QuizQuestion.objects.all(), question_total)

    return render(request, "pages/quiz_questions.html", {
        "quiz_questions": quiz_questions
    })
