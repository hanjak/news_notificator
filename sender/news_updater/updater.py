from apscheduler.schedulers.background import BackgroundScheduler
from news_updater import news_downloader

def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(news_downloader.send_webnews_notification, 'interval', minutes=360)
    scheduler.start()