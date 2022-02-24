import random
import re
import os
import time


readDevicesId = list(os.popen('adb devices').readlines())
deviceId = re.findall(r'^\w*\b', readDevicesId[1])[0]



# 远程Appium服务地址
# gzAppiumH = "http://10.10.1.123:4723/wd/hub"
gzAppiumH = "http://127.0.0.1:4723/wd/hub"

# 手机系统
gzPlatformN = "Android"

# 包信息
gzAppPack = "com.glazero.android"
gzAppActivity = "com.glazero.android.SplashActivity"

# 登录账号
email = "1010642719@qq.com"
pwd = "Qwe222222"

# 手机列表
gzPhoneList = [
    # {'gzDeviceMode': "samsungA51", 'gzDeviceN': "10.10.1.157:5555", 'gzPlatformVer': "10"},
    {'gzDeviceMode': "samsungA51", 'gzDeviceN': "R58N828LKMP", 'gzPlatformVer': "10"},
    {'gzDeviceMode': "samsungS10e", 'gzDeviceN': "10.10.1.20:5555", 'gzPlatformVer': "11"}
]

# 业务参数
gzRegionList = [
    {'CN': "中国区", 'region': "中国", 'code': "+86"},
    {'US': "美国区", 'region': "美国", 'code': "+1"}
]

# default 默认连接三星A51 中国区
CONNECTTO = gzPhoneList[0]['gzDeviceN']
PLATFORMVER = gzPhoneList[0]['gzPlatformVer']
REGION = gzRegionList[0]['code']


# 生成随机邮箱
def randomEmail():
    metaData = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    emailType = ['@qq.com', '@163.com', '@outlook.com', '@glazero.com']
    emailLength = random.randint(4, 10)
    emailPrefox = "".join(random.choice(metaData) for i in range(emailLength))
    emailSuffix = random.choice(emailType)
    email = emailPrefox + emailSuffix
    return email


# 判断元素是否存在
def isElementPresent(driver, by, value):
    try:
        driver.find_element(by=by, value=value)
    except Exception as e:
        # 打印异常信息
        print(e)
        # 发生异常，表示页面中没有该元素
        return False
    else:
        # 没有发生异常，表示页面存在该元素
        return True
