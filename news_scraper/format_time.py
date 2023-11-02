from datetime import datetime, timedelta
import pytz

def getFormattedCurrentTime():
    return datetime.now(pytz.timezone('Asia/Seoul')).strftime("%Y년 %m월 %d일 %H시 %M분 %S초")