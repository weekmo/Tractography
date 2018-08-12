
[![license - MIT](https://img.shields.io/github/license/mashape/apistatus.svg)](https://opensource.org/licenses/MIT)

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
from tractography.io import read_ply,write_trk,export_bundles  # ,register_all
from tractography.registration import register
from dipy.viz import window

# Read bundles
data1 = read_ply('target.ply')
data2 = read_ply('subject.ply')

# Register bundle
aligned_bundle = register(target=data1, subject=data2)

# Write to trk file
write_trk("aligned_bundle.trk", aligned_bundle)

# Export images before and after registration
export_bundles([data1, data1],
             colors=[window.colors.orange, window.colors.blue],
             show=False,
             fname='before_registration.png')

export_bundles([data1, aligned_bundle],
             colors=[window.colors.orange, window.colors.blue],
             show=False,
             fname='after_registration.png')
```