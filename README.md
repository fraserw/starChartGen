Instructions on using the starcharts utilities.
===============================================

Requirements:
-------------

 * panstamps https://pypi.org/project/panstamps/
 * pyephem
 * mp_ephem
 * montage and montage_wrapper (http://www.astropy.org/montage-wrapper/)

Steps to run:
-------------

1) Move to the operating directory to where you want to download all images, create timing window and ephemeris files, etc.

Create two directories, *mpc*, and *ephs*.

Copy into *mpc* all mpc files of the targets you wish to create stamp images for.


2) **execute runElements.py**

Open runElements.py. Go to line 102 and edit the *files* array. One entry per target. Each entry must contain the full relative path to the mpc file in question. Adjust the two for-loops below according to which dates you care to generate ephemerides for. Each loop covers a year.

Execute runElements.py. It will create an ephemeris file in the Gemini format for each target, as well as a master ephemeris file that contains the full contents of each target's ephemeris file.

A window will pop up showing the ephemerides of all targets you have specified. Make sure that looks reasonable.


2) **execute  getCuts_PANSTAMPS.py**
