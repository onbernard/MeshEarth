# MeshEarth
Transformation from MeshRoom coordinates to local tangential plane coordinates using GPS metadata

## Description

This addon adds an operator to the object property panel. You first select the Structure From Motion file created by MeshRoom then a CSV file created by
exiftool using the command : "exiftool -filename -gpslatitude -gpslongitude -gpsaltitude -n -csv -D <IMAGES_DIR>" where IMAGES_DIR is the directory containing
the images you provided to MeshRoom. A more integrated way is in the works. Then you apply the transformation to the model by clicking on Align to ENU. 
Positive x is east, positive y is north, positive z is up. Import the model accordingly.

## Dependencies
This addon requires sklearn and pyproj to work. If these are not installed, you can do so in the addon preference window. As they are installed when interpreter
is running, imports might fail if there are dependencies issues. Try restarting blender if that happens.

## Examples
You will find a 3d model, a csv and a sfm file in the example folder to try it out yourself.