from django.shortcuts import render, redirect
from django.contrib.auth.models import User

def profile(request):
    args = {'user': request.user}
    return render(request, 'users/profile.html', args)
