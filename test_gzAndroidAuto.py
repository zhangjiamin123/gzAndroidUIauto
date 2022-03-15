"""
----------------------------------
@Author: Zhang jia min
@Version: 1.0
@Date: 20220130
----------------------------------
"""
from appium.webdriver.connectiontype import ConnectionType
from gz_start_appium import StartAppium
import gz_public
import initPhone
import pytest
import allure
import time


def setup_module():
    global driver
    driver = StartAppium.start_appium()
    driver.implicitly_wait(10)

    # 当前没有网络连接，设置wifi连接
    if driver.network_connection == 0:
        driver.set_network_connection(ConnectionType.WIFI_ONLY)

    # 检查屏幕是否点亮
    if not initPhone.InitPhone.isAwake():
        # 26 电源键
        initPhone.InitPhone.keyEventSend(26)
        # 82 解锁键
        initPhone.InitPhone.keyEventSend(82)
        # 1
        initPhone.InitPhone.keyEventSend(8)
        # 2
        initPhone.InitPhone.keyEventSend(9)
        # 3
        initPhone.InitPhone.keyEventSend(10)
        # 4
        initPhone.InitPhone.keyEventSend(11)
        # 回车键
        initPhone.InitPhone.keyEventSend(66)
        # 回到桌面
        initPhone.InitPhone.keyEventSend(3)

    # 已安装aosu 先卸载
    if initPhone.InitPhone.isAppExist():
        initPhone.InitPhone.uninstallApp()

    # 安装aosu app
    initPhone.InitPhone.installApp()


def teardown_module():
    driver.quit()


@allure.feature('登录模块')
class TestGzLogin(object):
    @staticmethod
    def setup_method():
        if driver.current_activity != ".SplashActivity":
            driver.launch_app()
            driver.wait_activity("com.glazero.android.SplashActivity", 2, 2)

    @allure.story('用户名和密码输入框右侧的关闭按钮和显示/隐藏按钮')
    def test_gzLoginClearShowHide(self):
        with allure.step('step1: 在splash页，点击 登录 按钮'):
            driver.find_element_by_id("com.glazero.android:id/splash_login").click()
            driver.implicitly_wait(10)

        with allure.step('step2: 输入用户名'):
            driver.find_elements_by_id("com.glazero.android:id/edit_text")[0].clear()
            driver.implicitly_wait(10)
            driver.find_elements_by_id("com.glazero.android:id/edit_text")[0].click()
            driver.implicitly_wait(10)
            inputText = gz_public.randomEmail()
            driver.find_elements_by_id("com.glazero.android:id/edit_text")[0].send_keys(inputText)
            driver.implicitly_wait(10)

        # 不能隐藏键盘，因为键盘收起后输入框带有默认的提示文案，例如，邮箱地址
        # 验证输入的内容正确
        assert driver.find_elements_by_id("com.glazero.android:id/edit_text")[0].text == inputText

        with allure.step('step3: 点击 用户名输入框 右侧的清除按钮‘X’'):
            driver.find_element_by_id("com.glazero.android:id/img_delete").click()
            driver.implicitly_wait(10)

        # 验证 清除后的输入框为空
        assert driver.find_element_by_id("com.glazero.android:id/textinput_placeholder").text == ''

        with allure.step('step4: 输入密码'):
            driver.find_elements_by_id("com.glazero.android:id/edit_text")[1].clear()
            driver.implicitly_wait(10)
            driver.find_elements_by_id("com.glazero.android:id/edit_text")[1].click()
            driver.implicitly_wait(10)
            randomText = inputText.split('@')[0]
            driver.find_elements_by_id("com.glazero.android:id/edit_text")[1].send_keys(randomText)
            driver.implicitly_wait(10)

        # 不能隐藏键盘，因为键盘收起后输入框带有默认的提示文案，例如，密码
        # 验证输入的内容正确
        assert driver.find_elements_by_id("com.glazero.android:id/edit_text")[1].text == randomText

        with allure.step('step5: 点击 密码输入框 右侧的显示按钮'):
            driver.find_element_by_id("com.glazero.android:id/img_pwd_visible").click()
            driver.implicitly_wait(10)

        # 验证输入的内容正确，因为点击两个按钮后没有变化，所以暂时先这样断言，后续跟开发沟通，区分一下这两个按钮
        assert driver.find_elements_by_id("com.glazero.android:id/edit_text")[1].text == randomText

        with allure.step('step6: 点击 密码输入框 右侧的清除按钮‘X’'):
            driver.find_element_by_id("com.glazero.android:id/img_delete").click()
            driver.implicitly_wait(10)

        # 验证 清除后的输入框为空
        assert driver.find_element_by_id("com.glazero.android:id/textinput_placeholder").text == ''

        # 隐藏键盘
        driver.hide_keyboard()

        # 点击 右上角的关闭按钮
        driver.find_element_by_id("com.glazero.android:id/img_title_close").click()
        driver.implicitly_wait(10)

        # 回到 splash页面，断言登录和创建账号按钮（不断言文本，因为跟语言变化）
        assert driver.find_element_by_id("com.glazero.android:id/splash_login")
        assert driver.find_element_by_id("com.glazero.android:id/splash_create_account")

    @allure.story('输入用户名和密码登录aosu app')
    def test_gzLogin(self, user_name=gz_public.email, pass_word=gz_public.pwd, region=gz_public.REGION):
        with allure.step('step1：在splash页，点击 登录 按钮'):
            driver.find_element_by_id("com.glazero.android:id/splash_login").click()
            driver.implicitly_wait(10)

        with allure.step('step2：输入用户名'):
            driver.find_elements_by_id("com.glazero.android:id/edit_text")[0].clear()
            driver.implicitly_wait(10)
            driver.find_elements_by_id("com.glazero.android:id/edit_text")[0].click()
            driver.implicitly_wait(10)
            driver.find_elements_by_id("com.glazero.android:id/edit_text")[0].send_keys(user_name)

        # 输入完成后隐藏键盘
        driver.hide_keyboard()

        with allure.step('step3: 输入密码'):
            driver.find_elements_by_id("com.glazero.android:id/edit_text")[1].clear()
            driver.implicitly_wait(10)
            driver.find_elements_by_id("com.glazero.android:id/edit_text")[1].click()
            driver.implicitly_wait(10)
            driver.find_elements_by_id("com.glazero.android:id/edit_text")[1].send_keys(pass_word)

        # 输入完成后隐藏键盘
        driver.hide_keyboard()

        with allure.step('step4：选择地区'):
            driver.find_elements_by_id("com.glazero.android:id/edit_text")[2].click()
            driver.implicitly_wait(10)
            driver.find_element_by_android_uiautomator(
                'new UiScrollable(new UiSelector().scrollable(true)).scrollIntoView(new UiSelector().text("%s"))' % region)
            driver.implicitly_wait(10)
            driver.find_element_by_xpath(
                '//android.widget.TextView[@text="%s"]' % region).click()  # 此时只能写类名
            driver.implicitly_wait(10)
        # 点击登录按钮之前截图
        time.sleep(3)
        driver.save_screenshot('./report/login.png')
        driver.implicitly_wait(10)

        with allure.step('step5：点击 登录 按钮'):
            allure.attach.file("./report/login.png", name="登录页面", attachment_type=allure.attachment_type.JPG)
            driver.find_element_by_id("com.glazero.android:id/button").click()
            driver.implicitly_wait(10)

        # 点击登录按钮之后即进入首页后截图截图
        time.sleep(5)
        driver.save_screenshot('./report/homePage.png')
        driver.implicitly_wait(10)

        with allure.step('step6: 登录成功'):
            allure.attach.file("./report/homePage.png", name="登陆成功 进入首页", attachment_type=allure.attachment_type.JPG)

        # 断言是否进入首页，关键元素是：菜单按钮、logo、添加设备按钮、设备tab、回放tab、在线客服tab
        assert driver.current_activity in (".main.MainActivity", ".account.login.LoginActivity")
        assert driver.find_element_by_id("com.glazero.android:id/img_menu")
        assert driver.find_element_by_id("com.glazero.android:id/img_logo")
        assert driver.find_element_by_id("com.glazero.android:id/img_add_device")
        assert driver.find_element_by_id("com.glazero.android:id/img_tab_device")
        assert driver.find_elements_by_id("com.glazero.android:id/img_tab_playback")
        assert driver.find_element_by_id("com.glazero.android:id/img_tab_service")

    @staticmethod
    def teardown_method():
        driver.close_app()
        driver.implicitly_wait(10)


@allure.feature('用户中心模块')
class TestUserCenter(object):
    # 执行这个测试类，前提条件是要登录，登录后才能执行这组用例
    # 登录前先要启动app
    # 那么就要使用setup_class
    @staticmethod
    def setup_class():
        driver.close_app()
        driver.implicitly_wait(10)
        driver.launch_app()
        driver.implicitly_wait(10)

        # 登录状态下启动app 进入首页 activity 是：.SplashActivity，不是：.account.login.LoginActivity，所以不能通过activity判断是否在首页
        # 通过登录后首页左上角的menu图标判断
        if not gz_public.isElementPresent(driver=driver, by="id", value="com.glazero.android:id/img_menu"):
            TestGzLogin.test_gzLogin(self=NotImplemented)
            driver.implicitly_wait(10)

    @allure.story('修改登录密码')
    def test_changePassword(self, old_pass_word=gz_public.pwd, new_pass_word='Qwe101010'):
        with allure.step('step1：点击用户中心菜单'):
            driver.find_element_by_id('com.glazero.android:id/img_menu').click()
            driver.implicitly_wait(10)

        with allure.step('step2：点击 账号管理'):
            driver.find_elements_by_id('com.glazero.android:id/tv_menu_item_name')[0].click()
            driver.implicitly_wait(10)

        with allure.step('step3：点击 修改密码'):
            driver.find_element_by_id('com.glazero.android:id/rl_reset_password_container').click()
            driver.implicitly_wait(10)

        assert driver.find_element_by_id('com.glazero.android:id/button').is_enabled() is False

        with allure.step('step4：点击密码输入旧密码'):
            driver.find_elements_by_id('com.glazero.android:id/edit_text')[0].click()
            driver.implicitly_wait(10)

            # 旧密码
            driver.find_elements_by_id('com.glazero.android:id/edit_text')[0].send_keys(old_pass_word)
            driver.implicitly_wait(10)

            driver.hide_keyboard()

        with allure.step('step5：点击新密码输入新密码'):
            # 新密码
            driver.find_elements_by_id('com.glazero.android:id/edit_text')[1].click()
            driver.implicitly_wait(10)

            driver.find_elements_by_id('com.glazero.android:id/edit_text')[1].send_keys(new_pass_word)
            driver.implicitly_wait(10)
            driver.hide_keyboard()

        with allure.step('step6：点击重新输入新密码'):
            # 确认新密码
            driver.find_elements_by_id('com.glazero.android:id/edit_text')[2].click()
            driver.implicitly_wait(10)

            driver.find_elements_by_id('com.glazero.android:id/edit_text')[2].send_keys(new_pass_word)
            driver.implicitly_wait(10)
            driver.hide_keyboard()

        assert driver.find_element_by_id('com.glazero.android:id/button').is_enabled() is True

        with allure.step('step7：点击 更新密码 按钮'):
            driver.find_element_by_id('com.glazero.android:id/button').click()
            driver.implicitly_wait(10)

        with allure.step('step8：点击 返回登录 按钮'):
            driver.find_element_by_id('com.glazero.android:id/btn').click()
            driver.implicitly_wait(10)

        # 改回原密码
        gz_public.change_password('Qwe101010', 'Qwe222222', '1010642719@qq.com', 1, 'api-cn.snser.wang', 'CN', '86')

        # 密码复原后再回到登录状态
        TestGzLogin.test_gzLogin(self, gz_public.email, gz_public.pwd)

    @allure.story('退出')
    def test_logOut(self):
        with allure.step('step1: 点击首页右上角的菜单按钮'):
            driver.find_element_by_id("com.glazero.android:id/img_menu").click()
            driver.implicitly_wait(10)

        # 断言 进入了个人中心菜单
        assert driver.find_element_by_id("com.glazero.android:id/ivUserIcon")
        assert driver.find_element_by_id("com.glazero.android:id/tvUserEmail").text == gz_public.email

        with allure.step('step2: 点击 菜单中的退出登录项'):
            driver.find_elements_by_id("com.glazero.android:id/tv_menu_item_name")[7].click()
            driver.implicitly_wait(10)

        with allure.step('step3: 点击 弹窗中的确认按钮'):
            driver.find_element_by_id("com.glazero.android:id/btn_dialog_confirm").click()
            driver.implicitly_wait(10)

        # 断言 登录页面元素，退出登录后，该页面显示登录的邮箱和地区，并且登录按钮置灰不可点击
        assert driver.find_elements_by_id("com.glazero.android:id/edit_text")[0].text == gz_public.email
        driver.implicitly_wait(10)
        assert gz_public.REGION in driver.find_elements_by_id("com.glazero.android:id/edit_text")[2].text
        driver.implicitly_wait(10)
        assert driver.find_element_by_id("com.glazero.android:id/button").is_enabled() is False

    @staticmethod
    def teardown_class():
        driver.close_app()
        driver.implicitly_wait(10)


if __name__ == '__main__':
    # pytest.main(["-q", "-s", "-ra", "test_gzAndroidAuto.py::TestUserCenter::test_logOut"])
    pytest.main(["-q", "-s", "-ra", "test_gzAndroidAuto.py", "--alluredir=./report"])
