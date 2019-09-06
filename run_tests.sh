#!/usr/bin/env bash

source ~/.bash_profile

conda create -n py35 -y python=3.5
conda activate py35 
pip install . pytest pandas
pytest > "py35.txt"
conda deactivate
conda remove -n py35 -y --all


conda create -n py36 -y python=3.6
conda activate py36
pip install . pytest pandas
pytest > "py36.txt"
conda deactivate
conda remove -n py36 -y --all


conda create -n py37 -y python=3.7
conda activate py37
pip install . pytest pandas
pytest > "py37.txt"
conda deactivate
conda remove -n py37 -y --all



