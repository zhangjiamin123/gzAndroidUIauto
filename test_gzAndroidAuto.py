"""
----------------------------------
@Author: Zhang jia min
@Version: 1.0
@Date: 20220130
----------------------------------
"""
# from appium.webmaster.connectiontype import ConnectionType
# from selenium.webdriver.support import expected_conditions
# import pytest_repeat
import logging
from appium import webdriver
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from gz_public import get_dsc
from gz_start_appium import StartAppium
import gz_public
import initPhone
import pytest
import allure
import time

logging.basicConfig(filename='./log/runTest.log', level=logging.DEBUG, datefmt='[%Y-%m-%d %H:%M:%S]',
                    format='%(asctime)s %(levelname)s %(filename)s [%(lineno)d] %(threadName)s : %(message)s')

devices = ['SamsungA51', 'moto_z4']

dev_tmp = []

for i in devices:
    tmp = get_dsc(device=i)
    dev_tmp.append(tmp)


def setup_module():
    phone_1 = dev_tmp.pop(0)
    print('phone_1: ', phone_1)
    phone_2 = dev_tmp.pop(0)
    print('phone_2: ', phone_2)

    global master, slave

    StartAppium.start_appium(port=phone_1["port"])
    time.sleep(3)
    master = webdriver.Remote("http://127.0.0.1:%s/wd/hub" % phone_1["port"], phone_1["des"])
    master.implicitly_wait(10)

    # 用一个手机时注释掉该段，用两个手机时打开，连同第84行
    '''
    StartAppium.start_appium(port=phone_2["port"])
    time.sleep(3)
    slave = webdriver.Remote("http://127.0.0.1:%s/wd/hub" % phone_2["port"], phone_2["des"])
    slave.implicitly_wait(10)
    '''

    # 当前没有网络连接，设置wifi连接
    # if master.network_connection == 0:
    # master.set_network_connection(ConnectionType.WIFI_ONLY)

    # if slave.network_connection == 0:
    # slave.set_network_connection(ConnectionType.WIFI_ONLY)

    # 检查屏幕是否点亮
    if not initPhone.InitPhone.isAwake():
        # 26 电源键
        initPhone.InitPhone.keyEventSend(26)
        # 82 解锁键 去掉密码后可以注释掉下面的code
        # initPhone.InitPhone.keyEventSend(82)
        # 1
        # initPhone.InitPhone.keyEventSend(8)
        # 2
        # initPhone.InitPhone.keyEventSend(9)
        # 3
        # initPhone.InitPhone.keyEventSend(10)
        # 4
        # initPhone.InitPhone.keyEventSend(11)
        # 回车键
        # initPhone.InitPhone.keyEventSend(66)
        # 回到桌面
        initPhone.InitPhone.keyEventSend(3)

    # 已安装aosu 先卸载
    if initPhone.InitPhone.isAppExist():
        initPhone.InitPhone.uninstallApp()

    # 安装aosu app
    initPhone.InitPhone.installApp()


def teardown_module():
    master.quit()
    # slave.quit()


@allure.feature('登录模块')
class TestGzLogin(object):
    @staticmethod
    def setup_method():
        if master.current_activity != ".SplashActivity":
            master.launch_app()
            master.wait_activity("com.glazero.android.SplashActivity", 2, 2)

    @allure.story('用户名和密码输入框右侧的关闭按钮和显示/隐藏按钮')
    def test_gzLoginClearShowHide(self):
        with allure.step('step1: 在splash页，点击 登录 按钮'):
            master.find_element_by_id("com.glazero.android:id/splash_login").click()
            master.implicitly_wait(10)

        with allure.step('step2: 输入用户名'):
            master.find_elements_by_id("com.glazero.android:id/edit_text")[0].clear()
            master.implicitly_wait(10)
            master.find_elements_by_id("com.glazero.android:id/edit_text")[0].click()
            master.implicitly_wait(10)
            inputText = gz_public.randomEmail()
            master.find_elements_by_id("com.glazero.android:id/edit_text")[0].send_keys(inputText)
            master.implicitly_wait(10)

        # 不能隐藏键盘，因为键盘收起后输入框带有默认的提示文案，例如，邮箱地址
        # 验证输入的内容正确
        assert master.find_elements_by_id("com.glazero.android:id/edit_text")[0].text == inputText

        with allure.step('step3: 点击 用户名输入框 右侧的清除按钮‘X’'):
            master.find_element_by_id("com.glazero.android:id/img_delete").click()
            master.implicitly_wait(10)

        # 验证 清除后的输入框为空
        assert master.find_element_by_id("com.glazero.android:id/textinput_placeholder").text == ''

        with allure.step('step4: 输入密码'):
            master.find_elements_by_id("com.glazero.android:id/edit_text")[1].clear()
            master.implicitly_wait(10)
            master.find_elements_by_id("com.glazero.android:id/edit_text")[1].click()
            master.implicitly_wait(10)
            randomText = inputText.split('@')[0]
            master.find_elements_by_id("com.glazero.android:id/edit_text")[1].send_keys(randomText)
            master.implicitly_wait(10)

        # 不能隐藏键盘，因为键盘收起后输入框带有默认的提示文案，例如，密码
        # 验证输入的内容正确
        assert master.find_elements_by_id("com.glazero.android:id/edit_text")[1].text == randomText

        with allure.step('step5: 点击 密码输入框 右侧的显示按钮'):
            master.find_element_by_id("com.glazero.android:id/img_pwd_visible").click()
            master.implicitly_wait(10)

        # 验证输入的内容正确，因为点击两个按钮后没有变化，所以暂时先这样断言，后续跟开发沟通，区分一下这两个按钮
        assert master.find_elements_by_id("com.glazero.android:id/edit_text")[1].text == randomText

        with allure.step('step6: 点击 密码输入框 右侧的清除按钮‘X’'):
            master.find_element_by_id("com.glazero.android:id/img_delete").click()
            master.implicitly_wait(10)

        # 验证 清除后的输入框为空
        assert master.find_element_by_id("com.glazero.android:id/textinput_placeholder").text == ''

        # 隐藏键盘
        master.hide_keyboard()

        # 点击 右上角的关闭按钮
        master.find_element_by_id("com.glazero.android:id/img_title_close").click()
        master.implicitly_wait(10)

        # 回到 splash页面，断言登录和创建账号按钮（不断言文本，因为跟语言变化）
        assert master.find_element_by_id("com.glazero.android:id/splash_login")
        assert master.find_element_by_id("com.glazero.android:id/splash_create_account")

    @allure.story('输入用户名和密码登录aosu app')
    def test_gzLogin(self, user_name=gz_public.email, pass_word=gz_public.pwd, region=gz_public.REGION):
        # 点击 aosu 图标7次，在地区列表中出现中国
        for ii in range(1, 8):
            master.find_elements_by_class_name("android.widget.ImageView")[0].click()
            master.implicitly_wait(1)

        with allure.step('step1：在splash页，点击 登录 按钮'):
            master.find_element_by_id("com.glazero.android:id/splash_login").click()
            master.implicitly_wait(10)

        with allure.step('step2：输入用户名'):
            master.find_elements_by_id("com.glazero.android:id/edit_text")[0].clear()
            master.implicitly_wait(10)
            master.find_elements_by_id("com.glazero.android:id/edit_text")[0].click()
            master.implicitly_wait(10)
            master.find_elements_by_id("com.glazero.android:id/edit_text")[0].send_keys(user_name)

        # 输入完成后隐藏键盘
        master.hide_keyboard()

        with allure.step('step3: 输入密码'):
            master.find_elements_by_id("com.glazero.android:id/edit_text")[1].clear()
            master.implicitly_wait(10)
            master.find_elements_by_id("com.glazero.android:id/edit_text")[1].click()
            master.implicitly_wait(10)
            master.find_elements_by_id("com.glazero.android:id/edit_text")[1].send_keys(pass_word)

        # 输入完成后隐藏键盘
        master.hide_keyboard()

        with allure.step('step4：选择地区'):
            # 如果默认是指定的地区，那么就直接点击登录
            if master.find_elements_by_id("com.glazero.android:id/edit_text")[2].text[-3:] == region:
                time.sleep(1)
            else:
                # 如果默认不是指定的地区，那么就在地区列表中选择
                master.find_elements_by_id("com.glazero.android:id/edit_text")[2].click()
                master.implicitly_wait(10)
                master.find_element_by_android_uiautomator(
                    'new UiScrollable(new UiSelector().scrollable(true)).scrollIntoView(new UiSelector().text("%s"))' % region)
                master.implicitly_wait(10)
                master.find_element_by_xpath(
                    '//android.widget.TextView[@text="%s"]' % region).click()  # 此时只能写类名
                master.implicitly_wait(10)
        # 点击登录按钮之前截图
        time.sleep(3)
        ts = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())
        master.save_screenshot('./report/login_%s.png' % ts)
        master.implicitly_wait(10)

        with allure.step('step5：点击 登录 按钮'):
            allure.attach.file("./report/login_%s.png" % ts, name="登录页面",
                               attachment_type=allure.attachment_type.JPG)
            master.find_element_by_id("com.glazero.android:id/button").click()
            master.implicitly_wait(10)

        # 点击登录按钮之后即进入首页后截图截图
        time.sleep(5)
        master.save_screenshot('./report/homePage.png')
        master.implicitly_wait(10)

        with allure.step('step6: 登录成功'):
            allure.attach.file("./report/homePage.png", name="登陆成功 进入首页",
                               attachment_type=allure.attachment_type.JPG)

        # 登录后进入首页，有可能会弹出低电量的弹窗，发现后点击“知道了”关闭弹窗
        if gz_public.isElementPresent(driver=master, by="id",
                                      value="com.glazero.android:id/btn_dialog_confirm") is True:
            master.find_element_by_id("com.glazero.android:id/btn_dialog_confirm").click()
            master.implicitly_wait(10)

        # 没有设备的情况下启动app后会进入select model页面，兼容该页面，点击返回<，回到首页
        if gz_public.isElementPresent(driver=master, by="id", value="com.glazero.android:id/tv_title_string") is True:
            if master.find_element_by_id('com.glazero.android:id/tv_title_string').text == 'Select Model':
                master.find_element_by_id('com.glazero.android:id/img_title_back').click()
                master.implicitly_wait(10)

        # 断言是否进入首页，关键元素是：菜单按钮、logo、添加设备按钮、设备tab、回放tab、在线客服tab
        # 20230509：以下图标在1.11.18版本中已经发生变化
        assert master.current_activity in (".main.MainActivity", ".account.login.LoginActivity")
        assert master.find_element_by_id("com.glazero.android:id/img_menu")
        # 20230509：这个图标没有了
        # assert master.find_element_by_id("com.glazero.android:id/img_logo")
        assert master.find_element_by_id("com.glazero.android:id/img_add_device")
        assert master.find_element_by_id("com.glazero.android:id/img_tab_device")
        assert master.find_elements_by_id("com.glazero.android:id/img_tab_playback")
        assert master.find_element_by_id("com.glazero.android:id/img_tab_service")

    @staticmethod
    def teardown_method():
        master.close_app()
        master.implicitly_wait(10)


@allure.feature('添加设备-配网')
class TestAddDevices(object):
    """
    前提：
    1、执行这个测试类，前提条件是要登录，登录后才能执行这组用例
    2、登录前先要启动app
    3、那么就要使用setup_class
    """

    @staticmethod
    def setup_class():
        master.close_app()
        master.implicitly_wait(10)
        master.launch_app()
        master.implicitly_wait(10)

        # 登录状态下启动app 进入首页 activity 是：.SplashActivity，不是：.account.login.LoginActivity，所以不能通过activity判断是否在首页
        # 通过登录后首页左上角的menu图标判断
        if not gz_public.isElementPresent(driver=master, by="id", value="com.glazero.android:id/img_menu"):
            TestGzLogin.test_gzLogin(self=NotImplemented)
            master.implicitly_wait(10)

    @staticmethod
    def setup_method(self):
        # 检查屏幕是否点亮
        if not initPhone.InitPhone.isAwake():
            # 26 电源键
            initPhone.InitPhone.keyEventSend(26)
            time.sleep(1)

        # 不在首页的话 启动一下app
        if gz_public.isElementPresent(driver=master, by="id", value="com.glazero.android:id/img_menu") is False:
            master.launch_app()
            master.wait_activity("com.glazero.android.SplashActivity", 2, 2)
            time.sleep(3)

        # 在首页的话下滑刷新一下设备列表
        if gz_public.isElementPresent(driver=master, by="id", value="com.glazero.android:id/img_menu") is True:
            gz_public.swipe_down(driver=master)
            # 等待下来刷新完成
            time.sleep(3)

    @staticmethod
    def teardown_method(self):
        # 调用解绑接口，默认是中国区‘api-cn.aosulife.com’
        # gz_public._unbind('V8P1AH110002353', 1, 1)
        # 335
        gz_public._unbind('C2E2BH110000278', 1, 1)
        # 337
        # gz_public._unbind('C2E2BH110000233', 1, 1)
        # C6SP 基站
        # gz_public._unbind('H1L2AH110000650', 1, 1)
        # time.sleep(2)

        # 如果绑定失败的话，会停留在失败页面，每次执行完成后要回到首页
        if not gz_public.isElementPresent(driver=master, by="id", value="com.glazero.android:id/img_menu"):
            if master.find_element_by_id('com.glazero.android:id/tv_tip').text == 'Connection failed':
                master.find_element_by_id('com.glazero.android:id/img_title_close').click()
                master.implicitly_wait(10)

        # 接口解绑成功后，再次绑定时，客户端提示：设备被其他账号绑定，但实际上绑定成功的情况，所以等待20秒
        # time.sleep(20)

        # c2e特殊场景验证，等待1小时后进行绑定
        # 强制等待时间过程driver会断开
        # time.sleep(600)
        '''
        for _i in range(1, 2):
            time.sleep(10)
            master.find_element_by_id('com.glazero.android:id/img_tab_device').click()
        '''

    @allure.title('V8P 绑定-解绑')
    @allure.story('用户循环测试V8P的绑定和解绑')
    def test_addV8P(self, ssid='11111111', pwd='12345678'):
        with allure.step(
                'step1：点击右上角的+号，开始执行时间为：%s' % time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())):
            master.find_element_by_id('com.glazero.android:id/img_add_device').click()
            master.implicitly_wait(10)

        with allure.step('step2：选择V8P'):
            master.find_element_by_xpath('//android.widget.TextView[@text="Pro · V8P"]').click()
            master.implicitly_wait(10)

        with allure.step('step3：点击continue'):
            master.find_element_by_id('com.glazero.android:id/next_step').click()
            master.implicitly_wait(10)

        with allure.step('step4：继续点击下一步'):
            master.find_element_by_id('com.glazero.android:id/next_step').click()
            master.implicitly_wait(10)

        with allure.step('step5：继续点击下一步'):
            master.find_element_by_id('com.glazero.android:id/next_step').click()
            master.implicitly_wait(10)

        with allure.step('step6：继续点击下一步'):
            master.find_element_by_id('com.glazero.android:id/next_step').click()
            master.implicitly_wait(10)

        with allure.step('step7：继续点击下一步'):
            master.find_element_by_id('com.glazero.android:id/next_step').click()
            master.implicitly_wait(10)

        with allure.step('step8：如果弹出wifi权限弹窗则给予权限'):
            if gz_public.isElementPresent(driver=master, by="id",
                                          value="com.glazero.android:id/btn_dialog_confirm") is True:
                if master.find_element_by_id('com.glazero.android:id/btn_dialog_confirm').text == 'GO SETTINGS':
                    master.find_element_by_id('com.glazero.android:id/btn_dialog_confirm').click()
                    master.implicitly_wait(10)

                if master.find_element_by_id(
                        'com.android.permissioncontroller:id/permission_allow_foreground_only_button').text == 'Allow only while using the app':
                    master.find_element_by_id(
                        'com.android.permissioncontroller:id/permission_allow_foreground_only_button').click()
                    master.implicitly_wait(10)

        with allure.step('step9：输入ssid和pwd'):
            # 先清除ssid
            master.find_elements_by_id('com.glazero.android:id/edit_text')[0].clear()
            # 第2次执行的时候会带ssid和pwd信息，所以不能用文本去识别
            # master.find_element_by_xpath('//android.widget.EditText[@text="Wi-Fi Name"]').clear()
            master.implicitly_wait(10)
            # 再输入ssid
            master.find_elements_by_id('com.glazero.android:id/edit_text')[0].send_keys(ssid)
            master.implicitly_wait(10)

            # 先清除pwd
            master.find_elements_by_id('com.glazero.android:id/edit_text')[1].clear()
            master.implicitly_wait(10)
            # 再输入pwd
            master.find_elements_by_id('com.glazero.android:id/edit_text')[1].send_keys(pwd)
            master.implicitly_wait(10)

            # 点击 下一步
            master.find_element_by_id('com.glazero.android:id/next_step').click()
            master.implicitly_wait(10)

        with allure.step('step10：继续点击下一步'):
            master.find_element_by_id('com.glazero.android:id/next_step').click()
            master.implicitly_wait(10)

        with allure.step('step11：继续点击下一步'):
            master.find_element_by_id('com.glazero.android:id/next_step').click()
            master.implicitly_wait(10)

        with allure.step('step12：校验二维码页面生成成功'):
            if gz_public.isElementPresent(driver=master, by="id",
                                          value="com.glazero.android:id/btn_dialog_confirm") is True:
                assert master.find_element_by_id('com.glazero.android:id/tv_title_string').text == 'Scan QR Code'
                master.implicitly_wait(10)

            # 如果二维码生成失败，点击页面中的Refresh
            if gz_public.isElementPresent(driver=master, by='id',
                                          value='com.glazero.android:id/tv_scan_code_load_retry') is True:
                master.find_element_by_id('com.glazero.android:id/tv_scan_code_load_retry').click()
                master.implicitly_wait(10)

            # 二维码生成成功后，Iheard the “beep” sound 按钮会高亮
            assert master.find_element_by_id('com.glazero.android:id/button').is_enabled() is True

        with allure.step(
                'step13：等待配网成功页面出现，超时时间是7分钟，每2秒检查一次页面，结束时间为：%s' % time.strftime(
                    "%Y-%m-%d %H:%M:%S", time.localtime())):
            WebDriverWait(master, timeout=420, poll_frequency=2).until(
                lambda x: x.find_element_by_xpath('//android.widget.TextView[@text="Connected successfully"]'))
        # 出现后点击下一步
        master.find_element_by_id('com.glazero.android:id/btn').click()
        master.implicitly_wait(10)

        # 进入引导页面，引导页面弹出较慢，等待5秒
        time.sleep(5)
        if gz_public.isElementPresent(driver=master, by="id", value="com.glazero.android:id/tv_title_string"):
            if master.find_element_by_id('com.glazero.android:id/tv_title_string').text == 'Final Steps':
                # 关闭引导页面
                master.find_element_by_id('com.glazero.android:id/img_title_close').click()
                master.implicitly_wait(10)
                # 点击 YES
                master.find_element_by_xpath('//android.widget.Button[@text="YES"]').click()
                master.implicitly_wait(10)

        # 验证回到了首页
        assert master.find_element_by_id("com.glazero.android:id/img_menu")
        assert master.find_element_by_id("com.glazero.android:id/img_logo")

        '''
        with allure.step('绑定失败页面'):
            assert master.find_element_by_xpath('//android.widget.TextView[@text="Connection failed"]')
            assert master.find_element_by_id('com.glazero.android:id/btn').text == 'RECONNECT'
        '''

    def test_addV8S(self):
        pass

    @allure.title('C2E 绑定-解绑')
    @allure.story('用户循环测试C2E的绑定和解绑，每次绑定间隔1个小时')
    def test_addC2E(self, ssid='11111111-5g', pwd='12345678'):
        with allure.step(
                'step1：点击右上角的+号，开始执行时间为：%s' % time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())):
            master.find_element_by_id('com.glazero.android:id/img_add_device').click()
            master.implicitly_wait(10)

        with allure.step('step2：选择C2E'):
            master.find_element_by_xpath('//android.widget.TextView[@text="P1"]').click()
            master.implicitly_wait(10)

        with allure.step('step3：弹出照相机权限后点击cancel'):
            master.find_element_by_id('com.glazero.android:id/btn_dialog_cancel').click()
            master.implicitly_wait(10)

        with allure.step('step4：点击Use other methods'):
            master.find_element_by_id('com.glazero.android:id/tv_other_way').click()
            master.implicitly_wait(10)

        with allure.step('step5：点击continue'):
            master.find_element_by_id('com.glazero.android:id/button').click()
            master.implicitly_wait(10)

        with allure.step('step6：继续点击continue'):
            master.find_element_by_id('com.glazero.android:id/button').click()
            master.implicitly_wait(10)

        with allure.step('step7：如果弹出wifi权限弹窗则给予权限'):
            if gz_public.isElementPresent(driver=master, by="id",
                                          value="com.glazero.android:id/btn_dialog_confirm") is True:
                if master.find_element_by_id('com.glazero.android:id/btn_dialog_confirm').text == 'GO SETTINGS':
                    master.find_element_by_id('com.glazero.android:id/btn_dialog_confirm').click()
                    master.implicitly_wait(10)

                if master.find_element_by_id(
                        'com.android.permissioncontroller:id/permission_allow_foreground_only_button').text == 'Allow only while using the app':
                    master.find_element_by_id(
                        'com.android.permissioncontroller:id/permission_allow_foreground_only_button').click()
                    master.implicitly_wait(10)

        with allure.step('step8：输入ssid和pwd'):
            # 先清除ssid
            master.find_elements_by_id('com.glazero.android:id/edit_text')[0].clear()
            master.implicitly_wait(10)
            # 再输入ssid
            master.find_elements_by_id('com.glazero.android:id/edit_text')[0].send_keys(ssid)
            master.implicitly_wait(10)

            # 先清除pwd
            master.find_elements_by_id('com.glazero.android:id/edit_text')[1].clear()
            master.implicitly_wait(10)
            # 再输入pwd
            master.find_elements_by_id('com.glazero.android:id/edit_text')[1].send_keys(pwd)
            master.implicitly_wait(10)

            # 点击 下一步
            master.find_element_by_id('com.glazero.android:id/next_step').click()
            master.implicitly_wait(10)

        with allure.step('step9：校验二维码页面生成成功'):
            # 二维码页面有唯一的标识：
            if gz_public.isElementPresent(driver=master, by="id",
                                          value="com.glazero.android:id/lottie_guide_scan_qr_code") is True:
                assert master.find_element_by_id('com.glazero.android:id/tv_title_string').text == 'Scan QR Code'
                # 进入二维码页面后先截图
                ts_qr = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())
                master.save_screenshot('./report/C2E/qr_code_%s.png' % ts_qr)
                time.sleep(3)

                # 将截图添加到报告中
                allure.attach.file("./report/C2E/qr_code_%s.png" % ts_qr, name="QR code",
                                   attachment_type=allure.attachment_type.JPG)
                master.implicitly_wait(10)

            # 如果二维码生成失败，点击页面中的Refresh
            if gz_public.isElementPresent(driver=master, by='id',
                                          value='com.glazero.android:id/tv_scan_code_load_retry') is True:
                master.find_element_by_id('com.glazero.android:id/tv_scan_code_load_retry').click()
                master.implicitly_wait(10)

        with allure.step(
                'step10：等待配网成功页面出现，超时时间是7分钟，每2秒检查一次页面，结束时间为：%s' % time.strftime(
                    "%Y-%m-%d %H:%M:%S", time.localtime())):
            try:
                WebDriverWait(master, timeout=420, poll_frequency=2).until(
                    lambda x: x.find_element_by_xpath('//android.widget.TextView[@text="Connected successfully"]'))
            except TimeoutException:
                logging.error('绑定失败')
                ts_fail = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())
                master.save_screenshot('./report/C2E/fail_%s.png' % ts_fail)
                time.sleep(3)
                allure.attach.file("./report/C2E/fail_%s.png" % ts_fail, name="fail",
                                   attachment_type=allure.attachment_type.JPG)
                master.implicitly_wait(10)
            else:
                logging.info('绑定成功')
                ts_success = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())
                master.save_screenshot('./report/C2E/success_%s.png' % ts_success)
                time.sleep(3)
                allure.attach.file("./report/C2E/success_%s.png" % ts_success, name="success",
                                   attachment_type=allure.attachment_type.JPG)
                master.implicitly_wait(10)

                # with allure.title('step11：绑定成功后点击 下一步'):
                # 出现后点击下一步
                master.find_element_by_id('com.glazero.android:id/btn').click()
                master.implicitly_wait(10)

                # 进入引导页面，引导页面弹出较慢，等待5秒
                time.sleep(4)
                # with allure.title('step12：关闭引导页面回到首页'):
                if gz_public.isElementPresent(driver=master, by="id",
                                              value="com.glazero.android:id/tv_title_string") is True:
                    if master.find_element_by_id('com.glazero.android:id/tv_title_string').text == 'Final Steps':
                        # 关闭引导页面
                        master.find_element_by_id('com.glazero.android:id/img_title_close').click()
                        master.implicitly_wait(10)

                        # 点击 YES
                        master.find_element_by_xpath('//android.widget.Button[@text="YES"]').click()
                        master.implicitly_wait(10)

                        # 验证回到了首页
                        time.sleep(2)
                        assert master.find_element_by_id("com.glazero.android:id/img_menu")
                        assert master.find_element_by_id("com.glazero.android:id/img_logo")

    @allure.title('C6SP基站绑定解绑')
    @allure.story('C6SP基站绑定后涂鸦状态和aosu状态不一致，涂鸦状态是离线，aosu状态是在线，等待一段时间后状态仍然不同步')
    def test_addC6SP_station(self, ssid='11111111-5g', pwd='12345678', home_base_sn='H1L2AH110000650'):
        with allure.step(
                'step1：点击右上角的+号，开始执行时间为：%s' % time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())):
            master.find_element_by_id('com.glazero.android:id/img_add_device').click()
            master.implicitly_wait(10)

        with allure.step('step2：选择c6sp套装'):
            master.find_element_by_xpath('//android.widget.TextView[@text="Max/Pro\nSystem"]').click()
            master.implicitly_wait(10)

        with allure.step('step3：弹出照相机权限后点击cancel'):
            master.find_element_by_id('com.glazero.android:id/btn_dialog_cancel').click()
            master.implicitly_wait(10)

        with allure.step('step4：点击Use other methods'):
            master.find_element_by_id('com.glazero.android:id/tv_other_way').click()
            master.implicitly_wait(10)

        with allure.step('step5：点击continue'):
            master.find_element_by_id('com.glazero.android:id/button').click()
            master.implicitly_wait(10)

        with allure.step('step6：继续点击continue'):
            master.find_element_by_id('com.glazero.android:id/button').click()
            master.implicitly_wait(10)

        with allure.step('step7：继续点击continue'):
            master.find_element_by_xpath('//android.widget.Button[@text="CONTINUE"]').click()
            master.implicitly_wait(10)

        with allure.step('step8：等待基站SN出现后，选择基站的SN'):
            try:
                WebDriverWait(master, timeout=30, poll_frequency=2).until(
                    lambda x: x.find_element_by_xpath('//android.widget.TextView[@text="%s"]' % home_base_sn))
            except TimeoutException:  # 此处不能写NoSuchElementException:
                logging.error('没有找到要绑定的基站sn: %s' % home_base_sn)
                ts_fail = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())
                master.save_screenshot('./report/C6SP/fail_%s.png' % ts_fail)
                time.sleep(3)
                allure.attach.file("./report/C6SP/fail_%s.png" % ts_fail, name="fail",
                                   attachment_type=allure.attachment_type.JPG)
                master.implicitly_wait(10)

                # 没有找到待绑定的sn可能是因为没有解绑，在这里解绑一下，保证后面步骤的运行
                gz_public._unbind(home_base_sn, 1, 1)
                time.sleep(3)
            else:
                logging.info('找到了要绑定的基站sn: %s' % home_base_sn)
                ts_success = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())
                master.save_screenshot('./report/C6SP/success_%s.png' % ts_success)
                time.sleep(3)
                allure.attach.file("./report/C6SP/success_%s.png" % ts_success, name="success",
                                   attachment_type=allure.attachment_type.JPG)
                master.implicitly_wait(10)

                # 出现后点击SN
                master.find_element_by_xpath('//android.widget.TextView[@text="%s"]' % home_base_sn).click()
                master.implicitly_wait(10)

        with allure.step('step9：跳转到Name Your HomeBase页面后，点击continue'):
            try:
                WebDriverWait(master, timeout=30, poll_frequency=2).until(
                    lambda x: x.find_element_by_id('com.glazero.android:id/subtitle'))

            except TimeoutException:
                logging.error('没有找到Name Your HomeBase这个元素')
                ts_fail = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())
                master.save_screenshot('./report/C6SP/fail_%s.png' % ts_fail)
                time.sleep(3)
                allure.attach.file("./report/C6SP/fail_%s.png" % ts_fail, name="fail",
                                   attachment_type=allure.attachment_type.JPG)
                master.implicitly_wait(10)

                # 虽然绑定失败了，解绑一下，为下一次绑定做好准备，以免提示已绑定
                gz_public._unbind(home_base_sn, 1, 1)
                time.sleep(3)
            else:
                logging.info('已经跳转到了Name Your HomeBase')
                master.find_element_by_xpath('//android.widget.Button[@text="CONTINUE"]').click()
                master.implicitly_wait(10)

        with allure.step(
                'step10：跳转到绑定成功页面，超时时间是5分钟，每2秒检查一次页面，结束时间为：%s' % time.strftime(
                    "%Y-%m-%d %H:%M:%S", time.localtime())):
            try:
                WebDriverWait(master, timeout=300, poll_frequency=2).until(
                    lambda x: x.find_element_by_id('com.glazero.android:id/subtitle'))
            except TimeoutException:
                logging.error('绑定失败')
                ts_fail = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())
                master.save_screenshot('./report/C6SP/fail_%s.png' % ts_fail)
                time.sleep(3)
                allure.attach.file("./report/C6SP/fail_%s.png" % ts_fail, name="fail",
                                   attachment_type=allure.attachment_type.JPG)
                master.implicitly_wait(10)

                # 虽然绑定失败了，解绑一下，为下一次绑定做好准备，以免提示已绑定
                gz_public._unbind(home_base_sn, 1, 1)
                time.sleep(3)
            else:
                logging.info('绑定成功')
                ts_success = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())
                master.save_screenshot('./report/C6SP/success_%s.png' % ts_success)
                time.sleep(3)
                allure.attach.file("./report/C6SP/success_%s.png" % ts_success, name="success",
                                   attachment_type=allure.attachment_type.JPG)
                master.implicitly_wait(10)

                # 点击右上角的关闭X按钮，回到首页
                master.find_element_by_id('com.glazero.android:id/img_title_close').click()
                master.implicitly_wait(10)
                gz_public.swipe_down(driver=master)
                time.sleep(3)

                ts_success = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())
                master.save_screenshot('./report/C6SP/success_%s.png' % ts_success)
                time.sleep(3)
                allure.attach.file("./report/C6SP/success_%s.png" % ts_success, name="success",
                                   attachment_type=allure.attachment_type.JPG)
                master.implicitly_wait(10)

                # 等待1分钟后再查询涂鸦状态，保证有充分的时间设备在涂鸦端上线
                time.sleep(60)

                # 绑定成功后，检查设备的涂鸦状态是否为在线，如果涂鸦端不在线，问题复现，退出pytest
                rsp = gz_public.aosu_admin_get_dev_info(home_base_sn)
                logging.info("aosu状态为：" + str(rsp.json()['data']['list'][0]['online']))
                logging.info("tuya状态为：" + str(rsp.json()['data']['list'][0]['tuyayOnline']))
                print("aosu状态为：", rsp.json()['data']['list'][0]['online'])
                print("tuya状态为：", rsp.json()['data']['list'][0]['tuyayOnline'])
                if rsp.json()['data']['list'][0]['tuyayOnline'] is False:
                    # pytest.exit('涂鸦在线，测试在这种情况下，是否执行teardown的内容   ---   结果是执行')
                    pytest.exit('绑定完成1分钟后查询涂鸦状体为离线，问题复现，终止执行pytest，请查看固件日志！')
                else:
                    # 绑定成功后，涂鸦状态为在线，那么就解绑该设备
                    gz_public._unbind(home_base_sn, 1, 1)
                    time.sleep(3)

    @staticmethod
    def teardown_class():
        master.close_app()
        master.implicitly_wait(10)


@allure.feature('用户中心模块')
class TestUserCenter(object):
    # 执行这个测试类，前提条件是要登录，登录后才能执行这组用例
    # 登录前先要启动app
    # 那么就要使用setup_class
    @staticmethod
    def setup_class():
        master.close_app()
        master.implicitly_wait(10)
        master.launch_app()
        master.implicitly_wait(10)

        # 登录状态下启动app 进入首页 activity 是：.SplashActivity，不是：.account.login.LoginActivity，所以不能通过activity判断是否在首页
        # 通过登录后首页左上角的menu图标判断
        if not gz_public.isElementPresent(driver=master, by="id", value="com.glazero.android:id/img_menu"):
            TestGzLogin.test_gzLogin(self=NotImplemented)
            master.implicitly_wait(10)

    @allure.story('修改登录密码')
    def test_changePassword(self, old_pass_word=gz_public.pwd, new_pass_word='Qwe101010'):
        with allure.step('step1：点击用户中心菜单'):
            master.find_element_by_id('com.glazero.android:id/img_menu').click()
            master.implicitly_wait(10)

        with allure.step('step2：点击 账号管理'):
            master.find_elements_by_id('com.glazero.android:id/tv_menu_item_name')[0].click()
            master.implicitly_wait(10)

        with allure.step('step3：点击 修改密码'):
            master.find_element_by_id('com.glazero.android:id/rl_reset_password_container').click()
            master.implicitly_wait(10)

        assert master.find_element_by_id('com.glazero.android:id/button').is_enabled() is False

        with allure.step('step4：点击密码输入旧密码'):
            master.find_elements_by_id('com.glazero.android:id/edit_text')[0].click()
            master.implicitly_wait(10)

            # 旧密码
            master.find_elements_by_id('com.glazero.android:id/edit_text')[0].send_keys(old_pass_word)
            master.implicitly_wait(10)

            master.hide_keyboard()

        with allure.step('step5：点击新密码输入新密码'):
            # 新密码
            master.find_elements_by_id('com.glazero.android:id/edit_text')[1].click()
            master.implicitly_wait(10)

            master.find_elements_by_id('com.glazero.android:id/edit_text')[1].send_keys(new_pass_word)
            master.implicitly_wait(10)
            master.hide_keyboard()

        with allure.step('step6：点击重新输入新密码'):
            # 确认新密码
            master.find_elements_by_id('com.glazero.android:id/edit_text')[2].click()
            master.implicitly_wait(10)

            master.find_elements_by_id('com.glazero.android:id/edit_text')[2].send_keys(new_pass_word)
            master.implicitly_wait(10)
            master.hide_keyboard()

        assert master.find_element_by_id('com.glazero.android:id/button').is_enabled() is True

        with allure.step('step7：点击 更新密码 按钮'):
            master.find_element_by_id('com.glazero.android:id/button').click()
            master.implicitly_wait(10)

        with allure.step('step8：点击 返回登录 按钮'):
            master.find_element_by_id('com.glazero.android:id/btn').click()
            master.implicitly_wait(10)

        # 改回原密码，默认_region='CN', country_code='86'，如果换区的话需要传不同的参数
        gz_public.change_password(gz_public.change_pwd_to, gz_public.pwd, gz_public.email, gz_public._type,
                                  gz_public.gzHostCnTmp)

        # 密码复原后再回到登录状态
        TestGzLogin.test_gzLogin(self, gz_public.email, gz_public.pwd)

    @allure.story('分享设备')
    def test_shareDevice(self):
        with allure.step('step1：点击用户中心菜单'):
            master.find_element_by_id('com.glazero.android:id/img_menu').click()
            master.implicitly_wait(10)

        with allure.step('step2：点击 用户分享'):
            master.find_elements_by_id('com.glazero.android:id/tv_menu_item_name')[1].click()
            master.implicitly_wait(10)

        with allure.step('step3：点击 分享设备'):
            master.find_element_by_id('com.glazero.android:id/tv_share_device').click()
            master.implicitly_wait(10)

        with allure.step('step4：选择设备，例如第一个设备'):
            master.find_elements_by_id('com.glazero.android:id/iv_device_icon')[0].click()
            master.implicitly_wait(10)

        with allure.step('分享的邮箱地址'):
            master.find_element_by_id('com.glazero.android:id/et_share_user_email').click()
            master.implicitly_wait(10)
            master.find_element_by_id('com.glazero.android:id/et_share_user_email').send_keys(gz_public.home_user)
            master.implicitly_wait(10)
            master.hide_keyboard()

        # 选中设备并填写邮箱后，页面底部按钮变成高亮可以点击
        assert master.find_element_by_id('com.glazero.android:id/btn_share').is_enabled() is True

        with allure.step('点击 分享 按钮'):
            master.find_element_by_id('com.glazero.android:id/btn_share').click()
            master.implicitly_wait(10)

        if gz_public.isElementPresent(driver=master, by="id", value="com.glazero.android:id/img_prompt_image"):
            master.find_element_by_id('com.glazero.android:id/tv_share_management').click()
            master.implicitly_wait(10)

    @allure.story('退出')
    def test_logOut(self):
        with allure.step('step1: 点击首页右上角的菜单按钮'):
            master.find_element_by_id("com.glazero.android:id/img_menu").click()
            master.implicitly_wait(10)

        # 断言 进入了个人中心菜单
        assert master.find_element_by_id("com.glazero.android:id/ivUserIcon")
        assert master.find_element_by_id("com.glazero.android:id/tvUserEmail").text == gz_public.email

        with allure.step('step2: 点击 菜单中的退出登录项'):
            master.find_elements_by_id("com.glazero.android:id/tv_menu_item_name")[7].click()
            master.implicitly_wait(10)

        with allure.step('step3: 点击 弹窗中的确认按钮'):
            master.find_element_by_id("com.glazero.android:id/btn_dialog_confirm").click()
            master.implicitly_wait(10)

        # 断言 登录页面元素，退出登录后，该页面显示登录的邮箱和地区，并且登录按钮置灰不可点击
        assert master.find_elements_by_id("com.glazero.android:id/edit_text")[0].text == gz_public.email
        master.implicitly_wait(10)
        assert gz_public.REGION in master.find_elements_by_id("com.glazero.android:id/edit_text")[2].text
        master.implicitly_wait(10)
        assert master.find_element_by_id("com.glazero.android:id/button").is_enabled() is False

    @staticmethod
    def teardown_class():
        master.close_app()
        master.implicitly_wait(10)


@allure.feature('设备列表/首页 模块')
class TestDeviceList(object):
    # 执行这个测试类，前提条件是要登录，登录后才能执行这组用例
    # 登录前先要启动app
    # 那么就要使用setup_class
    @staticmethod
    def setup_class():
        master.close_app()
        master.implicitly_wait(10)
        master.launch_app()
        master.implicitly_wait(10)

        # 登录状态下启动app 进入首页 activity 是：.SplashActivity，不是：.account.login.LoginActivity，所以不能通过activity判断是否在首页
        # 通过登录后首页左上角的menu图标判断
        if not gz_public.isElementPresent(driver=master, by="id", value="com.glazero.android:id/img_menu"):
            TestGzLogin.test_gzLogin(self=NotImplemented)
            master.implicitly_wait(10)

    @staticmethod
    def setup_method(self):
        # 检查屏幕是否点亮
        if not initPhone.InitPhone.isAwake():
            # 26 电源键
            initPhone.InitPhone.keyEventSend(26)
            time.sleep(1)

        # 在首页的话下滑刷新一下设备列表
        if gz_public.isElementPresent(driver=master, by="id", value="com.glazero.android:id/img_menu") is True:
            gz_public.swipe_down(driver=master)
            # 等待下来刷新完成
            time.sleep(3)

    @staticmethod
    def teardown_method(self):
        pass

    @allure.title('C2E校准')
    @allure.story('C2E重复校准是否会出现问题')
    def test_C2E_Calibrate(self, dev_name='IndoorCam'):
        # 在首页的话执行step1-3
        if gz_public.isElementPresent(driver=master, by="id",
                                      value="com.glazero.android:id/img_menu") is True:
            with allure.step('step1: 在设备列表中滑动找到C2E设备（默认名字是IndoorCam，可在参数中修改名字）'):
                master.find_element_by_android_uiautomator(
                    'new UiScrollable(new UiSelector().scrollable(true)).scrollIntoView(new UiSelector().text('
                    '"%s")).scrollToEnd(10,5)' % dev_name)
                master.implicitly_wait(10)

            with allure.step('step2: 点击设备名称，例如，IndoorCam'):
                master.find_element_by_xpath('//android.widget.TextView[@text="%s"]' % dev_name).click()
                master.implicitly_wait(10)
                time.sleep(3)  # 等待开流页面加载完成

            with allure.step('step3：点击Holder'):
                master.find_element_by_xpath('//android.widget.TextView[@text="Holder"]').click()
                master.implicitly_wait(10)
                time.sleep(2)  # 等待Holder菜单加载完成

        # 如果停留在校准页面，那么就直接点击校准按钮，执行step4-5
        if gz_public.isElementPresent(driver=master, by="id",
                                      value="com.glazero.android:id/btn_calibration") is True:
            with allure.step('step4：点击Calibrate'):
                master.find_element_by_xpath('//android.widget.TextView[@text="Calibrate"]').click()
                master.implicitly_wait(10)
                time.sleep(1)

                # 点击校准后，有可能会弹出提示弹窗（turn on the tracking, and the camera will follow the moving object），发现后点击“GOT
                # IT”，关闭弹窗
                if gz_public.isElementPresent(driver=master, by="id",
                                              value="com.glazero.android:id/positive_btn") is True:
                    master.find_element_by_id("com.glazero.android:id/positive_btn").click()
                    master.implicitly_wait(10)

                # 检验校准过程中的状态
                WebDriverWait(master, timeout=30, poll_frequency=1).until(lambda x: x.find_element_by_id('com.glazero'
                                                                                                         '.android:id'
                                                                                                         '/pb_calibtating'))
                # master.find_element_by_xpath('//android.widget.ProgressBar[@index=3]')
                # 添加日志
                logging.info('校准中')
                # 添加截图
                calibrating = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())
                master.save_screenshot('./report/C2E/calibrating_%s.png' % calibrating)
                time.sleep(3)
                allure.attach.file("./report/C2E/calibrating_%s.png" % calibrating, name="calibrating",
                                   attachment_type=allure.attachment_type.JPG)
                master.implicitly_wait(10)

            with allure.step('step5：等待校准完成，校准按钮变成初始状态'):
                # 等待校准过程中的图标消失
                WebDriverWait(master, timeout=50, poll_frequency=1).until_not(
                    lambda x: x.find_element_by_id('com.glazero.android:id/pb_calibtating'))
                # 添加截图
                calibrate_after = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())
                master.save_screenshot('./report/C2E/calibrate_after_%s.png' % calibrate_after)
                # 添加日志
                logging.info('校准完成')
                time.sleep(3)
                allure.attach.file("./report/C2E/calibrate_after_%s.png" % calibrate_after, name="calibrate_after",
                                   attachment_type=allure.attachment_type.JPG)
                master.implicitly_wait(10)

    @staticmethod
    def teardown_class():
        pass
        # master.close_app()
        # master.implicitly_wait(10)


@allure.feature("开流专项")
class TestOpenFlow(object):
    """
    20230424 zhang jia min
    开流专项：多次开流、长时间开流
    设备：V8S C2E
    手机：三星、moto
    前提：
    1、执行这个测试类，前提条件是要登录，登录后才能执行这组用例
    2、登录前先要启动app
    3、那么就要使用setup_class
    """
    # 在pytest中不能使用__init__(self, dev_name)方法，所以在setup_method中采用全局变量的方式获取设备名称
    @staticmethod
    def setup_class():
        master.close_app()
        master.implicitly_wait(10)
        master.launch_app()
        master.implicitly_wait(10)

        # 登录状态下启动app 进入首页 activity 是：.SplashActivity，不是：.account.login.LoginActivity，所以不能通过activity判断是否在首页
        # 通过登录后首页左上角的menu图标判断
        if not gz_public.isElementPresent(driver=master, by="id", value="com.glazero.android:id/img_menu"):
            TestGzLogin.test_gzLogin(self=NotImplemented)
            master.implicitly_wait(10)

    @staticmethod
    def setup_method(self):
        # 检查屏幕是否点亮
        if not initPhone.InitPhone.isAwake():
            # 26 电源键
            initPhone.InitPhone.keyEventSend(26)
            time.sleep(1)

        # 不在首页的话 启动一下app
        if gz_public.isElementPresent(driver=master, by="id", value="com.glazero.android:id/img_menu") is False:
            master.launch_app()
            master.wait_activity("com.glazero.android.SplashActivity", 2, 2)
            time.sleep(3)

        # 在首页的话下滑刷新一下设备列表
        if gz_public.isElementPresent(driver=master, by="id", value="com.glazero.android:id/img_menu") is True:
            gz_public.swipe_down(driver=master)
            # 等待下来刷新完成
            time.sleep(3)

    @allure.title('V8P 开流')
    @allure.story('用户循环测试V8P的开流-关流，即多次开流')
    def test_v8p_open_flow(self):
        """
        :前提条件：① 账号下要绑定V8P设备；② 关闭消息通知，不要弹push，会遮挡按钮的点击
        :设备为在线状态，可以开流
        :网络稳定，可以考虑放在屏蔽箱里执行
        :电量充足，不能关机
        :如果中间有升级弹窗出现，点击取消或忽略本次升级，其他弹窗类似
        """
        # 获取v8p设备的名字
        dev_name = gz_public.get_devices_list(model='V8P')

        with allure.step('step1: 在设备列表中滑动找到要开流的设备，例如，v8p'):
            master.find_element_by_android_uiautomator(
                'new UiScrollable(new UiSelector().scrollable(true)).scrollIntoView(new UiSelector().text('
                '"%s")).scrollToEnd(10,5)' % dev_name)
            master.implicitly_wait(10)

            # 确认找到了设备
            assert master.find_element_by_id('com.glazero.android:id/device_name').text == dev_name

        with allure.step('step2: 点击设备名称，例如，可视门铃Pro'):
            master.find_element_by_xpath('//android.widget.TextView[@text="%s"]' % dev_name).click()
            master.implicitly_wait(10)

            # 确认进入了指定设备的开流页面，页面title应为设备名称
            assert master.find_element_by_id('com.glazero.android:id/tv_title').text == dev_name

        with allure.step('step3: 进入指定设备的开流页面后开流40秒，开始时间点为：%s' % time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())):

            # 实时视频加载中… 等待3秒
            if gz_public.isElementPresent(driver=master, by="id",
                                              value="com.glazero.android:id/tv_live_play_loading") is True:
                time.sleep(3)

            # 如果出现：当前网络不可用，请检查网络连接，点击：刷新重试
            if gz_public.isElementPresent(driver=master, by="id",
                                              value="com.glazero.android:id/bt_play_retry") is True:
                master.find_element_by_id('com.glazero.android:id/bt_play_retry').click()
                master.implicitly_wait(10)

            # 开流开始后 截一张图
            start_flow = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())
            master.save_screenshot('./report/V8P/start_flow_%s.png' % start_flow)
            time.sleep(3)

            # 将截图添加到报告中
            allure.attach.file("./report/V8P/start_flow_%s.png" % start_flow, name="start flow",
                                   attachment_type=allure.attachment_type.JPG)
            master.implicitly_wait(10)

            # 开流40秒
            for ii in range(1, 3):
                # 如果出现：长时间查看实时视频会加速门铃电量消耗，是否为您退出实时视频？，点击：继续观看
                if gz_public.isElementPresent(driver=master, by="id",
                                                  value="com.glazero.android:id/liveplay_power_prompt_got_it") is True:
                    master.find_element_by_id('com.glazero.android:id/liveplay_power_prompt_got_it').click()

        with allure.step('step4：点击页面左上角的 返回，结束开流，结束时间点为：%s' % time.strftime("%Y-%m-%d %H:%M:%S",
                                                                                                    time.localtime())):
            # 开流结束时 截一张图：
            close_flow = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())
            master.save_screenshot('./report/V8P/close_flow_%s.png' % close_flow)
            time.sleep(3)

            # 将截图添加到报告中
            allure.attach.file("./report/V8P/close_flow_%s.png" % close_flow, name="close flow",
                                   attachment_type=allure.attachment_type.JPG)
            master.implicitly_wait(10)

            # 开流失败判定条件及处理：
            # ①开流40秒后如果播放器上的控件状态为不可用，即，视频质量切换、录像、截屏、静音的enabled is false；
            # ②或者开流40秒后如果app崩溃了，找不到播放器上的控件都视为开流失败；
            # ③截取app日志最新1000行、截取ty日志最新1000行，添加到allure的附件当中；
            if master.find_element_by_id("com.glazero.android:id/btn_in_video_clarity_hd").is_enabled() is False and \
                    master.find_element_by_id("com.glazero.android:id/btn_record_start").is_enabled() is False and \
                    master.find_element_by_id("com.glazero.android:id/btn_snapshot").is_enabled() is False and \
                    master.find_element_by_id("com.glazero.android:id/btn_unmute").is_enabled() is False:
                current_time = time.strftime("%Y%m%d", time.localtime())

                # 获取app日志
                gz_public.get_app_log('app', current_time, 1000)
                # 将日志添加到报告中
                allure.attach.file("./report/V8P/log_attch/app_log.log", name="app log", attachment_type=allure.attachment_type.TEXT)
                master.implicitly_wait(10)

                # 获取ty日志
                gz_public.get_app_log('ty', current_time, 1000)
                # 将日志添加到报告中
                allure.attach.file("./report/V8P/log_attch/ty_log.log", name="ty log", attachment_type=allure.attachment_type.TEXT)
                master.implicitly_wait(10)

            elif gz_public.isElementPresent(driver=master, by="id", value="com.glazero.android:id"
                                                                          "/btn_in_video_clarity_hd") is False and \
                    gz_public.isElementPresent(driver=master, by="id",
                                               value="com.glazero.android:id/btn_record_start") is False:
                current_time = time.strftime("%Y%m%d", time.localtime())
                # 获取app日志
                gz_public.get_app_log('app', current_time, 1000)
                # 获取ty日志
                gz_public.get_app_log('ty', current_time, 1000)

            # 点击左上角的 返回按钮
            master.find_element_by_id('com.glazero.android:id/btn_back').click()
            master.implicitly_wait(10)

            # 确认回到了首页
            assert master.find_element_by_id("com.glazero.android:id/img_tab_device")

    def test_addV8S(self):
        pass


if __name__ == '__main__':
    # pytest.main(["-q", "-s", "-ra", "test_gzAndroidAuto.py::TestUserCenter::test_logOut"])

    # C6SP 绑定
    # pytest.main(["-q", "-s", "-ra", "--count=%d" % 500, "test_gzAndroidAuto.py::TestAddDevices::test_addC6SP_station",
    #             "--alluredir=./report/C6SP"])

    # C2E 绑定
    # pytest.main(["-q", "-s", "-ra", "--count=%d" % 500, "test_gzAndroidAuto.py::TestAddDevices::test_addC2E",
    #              "--alluredir=./report/C2E"])

    # C2E 校准
    # pytest.main(["-q", "-s", "-ra", "--count=%d" % 1000, "test_gzAndroidAuto.py::TestDeviceList::test_C2E_Calibrate",
    #             "--alluredir=./report/C2E"])

    # V8P 开流
    pytest.main(["-q", "-s", "-ra", "--count=%d" % 500, "test_gzAndroidAuto.py::TestOpenFlow::test_v8p_open_flow",
                 "--alluredir=./report/V8P"])
