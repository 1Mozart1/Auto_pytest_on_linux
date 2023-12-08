import yaml
import pytest
import random, string
from sshcheckers import ssh_checkout, upload_files, ssh_getout
from datetime import datetime
import sys

with open('config.yaml', encoding='utf-8') as f:
    data = yaml.safe_load(f)


@pytest.fixture(autouse=True, scope='module')
def test_deploy():
    res = []
    upload_files(f"{data.get('host')}",
                 f"{data.get('user')}",
                 f"{data.get('pswd')}",
                 "/home/user/test/p7zip-full.deb",
                 '/home/user2/p7zip-full.deb')
    res.append(ssh_checkout(f"{data.get('host')}",
                            f"{data.get('user')}",
                            f"{data.get('pswd')}",
                            'echo "1" | sudo -S dpkg -i /home/user2/p7zip-full.deb',
                            'Настраивается пакет'))
    res.append(ssh_checkout(f"{data.get('host')}",
                            f"{data.get('user')}",
                            f"{data.get('pswd')}",
                            'echo "1" | sudo -S dpkg -s p7zip-full',
                            'Status: install ok installed'))
    assert all(res)


@pytest.fixture(autouse=True, scope='module')
def make_folders():
    return ssh_checkout(f"{data.get('host')}",
                        f"{data.get('user')}",
                        f"{data.get('pswd')}",
                        "mkdir -p {} {} {} {}".format(data['folder_in'],
                                                      data['folder_out'],
                                                      data['folder_ex'],
                                                      data['folder_ex2']),
                        "")


@pytest.fixture()
def clear_folders():
    return ssh_checkout(f"{data.get('host')}",
                        f"{data.get('user')}",
                        f"{data.get('pswd')}",
                        "rm -rf {}/* {}/* {}/* {}/*".format(data['folder_in'],
                                                            data['folder_out'],
                                                            data['folder_ex'],
                                                            data['folder_ex2']),
                        "")


@pytest.fixture(autouse=True)
def make_files():
    list_of_files = []
    for i in range(data['count']):
        filename = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
        if ssh_checkout(f"{data.get('host')}",
                        f"{data.get('user')}",
                        f"{data.get('pswd')}",
                        "cd {}; dd if=/dev/urandom of={} bs=1M count=1 iflag=fullblock".format(data['folder_in'],
                                                                                               filename),
                        ""):
            list_of_files.append(filename)
    return list_of_files


@pytest.fixture()
def make_subfolder():
    testfilename = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
    subfoldername = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
    if not ssh_checkout(f"{data.get('host')}",
                        f"{data.get('user')}",
                        f"{data.get('pswd')}",
                        "cd {}; mkdir {}".format(data['folder_in'], subfoldername), ""):
        return None, None
    if not ssh_checkout(f"{data.get('host')}",
                        f"{data.get('user')}",
                        f"{data.get('pswd')}",
                        "cd {}/{}; dd if=/dev/urandom of={} bs=1M count=1 iflag=fullblock".format(data['folder_in'],
                                                                                                  subfoldername,
                                                                                                  testfilename), ""):
        return subfoldername, None
    else:
        return subfoldername, testfilename


@pytest.fixture(autouse=True)
def print_time():
    print('Start: {}'.format(datetime.now().strftime("%H:%M:%S.%f")))
    yield
    print('Stop: {}'.format(datetime.now().strftime("%H:%M:%S.%f")))


# @pytest.fixture(autouse=True)
# def stat_log():
#     yield
#     time = datetime.now().strftime("%H:%M:%s.%f")
#     stat = ssh_getout(f'{data.get("host")}',
#                       f'{data.get("user")}',
#                       f'{data.get("pswd")}',
#                       'cat /proc/loadavg')
#     file_size = sys.getsizeof('/home/user/folder_out/arh1.7z')
#     ssh_checkout(f"echo 'time:{time} count:{data.get('count')} size:{file_size} stat:{stat}' >> stat.txt", '')


@pytest.fixture()
def test_delete():
    assert ssh_checkout(f'{data.get("host")}',
                        f'{data.get("user")}',
                        f'{data.get("pswd")}',
                        f'echo {data.get("pswd")} | sudo -S dpkg -r p7zip-full',
                        "Удаляется")
