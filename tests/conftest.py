import yaml
import pytest
import random, string
from zip import checkout, getout
from datetime import datetime
import sys

with open('config.yaml') as f:
    data = yaml.safe_load(f)


@pytest.fixture()
def make_folders():
    return checkout(
        "mkdir -p {} {} {} {}".format(data['folder_in'], data['folder_out'], data['folder_ex'], data['folder_ex2']), "")


@pytest.fixture()
def clear_folders():
    return checkout("rm -rf {}/* {}/* {}/* {}/*".format(data['folder_in'], data['folder_out'], data['folder_ex'],
                                                        data['folder_ex2']), "")


@pytest.fixture()
def make_files():
    list_of_files = []
    for i in range(data['count']):
        filename = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
        if checkout("cd {}; dd if=/dev/urandom of={} bs=1M count=1 iflag=fullblock".format(data['folder_in'], filename),
                    ""):
            list_of_files.append(filename)
    return list_of_files


@pytest.fixture()
def make_subfolder():
    testfilename = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
    subfoldername = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
    if not checkout("cd {}; mkdir {}".format(data['folder_in'], subfoldername), ""):
        return None, None
    if not checkout(
            "cd {}/{}; dd if=/dev/urandom of={} bs=1M count=1 iflag=fullblock".format(data['folder_in'], subfoldername,
                                                                                      testfilename), ""):
        return subfoldername, None
    else:
        return subfoldername, testfilename


@pytest.fixture(autouse=True)
def print_time():
    print('Start: {}'.format(datetime.now().strftime("%H:%M:%S.%f")))
    yield
    print('Stop: {}'.format(datetime.now().strftime("%H:%M:%S.%f")))


@pytest.fixture(autouse=True)
def stat_log():
    yield
    time = datetime.now().strftime("%H:%M:%s.%f")
    stat = getout('cat /proc/loadavg')
    file_size = sys.getsizeof('/home/user/folder_out/arh1.7z')
    checkout(f"echo 'time:{time} count:{data.get('count')} size:{file_size} stat:{stat}' >> stat.txt", '')
