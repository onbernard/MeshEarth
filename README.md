# MeshEarth
Transformation from MeshRoom coordinates to local tangential plane coordinates using GPS metadata

## Description

This addon adds an operator to the object property panel. You first select the Structure From Motion file created by MeshRoom then a CSV file created by
exiftool using the command : "exiftool -filename -gpslatitude -gpslongitude -gpsaltitude -n -csv -D <IMAGES_DIR>" where IMAGES_DIR is the directory containing
the images you provided to MeshRoom. A more integrated way is in the works. Then you apply the transformation to the model by clicking on Align to ENU. 
Positive x is east, positive y is north, positive z is up.

## Dependencies
This addon requires sklearn and pyproj to work. If these are not installed, you can do so in the addon preference window.