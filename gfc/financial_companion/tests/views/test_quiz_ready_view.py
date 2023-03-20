from .test_view_base import ViewTestCase
from django.http import HttpResponse
from financial_companion.models import User, QuizQuestion, QuizSet
from django.urls import reverse
from django.contrib.messages import get_messages
from typing import Any
from django.contrib.messages.storage.base import Message


class QuizReadyViewTestCase(ViewTestCase):
    """Unit tests of the quiz ready view"""

    def setUp(self):
        self.base_url = '/quiz_ready/'
        self.url: str = reverse('quiz_ready', kwargs={"question_total": 1})
        self.user: User = User.objects.get(username='@johndoe')
        self.page_contain_list: list[Any] = [
            "Start Quiz",
            "Leave Quiz"
        ]

    def test_valid_quiz_ready_url(self):
        self.assertEqual(self.url, '/quiz_ready/1/')

    def test_valid_get_ready_quiz(self):
        self._login(self.user)
        response: HttpResponse = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pages/quiz/quiz_ready.html')
        self.assertTemplateUsed(response, 'partials/quiz/quiz_about_info.html')
        self._assert_response_contains(response, self.page_contain_list)
        self.assertTrue(len(response.context["quiz_set"].questions.all()) == 1)

    def test_invalid_redirects_if_question_total_is_less_than_1(self):
        self._login(self.user)
        url: str = f"{self.base_url}0/"
        response_url: str = reverse("quiz")
        response: HttpResponse = self.client.get(url)
        self.assertRedirects(
            response,
            response_url,
            status_code=302,
            target_status_code=200)
        messages_list: list[Message] = list(
            get_messages(response.wsgi_request))
        self.assertTrue(any(
            message.message == 'Invalid number of questions specified to create quiz' for message in messages_list))

    def test_valid_redirects_if_question_total_is_higher_than_the_number_of_questions_available(
            self):
        self._login(self.user)
        url: str = f"{self.base_url}1000/"
        response_url: str = reverse("quiz")
        response: HttpResponse = self.client.get(url)
        self.assertRedirects(
            response,
            response_url,
            status_code=302,
            target_status_code=200)
        messages_list: list[Message] = list(
            get_messages(response.wsgi_request))
        self.assertTrue(any(
            message.message == 'Not enough questions in database to start quiz' for message in messages_list))

    def test_valid_new_quiz_set_made_if_questions_not_already_in_quiz_set_together(
            self):
        QuizSet.objects.all().delete()
        quiz_set_count_before: int = QuizSet.objects.count()
        self._login(self.user)
        response: HttpResponse = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        quiz_set_count_after: int = QuizSet.objects.count()
        self.assertEqual(quiz_set_count_before + 1, quiz_set_count_after)

    def test_valid_new_quiz_set_not_made_if_questions_already_in_quizset_together(
            self):
        QuizSet.objects.all().delete()
        quiz_set: QuizSet = QuizSet.objects.create(
            seeded=False
        )
        for question in QuizQuestion.objects.all():
            quiz_set.questions.add(question)

        quiz_set_count_before: int = QuizSet.objects.count()
        self._login(self.user)
        url: str = f"{self.base_url}{QuizQuestion.objects.count()}/"
        response: HttpResponse = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        quiz_set_count_after: int = QuizSet.objects.count()
        self.assertEqual(quiz_set_count_before, quiz_set_count_after)

    def test_invalid_question_total_must_be_int_try_str(self):
        url: str = f"{self.base_url}hi/"
        response: HttpResponse = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_invalid_question_total_must_be_int_try_float(self):
        url: str = f"{self.base_url}1.2/"
        response: HttpResponse = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_valid_get_view_redirects_when_not_logged_in(self):
        self._assert_require_login(self.url)
