from urllib.request import *
from io import StringIO
import numpy as np
import cartopy.crs as ccrs
import cartopy
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

def data():
    latitude = 45.411
    longitude = -75.698
    url = "http://services.swpc.noaa.gov/text/aurora-nowcast-map.txt"
    page = urlopen(url)
    webPageText = StringIO(urlopen(url).read().decode('utf-8'))
    pixelData = np.loadtxt(webPageText)
    return pixelData, latitude, longitude

def colorMap():
    colors = {'red': [(0.00, 0.1725, 0.1725),(0.50, 0.1725, 0.1725),(1.00, 0.8353, 0.8353)],
             'green': [(0.00, 0.9294, 0.9294),(0.50, 0.9294, 0.9294),(1.00, 0.8235, 0.8235)],
             'blue': [(0.00, 0.3843, 0.3843),(0.50, 0.3843, 0.3843),(1.00, 0.6549, 0.6549)],
             'alpha': [(0.00, 0.0, 0.0),(0.50, 1.0, 1.0),(1.00, 1.0, 1.0)]}
    return(LinearSegmentedColormap("name",colors))
def draw():
    fig = plt.figure(figsize=(60,30))
    pixelData, lat, long = data()

    north = fig.add_subplot(1, 3, 1, projection=ccrs.Orthographic(0, 90))
    north.gridlines()
    north.coastlines()
    north.stock_img()
    north.imshow(pixelData,vmin = 0,vmax = 100,transform = ccrs.PlateCarree(),extent = (-180,180,-90,90),origin = "lower",cmap = colorMap())

    all = fig.add_subplot(1, 3, 2, projection=ccrs.NearsidePerspective(long,lat,satellite_height = 5000000,globe = None))
    all.gridlines()
    all.coastlines()
    all.stock_img()
    all.imshow(pixelData,vmin = 0,vmax = 100,transform = ccrs.PlateCarree(),extent = (-180,180,0,90),origin = "lower",cmap = colorMap())

    south = fig.add_subplot(1, 3, 3, projection=ccrs.Orthographic(180, -90))
    south.gridlines()
    south.coastlines()
    south.stock_img()
    south.imshow(pixelData,vmin = 0,vmax = 100,transform = ccrs.PlateCarree(),extent = (-180,180,-90,0),origin = "lower",cmap = colorMap())

    plt.show()
draw()
