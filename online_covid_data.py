import csv
from urllib.request import urlretrieve as retrieve
from plotly.graph_objs import Bar
from plotly import offline
from datetime import datetime


#Download data
url = 'https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/ecdc/total_deaths.csv'
retrieve(url, 'web_covid_data.csv')

#Open data
with open('web_covid_data.csv', 'r') as read_data_file:
	csv_reader = csv.reader(read_data_file)
	header_row = next(csv_reader)

	#Get deaths from data
	dates, change_in_deaths, rolling_avs = [], [], []
	yday_death = 0
	seven_day_list = []
	week_rolling_total = 0
	
	for row in csv_reader:
		if datetime.strptime(row[0], '%Y-%m-%d') >= datetime.strptime('2020-03-07', '%Y-%m-%d'):
			current_date = datetime.strptime(row[0], '%Y-%m-%d')
			change_in_death = int(row[200]) - yday_death
			yday_death = int(row[200])
			dates.append(current_date)
			change_in_deaths.append(change_in_death)

			#Add line of best fit
			if len(seven_day_list) < 7:
				seven_day_list.append(change_in_death)
				week_rolling_total += change_in_death
				rolling_av = week_rolling_total / len(seven_day_list)
				rolling_avs.append(rolling_av)
			else:
				seven_day_list.append(change_in_death)
				del(seven_day_list[0])
				rolling_av = sum(seven_day_list) / len(seven_day_list)
				rolling_avs.append(rolling_av)
		else:
			continue

#Plot the data
data = [{
	'type': 'bar',
	'x': dates,
	'y': change_in_deaths,
	'opacity': 1,
	'name': 'X vs Y',
},
{
	'type': 'scatter',
	'x': dates,
	'y': rolling_avs,
	'name': 'Seven Day Rolling average',
}]

my_layout = {
	'title': 'Daily additional COVID-19 associated UK deaths by date reported',
	'xaxis': {'title': 'Date'},
	'yaxis': {'title': 'Daily Deaths'},
}

fig = {'data': data, 'layout': my_layout}
offline.plot(fig, filename='covid_data.html')
