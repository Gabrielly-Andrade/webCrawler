# -*- encoding: utf-8 -*-
# Created on 2017-12-27 22:24:36
# Project: epocacosmeticos
# Author: Gabrielly de Andrade

# Import the module to webscrape dynamic content from a page
from selenium import webdriver
import csv


def csvFile():
    csvFile = open("../results.csv", "w", newline='')
    file = csv.writer(csvFile)
    file.writerow(["title", "productName", "url"])
    csvFile.close()


def appendCSVFile(title, productName, url):
    with open("../results.csv", "a", newline='') as csvFile:
        write = csv.writer(csvFile)
        write.writerow([title.text, productName.get_attribute("title"), \
                        url.get_attribute("href")])
    csvFile.close()


def checkRepetition(url):
    global products
    link = url.get_attribute("href")
    if link not in products:
        products.add(link)
        return False
    return True


def extractFromURL(driver):
    # This function extract the title, product name and url
    # from each product of the page given
    global numPagination
    global html
    # temporary, need smth better
    try:
        driver.implicitly_wait(10)
        titleList = driver.find_elements_by_xpath(
            "//span[@class='shelf-default__brand']/a")
        productNameList = driver.find_elements_by_class_name(
            "shelf-default__item")
        urlList = driver.find_elements_by_class_name(
            "shelf-default__link")
    except Exception:
        print("Opps. Error in page", numPagination, "from", html, "trying again...")
        setUp(html, numPagination)
    else:
        try:
            for i in range(len(titleList)):
                if checkRepetition(urlList[i]) == False:
                    appendCSVFile(titleList[i], productNameList[i], urlList[i])
                else:
                    print("produto repetido: ", urlList[i].get_attribute("href"))
        except Exception:
            print("Sorry, something went wrong on page", numPagination, "from", html, "trying again...")
            setUp(html, numPagination)
    finally:
        driver.close()


def setUp(categoryURL, numberPage=1):
    # This function control the number (section or navigation) of each
    # category page and create a loop to call other auxiliary functions
    global numPagination
    numPagination = numberPage
    global products
    products = set()
    while True:
        driver = getWebDriver()
        driver.get(categoryURL + "#" + str(numPagination))
        if not driver.find_elements_by_class_name("shelf-default__item"):
            driver.close()
            break
        extractFromURL(driver)
        numPagination += 1


def getLinks(driver, mainURL):
    # This function get all the links in the category section
    # and return a list of pages to scrape
    driver.get(mainURL)
    pages = []
    pageList = driver.find_elements_by_xpath(
        "//ul[@class='menu__list']/li[1]/div/ul/li/a")
    for i in range(0, len(pageList)):
        url = pageList[i].get_attribute("href")
        if "ofertas" not in url:
            pages.append(url)
    driver.close()
    return pages


def getWebDriver():
    # This function returns the instance of Firefox
    # WebDriver
    driver = webdriver.Firefox()
    driver.maximize_window()
    return driver


def main():
    global html
    csvFile()
    driver = getWebDriver()
    pages = getLinks(driver, "http://www.epocacosmeticos.com.br/")
    print(pages)
    for i in range(0, len(pages)):
        html = pages[i]
        setUp(html)


if __name__ == '__main__':
    main()
