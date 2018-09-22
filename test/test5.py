from src.tractography.registration import Register_ICP
from src.tractography.io import read_ply
from src.tractography.viz import draw_brain

target = read_ply('../data/132118/m_ex_atr-left_shore.ply')
subject = read_ply('../data/150019/m_ex_atr-left_shore.ply')

reg = Register_ICP(static=target,moving=subject)
x = reg.optimize(target,subject)

draw_brain([target,subject,x],[[0,0,1],[1,0,0],[.8,0,0]])
