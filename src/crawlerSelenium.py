# -*- encoding: utf-8 -*-
# Created on 2017-12-27 22:24:36
# Project: epocacosmeticos
# Author: Gabrielly de Andrade

#Import the module to webscrape dynamic content from a page
from selenium import webdriver
import csv

def csvFile():
	csvFile = open("../results.csv","w", newline='')
	file = csv.writer(csvFile)
	file.writerow(["title","productName","url"])
	csvFile.close()

def appendCSVFile(titleList, productNameList, urlList):
	global products
	for i in range (len(titleList)):			
		link = urlList[i].get_attribute("href")
		if link not in products:
			with open("../results.csv","a", newline='') as csvFile:	
				write = csv.writer(csvFile)
				write.writerow([titleList[i].text, \
					productNameList[i].get_attribute("title"), \
					urlList[i].get_attribute("href")])
				products.add(link)
			csvFile.close()
		else:
			print("PRODUTO REPETIDO ", urlList[i].get_attribute("href")) #temporary

def categoryPage(categoryURL, numberPage):
	#This function is responsible for navigate to a page given
	#with the main url (url category page) and the number
	#of the page (or section)
	global driver
	driver = webdriver.Firefox()
	driver.maximize_window()
	driver.get(categoryURL + "#" + str(numberPage))

def extractFromURL():
	#This function extract the title, product name and url 
	#from each product of the page given
	global driver
	global numPagination
	global html
	#temporary, need smth better
	try:
		driver.implicitly_wait(10)
		titleList = driver.find_elements_by_xpath("//span[@class='shelf-default__brand']/a")
		productNameList = driver.find_elements_by_class_name("shelf-default__item")
		urlList = driver.find_elements_by_class_name("shelf-default__link")		
	except Exception:
		print("Opps. Error in page", numPagination, "from", html)
		print("Trying again...")
		setUp(html,numPagination)
	else:
		try:
			appendCSVFile(titleList, productNameList, urlList)
		except Exception:
			print("Sorry, something went wrong on page", numPagination, "from", html)
			print("Trying again...")
			setUp(html,numPagination)
	finally:
		driver.close()	

def setUp(categoryURL, numberPage=1):
	#This function control the number (section or navigation) of each  
	#category page and create a loop to call other auxiliary functions
	global driver
	global numPagination
	numPagination = numberPage
	while True:
		categoryPage(categoryURL, numPagination)
		if not driver.find_elements_by_class_name("shelf-default__item"):
			driver.close()
			break
		extractFromURL()			
		numPagination += 1

def getLinks(mainURL):
	#This function get all the links in the category section
	#and return a list of pages to scrape	
	global driver
	driver = webdriver.Firefox()
	driver.maximize_window()
	driver.get(mainURL)
	pages = []
	pageList = driver.find_elements_by_xpath("//ul[@class='menu__list']/li[1]/div/ul/li/a")
	for i in range (0,len(pageList)):
		pages.append(pageList[i].get_attribute("href"))
	driver.close()
	return pages

def main ():
	global html
	global products
	products = set()
	csvFile()
	pages = getLinks("http://www.epocacosmeticos.com.br/")
	print (pages)
	for i in range (0,len(pages)): 
		html = pages[i]
		setUp(html)


if __name__ == '__main__':
    main()