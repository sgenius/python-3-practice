# Layering in Mosaic

The idea is that, *apart* from the lo-res / hi-res combination of cells, we have layers of cells.

Each layer sits on top of each other.

Each superior layer is made out of composite cells in the layer below, with lower resolution.

The idea would be to display superior (eg. less resolution) layers instead of the original images when the zoom is lower. This provides the same image quality with less file loads.

We can have many layers on top of each other. Showing lower layers could get triggered on zoom, or by detecting how many images in the current layer are visible at a time.

Each layer *could* have lo-res / hi-res versions but there is no need. Layers would essentially replace the need for this.

## Image organization

The base layer (0) is composed of the current, original cells. Each cell occupies a space in a grid. We assume all cells are the same size and therefore know where each cell sits in the "virtual" coordinate space of the canvas.

Currently, each image name has the format "{x},{y}.jpg", where x and y are integers; for example, "0,0.jpg" or "4,-2.jpg". A few images also preserve historical changes: these file names have the format "{x},{y}-before-{yyyy-mm-dd}.jpg".

The low resolution images have the format "thumb_{x},{y}.jpg".

All of these images currently live in the same directory in the project: public/images/mosaic.

With layers, we would instead create folders with layers: eg. public/images/mosaic/layers/{x}, where x is the layer number. Each image in each layer gets identified with the cartesian coordinates that have the lowest possible number (more on this below).

## Image composition

The idea is that the images in each layer are composed of a number of images of the previous (lower) layer. We could customize the composition: for example, 5x by 3y to create a 15-cell-wide next step. For starters, we should keep it easy to calculate, and make it 2x by 2y.

In a general sense, images in a layer are composed of (m^layer index)x by (n^layer index)y original cells.

Images in all layers are identified by the place they fall in the *original* cartesian plane - specifically, the one that corresponds to its "lowest" corner in each dimension.

For example, using 2x by 2y: in layer 1, there would be an image with coordinates [0, 0] and it's comprised of the contents of a composition of a rectangle of two by two cells, composed by the cells [0, 0], [0, 1], [1, 0], and [1, 1]. Another rectangle in layer 1, composed of [2, 0], [2, 1], [3, 0], [3, 1] would have the coordinates [2, 0] in layer 1.

For layer 2, the images contain (2^2)x by (2^2)y original cells (four by four), so [0, 0] is composed of [0...3, 0...3].

For layer 3, the images now contain (2^3)x by (2^3)y (eight by eight); [0, 0] is composed of [0...7, 0...7], and so on.

Each actual filename in the layer should probably identify:
- the layer index,
- the m and n variables,
- the coordinates. 

For example: "l1x2y2-0,0.jpg" would be the unique filename for the image in layer 1 sitting on [0, 0] calculated with the method above (m = 2, n = 2).

This is in addition to the layer directory, so the path would be "public/images/mosaic/layers/1/l1x2y2-0,0.jpg".

The m and n variables need to be stable, known, and preconfigured. This way, the system can easily anticipate which cells exist in each layer and calculate the file names to load.

## Image creation
We would create images for each layer in a backend process, by:
- Creating an in-memory canvas of the desired size as per the m and n variables,
- Attempting to load the *original* files that compose each layer, substituting with a plain default file if not found,
- Reducing the physical size (eg. pixels) of each file by a factor of 1/(m^layer index) by 1/(n^layer index),
- Pasting the reduced pixels in the correct place on the canvas,
- Writing the result to a new file.

In this process, since we're always basing layers on the original files, the quality loss should be minimized at the expense of much more processing.

If we wished to save on processing time/power, we could base each layer on the files of the previous one instead. The problem here is that the image quality would get progressively worse with each layer.

Of cardinal importance would be the image reduction algorithm to use. Sadly, the best algorithms are locked away from freely available software. The option always exists to implement such an algorithm oneselves, but for starters we won't go that route.

## Image display
The frontend, at every moment, should know what layer to display.

There are two possible mechanisms to do this.

### Using the zoom value
On a set of predetermined zoom breakpoints, we would toggle the display of the next or previous layer. The algorithm is the same that currently powers the lo-res / hi-res cell display (a system that has a single breakpoint).

We would need to experiment to know where to put these breakpoints. The idea would be to optimize the view quality of the content on each zoom.

Since the calculation is static, it's simple to program and easy on the processor. This works well for desktop or laptop computers with decent hardware, too. However, the behaviour in other systems, including mobile devices, is not the best.

### Using the viewport coordinates
This method is much more processor-intensive: it implies checking, after each zoom change, what original cells would need to be displayed on the top-right and the bottom-left extremes of the *viewport* (the canvas), then figuring out exactly which files we need to render.

This method can work well to minimize the amount of files needed in memory / to be loaded from the network, which is a current concern.

## Saving memory
Currently, image objects covering the totality of the theoretical cartesian space of the mosaic are created on initialization. The objects are placed on the canvas and not moved; instead, lo-res images are stretched, and hi-res (unstretched) images substitute them when it's time to switch.

We could save memory by using layers by ensuring that only the image objects pertaining to the current layer exist. Each layer needs substantially less files than the one below. Images do not need to stretch because they've been created with the correct size already.

If using viewport coordinates to calculate what to view, we can even only instantiate the image objects currently needed, plus a few at the edges, instead of loading and rendering the whole mosaic - even the hi-res files that will never get seen.