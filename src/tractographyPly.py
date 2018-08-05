def read(fname):
    from plyfile import PlyData, PlyElement
    import numpy as np

    ply = PlyData.read(fname)
    data = []
    indeces = np.asarray([i[0] for i in ply.elements[1].data])
    temp=[]
    for i,item in enumerate(ply.elements[0].data):
        i+=1
        temp.append([item[3],item[4],item[5]])
        if i in indeces:
            data.append(np.asarray(temp))
            temp=[]
    del temp
    del indeces
    del ply
    return data

def show_bundles(bundles, colors=None, show=True, fname=None):
    from dipy.viz import window, actor
    from time import sleep

    ren = window.Renderer()
    ren.SetBackground(1, 1, 1)
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

def write(fname,data,
          comments=['DTI Tractography, produced by fiber-track']):
    data_txt=''
    vert_num=0
    indeces=[]
    index=0
    with open(fname,'w') as f:
        for fib in data:
            index+=len(fib)
            indeces.append(index)
            for vert in fib:
                data_txt+=str(vert[0])+' '+str(vert[1])+' '+str(vert[2])+'\n'
                vert_num+=1
        f.write('ply\nformat ascii 1.0\n')
        for com in comments:
            f.write('comment '+com+'\n')
        f.write('element vertices '+str(vert_num))
        f.write('\nproperty float x\nproperty float y\nproperty float z\n')
        f.write('element fiber {}\nproperty int endindex'.format(len(indeces)))
        f.write('\nend_header\n'+data_txt)
        for i in indeces:
            f.write(str(i)+'\n')

    del data_txt
    del indeces

def register(traget_path,subject_path,points=40):
    from dipy.align.streamlinear import StreamlineLinearRegistration
    from dipy.tracking.streamline import set_number_of_points

    bundle1 = read(traget_path)
    bundle2 = read(subject_path)

    cb_subj1 = set_number_of_points(bundle1, points)
    cb_subj2 = set_number_of_points(bundle2, points)

    srr = StreamlineLinearRegistration()
    srm = srr.optimize(static=cb_subj1, moving=cb_subj2)

    return srm.transform(bundle2)

def register_all(data_path):
    from os import listdir,mkdir
    from os.path import isfile,isdir

    files_names={}
    index=0
    target_key=''
    for dir in listdir(data_path):
        dir=data_path+dir+'/'
        if isdir(dir):
            files_names[dir]=[f for f in listdir(dir) if isfile(dir+f)]

    for k in files_names.keys():
        if index ==0:
            target_key=k
        else:
            output_path=k[:-1]+'_output/'
            if not isdir(output_path):
                mkdir(output_path)
            for target_path,subject_path in zip(files_names[target_key],files_names[k]):
                if target_path == subject_path:
                    aligned_subject=register(target_key+target_path,k+subject_path)
                    write(output_path+subject_path,aligned_subject)
        index+=1