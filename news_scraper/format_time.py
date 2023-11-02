from datetime import datetime, timedelta
import pytz

def getFormattedCurrentDateTime():
    return datetime.now(pytz.timezone('Asia/Seoul')).strftime("%Y년 %m월 %d일 %H시 %M분 %S초")

def getFormattedCurrentDate():
    return datetime.now(pytz.timezone('Asia/Seoul')).strftime("%Y%m%d")