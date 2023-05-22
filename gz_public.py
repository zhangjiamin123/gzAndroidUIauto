import random
import os
import re
import yaml
import initPhone
import requests
import logging
import json
import uuid
from hashlib import md5
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# 远程Appium服务地址
# gzAppiumH = "http://10.10.1.123:4723/wd/hub"
gzAppiumH = "http://127.0.0.1:4723/wd/hub"

# gzHostCnTmp = 'api-cn.snser.wang'
gzHostCnTmp = 'api-cn.aosulife.com'

# 手机系统
gzPlatformN = "Android"

# 包信息
gzAppPack = initPhone.get_package_name()
gzAppActivity = "com.glazero.android.SplashActivity"

# 登录账号
email = "1010642719@qq.com"
pwd = "Qwe222222"

home_user = 'enoch@glazero.com'
home_user_pwd = 'Qwe123456'

# 修改后的密码
change_pwd_to = 'Qwe101010'

# 业务类型，默认是1
_type = 1

# 手机列表
gzPhoneList = [
    # {'gzDeviceMode': "samsungA51", 'gzDeviceN': "10.10.1.157:5555", 'gzPlatformVer': "10"},
    {'gzDeviceMode': "samsungA51", 'gzDeviceN': "R58N828LKMP", 'gzPlatformVer': "10"},
    {'gzDeviceMode': "samsungS10e", 'gzDeviceN': "10.10.1.20:5555", 'gzPlatformVer': "11"}
]

# 业务参数
gzRegionList = [
    {'CN': "中国区", 'region': "中国", 'code': "+86"},
    {'US': "美国区", 'region': "美国", 'code': "+1"}
]

# default 默认连接三星A51 中国区
# CONNECTTO = gzPhoneList[0]['gzDeviceN']
CONNECTTO = initPhone.get_dev_id()
# PLATFORMVER = gzPhoneList[0]['gzPlatformVer']
PLATFORMVER = initPhone.get_android_version()
REGION = gzRegionList[0]['code']


# 生成随机邮箱
def randomEmail():
    metaData = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    emailType = ['@qq.com', '@163.com', '@outlook.com', '@glazero.com']
    emailLength = random.randint(4, 10)
    emailPrefox = "".join(random.choice(metaData) for i in range(emailLength))
    emailSuffix = random.choice(emailType)
    email = emailPrefox + emailSuffix
    return email


# 判断元素是否存在
def isElementPresent(driver, by, value):
    try:
        driver.find_element(by=by, value=value)
    except Exception as e:
        # 打印异常信息
        print(e)
        # 发生异常，表示页面中没有该元素
        return False
    else:
        # 没有发生异常，表示页面存在该元素
        return True


# 获取屏幕尺寸
def get_page_size(driver):
    x = driver.get_window_size()['width']
    y = driver.get_window_size()['height']
    return x, y


# 下拉刷新
def swipe_down(driver):
    s = get_page_size(driver)
    sx = s[0] * 0.50
    sy = s[1] * 0.33
    ex = s[0] * 0.50
    ey = s[1] * 0.75
    driver.swipe(sx, sy, ex, ey)


def _md5(_pwd):
    password_encode = _pwd.encode('utf-8')
    password_md5 = md5(password_encode)
    password_hex = password_md5.hexdigest()
    return password_hex


def _headers():
    headers = {}
    headers['Content-Type'] = 'application/x-www-form-urlencoded'
    headers['User-Agent'] = 'PostmanRuntime/7.29.0'
    headers['Accept'] = '*/*'
    headers['Accept-Encoding'] = 'gzip, deflate, br'
    headers['Connection'] = 'keep-alive'
    headers['Gz-Pid'] = 'glazero'
    headers['Gz-Brand'] = 'samsung'
    headers['Imei'] = 'd71c95c2ea6bd816'
    headers['Gz-AppId'] = 'com.glazero.android'
    headers['Gz-AppVer'] = '1.3.0.2409'
    headers['Gz-Channel'] = 'internal'
    headers['Gz-FontSize'] = '1.1'
    headers['Gz-Imei'] = 'd71c95c2ea6bd816'
    headers['Gz-Lang'] = 'zh-Hans-CN'
    headers['Gz-Model'] = 'SM-A515U'
    headers[
        'Gz-NotifyPermission'] = '{filter=ALL, channels={%E9%97%A8%E9%93%83%E8%A2%AB%E5%BC%BA%E6%8B%86%E6%B6%88%E6%81%AF=4, %E6%8C%89%E9%97%A8%E9%93%83%E6%B6%88%E6%81%AF=4, %E4%BD%8E%E7%94%B5%E9%87%8F%E6%B6%88%E6%81%AF=4, %E9%97%A8%E9%93%83%E4%BA%8B%E4%BB%B6%E6%B6%88%E6%81%AF=4, %E5%85%B6%E4%BB%96%E6%9C%AA%E5%88%86%E7%BB%84%E6%B6%88%E6%81%AF=4, default=1}, channelGroups={default_group=false}, enabled=true, paused=false, BubblesAllowed=true}'
    headers['Gz-OsLang'] = ''
    headers['Gz-OsType'] = 'android'
    headers['Gz-OsVer'] = '29'
    headers['Gz-Sid'] = ''
    headers['Gz-Timezone'] = '+08:00'
    headers['Gz-Uid'] = ''
    return headers


def aosu_headers():
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    return headers


# 登录接口，获取sessionId，为修改密码接口提供必要的header
def _login(gz_host, _email, _region, country_code, _password, _type=1):
    global SID, UID
    url = 'https://' + gz_host + '/v1/user/login' + '?' + 'uuid=' + 'android_ui_auto' + '&' + 't=' + '001'
    data = 'countryAbbr=' + _region + '&' + 'countryCode=' + country_code + '&' + 'email=' + _email + '&' + 'password=' + _password + '&' + 'type=%d' % _type
    rsp = requests.post(url, headers=_headers(), data=data, timeout=(10, 10), verify=False)
    # rsp_json = rsp.json()
    SID = rsp.json()['data']['sid']
    UID = rsp.json()['data']['uid']


def change_password(old_pwd, new_pwd, _email, _type, gz_host, _region='CN', country_code='86'):
    old_pwd_md5 = _md5(old_pwd)
    new_pwd_md5 = _md5(new_pwd)
    _login(gz_host, _email, _region, country_code, old_pwd_md5, _type)
    url = 'https://' + gz_host + '/v1/user/changePassword' + '?' + 'uuid=' + 'android_ui_auto' + '&' + 't=' + '002'
    data = 'email=' + _email + '&' + 'newPassword=' + new_pwd_md5 + '&' + 'oldPassword=' + old_pwd_md5 + '&' + 'type=%d' % _type
    headers = _headers()
    headers['Gz-Sid'] = SID
    headers['Gz-Uid'] = UID
    requests.post(url, headers=headers, data=data, timeout=(10, 10), verify=False)
    # rsp_json = rsp.json()


def _unbind(sn='V8P1AH110002353', dev_type=1, delete_cloud_data=0, gz_host=gzHostCnTmp):
    pwd_md5 = _md5(pwd)
    _login(gz_host, _email=email, _region='CN', country_code='86', _password=pwd_md5, _type=1)
    url = 'https://' + gz_host + '/v1/bind/unbind' + '?' + 'uuid=' + 'android_ui_auto' + '&' + 't=' + '003'
    data = 'sn=' + sn + '&' + 'devType=%d' % dev_type + '&' + 'deleteCloudData=%d' % delete_cloud_data
    headers = _headers()
    headers['Gz-Sid'] = SID
    headers['Gz-Uid'] = UID
    rsp = requests.post(url, headers=headers, data=data, timeout=(10, 10), verify=False)
    logging.info(rsp.json())
    if rsp.json() == {'errno': 0, 'errmsg': '成功', 'data': {}}:
        print('解绑成功：', rsp.json())
    elif rsp.json() == {'errno': 701, 'errmsg': '已解绑或者未绑定', 'data': {}}:
        print('已解绑：', rsp.json())


def get_devices_list(model='V8P', gz_host=gzHostCnTmp):
    """
    获取设备列表中指定的model的设备，并将其返回
    :param gz_host: 域名，默认为中国区
    :param model: 默认是V8P
    :return: 将设备的名称返回
    """
    pwd_md5 = _md5(pwd)
    _login(gz_host, _email=email, _region='CN', country_code='86', _password=pwd_md5, _type=1)
    url = 'https://' + gz_host + '/v1/dev/getList' + '?' + 'uuid=' + 'android_ui_auto' + '&' + 't=' + '004'
    headers = _headers()
    headers['Gz-Sid'] = SID
    headers['Gz-Uid'] = UID
    rsp = requests.post(url, headers=headers, timeout=(10, 10), verify=False)
    logging.info(rsp.json())

    # 变量设备列表，筛选指定设备类型的设备名称并返回，例如，默认类型是V8P
    devices = list(rsp.json()["data"]["list"])
    if devices:
        for device in devices:
            # 获取指定设备类型的设备的名称，并且是主人设备，并且是在线的设备 满足条件的第一个
            if device["model"] == model and device["role"] == 0 and device["online"] == 1:
                dev_name = device["name"]
                return dev_name


def get_user_type(model='V8P', gz_host=gzHostCnTmp):
    """
    获取设备列表中指定的model的设备，并将其返回
    :param gz_host: 域名，默认为中国区
    :param model: 默认是V8P
    :return: 将设备的名称返回
    """
    pwd_md5 = _md5(pwd)
    _login(gz_host, _email=email, _region='CN', country_code='86', _password=pwd_md5, _type=1)
    url = 'https://' + gz_host + '/v1/cloud/getStatusList' + '?' + 'uuid=' + 'android_ui_auto' + '&' + 't=' + '005'
    headers = _headers()
    headers['Gz-Sid'] = SID
    headers['Gz-Uid'] = UID
    rsp = requests.post(url, headers=headers, timeout=(10, 10), verify=False)
    logging.info(rsp.json())

    # 变量设备列表，筛选指定设备类型的设备名称并返回，例如，默认类型是V8P
    user_type = rsp.json()["data"]["userType"]
    if user_type:
        return user_type


def aosu_admin_login(aosu_host='admin-cn.aosulife.com', pid='glazero', username='zhangjiamin', password='123'):
    pwd_md5 = _md5(password)
    headers = aosu_headers()
    url = 'https://' + aosu_host + '/admin/adminUser/login' + '?' + 'pid=' + pid + '&' + 'uuid=' + str(uuid.uuid1())
    data = 'pid=' + pid + '&' + 'username=' + username + '&' + 'password=' + pwd_md5 + '&' + 'uuid=' + str(uuid.uuid1())
    rsp = requests.post(url, headers=headers, data=data, timeout=(10, 10), verify=False)
    token = rsp.json()['data']['token']
    return token


def aosu_admin_get_dev_info(sn_sys='H1L2AH110000650', pid='glazero', gz_username='zhangjiamin',
                            aosu_host='admin-cn.aosulife.com'):
    # 获取token
    gz_sid = aosu_admin_login(aosu_host='admin-cn.aosulife.com', pid='glazero', username='zhangjiamin', password='123')
    headers = aosu_headers()
    url = 'https://' + aosu_host + '/admin/dev/getInfoList' + '?' + 'pid=' + pid + '&' + 'uuid=' + str(uuid.uuid1())
    data = 'pid=' + pid + '&' + 'gz_sid=' + gz_sid + '&' + 'gz_username=' + gz_username + '&' + 'snSys=' + sn_sys + \
           '&sn=&tuyaUuid=&devType=&' + 'uuid=' + str(uuid.uuid1())
    rsp = requests.post(url, headers=headers, data=data, timeout=(10, 10), verify=False)
    return rsp
    # print(rsp.json())
    # print("aosu状态为：", rsp.json()['data']['list'][0]['online'])
    # print("tuya状态为：", rsp.json()['data']['list'][0]['tuyayOnline'])


def get_dsc(device="SamsungA51"):
    path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
    yaml_url = os.path.join(path, 'gz_ui_auto\\devices.yaml')
    print("yaml配置文件地址：%s" % yaml_url)
    f = open(yaml_url, 'r', encoding='utf-8')
    file = f.read()
    f.close()
    data = yaml.load(file, Loader=yaml.FullLoader)
    for content in data:
        if device in content["desc"]:
            return content


def get_app_log(log_type, log_date, current_time, numbers_of_lines=1000):
    """
    获取app日志或者涂鸦日志
    :param current_time: 取日志时的时间，格式：年月日-时分秒，用于命名文件，不同的附件要对应不同的文件
    :param log_type: app 或者 ty
    :param log_date: 日志文件中的日期例如，20230510，用于选择对应的日志文件
    :param numbers_of_lines：返回日志的行数，默认是最新的1000行
    :结果: 将重定向的日志文件pull到本地，作为allure的attachment
    """
    if log_type == 'app':
        file_name = 'glazero_app_android_' + str(log_date) + '.log'
    elif log_type == 'ty':
        file_name = 'glazero_app_android_ty_' + str(log_date) + '.log'

    # 获取device id
    cmd = 'adb devices'
    with os.popen(cmd, 'r') as f_log:
        devs_id = f_log.readlines()
        dev_id = re.findall(r'^\w*\b', devs_id[1])[0]

    # 进入adb shell后进入日志目录，获取对应日期和对应日志类型的的日志
    cmd = 'adb -s %s shell "cd /sdcard/Android/data/com.glazero.android/files/log && ls && cat %s | tail -n %d > ' \
          '%s_log_%s.log && ls"' % (dev_id, file_name, numbers_of_lines, log_type, current_time)
    os.system(cmd)

    # 将到出的日志pull到本地
    cmd = 'adb pull /sdcard/Android/data/com.glazero.android/files/log/%s_log_%s.log ./report/V8P/log_attch' % (
        log_type, current_time)
    os.system(cmd)
