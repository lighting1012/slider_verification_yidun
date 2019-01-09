# 自动从网站上下载验证码底图和缺口图，以便测试

from PIL import Image
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from io import BytesIO
import time
import requests


def init():
    global url, driver, wait, zoom
    # 实际地址
    url = 'https://etax.jsgs.gov.cn/sso/login'
    driver = webdriver.Chrome()
    wait = WebDriverWait(driver, 5)
    zoom = 1


def open():
    driver.get(url)
    # 获取标签dom,隐式等待
    ok_buttom = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'xubox_setwin')))
    # 点击确认，登录按钮
    ok_buttom.click()
    login_buttom = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'go_login')))
    login_buttom.click()


def get_pic():
    roundd = 0
    panel = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'yidun_panel')))
    driver.execute_script("arguments[0].setAttribute(arguments[1], arguments[2])", panel, "display", "block")
    while roundd < 20:
        time.sleep(1)
        target = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'yidun_bg-img')))
        template = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'yidun_jigsaw')))
        slider = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'yidun_slider')))
        target_link = target.get_attribute('src')
        template_link = template.get_attribute('src')
        target_img = Image.open(BytesIO(requests.get(target_link).content))
        template_img = Image.open(BytesIO(requests.get(template_link).content))
        target_name = 'target/target_' + str(roundd) + '.jpg'
        template_name = 'template/template_' + str(roundd) + '.png'
        target_img.save(target_name)
        template_img.save(template_name)
        ActionChains(driver).move_to_element(slider).perform()
        time.sleep(1)
        ActionChains(driver).click(driver.find_element(By.CLASS_NAME, 'yidun_refresh')).perform()
        print(f'saving pictures_{roundd}')
        roundd += 1


if __name__ == '__main__':
    init()
    open()
    get_pic()
