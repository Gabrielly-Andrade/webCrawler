# -*- encoding: utf-8 -*-
# Created on 2017-12-16 22:17:36
# Project: epocacosmeticos
# Author: Gabrielly de Andrade

from selenium import webdriver
from bs4 import BeautifulSoup
import requests
import re
import csv
import json


class Products:

    def __init__(self, title, name, url):
        self.title = title
        self.name = name
        self.url = url


class ExportCsv:

    def __init__(self, file_name):
        self.file_name = file_name

    def create_file(self):
        csv_file = open(self.file_name, "w", newline='')
        file = csv.writer(csv_file)
        file.writerow(["title", "product name", "url"])
        csv_file.close()

    def append_file(self, title, name, url):
        with open("../results.csv", "a", newline='') as csv_file:
            write = csv.writer(csv_file)
            write.writerow([self.title, self.name, self.url])


class Crawler:

    def __init__(self):
        self.driver = webdriver.Firefox()
        self.driver.maximize_window()

    def get_categories(self, main_url):
        self.driver.get(main_url)
        categories_pages = []
        page_list = self.driver.find_elements_by_xpath(
            "//ul[@class='menu__list']/li[1]/div/ul/li/a")
        for page in page_list:
            url = page.get_attribute("href")
            if "ofertas" not in url:
                categories_pages.append(url)
        self.driver.quit()
        self.visit_categories(categories_pages)

    def visit_categories(self, categories_pages):
        for page in categories_pages:
            number_page = 1
            while True:
                self.__init__()
                self.driver.get(page + "#" + str(number_page))
                if not self.driver.find_elements_by_class_name(
                        "shelf-default__item"):
                    self.driver.quit()
                    break
                extract_products()
                number_page += 1

def main():
    csv_file = ExportCsv("../results.csv")
    csv_file.create_file()

    epoca_cosmeticos = Crawler()
    epoca_cosmeticos.get_categories("http://www.epocacosmeticos.com.br/")


if __name__ == '__main__':
    main()