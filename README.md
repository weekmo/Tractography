# Tractograpy
## It is a module deals withe Brain Bundles
It includes functions to read/write and register bundles<br/>
## Installation:
Easy to install by using
```commandline
pip install tractography
```
## Example:
```python
from tractographyPly import read_ply,write_trk,show_bundles,register
from dipy.viz import window

# Read bundles
data1 = read_ply('../data/132118/m_ex_atr-left_shore.ply')
data2 = read_ply('../data/150019/m_ex_atr-left_shore.ply')

# Register bundle
aligned_bundle = register(target=data1, subject=data2)

# Write to trk file
write_trk("../data/aligned_bundle.trk", aligned_bundle)

# Export images before and after registration
show_bundles([data1, data1],
             colors=[window.colors.orange, window.colors.blue],
             show=False,
             fname='../data/before_registration.png')

show_bundles([data1, aligned_bundle],
             colors=[window.colors.orange, window.colors.blue],
             show=False,
             fname='../data/after_registration.png')
```