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

def appendCsvFile(titleList, productNameList, urlList):
	for i in range (len(titleList)):
		with open("../results.csv","a", newline='') as csvFile:
			write = csv.writer(csvFile)
			write.writerow([titleList[i].text, \
				productNameList[i].get_attribute("title"), \
				urlList[i].get_attribute("href")])
		csvFile.close()

def navigation(url, numberPage):
	global driver
	driver = webdriver.Chrome()
	driver.get(url + str(numberPage))

def extractFromURL():
	global driver
		
	titleList = driver.find_elements_by_xpath("//span[@class='shelf-default__brand']/a")
	productNameList = driver.find_elements_by_class_name("shelf-default__item")
	urlList = driver.find_elements_by_class_name("shelf-default__link")

	appendCsvFile(titleList, productNameList, urlList)
	driver.close()	

def setUp(url):
	global driver
	numberPage = 1
	while True:
		navigation(url, numberPage)
		if not driver.find_elements_by_class_name("shelf-default__item"):
			driver.close()
			break
		extractFromURL()			
		numberPage += 1

def main ():
	csvFile()
	setUp("http://www.epocacosmeticos.com.br/selecao/acao#")

if __name__ == '__main__':
    main()