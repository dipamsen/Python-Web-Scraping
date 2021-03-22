from selenium import webdriver
from bs4 import BeautifulSoup
import time
import csv
import requests

url = "https://exoplanets.nasa.gov/discovery/exoplanet-catalog/"

browser = webdriver.Chrome("chromedriver")

browser.get(url)

time.sleep(10)


def scrape_more_data(hyperlink):
  try:
    page = requests.get(hyperlink)
    soup = BeautifulSoup(page.content, 'html.parser')
    temp_list = []
    for tr_tag in soup.find_all("tr", attrs={"class", "fact_row"}):
      td_tags = tr_tag.find_all("td")
      for td_tag in td_tags:
        try:
          temp_list.append(td_tag.find_all(
              "div", attrs={"class", "value"})[0].contents[0])
        except:
          temp_list.append("")
  except:
    time.sleep(1)
    scrape_more_data(hyperlink)
  new_planet_data.append(temp_list)


headers = ["Name", "Light Years from Earth", "Planet Mass", "Stellar Magnitude", "Discovery Date",
           "Hyperlink", "Mass", "Planet Radius", "Orbital Radius", "Orbital Period", "Eccentricity", "Detection Method"]
planet_data = []
new_planet_data = []
final_planet_data = []


def scrape():
  for i in range(1, 437):
    while True:
      time.sleep(2)
      soup = BeautifulSoup(browser.page_source, "html.parser")
      current_page_number = int(soup.find_all(
          "input", attrs={"class", "page_num"})[0].get("value"))
      if current_page_number < i:
        browser.find_element_by_xpath(
            "//*[@id=\"primary_column\"]/footer/div/div/div/nav/span[2]/a").click()
      elif current_page_number > i:
        browser.find_element_by_xpath(
            "//*[@id=\"primary_column\"]/footer/div/div/div/nav/span[1]/a").click()
      else:
        break
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
      hyperlink_tag = li_tags[0]
      temp_list.append("https://exoplanets.nasa.gov" +
                       hyperlink_tag.find_all('a', href=True)[0]["href"])
      planet_data.append(temp_list)
    browser.find_element_by_xpath(
        "//*[@id=\"primary_column\"]/footer/div/div/div/nav/span[2]/a").click()
    print(f'{i} pages done.')


scrape()
for index, data in enumerate(planet_data):
  scrape_more_data(data[5])
  print(f"{index+1} page done")

for index, data in enumerate(planet_data):
  new_planet_data_elt = new_planet_data[index]
  new_planet_data_elt = [elem.replace("\n", "")
                         for elem in new_planet_data_elt]
  new_planet_data_elt = new_planet_data_elt[:7]
  final_planet_data.append(data + new_planet_data_elt)

with open("nasa.csv", "w") as f:
  csvWriter = csv.writer(f)
  csvWriter.writerow(headers)
  csvWriter.writerows(final_planet_data)
