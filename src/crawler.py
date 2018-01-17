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


def main():
    csv_file = ExportCsv("../results.csv")
    csv_file.create_file()


if __name__ == '__main__':
    main()