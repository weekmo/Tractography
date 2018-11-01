
[![license - GPL](https://img.shields.io/aur/license/yaourt.svg)](https://www.gnu.org/licenses/gpl-3.0.txt)

# Tractograpy

## It is a module deals withe Brain Bundles

It includes functions to read/write, visualise and register bundles
### "It's always preferred to use source code!"
## Installation:

Easy to install by downloading install.sh and run it:
#### On Linux
```commandline
./install.sh
```
#### On widows by using bash
```commandline
bash install.sh 
```
#### By pip
```commandline
pip install tractography
```
#### By conda

```commandline
conda install -c weekmo tractography
```

## Example 1:
#### Register two bundles
```python

from tractography.io import read_ply,write_trk
from tractography.registration import register
from tractography.viz import draw_bundles

# Read bundles
data1 = read_ply('target.ply')
data2 = read_ply('subject.ply')

# Register bundle
aligned_bundle,mat = register(target=data1, subject=data2)

# Write to trk file
write_trk("aligned_bundle.trk", aligned_bundle)

# Export images before and after registration
draw_bundles([data1,data2])
draw_bundles([data1,aligned_bundle])
```

## Example 2:
#### Show all bundles in a folder
```python
from tractography.viz import draw_bundles
from os import listdir
from os.path import isfile
from tractography.io import read_ply
import argparse

parser = argparse.ArgumentParser(description='Input argument parser.')
parser.add_argument('-f', type=str, help='location of files')
args = parser.parse_args()
# data_path = 'data/'
data_path = args.f
files = [data_path + f for f in listdir(data_path) if isfile(data_path + f) and f.endswith('.ply')]

brain = []
for name in files:
    brain.append(read_ply(name))
draw_bundles(brain)
```
Enjoy
