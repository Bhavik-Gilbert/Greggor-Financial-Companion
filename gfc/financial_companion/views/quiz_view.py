from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import random
from ..models import QuizQuestion, QuizScore, QuizSet, User
from ..helpers import paginate, ScoreListOrderType


@login_required
def quiz_view(request: HttpRequest, sort_type: str = ScoreListOrderType.RECENT, question_total: int = 5) -> HttpResponse:
    """View to start quizzes"""

    user: User = request.user
    quiz_scores: list[QuizScore] = QuizScore.objects.filter(user=user)
    question_total = int(question_total)

    if len(quiz_scores) > 0:
        if sort_type == ScoreListOrderType.HIGHEST:
            pagenated_quiz_scores: list[QuizScore] = paginate(request.GET.get('page', 1), sorted(quiz_scores, key=lambda score: score.get_score(), reverse=True))
        else:
            pagenated_quiz_scores: list[QuizScore]  = paginate(request.GET.get('page', 1), quiz_scores)

    return render(request, "pages/quiz/quiz.html", {
        "quiz_scores": pagenated_quiz_scores,
        "score_order_type": sort_type,
        "score_list_order_types": ScoreListOrderType,
        "question_total": question_total,
        "quiz_total_choices": [5, 10, 15, 20]
    })


@login_required
def quiz_ready_view(request: HttpRequest,
                       question_total: int) -> HttpResponse:
    """View to generate quizzes"""
    question_total = int(question_total)
    if QuizQuestion.objects.count() < question_total:
        messages.add_message(
            request,
            messages.WARNING,
            'Not enough questions in database to start quiz')
        return redirect("quiz")

    quiz_questions: list[QuizQuestion] = random.sample(
        list(QuizQuestion.objects.all()), question_total)

    if not QuizSet.set_exists(quiz_questions):
        quiz_set: QuizSet = QuizSet.objects.create(
            seeded = False
        )
        
        for question in quiz_questions:
            quiz_set.questions.add(question)
    else:
        quiz_set: QuizSet = QuizSet.get_set_from_questions(quiz_questions)

    if quiz_set is None:
        messages.add_message(
            request,
            messages.ERROR,
            "Quiz couldn't be generated")
        return redirect("quiz") 

    return render(request, "pages/quiz/quiz_ready.html", {
        "quiz_set": quiz_set
    })

@login_required
def quiz_question_view(request: HttpRequest, pk: int) -> HttpResponse:
    """View to partake in quizzes"""

    user: User = request.user
    try:
        quiz_set: QuizSet = QuizSet.objects.get(id=pk)
    except Exception:
        messages.add_message(
            request,
            messages.ERROR,
            "The quiz specified does not exit")
        return redirect("quiz")
    
    if request.method == "POST":
        if "quiz_submit" in request.POST:
            total_questions: int = quiz_set.questions.count()
            correct_answers: int = 0
            for quiz_question in quiz_set.questions.all():
                try:
                    response_answer: str = request.POST[str(quiz_question.id)]
                    if quiz_question.is_answer(response_answer):
                        correct_answers += 1
                except Exception:
                    total_questions -= 1
                
            quiz_score: QuizScore = QuizScore.objects.create(
                user=user,
                total_questions=total_questions,
                correct_questions=correct_answers,
                quiz_set=quiz_set
            )

            return redirect("quiz_score", pk=quiz_score.id)

    return render(request, "pages/quiz/quiz_questions.html", {
        "quiz_set": quiz_set
    })

@login_required
def quiz_score_view(request: HttpRequest, pk: int) -> HttpResponse:
    """View to show score after quiz"""
    user: User = request.user

    try:
        quiz_score: QuizScore = QuizScore.objects.get(id=pk, user=user)
    except Exception:
        messages.add_message(
            request,
            messages.ERROR,
            "The score specified does not exit")
        return redirect("quiz")

    return render(request, "pages/quiz/quiz_score.html", {
        "quiz_score": quiz_score
    })
