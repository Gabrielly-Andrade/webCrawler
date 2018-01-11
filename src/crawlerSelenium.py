# -*- encoding: utf-8 -*-
# Created on 2017-12-27 22:24:36
# Project: epocacosmeticos
# Author: Gabrielly de Andrade

# Import the module to webscrape dynamic content from a page
from selenium import webdriver
import csv


def csv_file():
    csvfile = open("../results.csv", "w", newline='')
    file = csv.writer(csvfile)
    file.writerow(["title", "productName", "url"])
    csvfile.close()


def append_csv_file(title, name, url):
    with open("../results.csv", "a", newline='') as csvfile:
        write = csv.writer(csvfile)
        write.writerow([title.text, name.get_attribute("title"),
                        url.get_attribute("href")])
        csvfile.close()


def check_repetition(url):
    # This function check for repeated url's
    global products
    link = url.get_attribute("href")
    if link not in products:
        products.add(link)
        return False
    return True


def extract_from_url(driver):
    # This function extract the title, product name and url
    # from each product of the page given
    global num_pagination
    global page
    try:
        driver.implicitly_wait(10)
        title_list = driver.find_elements_by_xpath(
            "//span[@class='shelf-default__brand']/a")
        name_list = driver.find_elements_by_class_name(
            "shelf-default__item")
        url_list = driver.find_elements_by_class_name(
            "shelf-default__link")
        for i in range(len(title_list)):
            if not check_repetition(url_list[i]):
                append_csv_file(title_list[i], name_list[i], url_list[i])
            else:
                print("repeated product: ", url_list[i].get_attribute("href"))
    except Exception:
        print("Ops. Error in page", num_pagination, "from", page, "trying again...")
        set_up(page, num_pagination)
    finally:
        driver.close()


def set_up(category_url, number_page=1):
    # This function control the number (section or navigation) of each
    # category page and create a loop to call other auxiliary functions
    global num_pagination
    num_pagination = number_page
    global products
    products = set()
    while True:
        driver = get_webdriver()
        driver.get(category_url + "#" + str(num_pagination))
        if not driver.find_elements_by_class_name("shelf-default__item"):
            driver.close()
            break
        extract_from_url(driver)
        num_pagination += 1


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
    global page
    csv_file()
    driver = get_webdriver()
    pages = get_links(driver, "http://www.epocacosmeticos.com.br/")
    print(pages)
    for page in pages:
        set_up(page)


if __name__ == '__main__':
    main()
