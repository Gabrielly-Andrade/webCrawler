# -*- encoding: utf-8 -*-
# Created on 2018-01-13 16:44:21
# Project: epocacosmeticos
# Author: Gabrielly de Andrade

import unittest
from crawler import Crawler


class TestCrawler(unittest.TestCase):

    def test_get_categories(self):
        instance_driver = Crawler()
        result = instance_driver.get_categories("http://www.epocacosmeticos.com.br/")
        self.assertEqual(result, ['https://www.epocacosmeticos.com.br/perfumes',
                                  'https://www.epocacosmeticos.com.br/cabelos',
                                  'https://www.epocacosmeticos.com.br/maquiagem',
                                  'https://www.epocacosmeticos.com.br/dermocosmeticos',
                                  'https://www.epocacosmeticos.com.br/tratamentos',
                                  'https://www.epocacosmeticos.com.br/corpo-e-banho',
                                  'https://www.epocacosmeticos.com.br/unhas',
                                  'https://www.epocacosmeticos.com.br/lancamentos',
                                  'https://www.epocacosmeticos.com.br/ganhe-brindes',
                                  'https://www.epocacosmeticos.com.br/quero-cupom'])


if __name__ == '__main__':
    unittest.main()






















'''
class webCrawlerTest(unittest.TestCase):

	def csvFile(self):
		csvFile = open("../results.csv","w", newline='')
		file = csv.writer(csvFile)
		file.writerow(["title","productName","url"])
		csvFile.close()

	def appendCsvFile(self, title, productName, url):
		with open("../results.csv","a", newline='') as csvFile:
			write = csv.writer(csvFile)
			write.writerow([title , productName , url])
		csvFile.close()

	def setUp(self):
		self.driver = webdriver.Chrome()

	def extractFromURL(self, url):
		for numberPage in range (1,2):
			driver = self.driver
			driver.get("http://www.epocacosmeticos.com.br/selecao/acao#1")
			#driver.get(url + str(numberPage))

			titleList = driver.find_elements_by_xpath("//span[@class='shelf-default__brand']/a")
			productNameList = driver.find_elements_by_class_name("shelf-default__item")
			urlList = driver.find_elements_by_class_name("shelf-default__link")

			for i in range (len(titleList)):
				self.appendCsvFile(titleList[i].text, productNameList[i].get_attribute("title"), \
				urlList[i].get_attribute("href"))	
	
	def tearDown(self):
		self.driver.close()


def main ():
	webCrawler().csvFile()
	webCrawler().extractFromURL("http://www.epocacosmeticos.com.br/selecao/acao#")

if __name__ == '__main__':
    unittest.main()

  '''