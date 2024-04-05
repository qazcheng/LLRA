import re
import csv
from PIL import Image
import pytesseract
import cv2
import numpy as np

# 打开视频文件
video_capture = cv2.VideoCapture('IOT.mp4')

# 初始化一些变量
frame_rate = 100  # 截取频率（每秒一帧）
prev_time = 0
frame_count = 0  # 用于保存图像的计数

# 配置Tesseract参数，设置为只识别数字
custom_config = r'--oem 3 --psm 11 outputbase digits'

# 创建CSV文件并写入列标题
with open('output_numbers.csv', mode='w', newline='') as csv_file:
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(['Time (seconds)', 'Extracted Numbers'])

while True:
    # 读取视频帧
    ret, frame = video_capture.read()

    # 检查是否成功读取帧
    if not ret:
        break

    # 获取当前帧的时间
    current_time = video_capture.get(0)  # 0表示获取帧时间

    # 每隔一秒截取一帧
    if current_time - prev_time >= frame_rate:
        prev_time = current_time

        # 转换图像为灰度
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # 应用阈值二值化
        _, binary = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY)

        # 进行去噪声处理
        denoised = cv2.medianBlur(binary, 3)
        # 保存预处理后的图像（可选）
        # cv2.imwrite('preprocessed_image.jpg', denoised)
        # 使用Tesseract进行文字识别，仅识别数字
        text = pytesseract.image_to_string(Image.fromarray(denoised), config=custom_config)

        # 使用正则表达式提取数字
        numbers = re.findall(r'\d+\.\d+', text)
        # numbers = re.findall(r'[\d. ]+', text)
        #打印提取的数字
        for number in numbers:
            print(number)
        # 打印提取的数字
        print(f"Time: {current_time:.2f} seconds - Text: {text}")

        # 将提取的数字写入CSV文件
        with open('output_numbers.csv', mode='a', newline='') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow([current_time, ', '.join(numbers)])

# 释放视频捕获对象
video_capture.release()
