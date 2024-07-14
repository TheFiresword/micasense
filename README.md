# Readme

NB: This code is strongly inspired from the official micasense github repo here : [text](https://github.com/micasense/imageprocessing/tree/master/micasense)

## Setting up the Raspberry Pi

First, u need to make sure the IP adress of the raspberry pi is static and known. This can be done with ```setting.sh``` script.
Please look at the comments in the script for documentation.

## How to prepare images acquisition ?

Execute the ```setvenv.py``` script to install all the requirements in a conda environment. U'll only need to activate
this conda environment to be ready to take your amazing images.

## Launch images acquisition

The script ```acquisition.py``` is destined to automate the images acquisition. You can pass down 2 parameters to this
script : the acquisition frequence (number of seconds)

## And now, realign your images

The python script ```realign.py``` takes a bunch of arguments helping you to have full control over the alignment algorithm.
Don't forget to execute this script in the conda environment.

```bash
conda run -n micasense python realign.py
```