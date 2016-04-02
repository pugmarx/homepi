from stravalib import Client
from stravalib import unithelper
from datetime import datetime, timedelta

# Client ID: 10784
# Client Secret:	816fa1e5705955d43f044687aee60fbba8cc24ec
# Your Access Token:	0c293900673bf7ccf80180dfd3553a54fb8d9542

NAQ_ACCESS_TOKEN = '0c293900673bf7ccf80180dfd3553a54fb8d9542'
client = Client(access_token=NAQ_ACCESS_TOKEN)
athlete = client.get_athlete() # Get John's full athlete record
print("Hello, {}[{}]".format(athlete.firstname, athlete.email))

activities = client.get_activities(limit=10)
assert len(list(activities)) == 10

#find this week's activities
today=datetime.today().strftime('%d/%b/%Y')
todayntime=datetime.strptime(today,'%d/%b/%Y')
weekstart=todayntime - timedelta(days=todayntime.weekday())
weekend=weekstart + timedelta(days=6)
#activities=activities.reverse()

#print("** For this week, that started on {} **".format(weekstart))
print 'Since Monday ...'
ctd = 0
ctc = 0
rtd = 0
rtc = 0
prbc = 0
prbr = 0
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
print("*********************")
print "__ Cycling __"
print("Distance: {} km".format(ctd/1000))
print("Calories: {} cal".format(ctc))
print("*********************")

print "__ Running __"
print("Distance: {} km".format(rtd/1000))
print("Calories: {} cal".format(rtc))
print("*********************")
