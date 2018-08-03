from plyfile import PlyData, PlyElement
import numpy as np
from dipy.viz import window, actor
from time import sleep
class TractographyPly:
    def __init__(self,fname):
        self.ply = PlyData.read(fname)
        self.vertices_count = len(self.ply.elements[0].data)
        self.fiber_count=len(self.ply.elements[0].data)
        self.data = []
        self.indeces = np.asarray([i[0] for i in self.ply.elements[1].data])
        temp=[]
        for i,item in enumerate(self.ply.elements[0].data):
            i+=1
            temp.append([item[3],item[4],item[5]])
            if i in self.indeces:
                self.data.append(np.asarray(temp))
                temp=[]
        #self.data=np.asarray(self.data)

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
            f.write('end_header\n')
            for elem in self.ply.elements[0].data:
                f.write("{} {} {}\n".format(elem[3],elem[4],elem[5]))
            for elem in self.ply.elements[1].data:
                f.write(str(elem[0])+'\n')

def show_both_bundles(bundles, colors=None, show=True, fname=None):
    ren = window.Renderer()
    ren.SetBackground(1., 1, 1)
    for (i, bundle) in enumerate(bundles):
        color = colors[i]
        lines_actor = actor.streamtube(bundle, color, linewidth=0.3)
        lines_actor.RotateX(-90)
        lines_actor.RotateZ(90)
        ren.add(lines_actor)
    if show:
        window.show(ren)
    if fname is not None:
        sleep(1)
        window.record(ren, n_frames=1, out_path=fname, size=(900, 900))

def write_to_file(fname,data,comments=None):
    data_txt=''
    vert_num=0
    indeces=[]
    index=0
    with open(fname,'w') as f:
        for fib in data:
            indeces.append(len(fib)+index)
            for vert in fib:
                data_txt+=str(vert[0])+' '+str(vert[1])+' '+str(vert[2])+'\n'
                vert_num+=1
            index+=len(fib)
        f.write('ply\nformat ascii 1.0\ncomment DTI Tractography, produced by fiber-track\nelement vertices '+str(vert_num))
        f.write('\nproperty float x\nproperty float y\nproperty float z\n')
        f.write('element fiber {}\nproperty int endindex'.format(len(indeces)))
        f.write('\nend_header\n'+data_txt)
        for i in indeces:
            f.write(str(i)+'\n')