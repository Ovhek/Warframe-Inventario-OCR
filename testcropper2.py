import numpy as np
import cv2
from PIL import ImageGrab

import win32gui
import win32ui
import win32con

def background_screenshot(hwnd, width, height):
    wDC = win32gui.GetWindowDC(hwnd)
    dcObj=win32ui.CreateDCFromHandle(wDC)
    cDC=dcObj.CreateCompatibleDC()
    dataBitMap = win32ui.CreateBitmap()
    dataBitMap.CreateCompatibleBitmap(dcObj, width, height)
    cDC.SelectObject(dataBitMap)
    cDC.BitBlt((0,0),(width, height) , dcObj, (0,0), win32con.SRCCOPY)
    dataBitMap.SaveBitmapFile(cDC, 'img/screenshot.bmp')
    dcObj.DeleteDC()
    cDC.DeleteDC()
    win32gui.ReleaseDC(hwnd, wDC)
    win32gui.DeleteObject(dataBitMap.GetHandle())

hwnd = win32gui.FindWindow(None, "Warframe")
background_screenshot(hwnd, 2560, 1421)

import cv2
img_juego = cv2.imread("img/screenshot.bmp")

crop_img_juego = img_juego[280:1330,100:1800]
cv2.imwrite("img/juego_cropped.jpg", crop_img_juego)

#Resolución 2K
for row in range(4):
    a = (220+45)*row
    b = 280+(220+50)*(3-row)
    for column in range(6):
        c = 30+(220+60)*column
        d = 100+(220+60)*(5-column)
        crop_img = crop_img_juego[0+a:1330-b,0+c:1800-d]
        cv2.imwrite(f"img/imagenesAescanear/img_sin_procesar{row}{column}.jpg", crop_img)
    