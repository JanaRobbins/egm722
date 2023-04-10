import pandas as pd
import geopandas as gpd
import folium

wards = gpd.read_file('data_files/NI_Wards.shp')

m = wards.explore('Population', cmap='viridis')

df = pd.read_csv('data_files/Airports.csv') # read the csv data

# create a new geodataframe
airports = gpd.GeoDataFrame(df[['name', 'website']], # use the csv data, but only the name/website columns
                            geometry=gpd.points_from_xy(df['lon'], df['lat']), # set the geometry using points_from_xy
                            crs='epsg:4326') # set the CRS using a text representation of the EPSG code for WGS84 lat/lon


# add the airport points to the existing map
airports.explore('name',
                 m=m, # add the markers to the same map we just created
                 marker_type='marker', # use a marker for the points, instead of a circle
                 popup=True, # show the information as a popup when we click on the marker
                 legend=False, # don't show a separate legend for the point layer
                )

transport = pd.read_csv('data_files/transport_data.csv')

merged = wards.merge(transport, left_on='Ward Code', right_on='Ward Code')

m = merged.explore('Distance', # show the Distance column
                   cmap='plasma', # use the 'plasma' colormap from matplotlib
                   legend_kwds={'caption': 'Distance to nearest airport in km'} # set the caption to a longer explanation
                  )

airport_args = {
    'm': m, # add the markers to the same map we just created
    'marker_type': 'marker', # use a marker for the points, instead of a circle
    'popup': True, # show the information as a popup when we click on the marker
    'legend': False, # don't show a separate legend for the point layer
    'marker_kwds': {'icon': folium.Icon(color='red', icon='plane', prefix='fa')} # make the markers red with a plane icon from FA
}

# use the airport_args with the ** unpacking operator - more on this next week!
airports.explore('name', **airport_args)

m.save('NI_airport_j.html')