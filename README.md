# Recommender Systems for Police Photo Lineups
This repository contains source codes for the project: Recommender Systems for Police Photo Lineups. More information on the project can be found in paper Peska & Trojanova: Towards Recommender Systems for Police Photo Lineup, http://www.ksi.mff.cuni.cz/~peska/lineup/paper.pdf

Dataset of candidates attribute-based as well as visual-based features, accompanied with the implicit feedback from the forensic technicians received during the user-study on assembling lineups is available from:
https://zenodo.org/record/814222



In order to recreate project files, you need to:
- create dataset of candidates
- create visual descriptors of the candidate's images
- calculate cosine distances of attribute-based and visual-based representation of objects
- create sample lineup assembling pages

In order to create the raw dataset of candidates, please run:
- dataset_creation.r

In order to create visual descriptor features, please run:
- createVisualDescriptors.py. Please note that you will need VGG-FACE caffemodel, which can be downloaded from the Caffe model zoo

The cosine distance matrices are calculated in:
- calculateCB-RSFeatures.py	
- calculateVisual-RSFeatures.py

Finally, the sample web pages with lineup assembling tasks are created via:
- createLineupPages.py


