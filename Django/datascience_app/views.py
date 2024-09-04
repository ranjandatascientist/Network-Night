from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils import timezone
from .models import User, UserSession
from .forms import UserCreationForm, AuthenticationForm
from django.http import JsonResponse
from django.contrib.auth import authenticate, login as django_login
import uuid

def home(request):
    return render(request, 'index.html')

def login_signup(request):
    return render(request, 'login_signup.html')

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
                
        if form.is_valid():
            user = form.save(commit=False)
            
            # Set the password using the model's method
            user.set_password(form.cleaned_data['password'])
            user.save()
            
            messages.success(request, "Account created successfully!")
            return redirect('loginSignup')
        else:
            messages.error(request, 'Error creating account. Please check the form.')
    else:
        form = UserCreationForm()
        
    return render(request, 'login_signup.html', {'form': form})

def login(request):
    if request.method == 'POST':
        print("POST request received")
        
        # Try to get the JSON data
        try:
            import json
            data = json.loads(request.body)
            username = data.get('username')
            password = data.get('password')
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'message': 'Invalid data format'}, status=400)
        
        # Validate username and password are provided
        if not username or not password:
            return JsonResponse({'success': False, 'message': 'Username and password are required'}, status=400)
        
        try:
            # Authenticate the user
            user = authenticate(request, username=username, password=password)
            if user is not None:
                django_login(request, user)  # Log in the user using Django's built-in login function
                session_token = str(uuid.uuid4())
                
                # Create a new session for the user
                UserSession.objects.create(
                    UserID=user,
                    SessionToken=session_token,
                    ExpireDate=timezone.now() + timezone.timedelta(hours=7),
                    IpAddress=request.META.get('REMOTE_ADDR'),
                    UserAgent=request.META.get('HTTP_USER_AGENT')
                )
                
                # Store session token in Django session framework
                request.session['session_token'] = session_token
                
                # Return a success response
                return JsonResponse({'success': True, 'message': 'Logged in successfully'})
            else:
                # Return an error response if authentication fails
                return JsonResponse({'success': False, 'message': 'Invalid username or password'}, status=400)
        except Exception as e:
            print(f"Error occurred: {e}")
            return JsonResponse({'success': False, 'message': 'An unexpected error occurred'}, status=500)
    else:
        print("GET request received")
        form = AuthenticationForm()

    return render(request, 'login_signup.html', {'form': form})

def logout(request):
    session_token = request.session.pop('session_token', None)
    
    if session_token:
        # Delete the session from the database
        UserSession.objects.filter(SessionToken=session_token).delete()
    
    messages.success(request, 'Logged out successfully!')
    return redirect('loginSignup')
