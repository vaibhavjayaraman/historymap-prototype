from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            #log the user in 
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'users/signup.html', 
                    {'form': form}
    )

