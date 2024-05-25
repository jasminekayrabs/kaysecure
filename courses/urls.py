from django.urls import path
from . import views
from .views import course_detail, course_content, dashboard, submit_quiz, phishing_simulation_confirmation

urlpatterns = [
    path('<int:course_id>/', views.course_detail, name='course_detail'),
    path('course/<int:course_id>/content/', course_content, name='course_content'),
    path('course/<int:course_id>/module/<int:module_id>/', views.module_view, name='module_view'),
    path('quiz/submit/<int:quiz_id>/', views.submit_quiz, name='submit_quiz'),
    path('course/completion/<int:course_id>/', views.check_course_completion, name='check_course_completion'),
    path('dashboard/', dashboard, name='dashboard'),
    path('quiz/submit/<int:quiz_id>/', submit_quiz, name='submit_quiz'),
    path('certificate/<int:course_id>/', views.view_certificate, name='view_certificate'),
    path('send_phishing_email/<int:template_id>/', views.send_phishing_email, name='send_phishing_email'),
    path('phishing_website/', views.phishing_website, name='phishing_website'),
    path('phishing_form_submit/', views.phishing_form_submit, name='phishing_form_submit'),
    path('phishing_feedback/', views.phishing_feedback, name='phishing_feedback'),
    path('phishing_simulation_confirmation/', phishing_simulation_confirmation, name='phishing_simulation_confirmation'),
    path('password_cracking_simulation/', views.password_cracking_simulation, name='password_cracking_simulation'),
]

