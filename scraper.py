from selenium import webdriver
from bs4 import BeautifulSoup
import time
import csv

url = "https://exoplanets.nasa.gov/discovery/exoplanet-catalog/"

browser = webdriver.Chrome("chromedriver")

browser.get(url)

time.sleep(10)


def scrape():
  headers = ["Name", "Light Years from Earth",
             "Planet Mass", "Stellar Magnitude", "Discovery Date"]
  planet_data = []
  for i in range(0, 437):
    soup = BeautifulSoup(browser.page_source, "html.parser")
    for ul_tag in soup.find_all("ul", attrs={"class", "exoplanet"}):
      li_tags = ul_tag.find_all("li")
      temp_list = []
      for index, li_tag in enumerate(li_tags):
        if index == 0:
          temp_list.append(li_tag.find_all("a")[0].contents[0])
        else:
          try:
            temp_list.append(li_tag.contents[0])
          except:
            temp_list.append("")
      planet_data.append(temp_list)
    browser.find_element_by_xpath(
        "//*[@id=\"primary_column\"]/div[1]/div[2]/div[1]/div/nav/span[2]/a").click()
  with open("nasa.csv", "w") as f:
    csvWriter = csv.writer(f)
    csvWriter.writerow(headers)
    csvWriter.writerows(planet_data)


scrape()
