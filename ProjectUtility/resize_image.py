#!/usr/bin/python
# -*- coding: utf-8 -*-
import Image
import os
#Imports the Image and os libraries. os is part of standard libraries. Image is part of Python Image Library (PIL)
#PIL can be downloaded from: http://www.pythonware.com/products/pil/
 
#Creates sets and creates the directory onto where you want your files to be saved
outdir = "150images/"
os.mkdir("./"+outdir)
#If the directory already exists this will cause an OSError.
 
size = 150, 400 #Set the size that you want to resize your image to.
#Thumbnail automatically checks for ratio consistency so alter the important variable (height or width)
 
for files in os.listdir("."):
    #Sets the appropriate suffix to your files.
    outfile = os.path.splitext(files)[0] + "_thumbnail.jpg"
    #Transforms JPG formatted files
    if files.endswith(".jpg"):
        im = Image.open(files)
        try:
            im.thumbnail(size, Image.ANTIALIAS)
            im.save(outdir+outfile, "JPEG")
            print "Saved the file: %s" % outdir+outfile
        except IOError:
            print "cannot create thumbnail for '%s'" % infile
    #Transforms PNG formatted files
    if files.endswith(".png"):
        im = Image.open(files)
        try:
            im.thumbnail(size, Image.ANTIALIAS)
            im.save(outdir+outfile, "JPEG")
            print "Saved the file: %s" % outfile
        except IOError:
            print "cannot create thumbnail for '%s'" % infile