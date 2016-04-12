#!/usr/bin/env python
#
# !!! Needs psutil (+ dependencies) installing:
#
#    $ sudo apt-get install python-dev
#    $ sudo pip install psutil
#
import time
import os
import sys
if os.name != 'posix':
    sys.exit('platform not supported')
import psutil

from datetime import datetime
from oled.device import ssd1306, sh1106
from oled.render import canvas
from PIL import ImageDraw, ImageFont
from stravalib import Client
from stravalib import unithelper
from datetime import datetime, timedelta

# Client ID: 10##4
# Client Secret:        816fa1e5705955d43f044687aee60fbba8#####
# Your Access Token:    0c293900673bf7ccf80180dfd3553a54fb#####

ctd = 0
ctc = 0
rtd = 0
rtc = 0
prbc = 0
prbr = 0

def greet():
	return "Hello, {}! Since {}".format(athlete.firstname, datetime.date(weekstart).strftime('%d/%b'))
#print("Hello, {}[{}]".format(athlete.firstname, athlete.email))

def calculate_stats():
	global ctd, ctc, rtd, rtc, prbc, prbr, athlete, weekstart
	
	NAQ_ACCESS_TOKEN = '0c293900673bf7ccf80180dfd3553a54fb#####'
	client = Client(access_token=NAQ_ACCESS_TOKEN)
	athlete = client.get_athlete() # Get John's full athlete record


	activities = client.get_activities(limit=10)
	assert len(list(activities)) == 10

	#find this week's activities
	today=datetime.today().strftime('%d/%b/%Y')
	todayntime=datetime.strptime(today,'%d/%b/%Y')
	weekstart=todayntime - timedelta(days=todayntime.weekday())
	weekend=weekstart + timedelta(days=6)

#print("** For this week, that started on {} **".format(weekstart))
	#print 'Since Monday ...'
	for a in activities:
       	 if datetime.date(a.start_date) >= datetime.date(weekstart):
       	         act=client.get_activity(a.id) # need this for calories - not available in summary
       	         #TODO get segements + PRs 
       	         if a.type == 'Ride':
       	                 ctd += float(a.distance)
       	                 ctc += act.calories
       	         elif a.type == 'Run':
       	                 rtd += float(a.distance)
       	                 rtc += act.calories
                #print("On {} you did {} for distance {} at avg speed: {} calories {}".format(a.start_date, a.type, unithelper.kilometers(a.distance),a.average_speed, a.calories))

def cycling():
	#print("*********************")
	#print "__ Cycling __"
	#print("Distance: {} km".format(ctd/1000))
	#print("Calories: {} cal".format(ctc))
	#print("*********************")
	return "Rode:{0:.2f}km @ {1}cals".format(ctd/1000,ctc) 

def running():
	#print "__ Running __"
	#print("Distance: {} km".format(rtd/1000))
	#print("Calories: {} cal".format(rtc))
	#print("*********************")
	return "Ran:{0:.2f}km @ {1}cals".format(rtd/1000,rtc) 

def line():
	return "----------"                                  
def strava():
	return "_____s_t_r_a_v_a_________"

def stats(oled):
	font = ImageFont.load_default()
	font2 = ImageFont.truetype('fonts/C&C Red Alert [INET].ttf', 12)
	with canvas(oled) as draw:
		draw.text((0, 0), greet(), font=font2, fill=255)
        	#draw.text((0, 14), line(), font=font2, fill=255)
		draw.text((0, 12), cycling(), font=font2, fill=255)
        	#draw.text((0, 38), line(), font=font2, fill=255)
		draw.text((0, 24), running(), font=font2, fill=255)
		draw.text((0, 36), "         W00t W00t!",font=font2, fill=255)
		draw.text((0, 48), strava(), font=font2, fill=255)
		#time.sleep(1)

def main():
	calculate_stats()
	oled = ssd1306(port=1, address=0x3C)
	stats(oled)

if __name__ == "__main__":
    main()
