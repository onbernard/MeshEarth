import pandas as pd
import numpy as np
from pyproj import Transformer


class ExifHandler():

    def __init__(self, filePath=''):
        self.filePath = filePath
        exif_df = pd.read_csv(filePath).iloc[1:,:]
        exif_df = exif_df.astype(
            {'GPSLongitude': 'float', 'GPSLatitude': 'float', 'GPSAltitude': 'float'})
        ecef = 'epsg:4978'
        wgs = 'epsg:4979'
        transformer = Transformer.from_crs(wgs, ecef)
        exif_df[['Ex', 'Ey', 'Ez']] = [transformer.transform(x, y, z) for x, y, z in zip(
            exif_df.GPSLatitude, exif_df.GPSLongitude, exif_df.GPSAltitude)]
        self.exif_df = exif_df

    def get_df(self):
        return(self.exif_df)
