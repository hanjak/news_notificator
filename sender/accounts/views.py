from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login,logout
from django.contrib.auth.decorators import login_required
from .forms import SignUpForm,ProfileForm
from .models import Profile


def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        #profile_form = ProfileForm(request.POST, instance=request.user.profile)
        if form.is_valid():
            user = form.save()
            profile = user.profile
            profile.email=form.cleaned_data.get('email')
            profile.save()
            login(request, user)
            return redirect('news_updater:index')
    else:
        form = SignUpForm()
        #profile_form = ProfileForm()
    return render(request, 'accounts/signup.html', {
        'form': form
        })


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('news_updater:index')
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})

def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('news_updater:index')

#@login_required
def update_profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST,
                           instance=request.user.profile,)
        if form.is_valid():
            form.save()
            return redirect('news_updater:index')
    else:
        form = ProfileForm(data=request.POST, instance=request.user.profile)

    return render(request, 'accounts/update.html', {
        'form': form
        })

