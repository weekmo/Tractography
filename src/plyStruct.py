from plyfile import PlyData, PlyElement
import numpy as np
class plyStruct():
    "Class that process poly data and create isomap"

    def loadPolyData(self, subpath):
        "Loading ply file and its stream index"
        ply = PlyData.read(subpath)
        elemList = []
        elemDict = {}
        self.vprt = []
        self.plyData = []
        self.idx = []
        self.feDict = {}
        for i in range(len(ply.elements)):
            elemList.append(ply.elements[i].name)
            tmplist = []
            for j in range(len(ply.elements[i].properties)):
                tmplist.append(ply.elements[i].properties[j].name)
            elemDict[ply.elements[i].name] = tmplist

        if 'vertices' in elemDict.keys():
            prts = elemDict['vertices']

            # print(prts)
            for prt in prts:
                # print(prt)
                self.plyData.append(ply['vertices'].data[prt])
                self.vprt.append(prt)
                # nprt="self."+prt
                self.feDict[prt] = np.asarray(ply['vertices'].data[prt])
                # exec("{0} = {1}".format(nprt,tmpFe))
            self.plyData = np.asarray(self.plyData)
            self.plyData = self.plyData.T
        if 'fiber' in elemDict.keys():
            self.idx = ply['fiber'].data['endindex']
            self.idxLen = np.copy(self.idx)
            self.idxLen[1:] = self.idx[1:] - self.idxLen[:-1]


