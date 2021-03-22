import csv

data = []

with open("scrap-data.csv", 'r') as f:
  csv_r = csv.reader(f)
  for row in csv_r:
    data.append(row)


headers = data[0]

planet_data = data[1:]

for data_pt in planet_data:
  data_pt[2] = data_pt[2].lower()
planet_data.sort(key=lambda planet_data: planet_data[2])

with open("data-2.csv", 'a+') as f:
  csv_w = csv.writer(f)
  csv_w.writerow(headers)
  csv_w.writerows(planet_data)
