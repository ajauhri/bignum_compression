import MySQLdb
import requests
from datetime import date, timedelta 
from bs4 import BeautifulSoup
import const

url_2015 = 'http://weather.noaa.gov/pub/logs/heapstats/cmas-alerts_%s.log'
url_2014 = 'http://weather.noaa.gov/pub/logs/heapstats/2014/cmas-alerts_%s.log.gz'
url_2013 = 'http://weather.noaa.gov/pub/logs/heapstats/2013/cmas-alerts_%s.log'
url_2012 = 'http://weather.noaa.gov/pub/logs/heapstats/2013/2012/cmas-alerts_%s.log'

def init_db():
    const.conn = MySQLdb.connect(host="localhost", user="root", passwd="cmusv101", db="cmusv-wea")
    const.cur = const.conn.cursor()

def store(msg, date):   
    if not msg:
        return
    s = BeautifulSoup(msg) 
    if s.alert.info.polygon:
        polygon = s.alert.info.polygon.string
    else:
        polygon = ""
    effective_ts = s.alert.info.effective.string
    onset_ts = s.alert.info.onset.string
    expires_ts = s.alert.info.expires.string
    sendername = s.alert.info.sendername.string
    identifier = s.alert.identifier.string
    areadesc = s.alert.info.areadesc.string
    raw = " ".join(msg.split())
    raw = raw.replace('|','')
    print identifier, date
    try:
        const.cur.execute("""INSERT INTO cap_msgs (identifier, effective_ts, onset_ts, expires_ts, sendername, raw, areadesc, polygon, date) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s) ON DUPLICATE KEY UPDATE effective_ts = VALUES(effective_ts), onset_ts = VALUES(onset_ts), expires_ts = VALUES(expires_ts), sendername = VALUES(sendername), raw = VALUES(raw), areadesc = VALUES(areadesc), polygon = VALUES(polygon), date = VALUES(date)""", (identifier, effective_ts, onset_ts, expires_ts, sendername, raw, areadesc, polygon, date))
        const.conn.commit()
    except Exception, e:
        const.conn.rollback()
        print e

def init():
    init_db()
    start_date = date(2015, 1, 1)
    end_date = date.today() #date(2012, 12, 31) 
    i = start_date
    while i <= end_date:
        url_i = url_2015 % i.strftime('%m%d%Y')
        r = requests.get(url_i, stream=True)
        cap_started = False
        for line in r.iter_lines():
            if "==CAP==" in line:
                cap_msg = ""
                cap_started = True
            elif "==WMO==" in line:
                cap_started = False
                store(cap_msg, i.strftime('%Y-%m-%d'))
            elif cap_started:
                cap_msg += line
        i = i + timedelta(1)
    
if __name__ == "__main__":
    init()
