from appium import webdriver


class AssertHomePage(object):
    def homePage(driver):
        assert driver.find