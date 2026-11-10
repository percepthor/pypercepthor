#!/bin/bash

# clear python cache
find . | grep -E "(__pycache__|\.pyc|\.pyo$)" | xargs sudo rm -rf

# what a run of the test suite leaves in tests/
rm -rf tests/htmlcov tests/.coverage tests/.coverage.* tests/.hypothesis

# remove generated build
sudo rm -r build
sudo rm -r dist
sudo rm -r percepthor.egg-info
