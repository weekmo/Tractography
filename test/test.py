from src.tractography.io import read_ply,write_ply

data1=read_ply('../data/132118/m_ex_atr-left_shore.ply')
#data2=read_ply('../data/150019/m_ex_atr-left_shore.ply')
data2=read_ply('../data/terget.ply',[0,1,2])

write_ply('../data/test1.ply',data1)