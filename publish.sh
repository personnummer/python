#!/bin/bash
echo 'build'
python -m build
echo 'upload'
twine upload dist/*
echo 'done'