import csv
import urllib2
import pandas as pd

# Let ArcGIS Open Data do the filtering of the VicRoads crash data 
# Get the crash data CSV filtered to 'BICYCLIST > 1' 
# Could potentially also filter on map extent if required
# Remember this data changes frequently, so each time we run this it maybe different results
url = 'http://vicroadsopendata.vicroadsmaps.opendata.arcgis.com/datasets/c2a69622ebad42e7baaa8167daa72127_0.csv?where=BICYCLIST%20%3E%3D%201&inSR=102100&geometry=%7B%22xmin%22%3A13844444.803560872%2C%22ymin%22%3A-4749031.404608972%2C%22xmax%22%3A18499154.078013726%2C%22ymax%22%3A-4015235.9330714755%2C%22spatialReference%22%3A%7B%22wkid%22%3A102100%2C%22latestWkid%22%3A3857%7D%7D'
response = urllib2.urlopen(url)
cr = csv.reader(response)
# Push the response into a Pandas data frame called bc for bike crashes
bc = pd.read_csv(response, parse_dates=['ACCIDENT_DATE', 'ACCIDENT_TIME'])  

# This lets me look at the first ten rows, for just the 2 columns
bc[['DAY_OF_WEEK', 'TOTAL_PERSONS']][:10]

# Which day do most crashes happen on?
crashes_by_day = bc['DAY_OF_WEEK'].value_counts()
print crashes_by_day

# But lets take that further and plot them
#crashes_by_day.plot(kind='bar')

# Add an additional column to break out the months
bc['month'] = [t.month for t in bc.ACCIDENT_DATE]
# Then aggregate the totals by month
crashes_by_month = bc['month'].value_counts()
crashes_by_month = crashes_by_month.sort_index()

crashes_by_month.plot(kind='bar')


# Convert 'ACCIDENT_TIME' from a string to a timestamp
bc['ACCIDENT_TIME'] = pd.to_datetime(bc['ACCIDENT_TIME'], format ='%H.%M.%S')

bc2 = bc.set_index('ACCIDENT_TIME')
bc2.index.name = None

# Group into one minute intervals
crashes_by_minute = bc2.groupby(bc.ACCIDENT_TIME.map(lambda t: t.minute))



######NOTES#########
#Try to aggregate by time

#Check type of field
bc['ACCIDENT_TIME'].dtype

#bc['hour'] = [t.month for t in bc.ACCIDENT_DATE]

#Group by hour
# Set the index to the time field
#times = pd.to_datetime(bc.

#bc.set_index('ACCIDENT_TIME')
#crashes_by_hour = bc.groupby(lamda x: 

#crashes_by_hour = bc.groupby(bc.index.map(lambda t: t.minute))