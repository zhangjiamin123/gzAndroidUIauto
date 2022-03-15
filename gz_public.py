import random
import initPhone
import requests
import json
from hashlib import md5
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


# 远程Appium服务地址
# gzAppiumH = "http://10.10.1.123:4723/wd/hub"
gzAppiumH = "http://127.0.0.1:4723/wd/hub"

# 手机系统
gzPlatformN = "Android"

# 包信息
gzAppPack = initPhone.InitPhone.getPackageName()
gzAppActivity = "com.glazero.android.SplashActivity"

# 登录账号
email = "1010642719@qq.com"
pwd = "Qwe222222"

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
CONNECTTO = initPhone.InitPhone.getDeviceId()
# PLATFORMVER = gzPhoneList[0]['gzPlatformVer']
PLATFORMVER = initPhone.InitPhone.getAndroidVersion()
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
    # rsp_json = rsp.json()
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
    requests.post(url, headers=headers, data=data, verify=False)
    # rsp_json = rsp.json()
