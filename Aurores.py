
#Chaque bloc de numero correspond a une latitude, il y a 512 blocs, de la ligne 17 a 512+16 (ish)
#Chaque numero dans le bloc correspond a une longitude, il y en a 1024 par blocs
import sys; sys.path.append('/usr/lib/python3/dist-packages/matplotlib')
from math import *
from mpl_toolkits.basemap import Basemap
from urllib.request import *
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from datetime import datetime
import os
def checkPath(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)
def getPage():

    page = urlopen("http://services.swpc.noaa.gov/text/aurora-nowcast-map.txt")
    dividePageLines(page)

def dividePageLines(page):
    global timeLine
    i = 0
    lines = [0]*(512 + 17)
    for line in page:
        lines[i] = line
        i += 1
    analyzePage(lines)

def analyzePage(lines):
    global coordinatesx, coordinatesy, coordinatesvalue, values, maximum

    coordinatesx = [] #coordonee x (lat)
    coordinatesy = [] #coordonee y (long)
    coordinatesvalue = [] #La valeur a la coordonee correspondante
    values = 0 #Le nombre de valeurs differnts de 0
    minimum = 10
    maximum = 0

    for line in range (512):
        splitLine = lines[line + 17].split()
        for word in range (1024):
            if(int(splitLine[word]) >= minimum):
                if (int(splitLine[word]) > maximum):
                    maximum = int(splitLine[word])
                coordinatesx.append(line)
                coordinatesy.append(word)
                coordinatesvalue.append(int(splitLine[word]))
                values += 1
    print(values)
    print(maximum)
    drawMap()

def drawMap ():
    global iteration

    date = datetime.utcnow()
    m = Basemap(llcrnrlon=llLong,llcrnrlat=llLat,urcrnrlon=urLong,urcrnrlat=urLat,
                resolution='c',projection='merc',lon_0=centerLong,lat_0=centerLat)

    m.drawcoastlines()
    m.drawcountries()
    m.fillcontinents(color='grey',lake_color='white')
    parallels = np.arange(-90.,90.,20.)
    m.drawparallels(parallels, labels = [False, True, True, False])
    meridians = np.arange(-180.,180.,40.)
    m.drawmeridians(meridians, labels = [True, False, False, True])
    m.drawmapboundary(fill_color='white')
    m.nightshade(date)

    plt.title("Generated at " + str(date) + ", Maximum : "+str(maximum))

    for point in range (values):
        lat,long = -90 + coordinatesx[point] * 180/512, -180 + coordinatesy[point] * 360/1024
        xpt,ypt = m(long,lat)
        m.scatter(xpt, ypt,marker="s", c = color[coordinatesvalue[point]-1],s = 3, zorder = 10,edgecolors = "none",alpha =0.2)
    #mng = plt.get_current_fig_manager()
    #mng.resize(*mng.window.maxsize())
    foldername = "/home/leo/Python/Aurores/M:"+str(date.month) + "D:"+str(date.day)
    checkPath(foldername)
    filename = "Aurores-"+str(date.year)+"-"+str(date.month)+"-"+str(date.day)+"-"+chr(ord("a") + int(str(date.hour)))+"-"+chr(ord("a") + int(date.minute/5))
    plt.savefig(foldername+"/"+filename+".png")

color = ["#00FFFF","#02FCFC","#05F9F9","#07F7F7","#0AF4F4","#0CF2F2","#0FEFEF","#12ECEC","#14EAEA","#17E7E7","#19E5E5","#1CE2E2","#1EE0E0","#21DDDD","#24DADA","#26D8D8","#29D5D5","#2BD3D3","#2ED0D0","#30CECE","#33CBCB","#36C8C8","#38C6C6","#3BC3C3","#3DC1C1","#40BEBE","#42BCBC","#45B9B9","#48B6B6","#4AB4B4","#4DB1B1","#4FAFAF","#52ACAC","#55AAAA","#57A7A7","#5AA4A4","#5CA2A2","#5F9F9F","#619D9D","#649A9A","#679797","#699595","#6C9292","#6E9090","#718D8D","#738B8B","#768888","#798585","#7B8383","#7E8080","#807E7E","#837B7B","#857979","#887676","#8B7373","#8D7171","#906E6E","#926C6C","#956969","#976767","#9A6464","#9D6161","#9F5F5F","#A25C5C","#A45A5A","#A75757","#AA5555","#AC5252","#AF4F4F","#B14D4D","#B44A4A","#B64848","#B94545","#BC4242","#BE4040","#C13D3D","#C33B3B","#C63838","#C83636","#CB3333","#CE3030","#D02E2E","#D32B2B","#D52929","#D82626","#DA2424","#DD2121","#E01E1E","#E21C1C","#E51919","#E71717","#EA1414","#EC1212","#EF0F0F","#F20C0C","#F40A0A","#F70707","#F90505","#FC0202","#FF0000"]
llLong = -180
llLat = -80
urLong =180
urLat = 85
centerLong, centerLat = -70,48
getPage()


#cron job
#TODO : Régler la numérotation des fichiers
#TODO: Utiliser cartopy plutot que basemap
#TODO: Ne considérer que les données qui sont sont dans l'encadrement lower left - upper right
