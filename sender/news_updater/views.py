from django.shortcuts import render
from news_updater.models import Webnews
from accounts.models import Profile, User
from django.contrib.auth.models import User



def index(request):
    latest_webnews = Webnews.objects.first()
    text = latest_webnews.text

    return render(request, 'index.html',{
        'text':text})

def error_404(request,exception):
    latest_webnews = Webnews.objects.first()
    text = latest_webnews.text
    return render(request, 'index.html', {
        'text': text})