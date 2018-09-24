Instructions on using the starcharts utilities.
===============================================

Requirements:
-------------

 * panstamps https://pypi.org/project/panstamps/
 * pyephem (http://rhodesmill.org/pyephem/)
 * mp_ephem (get from OSSOS/JJ/Michele)
 * montage and montage_wrapper (http://www.astropy.org/montage-wrapper/)

Steps to run:
-------------

1) Move to the operating directory to where you want to download all images, create timing window and ephemeris files, etc.

Create two directories, *mpc*, and *ephs*.

Copy into *mpc* all mpc files of the targets you wish to create stamp images for.


2) **execute runElements.py**

Open runElements.py. Go to line 102 and edit the *files* array. One entry per target. Each entry must contain the full relative path to the mpc file in question. Adjust the two for-loops below according to which dates you care to generate ephemerides for. Each loop covers a year.

Execute runElements.py. It will create an ephemeris file in the Gemini format for each target, as well as a master ephemeris file that contains the full contents of each target's ephemeris file. *The ephemeris is for the 568 Mauna Kea site.*

A window will pop up showing the ephemerides of all targets you have specified. Make sure that looks reasonable.


2) **execute  getCuts_PANSTAMPS.py**

Example Usage: > getCuts_PANSTAMPS.py o5c016

Adjust the targetname accordingly. This script will open the ephemeris file created in step 2, and download a sufficient set of r-band panstarrs images from which a full map covering the entirety of the ephemeris can be generated.

This downloads a lot of data, and can take a multiple hours, even if your bandwidth is good. Note that it sometimes downloads multiple copies of the same file. This is a consequence of how the StSci MAST server handles the pixels, and cannot be avoided. Boo.

The individual PS images will be downloaded into a directory of the same name as the target.


3) **execute merge.py**

Example usage: > merge.py o5c016

Adjust the target name accordingly. This script will merge all fits files contained in the target directory. It will save the mosaic image to targetname.fits (with targetname adjusted accordingly).

*A subdirectory called mosaic will be created. This is kept for debugging purposes. Open the image and check that the merger was successful. If yes, delete mosaic directory before operating on the next target.*

**Important note about merging:** If for what ever reason, the download needs to be redone, it is usually best to nuke the entire downloads directory for the target in question. This is because merge.py will blindly merge all images in that directory. This can easily result in memory overflows or harddrive fill-ups if you try to merge images in very different regions of the sky, for example.


4) **use observabilityCheck.py**

Example usage: > observabilityCheck.py o5c016 Hawaii

Adjust the targetname accordingly. The locale (second command line option) can either be Hawaii or Arizona, and adjusts both the times shown (approximately twilight to twilight) and adjusted the observatory code appropriately.

A window will pop up showing a ~6x6' window on the left, and a larger zoom on the right. The nightly track will be shown by the black point, and the *approximate* uncertainty range (ignoring the fact that this is actually elliptical-ish) is shown by the white bands.

The keys 'g' and 'b' will move the timestamp forward one night. Any time 'g' is pressed, a Gemini-format timing window is written to targetname.tw. This can be ignored at LBT.

**Note:** right now the timing window is forced to only the 4 nights of the 2018B LBT run, if the locale is set to Arizona.
