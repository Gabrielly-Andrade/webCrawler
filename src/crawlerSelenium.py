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
	for i in range (len(titleList)):
		with open("../results.csv","a", newline='') as csvFile:
			write = csv.writer(csvFile)
			write.writerow([titleList[i].text, \
				productNameList[i].get_attribute("title"), \
				urlList[i].get_attribute("href")])
		csvFile.close()

def categoryPage(categoryURL, numberPage):
	#This function is responsible for navigate to a page given
	#with the main url (url category page) and the number
	#of the page (or section)
	global driver
	driver = webdriver.Firefox()
	driver.get(categoryURL + "#" + str(numberPage))

def extractFromURL():
	#This function extract the title, product name and url 
	#from each product of the page given
	global driver	
	titleList = driver.find_elements_by_xpath("//span[@class='shelf-default__brand']/a")
	productNameList = driver.find_elements_by_class_name("shelf-default__item")
	urlList = driver.find_elements_by_class_name("shelf-default__link")
	appendCSVFile(titleList, productNameList, urlList)
	driver.close()	

def setUp(categoryURL):
	#This function control the number (section or navigation) of each  
	#category page and create a loop to call other auxiliary functions
	global driver
	numberPage = 1
	while True:
		categoryPage(categoryURL, numberPage)
		if not driver.find_elements_by_class_name("shelf-default__item"):
			driver.close()
			break
		extractFromURL()			
		numberPage += 1

def getLinks(mainURL):
	#This function get all the links in the category section
	#and return a list of pages to scrape	
	global driver
	driver = webdriver.Firefox()
	driver.get(mainURL)
	pages = []
	pageList = driver.find_elements_by_xpath("//ul[@class='menu__list']/li[1]/div/ul/li/a")
	for i in range (0,len(pageList)):
		pages.append(pageList[i].get_attribute("href"))
	driver.close()
	return pages

def main ():
	csvFile()
	pages = getLinks("http://www.epocacosmeticos.com.br/")
	print (pages)
	#for i in range (0,len(pages)): -> not tested yet
	for i in range (0,1): #Testing only the "perfume" page
		setUp(pages[i])


if __name__ == '__main__':
    main()