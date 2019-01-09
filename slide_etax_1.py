# Google Chrome
# https://etax.jsgs.gov.cn/sso/login

from PIL import Image
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import cv2
import numpy as np
from io import BytesIO
import time
import requests


class CrackSlider():
    """
    通过浏览器截图，识别验证码中缺口位置，获取需要滑动距离，并模仿人类行为破解滑动验证码
    """

    def __init__(self):
        super(CrackSlider, self).__init__()
        # 实际地址
        self.url = 'https://etax.jsgs.gov.cn/sso/login'
        self.driver = webdriver.Chrome()
        self.wait = WebDriverWait(self.driver, 5)
        local_img = Image.open('target.jpg')
        size_loc = local_img.size
        self.zoom = 320 / int(size_loc[0])

    def open(self):
        self.driver.get(self.url)
        # 获取标签dom,隐式等待
        ok_buttom = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'xubox_setwin')))
        # 点击确认，登录按钮
        ok_buttom.click()
        login_buttom = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'go_login')))
        login_buttom.click()

    def get_pic(self):
        time.sleep(2)
        target = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'yidun_bg-img')))
        template = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'yidun_jigsaw')))
        target_link = target.get_attribute('src')
        template_link = template.get_attribute('src')
        target_img = Image.open(BytesIO(requests.get(target_link).content))
        template_img = Image.open(BytesIO(requests.get(template_link).content))
        target_img.save('target.jpg')
        template_img.save('template.png')

    # 将模板图片的空白部分裁剪掉
    def trim(self, img):
        # 找到所有非黑像素点
        coords = cv2.findNonZero(img)
        # 找到最小裁剪矩形范围
        x, y, w, h = cv2.boundingRect(coords)
        # 裁剪图像，舍弃拼图的突出部分（14个像素），以提高匹配正确率
        rect = img[y + 14:y + h - 14, x:x + w - 14]
        return rect

    def match(self, target, template):
        # 读取图像
        img_rgb = cv2.imread(target)
        # 对背景图进行灰度化处理
        img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
        # 读取图像
        template = cv2.imread(template, 0)
        # 裁剪碎片图
        new_template = self.trim(template)
        # 使用matchTemplate对原始灰度图像和碎片图进行匹配
        res = cv2.matchTemplate(img_gray, new_template, cv2.TM_CCOEFF_NORMED)
        # 使用minMaxLoc求出最佳匹配位置的坐标max_loc（左上角）
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
        top_left = max_loc
        # 返回匹配位置左上角的横坐标
        return top_left[0]

    def get_tracks(self, distance):
        print(distance)
        v = 0
        t = 0.05
        forward_tracks = []
        current = 0
        mid = distance * 3 / 5
        while current < distance:
            if current < mid:
                a = 2
            else:
                a = -3
            s = v * t + 0.5 * a * (t ** 2)
            v = v + a * t
            current += s
            forward_tracks.append(round(s))
        return forward_tracks

    # 模拟拖动
    def move_to_gap(self, distance):
        # 根据实验结果做的微调
        if distance < 120 or distance > 220:
            distance += 10
        if distance < 80:
            distance += 10
        tracks = self.get_tracks(distance * self.zoom)  # 对位移的缩放计算
        slider = self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'yidun_slider')))
        ActionChains(self.driver).click_and_hold(slider).perform()
        # 按轨迹拖动滑块
        for track in tracks:
            ActionChains(self.driver).move_by_offset(xoffset=track, yoffset=0).perform()
        # 抖动，模拟人的校准操作
        time.sleep(0.5)
        ActionChains(self.driver).move_by_offset(xoffset=-3, yoffset=0).perform()
        time.sleep(0.2)
        ActionChains(self.driver).move_by_offset(xoffset=3, yoffset=0).perform()
        time.sleep(0.5)
        ActionChains(self.driver).release().perform()


if __name__ == '__main__':
    count = 0
    target = 'target.jpg'
    template = 'template.png'
    f = open('experiment.txt', 'w')
    while count < 10:
        c = CrackSlider()
        count += 1
        f.write(f'第{count}次...')
        c.open()
        c.get_pic()
        distance = c.match(target, template)
        f.write(f'distance = {distance}\n')
        c.move_to_gap(distance)
        try:
            c.wait.until(
                EC.text_to_be_present_in_element((By.CLASS_NAME, 'yidun_tips__text'), '向右拖动滑块填充拼图'))
            f.write(f'fail!\n')
        except:
            f.write('success!\n')
        c.driver.close()
        time.sleep(1)
    f.close()
