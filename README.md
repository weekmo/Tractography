
[![license - GPL](https://img.shields.io/aur/license/yaourt.svg)](https://www.gnu.org/licenses/gpl-3.0.txt)

# Tractograpy

## It is a module deals withe Brain Bundles

It includes functions to read/write and register bundles

## Installation:

Easy to install by using pip (recommended)

```commandline
pip install tractography
```
or conda

```commandline
conda install -c weekmo tractography
```

## Example:

```python

from tractography.io import read_ply,write_trk,export_bundles
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
