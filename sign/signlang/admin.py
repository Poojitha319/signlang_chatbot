from django.contrib import admin
from .models import Alphabet, Number, Word, MathExercise, ScienceLesson, LearningProgress, UserProfile, Video

admin.site.register(Alphabet)
admin.site.register(Number)
admin.site.register(Word)
admin.site.register(MathExercise)
admin.site.register(ScienceLesson)
admin.site.register(LearningProgress)
admin.site.register(UserProfile)
@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ('title', 'uploaded_at')
