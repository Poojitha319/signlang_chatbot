from django.db import models
from django.contrib.auth.models import User

# User profile for teacher, student, and parent
class UserProfile(models.Model):
    USER_TYPES = (
        ('student', 'Student'),
        ('teacher', 'Teacher'),
        ('parent', 'Parent'),
        ('hr', 'HR'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_type = models.CharField(max_length=10, choices=USER_TYPES)

class Alphabet(models.Model):
    letter = models.CharField(max_length=2)
    sign_language_image = models.ImageField(upload_to='sign_language/alphabet/')
    explanation = models.TextField()

class Number(models.Model):
    number = models.IntegerField()
    sign_language_image = models.ImageField(upload_to='sign_language/numbers/')
    explanation = models.TextField()

class Word(models.Model):
    gujarati_word = models.CharField(max_length=100)
    sign_language_video = models.FileField(upload_to='sign_language/words/')
    explanation = models.TextField()

class MathExercise(models.Model):
    question = models.CharField(max_length=255)
    correct_answer = models.CharField(max_length=100)
    explanation = models.TextField()

class ScienceLesson(models.Model):
    title = models.CharField(max_length=255)
    sign_language_video = models.FileField(upload_to='sign_language/science/')
    content = models.TextField()
    exercises = models.ManyToManyField(MathExercise, blank=True)

class LearningProgress(models.Model):
    student = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    lesson_type = models.CharField(max_length=50)  # e.g., 'Math', 'Science'
    lesson_name = models.CharField(max_length=255)
    progress = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
    completed_at = models.DateTimeField(null=True, blank=True)
class Video(models.Model):
    title = models.CharField(max_length=100)
    file = models.FileField(upload_to='videos/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
