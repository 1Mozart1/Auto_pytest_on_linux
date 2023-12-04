import subprocess


def checkout(cmd, text):
    result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, encoding='utf-8')
    if text in result.stdout and result.returncode == 0:
        return True
    else:
        return False


if __name__ == '__main__':
    assert checkout('cd /home/user/tst; 7z a ../out/arx2', 'Everything is ok'), print('test1 FAIL')
    assert checkout('cd /home/zerg/tst; 7z e arx2.7z -o/homa/zerg/folder1 -y', 'Everything is ok'), print('test2 FAIL')
    assert checkout('cd /home/zerg/tst; 7z t arx2.7z', 'Everything is ok'), print('test3 FAIL')
