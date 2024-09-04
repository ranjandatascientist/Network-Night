from django.shortcuts import render

# Create your views here.
def login_signup(request):
    return render(request, 'Login Signup.html')
