import os
import re
import time


class InitPhone(object):
    @staticmethod
    def getDeviceId():
        global deviceId
        readDevicesId = list(os.popen('adb devices').readlines())
        deviceId = re.findall(r'^\w*\b', readDevicesId[1])[0]
        return deviceId

    @staticmethod
    def getAndroidVersion():
        devicesAndroidVersion = list(
            os.popen('adb -s ' + deviceId + ' shell getprop ro.build.version.release').readlines())
        androidVersion = re.findall(r'^\w*\b', devicesAndroidVersion[0])[0]
        return androidVersion

    @staticmethod
    def getPackageName():
        global packageName
        appPackageName = list(
            os.popen('aapt dump badging ' + './resource/gz-app-debug-1.3.0.2331-1645585404086.apk').readlines())
        appPackage = re.findall(r'\'com\w*.*?\'', appPackageName[0])[0]
        packageName = appPackage[1:-1]
        return packageName

    @staticmethod
    def isAppExist():
        existPackages = list(os.popen('adb -s ' + deviceId + ' shell pm list packages').readlines())
        # 去掉前面的package:和后面的\n
        transform = []

        for i in existPackages:
            transform.append(i.split(':')[1][:-1])

        if packageName in transform:
            return True
        else:
            return False

    @staticmethod
    def uninstallApp():
        if InitPhone.isAppExist():
            # adb install 和 uninstall执行完成后都会返回Success
            os.system('adb -s ' + deviceId + ' uninstall ' + packageName)
            time.sleep(5)

    @staticmethod
    def installApp():
        os.system('adb -s ' + deviceId + ' install ' + './resource/gz-app-debug-1.3.0.2331-1645585404086.apk')
        time.sleep(5)

    @staticmethod
    def isAwake():
        cmd = 'adb -s ' + deviceId + ' shell dumpsys window policy'
        screenAwakeValue = '      screenState=SCREEN_STATE_ON\n'
        allList = os.popen(cmd).readlines()
        if screenAwakeValue in allList:
            return True
        else:
            return False

    @staticmethod
    def setScreenAlwaysOn():
        # 设置亮屏时间时永不锁屏 -1
        os.system('adb -s ' + deviceId + ' shell settings put system screen_off_timeout -1')

    # def initPhone(): os.system('adb shell settings put system screen_off_timeout 600000') 设置默认壁纸IDLE.png os.system(
    # 'adb push ../resource/IDLE.png /sdcard/Download/') os.system('adb shell am start -d
    # file:////sdcard/Download/IDLE.png -a android.service.wallpaper.CROP_AND_SET_WALLPAPER -f 0x1
    # com.android.launcher3/.WallpaperCropActivity') os.system('adb shell am start -a
    # android.intent.action.ATTACH_DATA -c android.intent.category.DEFAULT -d file://sdcard/Download/IDLE.png')

    @staticmethod
    def keyEventSend(keycode):
        cmd = 'adb -s %s shell input keyevent %d' % (deviceId, keycode)
        os.system(cmd)
