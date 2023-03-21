from django import forms
from financial_companion.models import QuizQuestion, QuizSet, QuizScore, User


class QuizQuestionForm(forms.Form):
    """Form to answer quiz questions"""

    def __init__(self, user, quiz_set, *args, **kwargs):
        self.quiz_set: QuizSet = quiz_set
        self.user: User = user
        super(QuizQuestionForm, self).__init__(*args, **kwargs)

        if self.quiz_set is not None:
            for quiz_question in self.quiz_set.questions.all():
                self.fields[f"{quiz_question.id}"] = forms.ChoiceField(
                    choices=[(answer, answer)
                             for answer in quiz_question.get_potential_answers()],
                    widget=forms.RadioSelect,
                    required=True,
                    label=quiz_question.question
                )

    def save(self) -> QuizScore:
        """Create a new quiz score object."""
        if not self.is_valid():
            return None
        total_questions: int = self.quiz_set.questions.count()
        correct_answers: int = 0

        for form_question in self.cleaned_data.keys():
            quiz_question: QuizQuestion = self.quiz_set.questions.all().get(id=form_question)
            if quiz_question.is_answer(self.cleaned_data[form_question]):
                correct_answers += 1

        quiz_score: QuizScore = QuizScore.objects.create(
            user=self.user,
            total_questions=total_questions,
            correct_questions=correct_answers,
            quiz_set=self.quiz_set
        )

        return quiz_score
