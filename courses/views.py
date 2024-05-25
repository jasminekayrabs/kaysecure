# courses/views.py
from django.shortcuts import render, get_object_or_404, redirect
from .models import Course, Module, Slide, Quiz, UserModuleProgress, PhishingEmailTemplate
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail, EmailMessage
from django.conf import settings
from django.template.loader import render_to_string
from django.urls import reverse
from django.contrib import messages
from .email_backends import PhishingEmailBackend
from django.core.mail.backends.smtp import EmailBackend
from django.http import JsonResponse
import time

#Protected against SQL injections using get_object_or_404
def course_detail(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    return render(request, 'courses/course_detail.html', {'course': course})

@login_required
def dashboard(request):
    all_courses = Course.objects.all()
    user_progress_list = UserModuleProgress.objects.filter(user=request.user).select_related('module', 'module__course')
    
    accessed_courses_ids = user_progress_list.values_list('module__course__id', flat=True).distinct()
    accessed_courses = Course.objects.filter(id__in=accessed_courses_ids)
    recommended_courses = Course.objects.exclude(id__in=accessed_courses_ids)
    
    user_progress_dict = {progress.module.id: progress for progress in user_progress_list}

    for course in accessed_courses:
        total_modules = course.modules.count()
        modules_completed = UserModuleProgress.objects.filter(user=request.user, module__course=course, completed_quiz=True).count()
        course.progress_completed = (modules_completed == total_modules)
        course.modules_completed = modules_completed
        course.total_modules = total_modules

    return render(request, 'dashboard.html', {
        'accessed_courses': accessed_courses,
        'recommended_courses': recommended_courses,
        'user': request.user
    })

@login_required
def course_content(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    modules = course.modules.order_by('order')

    user_progress = UserModuleProgress.objects.filter(user=request.user, module__course=course)
    progress_dict = {progress.module.id: progress for progress in user_progress}

    for module in modules:
        if module.order == 1:
            module.is_unlocked = True  # First module is always unlocked
        else:
            previous_module = Module.objects.filter(course=course, order=module.order - 1).first()
            if previous_module and previous_module.id in progress_dict:
                previous_module_progress = progress_dict[previous_module.id]
                module.is_unlocked = previous_module_progress.completed_quiz
            else:
                module.is_unlocked = False  # Ensure module is locked if previous module is not completed

    return render(request, 'courses/course_content.html', {'course': course, 'modules': modules})

@login_required
def module_view(request, course_id, module_id):
    module = get_object_or_404(Module, pk=module_id, course_id=course_id)
    slides = module.slides.all() if module.content_type in [Module.ContentTypeChoices.SLIDES, Module.ContentTypeChoices.BOTH] else None
    quiz = module.quiz if hasattr(module, 'quiz') else None

    user_progress, created = UserModuleProgress.objects.get_or_create(user=request.user, module=module)

    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        slide_id = request.POST.get('slide_id')
        if slide_id and int(slide_id) not in user_progress.slides_viewed:
            user_progress.slides_viewed.append(int(slide_id))
            user_progress.save()
        all_slides_viewed = len(user_progress.slides_viewed) == slides.count()
        return JsonResponse({'all_slides_viewed': all_slides_viewed})

    if module.order > 1 and not module.is_unlocked:
        messages.error(request, "You must complete the previous module's quiz to proceed.")
        return redirect('course_content', course_id=course_id)

    return render(request, 'courses/module_detail.html', {
        'module': module,
        'slides': slides,
        'quiz': quiz,
    })



"""When a quiz is submitted, calculate the score. If the user passes, mark the current module as completed and unlock the next one."""

@login_required
def submit_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    module = quiz.module
    user_progress, created = UserModuleProgress.objects.get_or_create(user=request.user, module=module)

    if request.method == "POST":
        user_answers = []
        for key, value in request.POST.items():
            if key.startswith('question_'):
                user_answers.append(int(value))

        correct_answers = 0
        total_questions = quiz.question_set.count()

        for question in quiz.question_set.all():
            correct_choice = question.choice_set.filter(is_correct=True).first()
            if correct_choice and correct_choice.id in user_answers:
                correct_answers += 1

        user_score = (correct_answers / total_questions) * 100
        print(f"User score: {user_score}, Correct answers: {correct_answers}, Total questions: {total_questions}")

        if user_score >= quiz.passing_score:
            user_progress.completed_quiz = True
            user_progress.completed_module = True  
            user_progress.save()

            # Check if this is the last module in the course
            is_last_module = not Module.objects.filter(course=module.course, order=module.order + 1).exists()

            if is_last_module:
                # Redirect to the certificate page if this is the last module
                return JsonResponse({
                    'success': True,
                    'message': 'Quiz passed! Congratulations on completing the course.',
                    'next_url': reverse('check_course_completion', kwargs={'course_id': module.course.id})
                })

            # Unlock the next module
            next_module = Module.objects.filter(course=module.course, order=module.order + 1).first()
            if next_module:
                next_module.is_unlocked = True
                next_module.save()
                next_module_progress, created = UserModuleProgress.objects.get_or_create(user=request.user, module=next_module)
                next_module_progress.completed_module = True
                next_module_progress.save()

                next_url = reverse('module_view', kwargs={'course_id': module.course.id, 'module_id': next_module.id})
            else:
                next_url = reverse('course_content', kwargs={'course_id': module.course.id})

            return JsonResponse({
                'success': True,
                'message': 'Quiz passed! Proceeding to the next module.',
                'next_url': next_url
            })
        else:
            return JsonResponse({
                'success': False,
                'message': 'Quiz failed. Try again!'
            })
    else:
        return JsonResponse({'success': False, 'message': 'Invalid request method.'}, status=405)


@login_required
def check_course_completion(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    modules = course.modules.all()
    if all(UserModuleProgress.objects.get_or_create(user=request.user, module=module)[0].completed_quiz for module in modules):
        return render(request, 'certificate.html', {'course': course})
    return redirect('course_content', course_id=course.id)

@login_required
def all_progress_completed(user, course):
    """Utility function to check if a user has completed all modules in a course."""
    completed_modules = UserModuleProgress.objects.filter(user=user, module__course=course, is_completed=True).count()
    return completed_modules == course.modules.count()

@login_required
def view_certificate(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    modules = course.modules.all()
    if all(UserModuleProgress.objects.get(user=request.user, module=module).completed_quiz for module in modules):
        return render(request, 'certificate.html', {'course': course})
    else:
        messages.error(request, "You have not completed all modules in this course.")
        return redirect('dashboard')

@login_required
def send_phishing_email(request, template_id):
    template = get_object_or_404(PhishingEmailTemplate, id=template_id)
    user = request.user

    phishing_url = request.build_absolute_uri(reverse('phishing_website'))

    email_body = render_to_string('phishing_email.html', {
        'user': user,
        'phishing_url': phishing_url
    })

    email = EmailMessage(
        subject=template.subject,
        body=email_body,
        from_email=settings.PHISHING_EMAIL_FROM,
        to=[user.email],
        connection=PhishingEmailBackend()
    )
    email.content_subtype = 'html'
    email.send()

    return redirect('phishing_simulation_confirmation')

@login_required
def phishing_simulation_confirmation(request):
    return render(request, 'phishing_simulation_confirmation.html')

def phishing_website(request):
    return render(request, 'phishing_website.html')

def phishing_form_submit(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Log the credentials (or handle them appropriately)
        print(f"Phishing attempt: {username} / {password}")

        # Redirect to a page that shows the user they've been phished
        return redirect('phishing_feedback')

    return redirect('phishing_website')

def phishing_feedback(request):
    return render(request, 'phishing_feedback.html')


# Simulation
@login_required
def password_cracking_simulation(request):
    if request.method == 'POST':
        password = request.POST.get('password')
        crack_time = simulate_password_cracking(password)
        return render(request, 'password_cracking_result.html', {'password': password, 'crack_time': crack_time})
    return render(request, 'password_cracking_simulation.html')

def simulate_password_cracking(password):
    # A very simple and non-realistic password cracking simulation
    length = len(password)
    if length < 5:
        return 'a few seconds'
    elif length < 8:
        return 'a few minutes'
    elif length < 12:
        return 'a few hours'
    else:
        return 'several days'