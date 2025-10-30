from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import authenticate, login as auth_login
from django.contrib import messages
from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render, redirect


def home(request):
  return render(request , 'home.html')




def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            auth_login(request, user) 
            return render(request, 'home.html')
        else:
            messages.error(request, 'Invalid username or password')
            return render(request, 'login.html')

    return render(request, 'login.html')






from .models import student
from django.contrib.auth.models import User
from django.contrib import messages
#for signup page
def form(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        course = request.POST.get('course')
        year = request.POST.get('year')
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
            return render(request, 'login.html')

        user = User.objects.create_user(username=username, password=password,email = email)
        user.first_name = name
        user.save()

        
        student.objects.create(name=name, course=course, year=year, username=username, password=password)

        messages.success(request, 'Signup successful! Please log in.')
        return render(request, 'login.html')

    return render(request, 'home.html')


from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from .models import notice, User  

ADMIN_USERNAME = "INFOadmin"
ADMIN_PASSWORD = "admin123@#$"


def admin_panel(request):
    is_admin = request.session.get('is_admin', False)

    if request.method == "POST":
        # --- Admin login logic ---
        if 'login_submit' in request.POST:
            username = request.POST.get('username')
            password = request.POST.get('password')

            if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
                request.session['is_admin'] = True
                messages.success(request, "Admin login successful")
                return redirect('info:admin_panel')
            else:
                messages.error(request, "Invalid credentials")

        # --- Notice submission logic ---
        elif 'notice_submit' in request.POST:
            if not is_admin:
                messages.error(request, "You must login first")
                return redirect('info:admin_panel')

            text = request.POST.get('text')
            file = request.FILES.get('file')

            if text:
                # Save notice
                new_notice = notice.objects.create(text=text, file=file)
                messages.success(request, "Notice saved successfully")

                # Send email notification
                try:
                    
                    recipient_list = list(User.objects.values_list('email', flat=True))

                    if recipient_list:
                        send_mail(
                            subject="New Notice from INFOcascade",
                            message=f"A new notice has been posted:\n\n{text}",
                            from_email=None,  
                            recipient_list=recipient_list,
                            fail_silently=False,
                        )
                        messages.success(request, "Email notifications sent!")
                    else:
                        messages.warning(request, "No users found to notify.")
                except Exception as e:
                    messages.error(request, f"Error sending email: {e}")

                return redirect('info:notice_list')
            else:
                messages.error(request, "Please enter notice text before submitting.")

    return render(request, 'admin.html', {'is_admin': is_admin})




def notice_list(request):
    notices = notice.objects.order_by('-created_at')  # latest first
    return render(request, 'notice.html', {'notice': notices})


def logout_view(request):
    request.session.flush()
    return redirect('info:admin_panel')

import re
from django.db.models import Q
from django.utils.safestring import mark_safe
def notice_search(request):
    query = request.GET.get('q', '')
    notices = notice.objects.all().order_by('-created_at')

    if query:
        # Filter notices containing the query text
        notices = notices.filter(Q(text__icontains=query))

        # Highlight matches
        for n in notices:
            pattern = re.compile(re.escape(query), re.IGNORECASE)
            highlighted = pattern.sub(
                lambda m: f'<mark style="background-color:#fdd663; font-weight:600;">{m.group(0)}</mark>',
                n.text
            )
            n.text = mark_safe(highlighted)
            print(n.text)

    return render(request, 'notice.html', {'notice': notices, 'query': query})


from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from .models import chatMessage

@login_required
def chat_messages(request):
    """Return all chat messages in JSON format"""
    messages = chatMessage.objects.all().order_by('timestamp')
    data = [
        {
            'id': msg.id,
            'user': msg.user.username,
            'message': msg.message,
            'is_current_user': msg.user == request.user
        }
        for msg in messages
    ]
    return JsonResponse({'messages': data})


@login_required
def send_message(request):
    """Save a new message"""
    if request.method == "POST":
        message = request.POST.get('message', '').strip()
        if message:
            chatMessage.objects.create(user=request.user, message=message)
            return JsonResponse({'status': 'ok'})
    return JsonResponse({'status': 'error'})


@login_required
def delete_message(request, msg_id):
    """Allow user to delete their own messages"""
    try:
        msg = chatMessage.objects.get(id=msg_id, user=request.user)
        msg.delete()
        return JsonResponse({'status': 'deleted'})
    except chatMessage.DoesNotExist:
        return JsonResponse({'status': 'forbidden'})
