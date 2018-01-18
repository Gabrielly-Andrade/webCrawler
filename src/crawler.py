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

    def save_product(self):
        csv_file = ExportCsv("../results.csv")
        csv_file.append_file(self.title, self.name, self.url)


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
            write.writerow([title, name, url])


class Crawler:

    def __init__(self):
        self.__driver = webdriver.Firefox()
        self.__driver.maximize_window()

    def get_categories(self, main_url):
        self.__driver.get(main_url)
        categories_pages = []
        page_list = self.__driver.find_elements_by_xpath(
            "//ul[@class='menu__list']/li[1]/div/ul/li/a")
        for page in page_list:
            url = page.get_attribute("href")
            if "ofertas" not in url:
                categories_pages.append(url)
        self.__driver.quit()
        self.visit_categories(categories_pages)

    def visit_categories(self, categories_pages):
        for page in categories_pages:
            number_page = 1
            while True:
                self.__init__()
                self.__driver.get(page + "#" + str(number_page))
                if not self.__driver.find_elements_by_class_name(
                        "shelf-default__item"):
                    self.__driver.quit()
                    break
                self.extract_products()
                number_page += 1

    def extract_products(self):
        # This method extract the title, product name and url
        # from each product of the page given
        url_list = self.__driver.find_elements_by_class_name("shelf-default__link")
        for url in url_list:
            url = url.get_attribute("href")
            self.__driver.implicitly_wait(10)
            title = self.get_title(url)
            #name_list = extract_complete_name_products(url)
            #for name in name_list:
            new_product = Products(title, "test", url)
            new_product.save_product()
        self.__driver.close()

    def get_title(self, url):
        # This function extract the tag title from
        # each page of product
        soup = self.extract_source_code_product(url)
        title = soup.find("title").string
        return title

    def extract_source_code_product(self, url):
        # This function extract the source code
        # of each page of product
        source_code = url.get_attribute("href")
        source_code = requests.get(source_code)
        plain_text = source_code.text
        soup = BeautifulSoup(plain_text, "lxml")
        return soup


def main():
    csv_file = ExportCsv("../results.csv")
    csv_file.create_file()

    epoca_cosmeticos = Crawler()
    epoca_cosmeticos.get_categories("http://www.epocacosmeticos.com.br/")


if __name__ == '__main__':
    main()