#!/usr/bin/env python3

# from PyQt5.QtWidgets import QApplication, QSystemTrayIcon, QMenu, QAction, QHBoxLayout, QGroupBox, QSlider, QWidget, \
#     QActionGroup, QDesktopWidget, QMessageBox
# from PyQt5.QtGui import QIcon, QPixmap, QCursor, QImage
# from PyQt5.QtCore import Qt, QProcess, QMetaObject, QCoreApplication, QEvent, QObject, QTimer
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QPixmap, QImage

import sys
import os
import json
import requests
from os.path import exists


LOCAL = os.path.dirname(__file__)

 
# def procDownload():
if __name__ == "__main__":

    app = QApplication(sys.argv)
    screen = app.primaryScreen()
    size = screen.size()
    width = size.width()
    height = size.height()

    response = requests.get("https://www.bing.com/HPImageArchive.aspx?format=js&idx=0&n=1&mkt=en-US")
    image_data = json.loads(response.text)

    image_url = image_data["images"][0]["url"]
    
    urlbase = image_data["images"][0]["urlbase"][11:] # remove /th?id=OHR.
    title = image_data["images"][0]["title"]
    copyright = image_data["images"][0]["copyright"]

    image_url = image_url.split("&")[0]
    full_image_url = "https://www.bing.com" + image_url
    img_data = requests.get(full_image_url).content

    with open(f'{LOCAL}/Resources/imagename', 'w') as f:
        f.write(urlbase)

    with open(f'{LOCAL}/Resources/gallery/{urlbase}.jpeg', 'wb') as f:
        f.write(img_data)

    with open(f'{LOCAL}/Resources/gallery/{urlbase}', 'w') as f:
        f.write(title)
        f.write('\n')
        f.write(copyright)

    # width = 1920 # 1368
    # height = 1080 # 768

    image = QImage(f'{LOCAL}/Resources/gallery/{urlbase}.jpeg', 'JPG')
    locked = QPixmap.fromImage(image).scaled(width, height) #, Qt.KeepAspectRatio)

    for i in range(image.height()):
        for k in range(image.width()):
            image.setPixelColor(k, i, image.pixelColor(k,i).darker(160))

    authorize = QPixmap.fromImage(image).scaled(width, height) #, Qt.KeepAspectRatio)

    authorize.save(f'{LOCAL}/Resources/themes/wallpaper.authorize.jpg')
    locked.save(f'{LOCAL}/Resources/themes/wallpaper.locked.jpg')
    with open(f'{LOCAL}/Resources/themes/wallpaper.description', 'w') as f:
        f.write(title)
        f.write('\n')
        f.write(copyright)

    # helloSystem?
    if os.path.exists('/usr/local/bin/launch'): 
        os.system(f'launch Filer --set-wallpaper {LOCAL}/Resources/gallery/{urlbase}.jpeg')

    # LXDE?
    elif os.path.exists('/usr/bin/pcmanfm'): 
        os.system(f'pcmanfm --set-wallpaper {LOCAL}/Resources/gallery/{urlbase}.jpeg')

    # Unknown        
    else:
        print('oops!')


