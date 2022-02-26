from appium import webdriver
import gz_public


class StartAppium:
    @staticmethod
    def start_appium():
        desired_caps = dict(
            deviceName=gz_public.CONNECTTO,
            platformName=gz_public.gzPlatformN,
            platformVersion=gz_public.PLATFORMVER,
            appPackage=gz_public.gzAppPack,
            appActivity=gz_public.gzAppActivity,
            noReset=True,  # 如果是False的话是卸载再重装app，所以一定要指定是True
            autoGrantPermissions=True,  # 安装时自动赋予权限
            newCommandTimeout=6000,
            automationName='UiAutomator2'
        )

        driver = webdriver.Remote(gz_public.gzAppiumH, desired_caps, direct_connection=True)
        driver.implicitly_wait(10)
        return driver
