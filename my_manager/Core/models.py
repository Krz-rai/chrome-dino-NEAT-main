# models.py
from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
import uuid
import random

class Task(models.Model):
    create = models.DateTimeField(auto_now_add=True)
    created_when = models.DateTimeField(auto_now_add=True)
    uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    class Meta:
        abstract = True  

class Category(Task):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Passage(Task):
    title = models.CharField(max_length=255)
    text = RichTextField(null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='passages')

    def __str__(self):
        return self.title

class Question(Task):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='questions')
    passage = models.ForeignKey(Passage, on_delete=models.CASCADE, null=True, blank=True, related_name='questions')
    text = models.CharField(max_length=9999)
    explanation = RichTextField(null=True, blank=True)
    hint1 = RichTextField(null=True, blank=True)
    hint2 = RichTextField(null=True, blank=True)
    hint3 = RichTextField(null=True, blank=True)
    marks = models.IntegerField(default=5)

    def __str__(self):
        return self.text

class Answer(Task):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    text = models.CharField(max_length=9999)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.text

class QuizAttempt(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='quiz_attempts')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='quiz_attempts')
    score = models.IntegerField()
    total_marks = models.IntegerField()
    date_taken = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.category.name} - {self.date_taken.strftime('%Y-%m-%d %H:%M')}"

class QuestionResult(models.Model):
    quiz_attempt = models.ForeignKey(QuizAttempt, on_delete=models.CASCADE, related_name='question_results')
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    selected_answer = models.ForeignKey(Answer, on_delete=models.SET_NULL, null=True, blank=True)
    is_correct = models.BooleanField()
    used_hints = models.IntegerField(default=0)  # Optional: Track the number of hints used

    def __str__(self):
        return f"QuestionResult for {self.quiz_attempt} - {self.question.text[:50]}"
