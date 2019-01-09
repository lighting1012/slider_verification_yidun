# crack_slide_puzzle
use python and selenium to crack puzzle verification  
自动打开国家税务网的登陆页面，模拟滑动验证码的操作。为自动测试做准备  

## python3.6 依赖包：
pillow  
selenium  
opencv  
numpy  
time  
request  

## target/
存放验证码背景图
## template/
存放验证码碎片图
## get_test_picture.py
从网站上下载20组图片，以供测试  
## testing.py
对文件夹中20组图片进行测试，标记处匹配位置  
## slide_etax_1.py
自动进行10次破解验证码的实验，并记录  
## experiment.txt
10次验证码破解的记录

## 运行
python slide_etax_google.py
