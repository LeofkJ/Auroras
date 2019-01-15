# Auroras
While trying to see Auroras in southern Quebec with my friends, we noticed that we were too far south to regularly have good conditions. I made a Python program to get the data from the NOAA (US' National Oceanic and Atmospheric Administration) and display it on a map. 

There are two versions: One using basemap, better esthetically (for example, it shows where it is night time), but drastically less efficient, especially when it is processed by a laptop. (Basemap is also no longer updated, so all can break)

The other one uses the Cartopy library, which is much more efficient, but also lacks a few esthetic features that made basemap much more appealing
