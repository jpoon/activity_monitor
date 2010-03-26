#!/usr/bin/python

import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *

app = QApplication(sys.argv)

# create the window/frame
win = QWidget()

# the image file can be a .jpg, .png, ,gif, .bmp image file
# if not in the working directory, give the full path
# (filenames are case sensitive on Ubuntu/Linux)
image_file = "graphs/left_arm.png"
image = QPixmap(image_file)
width = image.width()
height = image.height()
# show the image name and size in the window title
info = "%s (%dx%d)" % (image_file, width, height) 
win.setWindowTitle(info)

# use a label to <strong class="highlight">display</strong> the image in
label = QLabel(win)
label.setGeometry(10, 10, width, height)
label.setPixmap(image)

win.show()

app.exec_()
