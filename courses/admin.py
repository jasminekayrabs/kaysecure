from django.contrib import admin
from .models import Course, Module, Quiz, Question, Choice, Slide, PhishingEmailTemplate

class CourseAdmin(admin.ModelAdmin):
    list_display = ('course_name', 'description', 'created_at')
    search_fields = ('course_name', 'description')

class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3  # Number of extra forms to display

class QuestionInline(admin.TabularInline):
    model = Question
    # inlines = [ChoiceInline]
    extra = 1

class QuizAdmin(admin.ModelAdmin):
    inlines = [QuestionInline]

admin.site.register(Course)
admin.site.register(Module)
admin.site.register(Quiz, QuizAdmin)
# admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice)
admin.site.register(Slide)
admin.site.register(PhishingEmailTemplate)