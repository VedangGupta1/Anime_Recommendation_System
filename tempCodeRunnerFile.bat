@echo off
echo Installing Python machine learning libraries and Tkinter...

REM Update pip to the latest version
python -m pip install --upgrade pip

REM Install libraries
pip install numpy
pip install pandas
pip install scikit-learn
pip install tensorflow
pip install keras

REM Install Tkinter
pip install tk

echo Installation complete.