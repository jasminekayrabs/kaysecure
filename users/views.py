from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordResetForm, SetPasswordForm
from django.contrib.auth.views import PasswordResetView
from django.contrib.auth.decorators import login_required
from .models import UserProgress
from django.views.decorators.csrf import csrf_protect
from django.utils.html import escape
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib import messages 
# from django.contrib.auth.views import (
#     PasswordResetView,
#     PasswordResetDoneView,
#     PasswordResetConfirmView,
#     PasswordResetCompleteView,
# )


def home(request):
    return render(request, 'home.html')
def render_terms(request):
    return render(request, "t&c.html")
def render_cookies(request):
    return render(request, "cpolicy.html")
def render_privacy(request):
    return render(request, "privpolicy.html")

@csrf_protect
def render_signup(request):
    if request.method == "POST":
        #Retrieve form data
        fname = escape(request.POST['fname'])
        username = escape(request.POST['username'])
        email = escape(request.POST['email'])
        password = request.POST['pass1']
        pass2 = request.POST['pass2']
        terms_accepted = request.POST.get('terms', False) == 'on'

        #FOR TERMS AND CONDITIONS
        if not terms_accepted:
            messages.error(request, 'Please accept the Terms and Conditions.')
            return redirect('signup')
        
        #create a user object
        myuser = User.objects.create_user(username=username, email=email, password=password)
        myuser.email = email
        myuser.full_name = fname
        myuser.user_name = username 
            #Set user as inactive
        myuser.is_active = False 
        myuser.save()

        # Generate activation token
        token = default_token_generator.make_token(myuser)

        #Build activation URL
        current_site = get_current_site(request)
        domain = current_site.domain
        uid = urlsafe_base64_encode(force_bytes(myuser.pk))
        protocol = 'https' if request.is_secure() else 'http'
        activation_url = f"{protocol}://{domain}{reverse('activate_account', kwargs={'uidb64': uid, 'token': token})}"

        # Render email template with context
        email_context = {
            'user': myuser,
            'activation_url': activation_url,
        }
        email_message = render_to_string('users/activation_email.html', email_context)

        # Send activation email
        subject = 'Activate your account'
        message = render_to_string('users/activation_email.html', {
            'user': myuser,
            'activation_url': activation_url,
        })
        send_mail(subject, '', settings.DEFAULT_FROM_EMAIL, [myuser.email], html_message=email_message)

        return redirect('activation_sent')
    return render(request, "users/signup2.html")

#RENDER ACTIVATION SENT PAGE 
def activation_sent(request):
    return render(request, 'users/activation_sent.html')

#Activate account 
def activate_account(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save() 
        messages.success(request, 'Your account has been activated. You can now log in.')
        return redirect('login')
    else:
        messages.error(request, 'Invalid activation link.')
        return redirect('home')


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('pass1')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('dashboard') 
        else:
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'users/login2.html')

def password_reset(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            associated_users = User.objects.filter(email=email)
            if associated_users.exists():
                for user in associated_users:
                    # Generate password reset token
                    uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
                    token = default_token_generator.make_token(user)
                    
                    # Build reset password URL
                    protocol = 'https' if request.is_secure() else 'http'
                    domain = get_current_site(request).domain
                    reset_url = f"{protocol}://{domain}{reverse('password_reset_confirm', kwargs={'uidb64': uidb64, 'token': token})}"
                    
                    # Render email template with context
                    email_context = {
                        'user': user,
                        'reset_url': reset_url,
                    }
                    email_message = render_to_string('users/password_reset_email.html', email_context)
                    
                    # Send password reset email
                    subject = 'Password Reset Request'
                    send_mail(subject, '', settings.DEFAULT_FROM_EMAIL, [email], html_message=email_message)
                    
                    # Redirect to password reset done page
                    return redirect('password_reset_done')
            else:
                messages.error(request, 'No user exists with this email address.')
    else:
        form = PasswordResetForm()
    return render(request, 'users/password_reset.html', {'form': form})

def password_reset_done(request):
    return render(request, 'users/password_reset_done.html')

def password_reset_confirm(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        if request.method == 'POST':
            form = SetPasswordForm(user, request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'Your password has been reset successfully.')
                return redirect('password_reset_complete')
        else:
            form = SetPasswordForm(user)
        return render(request, 'users/password_reset_confirm.html', {'form': form})
    else:
        messages.error(request, 'Invalid password reset link.')
        return redirect('home')

def password_reset_complete(request):
    return render(request, 'users/password_reset_complete.html')

def logout_view(request):
    logout(request)
    return redirect('home')