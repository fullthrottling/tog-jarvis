import json
import re
import win32con
import time
import os
import win32gui
import win32ui
import win32api
import cv2
import pytesseract
from .const import DEFINE_SCREENSHOP_PATH
from src.jsons.config import Config
from PIL import Image
import asyncio


def getInnnerWindows(whndl):
    def callback(hwnd, windows):
        if win32gui.IsWindowVisible(hwnd) and win32gui.IsWindowEnabled(hwnd):
            windows.append(hwnd)
        return True

    windows = []
    win32gui.EnumChildWindows(whndl, callback, windows)
    return windows


async def click(x, y, handle) -> None:
    win32gui.SendMessage(handle, win32con.WM_LBUTTONDOWN, 0, win32api.MAKELONG(x, y))
    await asyncio.sleep(0.2)
    win32gui.SendMessage(handle, win32con.WM_LBUTTONUP, 0, win32api.MAKELONG(x, y))
    await asyncio.sleep(0.2)


def getPathNCreate(path):
    if not os.path.exists(path):
        os.makedirs(path)
    return path


async def captureImage(hwnd, savePath, fileName, cLeft, cTop, cWidth, cHeight):
    left, top, right, bot = win32gui.GetWindowRect(hwnd)
    w = right - left
    h = bot - top

    hwndDC = win32gui.GetWindowDC(hwnd)
    mfcDC = win32ui.CreateDCFromHandle(hwndDC)
    saveDC = mfcDC.CreateCompatibleDC()

    saveBitMap = win32ui.CreateBitmap()
    saveBitMap.CreateCompatibleBitmap(mfcDC, cWidth, cHeight)
    saveDC.SelectObject(saveBitMap)
    saveDC.BitBlt((0, 0), (w, h), mfcDC, (cLeft, cTop), win32con.SRCCOPY)

    bmpinfo = saveBitMap.GetInfo()
    bmpstr = saveBitMap.GetBitmapBits(True)
    im = Image.frombuffer(
        "RGB",
        (bmpinfo["bmWidth"], bmpinfo["bmHeight"]),
        bmpstr,
        "raw",
        "BGRX",
        0,
        1,
    )
    im.save(savePath + fileName)
    win32gui.DeleteObject(saveBitMap.GetHandle())
    saveDC.DeleteDC()
    mfcDC.DeleteDC()
    win32gui.ReleaseDC(hwnd, hwndDC)


def get_text_from_image(image_path):
    img = cv2.imread(image_path)
    img = testImageModify(img)
    pytesseract.pytesseract.tesseract_cmd = (
        r"C:\Program Files\Tesseract-OCR\tesseract.exe"
    )
    config = "-l kor+eng --oem 3 --psm 6"
    d = pytesseract.image_to_data(
        img, output_type=pytesseract.Output.DICT, config=config
    )
    text = pytesseract.image_to_string(img, lang="kor+eng", config=config)
    n_boxes = len(d["text"])
    for i in range(n_boxes):
        if int(d["conf"][i]) > 60:
            (x, y, w, h) = (d["left"][i], d["top"][i], d["width"][i], d["height"][i])
            img = cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
    # cv2.imshow("img", img)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    return d, text


def testImageModify(img):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # img = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    # img = cv2.GaussianBlur(img, (5,5,),0)
    # img = cv2.Canny(img, 100, 200)
    # kernel = np.ones((1, 1), np.uint8)
    # img = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel)
    # cv2.imshow("img", img)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    return img


def getFindTextAndClick(hwnd, text, cLeft=0, cTop=0, cWidth=0, cHeight=0):
    captureImage(
        hwnd,
        getPathNCreate(DEFINE_SCREENSHOP_PATH),
        "tog.png",
        cLeft,
        cTop,
        cWidth,
        cHeight,
    )
    d, text = get_text_from_image(getPathNCreate(DEFINE_SCREENSHOP_PATH) + "tog.png")
    stringToNumber = re.sub(r"\D", "", text)
    cnt = d["text"].count(text)
    if 0 < cnt:
        idx = d["text"].index(text)
        left = d["left"][idx]
        top = d["top"][idx]
        # click(left, top, win)


def getConfig():
    with open("./config/config.json", "r") as f:
        config = json.load(f)
        return Config(config)


class Singleton(object):
    _instances = {}

    def __new__(class_, *args, **kwargs):
        if class_ not in class_._instances:
            class_._instances[class_] = super(Singleton, class_).__new__(
                class_, *args, **kwargs
            )
        return class_._instances
