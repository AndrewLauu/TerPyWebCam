# -*- coding: utf-8 -*-
import json
import os
import time
import cv2
import datetime


def shouldRec():
    timeOk = datetime.time.hour in range(8, 19)
    temperatureOk = (
        json.loads(os.popen("termux-battery-status").read())["temperature"] or 40 <= 45
    )
    return timeOk and temperatureOk


def formalImg(img):
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    resize_img = cv2.resize(gray_img, (500, 500))
    blur_img = cv2.GaussianBlur(resize_img, (21, 21), 0)
    return blur_img

def noti(img):
    pass


global preImg
preImg = None


def comp():

    os.system("termux-camera-photo" + "images\\watch\\watch.jpg")

    img = cv2.imread("images\\watch\\watch.jpg")
    img = formalImg(img)

    if not preImg:
        preImg = img
    else:
        # absdiff把两幅图的差的绝对值输出到另一幅图上面来
        img_delta = cv2.absdiff(preImg, img)

        # threshold阈值函数(原图像应该是灰度图,对像素值进行分类的阈值,当像素值高于（有时是小于）阈值时应该被赋予的新的像素值,阈值方法)
        thresh = cv2.threshold(img_delta, 25, 255, cv2.THRESH_BINARY)[1]

        # 膨胀图像
        thresh = cv2.dilate(thresh, None, iterations=2)

        # findContours检测物体轮廓(寻找轮廓的图像,轮廓的检索模式,轮廓的近似办法)
        contours, _ = cv2.findContours(
            thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
        )
        for c in contours:
            # 设置敏感度
            # contourArea计算轮廓面积
            if cv2.contourArea(c) > 1000:
                print("Something changed")
                noti(img)
                break
        else:
            print("Nothing happened")

        preImg = img

        print("finish")


def main():
    while shouldRec():
        comp()
        time.sleep(5)


if __name__ == "__main__":
    main()
