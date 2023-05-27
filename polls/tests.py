from django.test import TestCase
from django.utils import timezone
from django.urls import reverse
# Create your tests here.
import datetime

from .models import Question

class QuestionModelTests(TestCase):
    def test_was_published_recently_with_future_question(self):
        """
        was_published_recently() returns False
        for questions whose pub_date is in the future
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date = time)

        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        """
        was_published_recently() returns False for questions
        whose pub_date is older than 1 day.
        """

        time = timezone.now() - datetime.timedelta(days=1,seconds=1)
        old_question = Question(pub_date = time)

        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        """
        was_publishedrecently() returns True for questions 
        whose pub_date is within the last day.
        """
        time = timezone.now() - datetime.timedelta(hours = 23,minutes=59,seconds=59)
        recent_question = Question(pub_date = time)
        
        self.assertIs(recent_question.was_published_recently(), True)

def create_question(question_text, days):
    """
    create question with the given question_text and published with
    the given number of days offset to now
    (negative for questions published in the past and postive for 
    questions in the future)
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text,pub_date = time)


class QuestionIndexViewTests(TestCase):
    def test_no_questions(self):
        """
        if no questions exists 
        """
        response = self.client.get(reverse("polls:index"))
        self.assertEqual(response.status_code,200)
        self.assertContains(response,"No polls are available")
        self.assertQuerysetEqual(response.context["latest_question_list"],[])

    def test_past_question(self):
        """
        questions with pub_date in the past are displayed on the index page
        """
        question = create_question("Past question",-30)
        response = self.client.get(reverse("polls:index"))
        self.assertEqual(response.status_code,200)
        self.assertQuerysetEqual(response.context["latest_question_list"],[question],)

    def test_future_question(self):
        """
        questions with a pub_date in the future arent displayed
        """
        question = create_question("Future question",30)
        response = self.client.get(reverse("polls:index"))
        self.assertEqual(response.status_code,200)
        self.assertContains(response,"No polls are available")
        self.assertQuerysetEqual(response.context["latest_question_list"],[])

    def test_future_question_and_past_question(self): # press x for doubt
        """
        questions with both pub_dates are present but only past ones are displayed
        """
        question_past = create_question("Past question",-30)
        question_future = create_question("Future question",30)
        response = self.client.get(reverse("polls:index"))
        self.assertEqual(response.status_code,200)
        self.assertQuerysetEqual(response.context["latest_question_list"],[question_past])

    def test_two_past_questions(self):
        """
        questions index page displays multiple questions
        """
        question_1 = create_question("question_1",-30)
        question_2 = create_question("question_2",-15)
        response = self.client.get(reverse("polls:index"))
        self.assertEqual(response.status_code,200)
        self.assertQuerysetEqual(response.context["latest_question_list"],[question_2,question_1],)



        


