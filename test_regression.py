"""
----------------------------------
@Author: Zhang jia min
@Version: 1.0
@Date: 20230517
@desc: 回归用例
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

for device in devices:
    tmp = get_dsc(device=device)
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
    if not initPhone.isAwake():
        # 26 电源键
        initPhone.keyEventSend(26)
        # 82 解锁键 去掉密码后可以注释掉下面的code
        # initPhone.keyEventSend(82)
        # 1
        # initPhone.keyEventSend(8)
        # 2
        # initPhone.keyEventSend(9)
        # 3
        # initPhone.keyEventSend(10)
        # 4
        # initPhone.keyEventSend(11)
        # 回车键
        # initPhone.keyEventSend(66)
        # 回到桌面
        initPhone.keyEventSend(3)

    # 已安装aosu 先卸载
    if initPhone.isAppExist():
        initPhone.uninstallApp()

    # 安装aosu app
    initPhone.installApp()


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

            # 断言进入了登录页面
            assert master.find_element_by_id("com.glazero.android:id/tv_title_string").text == "登录"

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

        with allure.step('step7: 返回到splash页面'):
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
            # master.find_elements_by_class_name("android.widget.ImageView")[0].click()
            master.find_element_by_class_name("android.widget.ImageView").click()
            master.implicitly_wait(1)

        with allure.step('step1：在splash页，点击 登录 按钮'):
            master.find_element_by_id("com.glazero.android:id/splash_login").click()
            master.implicitly_wait(10)

            # 断言进入了登录页面
            assert master.find_element_by_id("com.glazero.android:id/tv_title_string").text == "登录"

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
            '''
            # 如果默认是指定的地区，那么就直接点击登录
            if master.find_elements_by_id("com.glazero.android:id/edit_text")[2].text[-3:] == region:
                time.sleep(1)
            else:
                # 如果默认不是指定的地区，那么就在地区列表中选择
            '''
            # 在回归用例中不能直接点击登录按钮，要走一遍地区选择过程
            master.find_elements_by_id("com.glazero.android:id/edit_text")[2].click()
            master.implicitly_wait(10)
            master.find_element_by_android_uiautomator(
                'new UiScrollable(new UiSelector().scrollable(true)).scrollIntoView(new UiSelector().text("%s"))' % region)
            master.implicitly_wait(10)
            master.find_element_by_xpath(
                '//android.widget.TextView[@text="%s"]' % region).click()  # 此时只能写类名
            master.implicitly_wait(10)
            time.sleep(1)

        with allure.step('step5：点击 登录 按钮'):
            # 点击登录按钮之前截图
            ts = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())
            master.save_screenshot('./report/regression/login_%s.png' % ts)
            time.sleep(3)

            allure.attach.file("./report/regression/login_%s.png" % ts, name="登录页面",
                               attachment_type=allure.attachment_type.JPG)
            master.implicitly_wait(10)

            master.find_element_by_id("com.glazero.android:id/button").click()
            master.implicitly_wait(10)

        with allure.step('step6: 登录成功'):
            # 点击登录按钮之后即进入首页后截图截图
            time.sleep(5)
            master.save_screenshot('./report/regression/homePage.png')
            time.sleep(3)

            allure.attach.file("./report/regression/homePage.png", name="登陆成功 进入首页",
                               attachment_type=allure.attachment_type.JPG)
            master.implicitly_wait(10)

            # 登录后进入首页，有可能会弹出低电量的弹窗，发现后点击“知道了”关闭弹窗
            while gz_public.isElementPresent(driver=master, by="id",
                                             value="com.glazero.android:id/btn_dialog_confirm") is True:
                master.find_element_by_id("com.glazero.android:id/btn_dialog_confirm").click()
                master.implicitly_wait(10)

            # 出现固件升级弹窗后，点击 取消/忽略此版本，多个弹窗的话，点击多次
            while gz_public.isElementPresent(driver=master, by="id",
                                             value="com.glazero.android:id/inner_layout_ota_prompt") is True:
                master.find_elements_by_id("com.glazero.android:id/button")[1].click()
                master.implicitly_wait(10)

            # 如果出现智能提醒，点击：知道了
            while gz_public.isElementPresent(driver=master, by="id",
                                             value="com.glazero.android:id/smart_warn_iv_top_icon") is True:
                master.find_element_by_id("com.glazero.android:id/button").click()
                master.implicitly_wait(10)

            """
            if gz_public.isElementPresent(driver=master, by="id",
                                          value="com.glazero.android:id/inner_layout_ota_prompt") is True:
                master.find_element_by_xpath('//android.widget.Button[@text="忽略此版本"]').click()
                master.implicitly_wait(10)
            """
            time.sleep(3)

            # 没有设备的情况下启动app后会进入select model页面，兼容该页面，点击返回<，回到首页
            if gz_public.isElementPresent(driver=master, by="id",
                                          value="com.glazero.android:id/tv_title_string") is True:
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
            assert master.find_element_by_id("com.glazero.android:id/img_tab_playback")
            assert master.find_element_by_id("com.glazero.android:id/img_tab_service")


'''
    @staticmethod
    def teardown_method():
        master.close_app()
        master.implicitly_wait(10)
'''


@allure.feature('用户中心模块')
class TestUserCenter(object):
    # 执行这个测试类，前提条件是要登录，登录后才能执行这组用例
    # 登录前先要启动app
    # 那么就要使用setup_class
    @staticmethod
    def setup_class():
        """
        master.close_app()
        master.implicitly_wait(10)
        master.launch_app()
        master.implicitly_wait(10)
        """
        """
        # 如果app没有启动，那么启动app
        if master.current_activity != ".SplashActivity":
            master.launch_app()
            master.wait_activity("com.glazero.android.SplashActivity", 2, 2)
        """
        # 登录状态下启动app 进入首页 activity 是：.SplashActivity，不是：.account.login.LoginActivity，所以不能通过activity判断是否在首页
        # 通过登录后首页左上角的menu图标判断
        if gz_public.isElementPresent(driver=master, by="id", value="com.glazero.android:id/img_menu") is False:
            TestGzLogin.test_gzLogin(self=NotImplemented)
            master.implicitly_wait(10)

    @staticmethod
    def setup_method():
        """
        # 如果崩了就再启动app
        if master.current_activity != ".SplashActivity":
            master.launch_app()
            master.wait_activity("com.glazero.android.SplashActivity", 2, 2)
        """
        # 如果不在首页就按手机的返回键，直到回到首页
        while gz_public.isElementPresent(driver=master, by="id",
                                         value="com.glazero.android:id/img_menu") is False:
            initPhone.keyEventSend(4)
            time.sleep(2)

    @allure.story('修改登录密码')
    def test_changePassword(self, old_pass_word=gz_public.pwd, new_pass_word='Qwe101010'):
        with allure.step('step1：点击用户中心菜单'):
            master.find_element_by_id('com.glazero.android:id/img_menu').click()
            master.implicitly_wait(10)

        with allure.step('step2：点击 账号管理'):
            # 使用下标的时候第一个元素容易点错
            # master.find_elements_by_id('com.glazero.android:id/tv_menu_item_name')[0].click()
            master.find_element_by_xpath('//android.widget.TextView[@text="账号管理"]').click()  # 此时只能写类名
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

    @allure.story('云录')
    def test_cloud(self):
        with allure.step('step1: 点击首页右上角的菜单按钮'):
            master.find_element_by_id("com.glazero.android:id/img_menu").click()
            master.implicitly_wait(10)

            # 断言 进入了个人中心菜单
            assert master.find_element_by_id("com.glazero.android:id/ivUserIcon").is_enabled() is True
            assert master.find_element_by_id("com.glazero.android:id/tvUserEmail").text == gz_public.email

        with allure.step('step2: 点击菜单中的 云录 项'):
            master.find_elements_by_id("com.glazero.android:id/tv_menu_item_name")[2].click()
            master.implicitly_wait(10)

            # 如果是新用户，跳到介绍页面，断言右上角是云录入口，展示云存介绍页面，展示 立即开通 按钮
            if gz_public.get_user_type() == 1:
                assert master.find_element_by_id("com.glazero.android:id/img_buy_cloud").is_enabled() is True
                assert master.find_element_by_id(
                    "com.glazero.android:id/iv_cloud_equity_details_1").is_enabled() is True
                assert master.find_element_by_id("com.glazero.android:id/btn_buy_cloud").is_enabled() is True

                with allure.step('step3: 点击右上角的云录入口，进入云存商城页面'):
                    master.find_element_by_id("com.glazero.android:id/btn_buy_cloud").click()
                    master.implicitly_wait(10)

                    assert master.find_element_by_id("com.glazero.android:id/hy_toolbar_title").text == '云存储'
                    assert master.find_element_by_id("com.glazero.android:id/hy_sub_title").text == '订单'

                with allure.step('step4: 返回到首页'):
                    initPhone.keyEventSend(4)
                    time.sleep(1)

                    initPhone.keyEventSend(4)
                    time.sleep(1)

                    initPhone.keyEventSend(4)
                    time.sleep(1)

                    # 断言回到首页
                    assert master.find_element_by_id("com.glazero.android:id/img_menu")

            # 如果是老用户，跳到云存商城页面，断言标题为：云存储，右上角是：订单 按钮
            if gz_public.get_user_type() == 2:
                assert master.find_element_by_id("com.glazero.android:id/hy_toolbar_title").text == '云存储'
                assert master.find_element_by_id("com.glazero.android:id/hy_sub_title").text == '订单'

                with allure.step('step3: 返回到首页'):
                    initPhone.keyEventSend(4)
                    time.sleep(1)

                    # 断言回到首页
                    assert master.find_element_by_id("com.glazero.android:id/img_menu")

    @allure.story('退出')
    def test_logOut(self):
        with allure.step('step1: 点击首页右上角的菜单按钮'):
            master.find_element_by_id("com.glazero.android:id/img_menu").click()
            master.implicitly_wait(10)

            # 断言 进入了个人中心菜单
            assert master.find_element_by_id("com.glazero.android:id/ivUserIcon")
            assert master.find_element_by_id("com.glazero.android:id/tvUserEmail").text == gz_public.email

        with allure.step('step2: 点击 菜单中的退出登录项'):
            master.find_elements_by_id("com.glazero.android:id/tv_menu_item_name")[8].click()
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

    # V8P 多次开流
    # pytest.main(["-q", "-s", "-ra", "--count=%d" % 500, "test_gzAndroidAuto.py::TestOpenFlow::test_v8p_open_flow",
    #              "--alluredir=./report/V8P"])

    # V8P 长时间开流
    # pytest.main(["-q", "-s", "-ra", "--count=%d" % 1, "test_gzAndroidAuto.py::TestOpenFlow"
    #                                                   "::test_v8p_open_flow_long_time", "--alluredir=./report/V8P"])
    # 执行回归用例
    pytest.main(["-q", "-s", "-ra", "--count=%d" % 1, "test_regression.py", "--alluredir=./report/regression"])
