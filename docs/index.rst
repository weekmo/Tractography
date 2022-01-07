|license - GPL|

Tractograpy
===========

It is a module deals with Brain Bundles
---------------------------------------

It includes functions to read/write, visualise and register bundles

“It’s always preferred to use source code!”
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Installation:
-------------
Easy to install by downloading install.sh and run it:

On Linux
^^^^^^^^
.. code:: console

   ./install.sh

On widows by using bash
^^^^^^^^^^^^^^^^^^^^^^^

.. code:: console

   bash install.sh 

By pip
^^^^^^

.. code:: console

   pip install tractography

By conda
^^^^^^^^

.. code:: console

   conda install -c weekmo tractography

Examples:
---------

Example 1:
^^^^^^^^^^

Register two bundles

.. code:: python


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

Example 2:
^^^^^^^^^^

Show all bundles in a folder

.. code:: python

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

Enjoy

.. |license - GPL| image:: https://img.shields.io/github/license/fzhu2e/GraphEM
   :target: https://www.gnu.org/licenses/gpl-3.0.txt
