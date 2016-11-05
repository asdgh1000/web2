import io


def save_file(fd, file_absolute_path):
    '''
    保存文件
    :param fd: 文件句柄
    :param file_absolute_path: 文件绝对路径
    :return:
    '''

    with open(file_absolute_path, 'wb+') as destination:
        for chunk in fd.chunks():
            destination.write(chunk)


def md5(fd):
    import hashlib

    byte_io = io.BytesIO()
    for chunk in fd.chunks():
        byte_io.write(chunk)

    hashlibMd5 = hashlib.md5(byte_io.getvalue())
    byte_io.close()
    return hashlibMd5.hexdigest()


def read_file_to_string(file_absolute_path):
    string_io = io.StringIO()
    with open(file_absolute_path, "r") as fd:
        string_io.write(fd.read())

    out_str = string_io.getvalue()
    string_io.close()
    return out_str


def write_file(file_absolute_path, content):
    with open(file_absolute_path, "w") as fd:
        fd.write(content)


def site_map_add_url(url):
    '''
    在站点地图中添加新的url
    :param url: 新的url
    :return:
    '''
    from django.conf import settings
    import os
    with open(os.path.join(settings.BASE_DIR, 'templates/sitemap.txt'), "a") as fd:
        fd.write(url+"\n")




