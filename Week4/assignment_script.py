import numpy as np
import rasterio as rio
import geopandas as gpd
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
from shapely.ops import unary_union
from shapely.geometry.polygon import Polygon
from cartopy.feature import ShapelyFeature
import matplotlib.patches as mpatches


def percentile_stretch(img, pmin=0., pmax=100.):
    '''
    This is where you should write a docstring.
    '''
    # here, we make sure that pmin < pmax, and that they are between 0, 100
    if not 0 <= pmin < pmax <= 100:
        raise ValueError('0 <= pmin < pmax <= 100')
    # here, we make sure that the image is only 2-dimensional
    if not img.ndim == 2:
        raise ValueError('Image can only have two dimensions (row, column)')

    minval = np.percentile(img, pmin)
    maxval = np.percentile(img, pmax)

    stretched = (img - minval) / (maxval - minval)  # stretch the image to 0, 1
    stretched[img < minval] = 0  # set anything less than minval to the new minimum, 0.
    stretched[img > maxval] = 1  # set anything greater than maxval to the new maximum, 1.

    return stretched


def img_display(img, ax, bands, stretch_args=None, **imshow_args):
    '''
    This is where you should write a docstring.
    '''
    dispimg = img.copy().astype(np.float32)  # make a copy of the original image,
    # but be sure to cast it as a floating-point image, rather than an integer

    for b in range(img.shape[0]):  # loop over each band, stretching using percentile_stretch()
        if stretch_args is None:  # if stretch_args is None, use the default values for percentile_stretch
            dispimg[b] = percentile_stretch(img[b])
        else:
            dispimg[b] = percentile_stretch(img[b], **stretch_args)

    # next, we transpose the image to re-order the indices
    dispimg = dispimg.transpose([1, 2, 0])

    # finally, we display the image
    handle = ax.imshow(dispimg[:, :, bands], **imshow_args)

    return handle, ax


# ------------------------------------------------------------------------
# note - rasterio's open() function works in much the same way as python's - once we open a file,
# we have to make sure to close it. One easy way to do this in a script is by using the with statement shown
# below - once we get to the end of this statement, the file is closed.
with rio.open('data_files/NI_Mosaic.tif') as dataset:
    img = dataset.read()
    xmin, ymin, xmax, ymax = dataset.bounds

# your code goes here!
# start by loading the outlines and point data to add to the map
myCRS = ccrs.UTM(29)

# next, create the figure and axis objects to add the map to
fig, ax = plt.subplots(1,1, figsize=(10,10), subplot_kw=dict(projection=myCRS))

# now, add the satellite image to the map
ax.imshow(img[3], cmap='gray', vmin=200, vmax=5000)

# next, add the county outlines to the map
ax.imshow(img[3], cmap='gray', vmin=200, vmax=5000, transorm=myCRS, extent=[xmin, xmax, ymin, ymax])

# then, add the town and city points to the map, but separately
towns = gpd.read_file('data_files/towns.shp')
is_town=towns['STATUS'] == 'Town'
is_city=towns['STATUS'] == 'City'

town_handle = ax.plot(towns[is_town].geometry.x,towns[is_town].geometry.y,'s',color='b',ms=6,transform=myCRS)
city_handle = ax.plot(towns[is_city].geometry.x,towns[is_city].geometry.y,'s',color='s',ms=9,transform=myCRS)

# finally, try to add a transparent overlay to the map


# note: one way you could do this is to combine the individual county shapes into a single shape, then
# use a geometric operation, such as a symmetric difference, to create a hole in a rectangle.
# then, you can add the output of the symmetric difference operation to the map as a semi-transparent feature.
overlay=ShapelyFeature(counties['geometry'],myCRS,edgecolor='r',facecolor='none')

# last but not least, add gridlines to the map
# add the county outlines
county_outlines = ShapelyFeature(counties['geometry'], myCRS, edgecolor='r', facecolor='none')

ax.add_feature(overlay)
ax.add_feature(county_outlines)

# create a handle to feed to the legend
county_handles = generate_handles([''], ['none'], edge='r')

ax.legend(county_handles + town_handle + city_handle,
          ['County Boundaries', 'Town', 'City'], fontsize=13, loc='upper left', framealpha=1)

# and of course, save the map!
fig.savefig('imgs/example_map.png',dpi=300, bbox_inches='tight')
