# -*- coding: UTF-8 -*-
"""
该脚本用于将图片分割成几块，然后用于开始菜单的磁贴
"""
import cv2
import os
import argparse
from PIL import Image
import matplotlib.pyplot as plt
import numpy as np

format_list = ["jpg", "JPG", "Jpeg", "PNG", "png"]
images_list = []


def read_image():
    file_list = os.listdir("./")
    img_list = []
    for file in file_list:
        if file.split(".")[-1] in format_list:
            img_list.append(file)
    return img_list


def img_resize(image):
    height, width = image.shape[0], image.shape[1]
    # 设置新的图片分辨率框架
    width_new = args.size[0]
    height_new = args.size[1]
    # 判断图片的长宽比率
    if width / height >= width_new / height_new:
        img_new = cv2.resize(image, (width_new, int(height * width_new / width)))
    else:
        img_new = cv2.resize(image, (int(width * height_new / height), height_new))
    return img_new


def img_show(x):
    cv2.namedWindow("img", 0)
    cv2.imshow("img", x)
    cv2.waitKey(0)


def showMulitImages(x):
    count = 0
    for file in x:
        count += 1
        plt.subplot(args.h, args.w, count)
        plt.imshow(cv2.cvtColor(cv2.imread(file), cv2.COLOR_BGR2RGB))
        plt.xticks([])
        plt.yticks([])
    plt.show()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='把图片按需要进行横向与竖向等分')

    parser.add_argument('--w', type=int, default="4", help='列数')
    parser.add_argument('--h', type=int, default="3", help='行数')
    parser.add_argument('--save_path', type=str, default="out", help='保存结果路径')
    parser.add_argument('--preImage', type=bool, default=False, help='是否预览图像')

    args = parser.parse_args()

    images_list = read_image()
    for image in images_list:
        img = cv2.imread(image)  # 变为Rgb图片
        """np.vstack()按垂直方向（行顺序）堆叠数组构成一个新的数组
        堆叠的数组需要具有相同的维度
        
            np.hstack()按水平方向（列顺序）堆叠数组构成一个新的数组
        堆叠的数组需要具有相同的维度
            plt.imshow(img)
            plt.show搭配使用，可以显示PIL格式的图片也可以显示array格式的图片
        """
        h, w = img.shape[0], img.shape[1]
        size = min(w // args.w, h // args.h)
        preShowList = []
        pre_show = np.array([])
        for i in range(args.h):
            for k in range(args.w):
                img_name = image.split('.')[0] + f"{i}_{k}.jpg"
                save_img = img[i * size:(i + 1) * size, k * size:(k + 1) * size, :]
                os.makedirs(os.path.join(args.save_path, image.split('.')[0]), exist_ok=True)
                result = f"{os.path.join(args.save_path, image.split('.')[0])}/{img_name}"
                cv2.imwrite(result, save_img)
                preShowList.append(result)
        if args.preImage:
            showMulitImages(preShowList)
