# 匹配模板和图片，并用矩形框出最相似的区域

import cv2


# 将模板图片的空白部分裁剪掉
def trim(img):
    # 找到所有非黑像素点
    coords = cv2.findNonZero(img)
    # 找到最小裁剪矩形范围
    x, y, w, h = cv2.boundingRect(coords)
    # 裁剪图像，舍弃拼图的突出部分（14个像素），以提高匹配正确率
    rect = img[y + 14:y + h - 14, x:x + w - 14]
    return rect


def show_experiment(num):
    target_pic = 'target/target_' + str(num) + '.jpg'
    template_pic = 'template/template_' + str(num) + '.png'
    # 加载原始RGB图像
    img_rgb = cv2.imread(target_pic)
    # 创建一个原始图像的灰度版本，所有操作在灰度版本中处理，然后在RGB图像中使用相同坐标还原
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)

    # 加载将要搜索的图像模板
    template = cv2.imread(template_pic, 0)
    cv2.imshow('img_gray', img_gray)
    cv2.imshow('template', template)
    new_template = trim(template)
    cv2.imshow('new', new_template)
    h, w = new_template.shape
    # 使用matchTemplate对原始灰度图像和图像模板进行匹配
    res = cv2.matchTemplate(img_gray, new_template, cv2.TM_CCOEFF_NORMED)
    # 使用minMaxLoc求出最大匹配位置的坐标max_loc（左上角）
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    top_left = max_loc
    # 根据左上角坐标求右下角坐标
    bottom_right = (top_left[0] + w, top_left[1] + h)
    # 使用灰度图像中的坐标对原始RGB图像进行标记
    # cv2.rectangle(图片，矩形对角线坐标1，矩形对角线坐标2，颜色，粗细)
    cv2.rectangle(img_rgb, top_left, bottom_right, (255, 255, 255), 2)
    # 显示图像
#    cv2.startWindowThread()
    cv2.imshow('Detected', img_rgb)
    cv2.waitKey(99000)
#    cv2.destroyAllWindows()


if __name__ == '__main__':
    for i in range(20):
        print(f'picture_{i},start...')
        show_experiment(i)
