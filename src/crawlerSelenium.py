# -*- encoding: utf-8 -*-
# Created on 2017-12-27 22:24:36
# Project: epocacosmeticos
# Author: Gabrielly de Andrade

# Import the module to webscrape dynamic content from a page
from selenium import webdriver
from bs4 import BeautifulSoup
import requests
import re
import csv
import json


def csv_file():
    csvfile = open("../results.csv", "w", newline='')
    file = csv.writer(csvfile)
    file.writerow(["title", "productName", "url"])
    csvfile.close()


def append_product(title, name, url):
    with open("../results.csv", "a", newline='') as csvfile:
        write = csv.writer(csvfile)
        write.writerow([title, name, url.get_attribute("href")])
        csvfile.close()


def extract_products(driver):
    # This function extract the title, product name and url
    # from each product of the page given
    driver.implicitly_wait(10) 
    url_list = driver.find_elements_by_class_name("shelf-default__link")
    i = 0
    for url in url_list:
        print (url)
        title = extract_title(url)
        name_list = extract_name_products(url)
        for name in name_list:
            append_product(title, name, url)
        i += 1
    driver.close()


def extract_source_code_product(url):
    # This function extract the source code
    # of each page of product
    source_code = url.get_attribute("href")
    source_code = requests.get(source_code)
    plain_text = source_code.text
    soup = BeautifulSoup(plain_text, "lxml")
    return soup


def extract_json_variations(url):
    # This function extract the json who contains
    # the variations of each product
    soup = extract_source_code_product(url)
    script = soup.find("script", text=re.compile(r"skuJson_\d"))
    json_text = re.search(r"\s*skuJson_\d\s*=\s*({.*})\s*;\s*",
                          script.string, flags=re.DOTALL | re.MULTILINE).group(1)
    return json_text


def extract_title(url):
    # This function extract the tag title from
    # each page of product
    soup = extract_source_code_product(url)
    title = soup.find("title").string
    return title


def extract_name_products(url):
    # This function extract the name of each product
    # plus your dimension from a script
    json_text = extract_json_variations(url)
    data = json.loads(json_text)
    name_list = []
    name_product = (data["name"])
    dimensions_list = (data["dimensionsMap"]["Variação"])
    for dimension in dimensions_list:
        name_list.append(name_product + " " + "-" + " " + dimension)
    return name_list


def set_up(category_url, number_page=1):
    # This function control the number (section or navigation) of each
    # category page and create a loop to call other auxiliary functions
    global products
    products = set()
    while True:
        driver = get_webdriver()
        driver.get(category_url + "#" + str(number_page))
        if not driver.find_elements_by_class_name("shelf-default__item"):
            driver.close()
            break
        extract_products(driver)
        number_page += 1


def get_links(driver, main_url):
    # This function get all the links in the category section
    # and return a list of pages to scrape
    driver.get(main_url)
    pages = []
    page_list = driver.find_elements_by_xpath(
        "//ul[@class='menu__list']/li[1]/div/ul/li/a")
    for page in page_list:
        url = page.get_attribute("href")
        if "ofertas" not in url:
            pages.append(url)
    driver.close()
    return pages


def get_webdriver():
    # This function returns the instance of Firefox
    # WebDriver
    driver = webdriver.Firefox()
    driver.maximize_window()
    return driver


def main():
    csv_file()
    driver = get_webdriver()
    pages = get_links(driver, "http://www.epocacosmeticos.com.br/")
    set_up(pages[0]) #Testing with perfumes page
    #for page in pages:
        #set_up(page)


if __name__ == '__main__':
    main()
