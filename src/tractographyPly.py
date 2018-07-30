from plyfile import PlyData, PlyElement
import numpy as np
class TractographyPly:
    def __init__(self,fname):
        self.ply = PlyData.read(fname)
        self.vertices_count = len(self.ply.elements[0].data)
        self.fiber_count=len(self.ply.elements[0].data)
        self.data = []
        indeces = np.asarray([i[0] for i in self.ply.elements[1].data])
        temp=[]
        for i,item in enumerate(self.ply.elements[0].data):
            i+=1
            temp.append([item[3],item[4],item[5]])
            if i in indeces:
                self.data.append(temp)
                temp=[]
        self.data=np.asarray(self.data)
    def writ_to_file(self,fname):
        with open(fname,'w') as f:
            f.write('ply\n')
            f.write('format ascii 1.0\n')
            for i in self.ply.comments:
                f.write('comment {}\n'.format(i))
            for elem in self.ply.elements:
                f.write('element {} {}\n'.format(elem.name,len(elem.data)))
                if(len(elem.properties)>1):
                    for i in range(3):
                        f.write(str(elem.properties[i])+'\n')
                else:
                    f.write(str(elem.properties[0])+'\n')
            for elem in self.ply.elements[0].data:
                f.write("{} {} {}\n".format(elem[3],elem[4],elem[5]))
            for elem in self.ply.elements[1].data:
                f.write(str(elem[0])+'\n')

path = '../data/132118/m_ex_atr-left_shore.ply'
x = TractographyPly(path)
x.writ_to_file('test.ply')