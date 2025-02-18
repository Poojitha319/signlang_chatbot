from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Alphabet, Number, Word, MathExercise, ScienceLesson, LearningProgress, Video
from .serializers import VideoSerializer
from rest_framework import status

# Alphabet and Number interpretation
class AlphabetAPIView(APIView):
    def get(self, request, letter):
        try:
            alphabet = Alphabet.objects.get(letter=letter)
            return Response({
                'letter': alphabet.letter,
                'explanation': alphabet.explanation,
                'sign_language_image_url': alphabet.sign_language_image.url
            })
        except Alphabet.DoesNotExist:
            return Response({'error': 'Letter not found'}, status=404)

class NumberAPIView(APIView):
    def get(self, request, number):
        try:
            number_instance = Number.objects.get(number=number)
            return Response({
                'number': number_instance.number,
                'explanation': number_instance.explanation,
                'sign_language_image_url': number_instance.sign_language_image.url
            })
        except Number.DoesNotExist:
            return Response({'error': 'Number not found'}, status=404)

# Word and sentence conversion to sign language
class WordAPIView(APIView):
    def get(self, request, word):
        try:
            word_instance = Word.objects.get(gujarati_word=word)
            return Response({
                'gujarati_word': word_instance.gujarati_word,
                'explanation': word_instance.explanation,
                'sign_language_video_url': word_instance.sign_language_video.url
            })
        except Word.DoesNotExist:
            return Response({'error': 'Word not found'}, status=404)

# Mathematics exercises
class MathExerciseAPIView(APIView):
    def get(self, request):
        exercises = MathExercise.objects.all()
        exercise_data = [{'question': ex.question, 'explanation': ex.explanation} for ex in exercises]
        return Response({'exercises': exercise_data})

# Science lesson API
class ScienceLessonAPIView(APIView):
    def get(self, request):
        lessons = ScienceLesson.objects.all()
        lesson_data = [{'title': lesson.title, 'content': lesson.content} for lesson in lessons]
        return Response({'lessons': lesson_data})

# Learning Progress
class LearningProgressAPIView(APIView):
    def get(self, request, student_id):
        progress_records = LearningProgress.objects.filter(student__user_id=student_id)
        progress_data = [{'lesson_name': record.lesson_name, 'progress': record.progress} for record in progress_records]
        return Response({'progress': progress_data})

# Video Upload View
class VideoUploadView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = VideoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# List and retrieve videos
class VideoListView(APIView):
    def get(self, request, *args, **kwargs):
        videos = Video.objects.all()
        serializer = VideoSerializer(videos, many=True)
        return Response(serializer.data)

# Retrieve a single video
class VideoDetailView(APIView):
    def get(self, request, pk, *args, **kwargs):
        try:
            video = Video.objects.get(pk=pk)
            serializer = VideoSerializer(video)
            return Response(serializer.data)
        except Video.DoesNotExist:
            return Response({'error': 'Video not found'}, status=404)
