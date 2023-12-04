from Test_7zip import checkout
import zlib

folder_in = '/home/user/folder_in'
folder_out = '/home/user/folder_out'
folder_ex = '/home/user/folder_ex'


def test_add_file():
    assert checkout(f'cd {folder_in}; 7z a {folder_out}/arh1', 'Everything is Ok'), print('test1 FAIL')


def test_extract_file():
    assert checkout(f'cd {folder_out}; 7z e arh1.7z -o{folder_ex} -y', 'Everything is Ok'), print('test2 FAIL')


def test_integrity_of_archive():
    assert checkout(f'cd {folder_out}; 7z t arh1.7z', 'Everything is Ok'), print('test3 FAIL')


def test_list_contents_of_archive():
    assert checkout(f'cd {folder_out}; 7z l arh1.7z', '2 files'), print('test4 FAIL')


def test_extract_files_with_full_paths():
    assert checkout(f'cd {folder_out}; 7z e arh1.7z -o{folder_out} -y', 'Everything is Ok'), print('test5 FAIL')


def crc32(cmd):
    with open(cmd, 'rb') as g:
        hash = 0
        while True:
            s = g.read(65536)
            if not s:
                break
            hash = zlib.crc32(s, hash)
        return "%08X" % (hash & 0xFFFFFFFF)


def test_crc232():
    res = crc32(f'{folder_out}/arh1.7z').lower()
    assert checkout(f'crc32 {folder_out}/arh1.7z', res), print('test6 FAIL')


if __name__ == '__main__':
    pytest.main(['--v'])
