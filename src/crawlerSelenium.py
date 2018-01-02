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

def appendCsvFile(title, productName, url):
	with open("../results.csv","a", newline='') as csvFile:
		write = csv.writer(csvFile)
		write.writerow([title , productName , url])
	csvFile.close()

chromePath = r"C:\Users\Gabri\webDriver\chromedriver.exe"

csvFile()

for numberPage in range (1,3):
	#Creating the instance of Chrome WebDriver
	driver = webdriver.Chrome(chromePath)
	#Navigating to the page given by the URL
	driver.get("http://www.epocacosmeticos.com.br/selecao/acao#" + str(numberPage))
	#Confirming that title has "Época Cosméticos" word in it
	assert "Época Cosméticos" in driver.title

	titleList = driver.find_elements_by_xpath("//span[@class='shelf-default__brand']/a")
	#print (titleList) 
	productNameList = driver.find_elements_by_class_name("shelf-default__product-name")
	urlList = driver.find_elements_by_class_name("shelf-default__link")

	for i in range (len(titleList)):
		appendCsvFile(titleList[i].text, \
				productNameList[i].text, urlList[i].get_attribute("href"))	

	titleList.clear()
	driver.close()

	'''
	Trying to use a automatic pagination, but without success :/ 
	#for i in range (1,3):
	driver.find_element_by_xpath("//*[@id='PagerBottom_26687552']/ul/li[8]").click()
	titleList2 = driver.find_elements_by_xpath("//span[@class='shelf-default__brand']/a") 
	for title in titleList2:
		print(title.text)
	'''
