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
admin_email = 'emailpyhanja@gmail.com'

def get_soup(url):
    """Gets url, returns bs object"""
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    return soup

def get_news(soup):
    """Gets bs object, returns list of bs object representing the articles in
    the news section of the webpage"""
    results = soup.find_all("article", class_="clanek col-12 mb-3 mt-3")
    return results


def get_news_info(news):
    """Gets list of bs objects representing the articles in the news section
    and substracts information about individual articles - text, date and
    links. Returns list of tuples, each tuple represents one news and
    contains(text, date, link)"""
    news_info = []
    for article in news:
        # get date of the news
        date = article.find(class_="clanekDatum").find("span").get_text()
        print (date)
        # get weblink to the news
        link_ending = article.find(class_="pt-3 mt-3") \
            .find("a") \
            .get("href")
        link_base = "www.zsverycaslavske.cz"
        link = link_base + link_ending
        # get text of the news
        text = article.find("a").text
        new_news = [text,date,link]
        news_info.append (new_news)
    return news_info

def get_emails_wants_email():
    """ returns list of emails of users (Profile objects)
    with field wants_email = True (of the users who wants to receive
     notification emails)."""
    emails = list(Profile.objects.filter(wants_email=True).
                  values_list('email', flat=True))
    return emails

def send_email_new_news (emails, news, link):
    """Sends email, which is supposed to be send if there is new information
    at the website"""
    subject = "ZS Very Caslavske NEWS NOTIFICATION"
    message_intro = "There is new information on the website " \
                    "www.verycaslavske.cz: "
    message_details = ". Details can be found here: "
    message = message_intro + news + message_details + link
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        emails
    )

def send_email_nothing_new(email):
    """Sends email, which is supposed to be send if there is no new information
    at the website"""
    subject = "ZS Very Caslavske NEWS NOTIFICATION"
    message = "There is no new information on the website " \
              "www.verycaslavske.cz"
    send_mail(subject,
              message,
              settings.DEFAULT_FROM_EMAIL,
              [email]
              )

def check_webnews():
    """Downloads all articles in the news section of the website and compares
    the articles with articles saved in database. If there is new information
    it sends the notification email to user who wants notification emails.
    If there is no new information, it sends email to admin that the checkup
    took place succesfully"""
    latest_webnews = Webnews.objects.first()
    print (latest_webnews.link)
    all_webnews = Webnews.objects.all()
    print (all_webnews)
    #selecting accounts with value wants_email = True
    emails = get_emails_wants_email()
    #scrapping of news
    news_list = get_news_info(get_news(get_soup(url)))
    print (news_list)
    #checking if there is new information
    for news in news_list:
        news_text = news[0]
        #check if the news is already in database or not
        exists = Webnews.objects.filter(text=news_text).exists()
        message_sent = False
        #if the news is not yet in database
        if exists == False:
            news_text = news[0]
            print (news_text)
            news_date = news[1]
            print (news_date)
            news_link = news[2]
            print (news_link)
            #creating new instance of Webnews
            new_webnews = Webnews(text = news_text,date=news_date,link=news_link)
            new_webnews.save()
            #send email
            send_email_new_news(emails, news_text, news_link)
            message_sent = True
    #if no new information, sending email to the admin
    if message_sent == False:
        send_email_nothing_new(admin_email)


