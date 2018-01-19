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
        return categories_pages

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
        url_list = self.get_urls()
        for url in url_list:
            url = url.get_attribute("href")
            self.__driver.implicitly_wait(10)
            soup = self.extract_source_code_product(url)
            title = self.get_title(url, soup)
            name_list = self.get_names(url, soup)
            for name in name_list:
                new_product = Products(title, name, url)
                new_product.save_product()
        self.__driver.close()

    @staticmethod
    def extract_source_code_product(url):
        # This function extract the source code
        # of each page of product
        source_code = requests.get(url)
        plain_text = source_code.text
        soup = BeautifulSoup(plain_text, "lxml")
        return soup

    @staticmethod
    def extract_json_variations(url, soup):
        # This function extract the json who contains
        # the variations of each product
        script = soup.find("script", text=re.compile(r"skuJson_0"))
        try:
            json_text = re.search(r"\s*skuJson_0\s*=\s*({.*})\s*;\s*",
                                  script.string, flags=re.DOTALL | re.MULTILINE).group(1)
        except AttributeError:
            pass
        else:
            return json_text

    @staticmethod
    def extract_name_product_without_variation(url, soup):
        # This function extract the main product name
        # from each page of product
        find_element = soup.find("div", {"class", "product__floating-info--name"})
        product_name = find_element.find("div").string
        return product_name

    @staticmethod
    def get_title(url, soup):
        # This function extract the tag title from
        # each page of product
        title = soup.find("title").string
        return title

    def get_urls(self):
        return self.__driver.find_elements_by_class_name("shelf-default__link")

    def get_names(self, url, soup):
        # This function extract the name of each product
        # plus your dimension from a script
        name_list = []
        product_name = self.extract_name_product_without_variation(url, soup)
        json_text = self.extract_json_variations(url, soup)
        if json_text:
            data = json.loads(json_text)
            dimensions_map = (data["dimensionsMap"])
            variations_list = list(dimensions_map.values())[0]
            if type(variations_list) == list and len(variations_list) > 1:
                for variation in variations_list:
                    name_list.append(product_name + " " + "-" + " " + variation)
                return name_list
        name_list.append(product_name)
        return name_list


def main():
    csv_file = ExportCsv("../results.csv")
    csv_file.create_file()

    epoca_cosmeticos = Crawler()
    categories_pages = epoca_cosmeticos.get_categories("http://www.epocacosmeticos.com.br/")
    epoca_cosmeticos.visit_categories(categories_pages)


if __name__ == '__main__':
    main()