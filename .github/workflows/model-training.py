name: Model Training

on: [push, pull_request]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2

    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.9.10'

    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install flake8 #add other packages here

    - name: Build
      working-directory: ./NN/Model-Training
      run: python -m py_compile ./main.py

    - name: Syntax checker
      working-directory: ./NN/Model-Training
      run: flake8 . --max-line-length 150
