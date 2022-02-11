from appium import webdriver
import gz_public


class StartAppium:
    @staticmethod
    def start_appium():
        desired_caps = dict(
            platformName=gz_public.gzPlatformN,
            deviceName=gz_public.CONNECTTO,
            platformVersion=gz_public.PLATFORMVER,
            appPackage=gz_public.gzAppPack,
            appActivity=gz_public.gzAppActivity,
            noReset=True,  # 不重启app
            autoGrantPermissions=True,  # 安装时自动赋予权限
            newCommandTimeout=6000,
            automationName='UiAutomator2'
        )

        driver = webdriver.Remote(gz_public.gzAppiumH, desired_caps, direct_connection=True)
        driver.implicitly_wait(10)
        return driver
