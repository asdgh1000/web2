

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
    import io

    byte_io = io.BytesIO()
    for chunk in fd.chunks():
        byte_io.write(chunk)

    hashlibMd5 = hashlib.md5(byte_io.getvalue())
    byte_io.close()
    return hashlibMd5.hexdigest()
