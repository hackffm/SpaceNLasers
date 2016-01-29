# quick and dirty bitplane editor

* Bitmap up to 40x40 pixels = the grid
* set/delete pixels
* multiple image manipulation commands

## functions
|Command|Key(s)|Comment|
|---|---|---|
|Paint/erase|Spacebar|Toggles between setting and deleting pixels|
|Mirror mode|m|Toggles horizontal mirroring for drawing|
|max. grid|a|increase width and height to maximum|
|Adjust grid width|w/W|increase/decrease widht|
|Adjust grid height|h/H|increase/decrease height|
|Horizontal line fill|l|Fills pixel under mouse pluse adjecent pixels to the left and right with current paint mode|
|Roll image|*Cursor keys*|Rolls the image of the current dimensions. Pixels shifted out on one side will be shifted in on the opposite side.|
|Rotate image|r|Rotates image counter-clockwise and crops image.|ll
|Crop|C|Crops the currently visible grid image to the rectangle containing pixels. All other pixels are deleted. Width and height will be adjusted.
|Invert|i|Invert visible grid|
|Clear|*Delete*|Clear visible grid|