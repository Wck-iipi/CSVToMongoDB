import requests
from requests.structures import CaseInsensitiveDict
from bs4 import BeautifulSoup
import csv
import concurrent.futures
import threading
import time
allStudentsTillNow = {}
csv_writer_lock = threading.Lock()
outputString = ''
emailDictionary = {}

def getResultsInCSV(emailOfStudent):
	print(emailOfStudent)
	writer = csv.writer(outfile)
	url = "http://14.139.56.19/scheme"+str(emailOfStudent[:2])+"/studentresult/result.asp"
	headers = CaseInsensitiveDict()
	headers["Content-Type"] = "application/x-www-form-urlencoded"

	data = "RollNumber="+str(str(emailOfStudent).replace('@nith.ac.in',''))

	resp = requests.post(url, headers = headers, data = data)
	html = resp.text
	parsed_html = BeautifulSoup(html,'lxml')

	# print(url)
	# print(data)
	tagsForEverythingExceptMarks=parsed_html.find_all('p',attrs={"style":'float:right;text-align: right; font-weight:bold;'})
	name = parsed_html.find_all('p', attrs = {"style": "float:right;text-align: right;font-weight:bold;"})
	arrayForEverythingExceptMarks=[]
	tagsForIndividualMarks =parsed_html.find_all(lambda tag: tag.name == 'td' and not tag.attrs)
	arrayForIndividualMarks=[]


	for element in tagsForEverythingExceptMarks:
		
		soupa = BeautifulSoup(str(element),'html.parser')
		# print(soupa.get_text())
		arrayForEverythingExceptMarks.append(soupa.get_text())
	
	nameSoup = BeautifulSoup(str(name), 'html.parser')
	requiredName = nameSoup.get_text()

	arrayForEverythingExceptMarks.append(requiredName.replace('[', '').replace(']','').strip())

	for element in tagsForIndividualMarks:
		soupa = BeautifulSoup(str(element),'html.parser')
		arrayForIndividualMarks.append(soupa.get_text())
	# print(arrayForEverythingExceptMarks[0])
	# print(arrayForEverythingExceptMarks[1])
	# print(arrayForEverythingExceptMarks)
	arrayForWritingRows = []
	if arrayForEverythingExceptMarks[0] and arrayForEverythingExceptMarks[1]:
		arrayForWritingRows.append([arrayForEverythingExceptMarks[0],arrayForEverythingExceptMarks[1],arrayForEverythingExceptMarks[-1]])
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
	
	arrayForWritingRows.append([''])
	
	with csv_writer_lock:
		writer.writerows(arrayForWritingRows)
	
	emailDictionary[emailOfStudent] = 1
	return emailOfStudent

emailArray =[]

with open('C:\\Users\\VarunK\\Desktop\\DSA\\QuestionsPython\\AllRollNumber.txt','r') as f:
	lines = f.read()
	emailArray =lines.replace('ï»¿','').split(',')

whatWeWantToLoopOver = []

for _ in range(10):

	with open('C:\\Users\\VarunK\\Desktop\\DSA\\QuestionsPython\\NITResults.csv', 'w', newline='') as outfile:
		with open('C:\\Users\\VarunK\\Desktop\\DSA\\QuestionsPython\\RollNumbersDone.txt','r') as bothfile:
			data = bothfile.read()

			emailArray2 =data.replace('ï»¿','').split('\n')
			if '' in emailArray2:
				emailArray2.remove('')
			bothfile.seek(0)
			# print(emailArray2)
			
			

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
							break
						except:
							time.sleep(5)
							continue

				# for result in results:
				# 		emailDictionary[result] = 1
						
					# print(email)
			
			for r in emailDictionary:
				outputString += r	
				outputString += "\n"
				
			# print(outputString)
	with open('C:\\Users\\VarunK\\Desktop\\DSA\\QuestionsPython\\RollNumbersDone.txt','w') as bothfile:
		bothfile.write(outputString)

	time.sleep(5)

		

#getResultsInCSV('21dcs006@nith.ac.in')

	

# 	with concurrent.futures.ThreadPoolExecutor() as executor:
# 		threadList=[]
		
# 		#indexOf182002 = emailArray.index('182002@nith.ac.in')
# 		for r in range(len(emailArray)):
# 		# for r in range(100):
# 			if not emailArray[r].replace('@nith.ac.in','').upper() in forbidenRollNumber:
# 				if not emailArray[r].replace('@nith.ac.in','').upper() in allStudentsTillNow:
# 					threadList.append(executor.submit(getResultsInCSV,emailArray[r]))


# with open('C:\\Users\\VarunK\\Desktop\\DSA\\QuestionsPython\\NITResults.csv','r') as infile1:
# 	with open('C:\\Users\\VarunK\\Desktop\\DSA\\QuestionsPython\\NITResultsExp.csv','w',newline='') as outfile1:
# 		csvReader=csv.reader(infile1)
# 		writer= csv.writer(outfile1)
# 		for data in csvReader:
# 			arrayToWrite=[]
# 			for x in data:
# 				arrayToWrite.append(x.strip())

# 			writer.writerow(arrayToWrite)