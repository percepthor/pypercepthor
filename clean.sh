#!/bin/bash

# clear python cache
find . | grep -E "(__pycache__|\.pyc|\.pyo$)" | xargs sudo rm -rf

# remove generated build
sudo rm -r build
sudo rm -r dist
sudo rm -r percepthor.egg-info
