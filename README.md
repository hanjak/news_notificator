# news_notificator
Simple web and webscrapping app that regulary checks web page  and if there is any news it sends notification to signed up users.

## Introduction
News Notificator is simple web app written in python and django. The main goal of the app is to check if there is some new information at the school webpage (ZS Very Caslavske, www.zsverycaslavske.cz) and, if yes, send notification email, so that parents dont need to check the web manually every day.

The app contains django authentication system (accounts), which allowes users to signup, login and log out, so that they can receive notification emails. If the user doesnt want to get notification emails anymore, she can edit settings in the update section.

The app also contains web scrapping part (news_updater), which scrapes the webpage using beuatifulsoup4 and the regulary activity is set using APScheduler. 

## TODO
Design
Tests
