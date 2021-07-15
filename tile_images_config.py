# -*- coding: UTF-8 -*-
"""
该脚本用于将图片分割成几块，然后用于开始菜单的磁贴
"""
import cv2
import os
import argparse
import traceback
import shutil
from PIL import Image
import matplotlib.pyplot as plt
import numpy as np

format_list = ["jpg", "JPG", "Jpeg", "PNG", "png"]
images_list = []


def read_image():
    file_list = os.listdir(args.src_path)
    img_list = []
    for file in file_list:
        if file.split(".")[-1] in format_list:
            img_list.append(os.path.join(args.src_path, file))
    return img_list


def img_show(x):
    cv2.namedWindow("img", 0)
    cv2.imshow("img", x)
    cv2.waitKey(0)


def showImages(x):
    count = 0
    for file in x:
        count += 1
        plt.subplot(args.row, args.col, count)
        plt.imshow(cv2.cvtColor(cv2.imdecode(np.fromfile(file, dtype=np.uint8), 1), cv2.COLOR_BGR2RGB))
        plt.xticks([])
        plt.yticks([])
    plt.show()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='把图片按需要进行横向与竖向等分')

    parser.add_argument('--row', type=int, default="3", help='行数')
    parser.add_argument('--col', type=int, default="4", help='列数')
    parser.add_argument('--src_path', type=str, default="./", help='源图片路径')
    parser.add_argument('--save_path', type=str, default="out", help='保存结果路径')
    parser.add_argument('--preImage', type=bool, default=False, help='是否预览图像')

    args = parser.parse_args()

    try:
        images_list = read_image()
        for image in images_list:
            img = cv2.imdecode(np.fromfile(image, dtype=np.uint8), 1)  # 变为Rgb图片
            """np.vstack()按垂直方向（行顺序）堆叠数组构成一个新的数组
            堆叠的数组需要具有相同的维度
            
                np.hstack()按水平方向（列顺序）堆叠数组构成一个新的数组
            堆叠的数组需要具有相同的维度
                plt.imshow(img)
                plt.show搭配使用，可以显示PIL格式的图片也可以显示array格式的图片
            """
            h, w = img.shape[0], img.shape[1]
            size = min(w // args.col, h // args.row)
            preShowList = []
            pre_show = np.array([])
            if "./" in image:
                image = image.replace("./", "")
            save_dir = os.path.join(args.save_path, image.split('.')[0])
            if os.path.exists(save_dir):
                shutil.rmtree(save_dir)
            os.makedirs(save_dir, exist_ok=True)
            for i in range(args.row):
                for k in range(args.col):
                    img_name = f"{i + 1}_{k + 1}.jpg"
                    save_img = img[i * size:(i + 1) * size, k * size:(k + 1) * size, :]
                    result = f"{save_dir}/{img_name}"
                    # cv2.imwrite(result, save_img)
                    cv2.imencode(".jpg", save_img)[1].tofile(result)  # 采用中文编码
                    preShowList.append(result)
            if args.preImage:
                showImages(preShowList)
            print(f"图片:{image} 裁剪完毕(*^_^*)")
    except Exception:
        print(f"裁剪{image}出错啦，检查一下吧")
        print(traceback.print_exc())
