import pandas as pd
import numpy as np
import math
from sklearn import linear_model
from pyproj import Transformer
from .exif_handler import ExifHandler
from .sfm_handler import SFMHandler


class transform():

    def __init__(self, exifFilePath, sfmFilePath):
        exif = ExifHandler(exifFilePath)
        sfm = SFMHandler(sfmFilePath)
        self.df = pd.merge(exif.get_df(),
                           sfm.get_df(), "inner", "FileName")
        self.clf = linear_model.LinearRegression()
        self.clf.fit(self.df[~self.df['x'].isnull()][['x', 'y', 'z']],
                     self.df[~self.df['x'].isnull()][['Ex', 'Ey', 'Ez']])
        self.xyz2llh = Transformer.from_crs('epsg:4978', 'epsg:4979')
        self.llh2xyz = Transformer.from_crs('epsg:4979', 'epsg:4978')

    def xyzEcefOrigin(self):
        return(self.clf.intercept_)

    def llhEcefOrigin(self):
        return(np.array(self.xyz2llh.transform(*self.clf.intercept_)))

    def ecefToEnuTransform(self):
        origin = self.llhEcefOrigin()
        lat = origin[0]
        lon = origin[1]
        return(np.array([
            [-math.sin(lon), -math.sin(lat)*math.cos(lon),
             math.cos(lat)*math.cos(lon), 0],
            [math.cos(lon), -math.sin(lat)*math.sin(lon),
             math.cos(lat)*math.sin(lon), 0],
            [0, math.cos(lat), math.sin(lat), 0],
            [0, 0, 0, 1]
        ]))

    def meshroomToEcefTransform(self):
        M = self.clf.coef_
        M = np.append(M, [[0], [0], [0]], axis=1)
        M = np.append(M, [[0, 0, 0, 1]], axis=0)
        return(M)

    def meshroomToEnuTransform(self):
        return(np.dot(self.ecefToEnuTransform(), self.meshroomToEcefTransform()))
