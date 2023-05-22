import os
import re
import time


def get_dev_id():
    cmd = 'adb devices'
    with os.popen(cmd, 'r') as f_obj:
        devs_id = f_obj.readlines()
        dev_id = re.findall(r'^\w*\b', devs_id[1])[0]
    return dev_id


def get_android_version():
    dev_id = get_dev_id()

    cmd = 'adb -s ' + dev_id + ' shell getprop ro.build.version.release'
    with os.popen(cmd, 'r') as f_obj:
        lines = f_obj.readlines()
        dev_android_ver = re.findall(r'^\w*\b', lines[0])[0]
    return dev_android_ver


def get_package_name():
    cmd = 'aapt dump badging ' + './resource/aosu_app_android_debug_1.11.18.5119_1683367354540.apk'
    with os.popen(cmd, 'r') as f_obj:
        lines = f_obj.readlines()
        app_package = re.findall(r'\'com\w*.*?\'', lines[0])[0]
        package_name = app_package[1:-1]

    return package_name


def isAppExist():
    dev_id = get_dev_id()
    package_name = get_package_name()

    cmd = 'adb -s ' + dev_id + ' shell pm list packages'
    with os.popen(cmd, 'r') as f_obj:
        exist_packages = f_obj.readlines()

    # 去掉前面的package:和后面的\n
    transform = []

    for i in exist_packages:
        transform.append(i.split(':')[1][:-1])

    if package_name in transform:
        return True
    else:
        return False


def uninstallApp():
    dev_id = get_dev_id()
    package_name = get_package_name()

    if isAppExist():
        # adb install 和 uninstall执行完成后都会返回Success
        os.system('adb -s ' + dev_id + ' uninstall ' + package_name)
        time.sleep(5)


def installApp():
    dev_id = get_dev_id()
    os.system('adb -s ' + dev_id + ' install ' + './resource/aosu_app_android_debug_1.11.18.5119_1683367354540.apk')
    time.sleep(5)


def isAwake():
    dev_id = get_dev_id()
    cmd = 'adb -s ' + dev_id + ' shell dumpsys window policy'
    screen_awake_value = '      screenState=SCREEN_STATE_ON\n'

    with os.popen(cmd, 'r') as f_obj:
        all_list = f_obj.readlines()

    if screen_awake_value in all_list:
        return True
    else:
        return False


def setScreenAlwaysOn():
    dev_id = get_dev_id()
    # 设置亮屏时间时永不锁屏 -1
    os.system('adb -s ' + dev_id + ' shell settings put system screen_off_timeout -1')

    # def initPhone(): os.system('adb shell settings put system screen_off_timeout 600000') 设置默认壁纸IDLE.png os.system(
    # 'adb push ../resource/IDLE.png /sdcard/Download/') os.system('adb shell am start -d
    # file:////sdcard/Download/IDLE.png -a android.service.wallpaper.CROP_AND_SET_WALLPAPER -f 0x1
    # com.android.launcher3/.WallpaperCropActivity') os.system('adb shell am start -a
    # android.intent.action.ATTACH_DATA -c android.intent.category.DEFAULT -d file://sdcard/Download/IDLE.png')


def keyEventSend(keycode):
    dev_id = get_dev_id()
    cmd = 'adb -s %s shell input keyevent %d' % (dev_id, keycode)
    os.system(cmd)
