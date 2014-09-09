import urllib2
import os
import re
import simplejson
from bs4 import BeautifulSoup

def crawl():
    installed_list = list()
    response = urllib2.urlopen("https://www.facebook.com/appcenter/my")
    page_source = response.read()
    soup = BeautifulSoup(page_source)
    print soup.find_all("td", class_ = "_51m- appsListItem")


def main():
    crawl()

if __name__ == '__main__':
    main()



