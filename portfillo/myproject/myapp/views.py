from django.conf import settings
from django.shortcuts import render,redirect
from django.contrib import messages
from .models import signup_page,message_sending
from django.contrib.auth.hashers import make_password,check_password
from django.core.mail import send_mail
from functools import wraps
# Create your views here.

def login_required(f):
    @wraps(f) 
    def wrapped(request,*args,**kwargs):
        if not request.session.get('is_logged_in'):
            return redirect('login')
        return f(request,*args,**kwargs)
    return wrapped

def register(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['cn_password']
        
        if password != confirm_password:
            messages.error(request, 'Password and Confirm Password do not match')
            return redirect('register')

        if signup_page.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists')
            return redirect('login')

        hashed_password = make_password(password)  # Hash the password
        database_save = signup_page(name=name, email=email, password=hashed_password)
        database_save.save()
        messages.success(request, 'Registered Successfully')
        return redirect('login')

    return render(request, 'register.html')


def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = signup_page.objects.get(email=email)
            if check_password(password, user.password):
                request.session['email'] = user.email
                request.session['name'] = user.name
                request.session['is_logged_in'] = True
                return redirect('index')
            else:
                messages.error(request, 'Invalid password.')
        except signup_page.DoesNotExist:
            messages.error(request, 'Email not found.')

    return render(request, 'login.html')

@login_required
def index(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        # Save message to database (optional)
        saved = message_sending(name=name, email=email, subject=subject, message=message)
        saved.save()

        # Compose message to send to admin
        full_message = f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}"

        try:
            send_mail(
                subject=f"Message from {name} - {subject}",
                message=full_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=['kavipriyan292004@gmail.com'],  # ✅ Only admin receives
                fail_silently=False,
            )
            messages.success(request, 'Your message has been sent to the admin successfully!')
        except Exception as e:
            messages.error(request, 'Failed to send your message. Please try again later.')

    return render(request, 'index.html')

def logout_view(request):
    request.session.flush()  # Clears all session data
    return redirect('register')  # Make sure 'register' is a valid URL name
