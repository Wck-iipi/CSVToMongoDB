import requests
from requests.structures import CaseInsensitiveDict
from bs4 import BeautifulSoup
import csv
import concurrent.futures
import threading
import time
from pathlib import Path
import time

base_path = Path(__file__).parent
file_path_csv = (base_path / "../NITResults.csv" ).resolve()
file_path_rollNumberTxt = (base_path / "./RollNumbersDone.txt")
file_path_allRollNumber = (base_path / "./AllRollNumber.txt" )

allStudentsTillNow = {}
csv_writer_lock = threading.Lock()


#gives the final results and returns emailOfStudent(No significance of return though)
def getResultsInCSV(emailOfStudent):

	start = time.time()
	#Follows: ["name", "rollNumber", "fatherName", "cgpa", "cgpaTotal", "sgpa", "year", "grade", "cumulativePointsSemester"]
	arrayToBeAddedToCSV = ['' for x in range(9)]

	arrayToBeAddedToCSV[3] = []
	arrayToBeAddedToCSV[5] = []
	arrayToBeAddedToCSV[7] = {}
	arrayToBeAddedToCSV[8] = []

	url = "http://14.139.56.19/scheme"+str(emailOfStudent[:2])+"/studentresult/result.asp"
	headers = CaseInsensitiveDict()
	headers["Content-Type"] = "application/x-www-form-urlencoded"

	rollNumberString = "RollNumber="+str(str(emailOfStudent).replace('@nith.ac.in',''))

	resp = requests.post(url, headers = headers, data = rollNumberString)
	html = resp.text
	parsed_html = BeautifulSoup(html,'lxml')

	#Below lines are there for scraping the CGPA, SGPA, and numbers grades in subjects 
	tagsForEverythingExceptMarks=parsed_html.find_all('p',attrs={"style":'float:right;text-align: right; font-weight:bold;'})
	name = parsed_html.find_all('p', attrs = {"style": "float:right;text-align: right;font-weight:bold;"})
	tagsForIndividualMarks =parsed_html.find_all(lambda tag: tag.name == 'td' and not tag.attrs)

	arrayForEverythingExceptMarks=[]
	arrayForIndividualMarks=[]

	# following lines will append the values to arrays
	for r in range(len(tagsForEverythingExceptMarks)):
		soupa = BeautifulSoup(str(tagsForEverythingExceptMarks[r]),'html.parser')
		arrayForEverythingExceptMarks.append(soupa.get_text().strip())


	nameSoup = BeautifulSoup(str(name), 'html.parser')
	requiredName = nameSoup.get_text()
	arrayToBeAddedToCSV[0] = requiredName.strip('[ ]')

	

	for element in tagsForIndividualMarks:
		soupa = BeautifulSoup(str(element),'html.parser')
		arrayForIndividualMarks.append(soupa.get_text().strip())
	
	# print(arrayForEverythingExceptMarks)
	

	#assigns rollNumber
	arrayToBeAddedToCSV[1] = arrayForEverythingExceptMarks[0]
	#assigns fatherName
	arrayToBeAddedToCSV[2] = arrayForEverythingExceptMarks[1]
	
	# print(arrayForEverythingExceptMarks)
	for r in range(2,len(arrayForEverythingExceptMarks)):
		# here 5 is when the data gets for new array(is fixed)
		
		if r % 5 == 2:
			arrayToBeAddedToCSV[7][int(arrayForEverythingExceptMarks[r][1:3])] = {}
		elif r % 5 == 3:
			arrayToBeAddedToCSV[5].append(float(arrayForEverythingExceptMarks[r].split('=')[1]))
		elif r % 5 == 4:
			arrayToBeAddedToCSV[8].append(float(arrayForEverythingExceptMarks[r]))
		elif r % 5 == 0:
			arrayToBeAddedToCSV[3].append(float(arrayForEverythingExceptMarks[r].split('=')[1]))
	
	arrayToBeAddedToCSV[4] = float(arrayForEverythingExceptMarks[-2].split('=')[1])

	if arrayToBeAddedToCSV[1][2].lower() == 'b':
		arrayToBeAddedToCSV[6] = arrayToBeAddedToCSV[1][:3].lower()
	else:
		arrayToBeAddedToCSV[6] = arrayToBeAddedToCSV[1][:2]



	numberEncountered = 0
	currentSem = 1
	for r in range(len(arrayForIndividualMarks)):
		if r % 6 == 0:
			if int(arrayForIndividualMarks[r]) < numberEncountered:
				currentSem += 1
				numberEncountered = 0
			else : 
				numberEncountered += 1

		if r % 6 == 1:
			arrayToBeAddedToCSV[7][currentSem][arrayForIndividualMarks[r]] =arrayForIndividualMarks[r+1: r+5] 

	# print(arrayToBeAddedToCSV)
	#locking since the writerows function is not multithreading safe
	start1 = time.time()
	with csv_writer_lock:
		writer.writerow(arrayToBeAddedToCSV)

	end = time.time()
	
	print(f"Current thread {threading.get_ident()} : Start Time :{start1-start}, End Time: {end-start1}")

	
	return emailOfStudent

emailArray =[]

with open(file_path_allRollNumber,'r') as f:
	lines = f.read()
	emailArray =lines.replace('ï»¿','').split(',')


isThereChange = False
with open(file_path_csv, 'w', newline='') as outfile:
	writer = csv.writer(outfile)
	writer.writerow(["name", "rollNumber", "fatherName", "cgpa", "cgpaTotal", "sgpa", "year", "grade", "cumulativePointsSemester"])
	whatWeWantToLoopOver = []

	for email in emailArray:
		whatWeWantToLoopOver.append(email)



	with concurrent.futures.ThreadPoolExecutor() as executor:
		for elementInLoopRequired in whatWeWantToLoopOver:

			for x in range(10):
				try :
					results = executor.submit(getResultsInCSV, elementInLoopRequired)
					break
				except:
					time.sleep(5)
					continue


