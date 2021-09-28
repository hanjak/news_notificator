import requests
from news_updater.models import Webnews
from accounts.models import Profile
import re
from bs4 import BeautifulSoup
from django.core.mail import send_mail
from django.conf import settings
from accounts.models import Profile, User
from django.contrib.auth.models import User


url = "https://www.zsverycaslavske.cz/"

def get_soup(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    return soup

def get_news(soup):
    results = soup.find (class_="pt-3 mt-3")
    results = soup.find_all("h3", class_="pt-3 mt-3")
    return results


def get_news_text(news):
    news_text = []
    for story in news:
        ref = story.find("a")
        ref_text=ref.text
        news_text.append(ref_text)
    return news_text



def send_webnews_notification():
    #selecting accounts with value wants_email = True
    emails = list(Profile.objects.filter(wants_email=True).
                  values_list('email', flat=True))

    url = "https://www.zsverycaslavske.cz/"
    #scrapping of news
    news_list = get_news_text(get_news(get_soup(url)))
    latest_webnews = Webnews.objects.first()
    #checking if there is new information
    for news in news_list:
        exists = Webnews.objects.filter(text=news).exists()
        message_sent = False
        #send email to the recepients
        if exists == False:
            subject = "ZS Very Caslavske NEWS NOTIFICATION"
            message_intro = "There is new information on the website " \
                      "www.verycaslavske.cz: "
            message = message_intro + news
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                emails
            )
            message_sent = True
            new_text = Webnews(text = news)
            new_text.save()
    #if no new information, sending email to the admin
    if message_sent == False:
        subject = "ZS Very Caslavske NEWS NOTIFICATION"
        message = "There is no new information on the website " \
                  "www.verycaslavske.cz"
        send_mail(subject,
                  message,
                  settings.DEFAULT_FROM_EMAIL,
                  ['emailpyhanja@gmail.com']
                )


