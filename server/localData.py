import csv
import datetime
import sys  
reload(sys)  
sys.setdefaultencoding('utf8') 
from os import listdir

ID_INDEX = 0
NAME_INDEX = 1
GROUP_INDEX = 2

MAX_RECORDS = 1000

def getToday():
	return datetime.date.today().strftime("%Y-%m-%d")

def saveData(studentID, select):
	t = datetime.datetime.now()
	d = getToday() + '.csv'
	filesNameList = listdir('data/records')
	records = []
	counterDict = {}
	if d in filesNameList:
		with open('data/records/' + d, 'r') as csvfile:
			reader = csv.reader(csvfile)
			for row in reader:
				records.append(row)
				s = row[2]
				if s not in counterDict:
					counterDict[s] = 1
				else:
					counterDict[s] += 1

	mostVal = 0
	mostSelector = ''

	for s in counterDict:
		if counterDict[s] > mostVal:
			mostVal = counterDict[s]
			mostSelector = s

	fileSize = len(records)
	if fileSize >= MAX_RECORDS:
		records.pop(0)
	records.append([t, studentID, select])
	with open('data/records/' + d, 'w') as csvfile:
		writer = csv.writer(csvfile)
		writer.writerows(records)

	return mostSelector

def readPersonList():
	res = {}
	with open('data/personList.csv', 'r') as csvfile:
		data = csv.reader(csvfile)
		for row in data:
			res[row[0]] = {
				'name': row[1],
				'category': row[2]
			}
	return res


class DataProcessor(object):
	def __init__(self):
		self.personList = readPersonList()

	def getPrice(self):
		res = 0
		with open('data/price.csv', 'r') as csvfile:
			data = csv.reader(csvfile)
			for row in data:
				res = row[0]
				break
		return res

	def processData(self, d):
		studentID = d['id']
		targetName = d['name'].encode('utf-8')
		if studentID not in self.personList:
			return '0'
		elif targetName != self.personList[studentID]['name']:
			return '0'
		else:
			person = self.personList[studentID]
			ck = person['category']
			s = saveData(studentID, d['select'])
			if ck == 'A':
				return {
					'category': 'a'
				}
			elif ck == 'B':
				return {
					'category': 'b',
					'data': s
				}
			else:
				return {
					'category': 'c'
				}


