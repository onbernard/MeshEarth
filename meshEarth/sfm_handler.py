import pandas as pd
import numpy as np
from yaml import load, dump
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper


class SFMHandler():

    def __init__(self, filePath=""):
        with open(filePath) as f:
            sfm = load(f, Loader=Loader)
        d = []
        for view in sfm['views']:
            d.append({
                'FileName': view['path'].split(sep='/')[-1],
                'poseId': int(view['poseId'])
            })
        sfm_df = pd.DataFrame(d)
        sfm_df['x'] = np.nan
        sfm_df['y'] = np.nan
        sfm_df['z'] = np.nan
        for pose in sfm['poses']:
            sfm_df.loc[sfm_df['poseId'] == int(pose['poseId']), ['x', 'y', 'z']] = [
                float(pose['pose']['transform']['center'][0]),
                float(pose['pose']['transform']['center'][1]),
                float(pose['pose']['transform']['center'][2])
            ]
        self.sfm_df = sfm_df

    def get_df(self):
        return(self.sfm_df)
