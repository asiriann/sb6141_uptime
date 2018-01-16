#!/usr/bin/python
# 2018-01-15 Tony Sirianni
# Used to check uptime of SB6141
# Will email when modem has been rebooted
import sys
import urllib2
from bs4 import BeautifulSoup
import datetime
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText

last_run_file = "/home/pi/last_run"
error_count_file = "/home/pi/error_count"
now = datetime.datetime.now()
status_page = 'http://192.168.100.1/indexData.htm'
max_retries = 60
fromaddr = "your@example.com"
toaddr =  "your@example.com"

try:
    page = urllib2.urlopen(status_page, timeout = 5)
except urllib2.URLError:
    try:
        file = open(error_count_file, "r")
	error_count = file.read()
        error_count = int(error_count) + 1
        file.close
        if  ( int(error_count) > max_retries ):
          msg = MIMEMultipart()
          msg['From'] = fromaddr
          msg['To'] = toaddr
          msg['Subject'] = "CANT REACH CABLE MODEM AFTER " + str(max_retries) + " RETRIES"
          body = "Tried reaching the cable modem for " + str(max_retries) + " tries.  Something is wrong"
          msg.attach(MIMEText(body, 'plain'))
          server = smtplib.SMTP('localhost', 25)
          server.ehlo()
          text = msg.as_string()
          server.sendmail(fromaddr, toaddr, text)
          error_count = "1"
          file = open(error_count_file, "w")
          file.write(error_count)
          file.close
          sys.exit(0)
        file = open(error_count_file, "w")
        file.write(str(error_count))
        file.close
        sys.exit(0)
    except IOError:
        file = open(error_count_file, "w")
        error_count = "1"
        file.write(error_count)
        file.close
        sys.exit(0)

file = open(error_count_file, "w")
error_count = "0"
file.write(error_count)
file.close
file = open(last_run_file, "r")
previous_uptime = file.read()
file.close

soup = BeautifulSoup(page, 'html.parser')

current_uptime = soup.find("td", text="System Up Time").find_next_sibling("td").text

print now.strftime("%Y-%m-%d %H:%M") + ' - ' + current_uptime

days,trash,time = current_uptime.split()
hours,minutes,seconds = time.split(":")
uptime_in_secs = (int(days) * 86400) + (int(hours.strip("h")) * 3600) + (int(minutes.strip("m")) * 60) + int(seconds.strip("s"))

file = open(last_run_file, "w")
file.write(str(uptime_in_secs))
file.close

if ( int(uptime_in_secs) <= int(previous_uptime)) :
	msg = MIMEMultipart()
	msg['From'] = fromaddr
	msg['To'] = toaddr
        msg['Subject'] = "CABLE MODEM REBOOT"
	body = str(now)
	msg.attach(MIMEText(body, 'plain'))

	server = smtplib.SMTP('localhost', 25)
	server.ehlo()
	text = msg.as_string()
	server.sendmail(fromaddr, toaddr, text)

sys.exit(0)
