import os
import re
import time
# coding=utf-8
# tmp = gz.get_devices_list()
# print(rst.content.decode('utf-8'))
# print(rst)
# print(tmp)
# str = "中国 +86"
# region = list(str)
# print(region[3:-1])
# print(str[-3:])


def get_app_log(log_type, log_date, numbers_of_lines=1000):
    """
    获取app日志或者涂鸦日志
    :param log_type: app 或者 ty
    :param log_date: 日志文件中的日期例如，20230510
    :param numbers_of_lines：返回日志的行数，默认是最新的1000行
    :return: 返回对应的日志文件
    """
    if log_type == 'app':
        file_name = 'glazero_app_android_' + str(log_date) + '.log'
    elif log_type == 'ty':
        file_name = 'glazero_app_android_ty_' + str(log_date) + '.log'

    # 获取device id
    devs_id = list(os.popen('adb devices').readlines())
    dev_id = re.findall(r'^\w*\b', devs_id[1])[0]

    # 进入adb shell后进入日志目录，获取对应日期和对应日志类型的的日志
    cmd = 'adb -s %s shell "cd /sdcard/Android/data/com.glazero.android/files/log && ls && cat %s | tail -n %d > ' \
          '%s_log.log && ls"' % (dev_id, file_name, numbers_of_lines, log_type)
    with os.popen(cmd, 'r') as f_log:
        log_files = f_log.readlines()
        print('手机端log目录：', log_files)

    # 将到出的日志pull到本地
    cmd = 'adb pull /sdcard/Android/data/com.glazero.android/files/log/%s_log.log ./report/V8P/log_attch' % log_type
    with os.popen(cmd, 'r') as f_log:
        redirect_file = f_log.readlines()
        print('导出完成：', redirect_file)

'''


    try:
        with open(file_name, 'r', encoding='utf-8') as f_obj:
            lines = f_obj.readlines()
    except FileNotFoundError:
        print("没有找到日志文件" + str(log_date))
        return None
    else:
        last_n_lines = lines[-numbers_of_lines:]
        return last_n_lines


contents = get_app_log('app', current_time, 1000)

print(contents)
'''
current_time = time.strftime("%Y%m%d", time.localtime())
print(current_time)
get_app_log('app', current_time, 500)
get_app_log('ty', current_time, 300)
