import csv
from urllib.request import urlretrieve as retrieve
import matplotlib.pyplot as plt
from datetime import datetime

#Download data
url = 'https://raw.githubusercontent.com/tomwhite/covid-19-uk-data/master/data/covid-19-totals-uk.csv'
retrieve(url, 'covid_data.csv')

#Open data
with open('covid_data.csv', 'r') as read_data_file:
	csv_reader = csv.reader(read_data_file)
	header_row = next(csv_reader)

	#Get deaths from data
	dates, deaths = [], []
	yday_death = 0
	for row in csv_reader:
		current_date = datetime.strptime(row[0], '%Y-%m-%d')
		death = int(row[3]) - yday_death
		yday_death = int(row[3])
		dates.append(current_date)
		deaths.append(death)

#Plot the data
plt.style.use('seaborn')
fig, ax = plt.subplots()
ax.plot(dates, deaths, c='red')

#Format the graph
ax.set_title("Covid-19 UK Deaths")
ax.set_xlabel('', fontsize=16)
fig.autofmt_xdate()
ax.set_ylabel('Daily Number of Deaths', fontsize=16)
ax.tick_params(axis='both', which='major', labelsize=16)

plt.show()
