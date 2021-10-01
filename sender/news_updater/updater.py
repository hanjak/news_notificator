from apscheduler.schedulers.background import BackgroundScheduler
from news_updater import news_downloader

def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(news_downloader.check_webnews, 'interval', minutes=300)
    scheduler.start()