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
        print('on')
    else:
        print('off')
        # 224 点亮屏幕
        keyEventSend(224)
    connectPhone()
