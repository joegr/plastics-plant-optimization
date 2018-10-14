To create a new conda environment do the following:

`conda env export > environment.yml`

To recreate a conda environment based on this file, do the following:

`conda env create -f environment.yml`

