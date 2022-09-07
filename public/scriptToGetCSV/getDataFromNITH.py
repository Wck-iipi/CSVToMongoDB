import requests
from requests.structures import CaseInsensitiveDict
from bs4 import BeautifulSoup
import csv
import concurrent.futures
import threading
import time
from pathlib import Path

base_path = Path(__file__).parent
file_path_csv = (base_path / "../NITResults.csv" ).resolve()
file_path_rollNumberTxt = (base_path / "./RollNumbersDone.txt")
file_path_allRollNumber = (base_path / "./AllRollNumber.txt" )

allStudentsTillNow = {}
csv_writer_lock = threading.Lock()
outputString = ''
emailDictionary = {}

# Emptying the rollNumberTxt file so that the file runs
with open(file_path_rollNumberTxt,'r') as f:
	f.write("")



#gives the final results and returns emailOfStudent(No significance of return though)
def getResultsInCSV(emailOfStudent):
	writer = csv.writer(outfile)
	url = "http://14.139.56.19/scheme"+str(emailOfStudent[:2])+"/studentresult/result.asp"
	headers = CaseInsensitiveDict()
	headers["Content-Type"] = "application/x-www-form-urlencoded"

	data = "RollNumber="+str(str(emailOfStudent).replace('@nith.ac.in',''))

	resp = requests.post(url, headers = headers, data = data)
	html = resp.text
	parsed_html = BeautifulSoup(html,'lxml')

	#Below lines are there for scraping the CGPA, SGPA, and numbers grades in subjects 
	tagsForEverythingExceptMarks=parsed_html.find_all('p',attrs={"style":'float:right;text-align: right; font-weight:bold;'})
	name = parsed_html.find_all('p', attrs = {"style": "float:right;text-align: right;font-weight:bold;"})
	tagsForIndividualMarks =parsed_html.find_all(lambda tag: tag.name == 'td' and not tag.attrs)

	arrayForEverythingExceptMarks=[]
	arrayForIndividualMarks=[]

	# following lines will append the values to arrays
	for element in tagsForEverythingExceptMarks:
		soupa = BeautifulSoup(str(element),'html.parser')
		arrayForEverythingExceptMarks.append(soupa.get_text())

	nameSoup = BeautifulSoup(str(name), 'html.parser')
	requiredName = nameSoup.get_text()

	arrayForEverythingExceptMarks.append(requiredName.replace('[', '').replace(']','').strip())

	for element in tagsForIndividualMarks:
		soupa = BeautifulSoup(str(element),'html.parser')
		arrayForIndividualMarks.append(soupa.get_text())
	arrayForWritingRows = []

	#Check if data is valid by checking if Roll Number and father's name are given 
	if arrayForEverythingExceptMarks[0] and arrayForEverythingExceptMarks[1]:
		arrayForWritingRows.append([arrayForEverythingExceptMarks[0],arrayForEverythingExceptMarks[1],arrayForEverythingExceptMarks[-1],"NULL","NULL","NULL"])
		currentIndex=2
		counterForCGPA=2
		for r in range(1000):
			rowForCSV=[]
			for q in range(6):
				rowForCSV.append(arrayForIndividualMarks[r*6+q])
			arrayForWritingRows.append(rowForCSV)

			if (r+1)*6 +1>len(arrayForIndividualMarks):
				tempArray=[]
				for x in range(5):
					tempArray.append(arrayForEverythingExceptMarks[counterForCGPA+x])
				arrayForWritingRows.append(tempArray)
				counterForCGPA+=5
				break

			if(int(arrayForIndividualMarks[(r+1)*6])==currentIndex):
				currentIndex+=1
			else:
				tempArray=[]
				for x in range(5):
					tempArray.append(arrayForEverythingExceptMarks[counterForCGPA+x])
				arrayForWritingRows.append(tempArray)
				counterForCGPA+=5
				currentIndex=2

	arrayForWritingRows.append(['NewLine','NewLine','NewLine','NewLine','NewLine','NewLine'])

	#locking since the writerows function is not multithreading safe
	with csv_writer_lock:
		writer.writerows(arrayForWritingRows)


	emailDictionary[emailOfStudent] = 1
	return emailOfStudent

emailArray =[]

with open(file_path_rollNumberTxt,'r') as f:
	lines = f.read()
	emailArray =lines.replace('ï»¿','').split(',')



whatWeWantToLoopOver = []
isThereChange = False
with open(file_path_csv, 'w', newline='') as outfile:
	with open(file_path_rollNumberTxt,'r') as bothfile:
		data = bothfile.read()

		emailArray2 =data.replace('ï»¿','').split('\n')
		emailArray2 = list(filter(('').__ne__, emailArray2))

		for r in emailArray2:
			emailDictionary[r] = 1


		for email in emailArray:

			if not email in emailDictionary:
				whatWeWantToLoopOver.append(email)



		with concurrent.futures.ThreadPoolExecutor() as executor:
			for elementInLoopRequired in whatWeWantToLoopOver:

				for x in range(10):
					try :
						results = executor.submit(getResultsInCSV, elementInLoopRequired)
						isThereChange = True
						break
					except:
						time.sleep(5)
						continue

		if isThereChange:
			for r in emailDictionary:
				outputString += r
				outputString += "\n"


if isThereChange:
	with open(file_path_rollNumberTxt,'w') as bothfile:
		bothfile.write(outputString)




