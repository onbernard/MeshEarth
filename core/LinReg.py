from ..dependencies import deps
import numpy as np

ECEF = 'epsg:4978'
LLH = 'epsg:4979'


def computeTransformMatrix(xyz_MR, xyz_ECEF):
    clf = deps['sklearn.linear_model'].LinearRegression()
    clf.fit(xyz_MR, xyz_ECEF)
    mr2ecef_matrix = np.append(clf.coef_, [[0], [0], [0]], axis=1)
    mr2ecef_matrix = np.append(mr2ecef_matrix, [[0, 0, 0, 1]], axis=0)
    ecef2llh_transformer = deps['pyproj'].Transformer.from_crs(ECEF, LLH)
    lat0, lon0, h0 = ecef2llh_transformer.transform(*clf.intercept_)
    ecef2enu_matrix = T = np.array([[-np.sin(lon0), np.cos(lon0), 0, 0],
                                    [-np.sin(lat0)*np.cos(lon0), -np.sin(lat0)
                                     * np.sin(lon0), np.cos(lat0), 0],
                                    [np.cos(lat0)*np.cos(lon0), np.cos(lat0)
                                     * np.sin(lon0), np.sin(lat0), 0],
                                    [0, 0, 0, 1]])
    return np.dot(ecef2enu_matrix, mr2ecef_matrix)
