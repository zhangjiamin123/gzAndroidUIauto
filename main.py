
# 按 Shift+F10 执行或将其替换为您的代码。
# 按 双击 Shift 在所有地方搜索类、文件、工具窗口、操作和设置。
# -*- encoding: utf-8 -*-
#import time
#from lib2to3.pgen2.driver import Driver
#from lib2to3.tests.support import driver
#from appium.webdriver.extensions.android.nativekey import AndroidKey
#from selenium.webdriver.common.by import By
import gz_public
from appium import webdriver

desired_caps = dict(
    platformName=gz_public.gzPlatformN,
    deviceName=gz_public.gzDeviceN,
    platformVersion=gz_public.gzPlatformVer,
    appPackage=gz_public.gzAppPack,
    appActivity=gz_public.gzAppActivity,
    #unicodeKeyboard=True,   #使用appium键盘
    #resetKeyboard=True,   #使用appium键盘
    noReset=True,   #不重启app
    autoGrantPermissions=True,   #安装时自动赋予权限
    newCommandTimeout=6000,
    automationName='UiAutomator2'
)

driver = webdriver.Remote(gz_public.gzAppiumH, desired_caps, direct_connection=True)
driver.implicitly_wait(10)

#step1：点击 登录 按钮
driver.find_element_by_id("com.glazero.android:id/splash_login").click()
driver.implicitly_wait(10)

#step2：输入用户名和密码
driver.find_elements_by_id("com.glazero.android:id/edit_text")[0].clear()
driver.implicitly_wait(10)
driver.find_elements_by_id("com.glazero.android:id/edit_text")[0].click()
driver.implicitly_wait(10)
driver.find_elements_by_id("com.glazero.android:id/edit_text")[0].send_keys(gz_public.email)

driver.hide_keyboard()

driver.find_elements_by_id("com.glazero.android:id/edit_text")[1].clear()
driver.implicitly_wait(10)
driver.find_elements_by_id("com.glazero.android:id/edit_text")[1].click()
driver.implicitly_wait(10)
driver.find_elements_by_id("com.glazero.android:id/edit_text")[1].send_keys(gz_public.pwd)

driver.hide_keyboard()

#step3：选择地区
driver.find_elements_by_id("com.glazero.android:id/edit_text")[2].click()
driver.implicitly_wait(10)
driver.find_element_by_android_uiautomator('new UiScrollable(new UiSelector().scrollable(true)).scrollIntoView(new UiSelector().text("+86"))')
driver.implicitly_wait(10)
driver.find_element_by_xpath('//android.widget.TextView[@text="+86"]').click()   #此时只能写类名
driver.implicitly_wait(10)

#step4：点击 登录 按钮
driver.find_element_by_id("com.glazero.android:id/button").click()
driver.implicitly_wait(10)

#tear down
#driver.quit()

def print_hi(name):
    # 在下面的代码行中使用断点来调试脚本。
    print(f'Hi, {name}')  # 按 Ctrl+F8 切换断点。


# 按间距中的绿色按钮以运行脚本。
#if __name__ == '__main__':
#    print_hi('PyCharm')

# 访问 https://www.jetbrains.com/help/pycharm/ 获取 PyCharm 帮助
