import numpy as np
import pandas as pd
from geopy.geocoders import Nominatim 
from geopy.distance import geodesic
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt

df = pd.read_csv("apartment_dataset.csv")

unit_price = []
address = []
bed_number = []

# calculate the average price, number of bedrooms
for i in range(len(df)):
    if '/mo' in df['Prices'][i]:
        current_price = df['Prices'][i]
        if 'bd' in current_price:
            current_bed_number = int(current_price[current_price.find('\n')+1:current_price.find('bd')])
        else:
            current_bed_number = 1
        bed_number.append(current_bed_number)
        unit_price.append(int(current_price[current_price.find('$')+1:current_price.find('/mo')].replace(',','').replace('+',''))/current_bed_number)
        if '|' in df['Addresses'][i]:
            address.append(df['Addresses'][i].split('|')[1])
        else:
            address.append(df['Addresses'][i])
    else:
        for current_price in df['Prices'][i].split('$')[1:]:
            if 'Studio' in current_price:
                current_bed_number = 1
                if '+' in current_price:
                    unit_price.append(int(current_price[0:current_price.find('+')].replace(',',''))/current_bed_number)
                else:
                    unit_price.append(int(current_price[0:current_price.find(' ')].replace(',',''))/current_bed_number)
            else:
                if '+' in current_price:
                    current_bed_number = int(current_price[current_price.find('+')+1:current_price.find('bd')])
                    unit_price.append(int(current_price[0:current_price.find('+')].replace(',',''))/current_bed_number)
                else:
                    current_bed_number = int(current_price[current_price.find(' ')+1:current_price.find('bd')])
                    unit_price.append(int(current_price[0:current_price.find(' ')].replace(',',''))/current_bed_number)
            bed_number.append(current_bed_number)
            
            if '|' in df['Addresses'][i]:
                address.append(df['Addresses'][i].split('|')[1])
            else:
                address.append(df['Addresses'][i])

apartment_info = pd.DataFrame(list(zip(address, bed_number, unit_price)), 
                                columns =  ['Address', 'Bedroom_Number', 'Price'])


# Remove the rows without addresses
for idx, address in enumerate(apartment_info['Address']):
    if 'undisclosed' in address:
        apartment_info.drop(idx,inplace=True)
apartment_info.set_index(np.arange(len(apartment_info)))


geo_locator = Nominatim(user_agent="http")

# Get the latitudes and longitudes of Harvard and MIT
havard_location = geo_locator.geocode('Harvard University, Cambridge, MA, Cambridge, MA')
havard_lat_long = [havard_location.latitude, havard_location.longitude]

mit_location =  geo_locator.geocode('Massachusetts Institute of Technology, Cambridge, MA') 
mit_lat_long = [mit_location.latitude, mit_location.longitude]

distance = []

# Caluate the distance between the apartments and Havard and MIT
for idx,address in enumerate(apartment_info['Address']):
    print(idx)
    current_location = geo_locator.geocode(address)
    if current_location is not None:
        current_lat_long = [current_location.latitude, current_location.longitude]
        current_distane = geodesic(havard_lat_long, current_lat_long).miles + geodesic(mit_lat_long, mit_lat_long).miles
        if current_distane<15:
            distance.append(geodesic(havard_lat_long, current_lat_long).miles + geodesic(mit_lat_long, mit_lat_long).miles)
        else:
            apartment_info.drop(idx,inplace=True)
    else:
        apartment_info.drop(idx,inplace=True)

apartment_info.set_index(np.arange(len(apartment_info)), inplace = True)

apartment_info['Distance'] = distance

# Visulize the relationship between distance, bedroom number and price

fig = plt.figure()
ax = fig.add_subplot( projection='3d')
ax.scatter(apartment_info['Bedroom_Number'], apartment_info['Distance'], apartment_info['Price'], marker='o')
ax.set_xlabel('Bedroom_Number')
ax.set_ylabel('Distance (mile)')
ax.set_zlabel('Price ($)')
plt.show()


apartment_info.to_csv('apartment_info.csv', index = False)