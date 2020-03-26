import calendar
import datetime


class DateManager():
	
	def getDate(self):
		today=datetime.date.today()

		oneday=datetime.timedelta(days=1)
		
		yesterday = (today-oneday).strftime("%Y-%m-%d")

		m1 = calendar.MONDAY
		m2 = calendar.SUNDAY
		nextDay = today
		today = today.strftime("%Y-%m-%d")
		while nextDay.weekday() != m1:
			nextDay += oneday

		nextMonday = nextDay.strftime("%Y-%m-%d")

		while nextDay.weekday() != m2:
			nextDay += oneday

		nextSunday = nextDay.strftime("%Y-%m-%d")

		return {
			'today': today,
			'yesterday': yesterday,
			'nextMonday': nextMonday,
			'nextSunday': nextSunday
		}
