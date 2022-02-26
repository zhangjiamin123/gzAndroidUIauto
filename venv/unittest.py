import os
import re
import time

def isAwake(deviceId = ''):
    if deviceId == '':
        cmd = 'adb shell dumpsys window policy'
    else:
        cmd = 'adb shell' + deviceId + 'dumsys window policy'
    # screenAwakeValue = 'mAwake=true\n'
    screenAwakeValue = '      screenState=SCREEN_STATE_ON\n'
    allList = os.popen(cmd).readlines()
    print(allList)
    if screenAwakeValue in allList:
        return True
    else:
        return False

def isAwakeAnother(deviceId = ''):
    cmd = 'adb shell dumpsys window policy | grep mAwake'
    print(os.system(cmd))

def initPhone():
    # 设置亮屏时间时永不锁屏 -1
    os.system('adb shell settings put system screen_off_timeout 600000')
    # 设置默认壁纸IDLE.png
    #os.system('adb push ../resource/IDLE.png /sdcard/Download/')
    # os.system('adb shell am start -d file:////sdcard/Download/IDLE.png -a android.service.wallpaper.CROP_AND_SET_WALLPAPER -f 0x1 com.android.launcher3/.WallpaperCropActivity')
    os.system('adb shell am start -a android.intent.action.ATTACH_DATA -c android.intent.category.DEFAULT -d file://sdcard/Download/IDLE.png')

def connectPhone():
    readDevicesId = list(os.popen('adb devices').readlines())
    devicesId = re.findall(r'^\w*\b', readDevicesId[1])[0]
    print('deviceId:',devicesId)
    devicesAndroidVersion = list(os.popen('adb shell getprop ro.build.version.release').readlines())
    androidVersion = re.findall(r'^\w*\b', devicesAndroidVersion[0])[0]
    print('androidVersion:', androidVersion)
    appPackageName = list(os.popen('aapt dump badging ' + '../resource/gz-app-debug-1.3.0.2331-1645585404086.apk').readlines())
    appPackage = re.findall(r'\'com\w*.*?\'', appPackageName[0])[0]
    print('appPackage:', appPackage[1:-1])
    existPackages = list(os.popen('adb shell pm list packages').readlines())

    # 去掉前面的package:和后面的\n
    transform = []
    for i in existPackages:
        transform.append(i.split(':')[1][:-1])

    if appPackage[1:-1] in transform:
        print('app exist, begin uninstall')
        # adb install 和 uninstall执行完成后都会返回Success
        os.system('adb uninstall ' + appPackage[1:-1])
        time.sleep(5)

    print('start isntall')
    os.system('adb install ' + '../resource/gz-app-debug-1.3.0.2331-1645585404086.apk')


def keyEventSend(keycode):
    cmd = 'adb shell input keyevent %d'%keycode
    os.system(cmd)

if __name__ == '__main__':
    if isAwake() == True:
        print('screen is on')
    else:
        print('screen is off')
        # 224 点亮屏幕
        keyEventSend(26)
        keyEventSend(82)
        # 1
        keyEventSend(8)
        # 2
        keyEventSend(9)
        # 3
        keyEventSend(10)
        # 4
        keyEventSend(11)
        # 回车键
        keyEventSend(66)

    # 回到桌面
    # keyEventSend(3)
    # initPhone()
    # isAwakeAnother()
    # connectPhone()
