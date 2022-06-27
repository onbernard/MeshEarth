from ..dependencies import deps
import numpy as np

ECEF = 'epsg:4978'
LLH = 'epsg:4979'


class SfmGpsImporter:
    def __init__(self, sfmfilepath, gpsfilepath):
        with open(sfmfilepath, 'r') as sf:
            sfm = sf.readlines()
        sfmparsed = SfmGpsImporter.parseyaml(sfm)
        with open(gpsfilepath, 'r') as gf:
            gps = gf.readlines()
        df = []
        for v in sfmparsed['views']:
            df.append({'poseId': v['poseId'],
                      'fileName': v['path'].split(sep='/')[-1]})
        for p in sfmparsed['poses']:
            for v in df:
                if p['poseId'] == v['poseId']:
                    l = p['pose']['transform']['center']
                    v['center'] = [float(l[0]), float(l[1]), float(l[2])]
        xyz_MR = []
        xyz_ECEF = []
        transformer = deps['pyproj'].Transformer.from_crs(LLH, ECEF)
        for g in gps[1:]:
            l = g.strip().split(',')
            for v in df:
                if v['fileName'] == l[1]:
                    if 'center' in v:
                        xyz = transformer.transform(
                            float(l[2]), float(l[3]), float(l[4]))
                        xyz_ECEF.append(xyz)
                        xyz_MR.append(v['center'])
                    v['llh'] = [float(l[2]), float(l[3]), float(l[4])]
                    v['ecef'] = xyz
        self.df = df
        self.xyz_ECEF = np.array(xyz_ECEF)
        self.xyz_MR = np.array(xyz_MR)

    @staticmethod
    def parseyaml(lines):
        def parsedic(i):
            d = {}
            while i < len(lines):
                curr = lines[i].strip().strip(',')
                i += 1
                if curr[0] == '}':
                    return (d, i)
                l = curr.split(':', 1)
                key = l[0].strip().strip('"')
                value = l[1].strip()
                if value == '[':
                    v = parsearr(i)
                    d[key] = v[0]
                    i = v[1]
                elif value == '{':
                    v = parsedic(i)
                    d[key] = v[0]
                    i = v[1]
                else:
                    d[key] = value.strip('"')

        def parsearr(i):
            a = []
            while i < len(lines):
                curr = lines[i].strip().strip(',')
                i += 1
                if curr[0] == ']':
                    return (a, i)
                if curr == '[':
                    v = parsearr(i)
                    i = v[1]
                    a.append(v[0])
                elif curr == '{':
                    v = parsedic(i)
                    i = v[1]
                    a.append(v[0])
                else:
                    a.append(curr.strip('"'))
        return parsedic(1)[0]
