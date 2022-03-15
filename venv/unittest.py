import os
import re
import time
import requests
import json
from hashlib import md5
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


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
    os.system('adb kill-server')
    os.system('adb start-server')

    print(readDevicesId)
    devicesId = re.findall(r'^\w*\b', readDevicesId[1])[0]
    # print('deviceId:',devicesId)
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

def _md5(_pwd):
    password_encode = _pwd.encode('utf-8')
    password_md5 = md5(password_encode)
    password_hex = password_md5.hexdigest()
    return password_hex

def _headers():
    headers={}
    headers['Content-Type']='application/x-www-form-urlencoded'
    headers['User-Agent']='PostmanRuntime/7.29.0'
    headers['Accept']='*/*'
    headers['Accept-Encoding']='gzip, deflate, br'
    headers['Connection']='keep-alive'
    headers['Gz-Pid']='glazero'
    headers['Gz-Brand']='samsung'
    headers['Imei']='d71c95c2ea6bd816'
    headers['Gz-AppId']='com.glazero.android'
    headers['Gz-AppVer']='1.3.0.2409'
    headers['Gz-Channel']='internal'
    headers['Gz-FontSize']='1.1'
    headers['Gz-Imei']='d71c95c2ea6bd816'
    headers['Gz-Lang']='zh-Hans-CN'
    headers['Gz-Model']='SM-A515U'
    headers['Gz-NotifyPermission']='{filter=ALL, channels={%E9%97%A8%E9%93%83%E8%A2%AB%E5%BC%BA%E6%8B%86%E6%B6%88%E6%81%AF=4, %E6%8C%89%E9%97%A8%E9%93%83%E6%B6%88%E6%81%AF=4, %E4%BD%8E%E7%94%B5%E9%87%8F%E6%B6%88%E6%81%AF=4, %E9%97%A8%E9%93%83%E4%BA%8B%E4%BB%B6%E6%B6%88%E6%81%AF=4, %E5%85%B6%E4%BB%96%E6%9C%AA%E5%88%86%E7%BB%84%E6%B6%88%E6%81%AF=4, default=1}, channelGroups={default_group=false}, enabled=true, paused=false, BubblesAllowed=true}'
    headers['Gz-OsLang']=''
    headers['Gz-OsType']='android'
    headers['Gz-OsVer']='29'
    headers['Gz-Sid']=''
    headers['Gz-Timezone']='+08:00'
    headers['Gz-Uid']=''
    return headers

# 登录接口，获取sessionId，为修改密码接口提供必要的header
def _login(gz_host, _email, _region, country_code, _password, _type=1):
    global SID, UID
    url = 'https://' + gz_host + '/v1/user/login' + '?' + 'uuid=' + 'android_ui_auto' + '&' + 't=' + '001'
    data = 'countryAbbr=' + _region +'&' +'countryCode=' + country_code + '&' + 'email='+ _email + '&' + 'password=' + _password + '&' + 'type=%d'%_type
    rsp = requests.post(url, headers=_headers(), data=data, verify=False)
    rsp_json = rsp.json()
    SID = rsp.json()['data']['sid']
    UID = rsp.json()['data']['uid']

def change_password(old_pwd, new_pwd, _email, _type, gz_host, _region, country_code):
    old_pwd_md5 = _md5(old_pwd)
    new_pwd_md5 = _md5(new_pwd)
    _login(gz_host, _email, _region, country_code, old_pwd_md5, _type)
    url = 'https://' + gz_host + '/v1/user/changePassword' + '?' + 'uuid=' + 'android_ui_auto' + '&' + 't=' + '002'
    data = 'email=' + _email + '&' + 'newPassword=' + new_pwd_md5 + '&' + 'oldPassword=' + old_pwd_md5 + '&' + 'type=%d'%_type
    headers = _headers()
    headers['Gz-Sid'] = SID
    headers['Gz-Uid'] = UID
    rsp = requests.post(url, headers=headers, data=data, verify=False)
    rsp_json = rsp.json()

if __name__ == '__main__':
    # change_password('Qwe101010', 'Qwe222222', '1010642719@qq.com', 1, 'api-cn.snser.wang', 'CN', '86')

    '''
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
    '''
    # connectPhone()