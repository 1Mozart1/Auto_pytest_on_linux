import yaml

from zip import checkout, getout

with open('config.yaml') as f:
    data = yaml.safe_load(f)


class TestPositive:

    def test_add_file(self, make_folders, clear_folders, make_files):
        res1 = checkout("cd {}; 7z a {}/arh1".format(data['folder_in'], data['folder_out']), 'Everything is Ok')
        res2 = checkout("ls {}".format(data['folder_out']), 'arh1.7z')
        assert res1 and res2, 'test1 FAIL'

    def test_extract_file(self, clear_folders, make_files):
        res = []
        res.append(checkout("cd {}; 7z a {}/arh1".format(data['folder_in'], data['folder_out']), 'Everything is Ok'))
        res.append(
            checkout("cd {}; 7z e arh1.7z -o{} -y".format(data['folder_out'], data['folder_ex']), 'Everything is Ok'))
        for item in make_files:
            res.append(checkout("ls {}".format(data['folder_ex']), item))
        assert all(res), "test FAIL"

    def test_integrity_of_archive(self):
        assert checkout("cd {}; 7z t arh1.7z".format(data['folder_out']), 'Everything is Ok'), 'test3 FAIL'

    def test_step4(self):
        assert checkout("cd {}; 7z u arh1.7z".format(data['folder_in']), 'Everything is Ok'), 'test4 FAIL'

    def test_list_contents_of_archive(self, clear_folders, make_files):
        res = []
        res.append(checkout("cd {}; 7z a {}/arh1".format(data['folder_in'], data['folder_out']), 'Everything is Ok'))
        for item in make_files:
            res.append(checkout("cd {}; 7z l arh1.7z".format(data['folder_out'], data['folder_ex']), item))
        assert all(res), 'test5 FAIL'

    def test_step6(self, clear_folders, make_files, make_subfolder):
        res = []
        res.append(checkout("cd {}; 7z a {}/arh".format(data['folder_in'], data['folder_out']), 'Everything is Ok'))
        res.append(
            checkout("cd {}; 7z x arh.7z -o{} -y".format(data['folder_out'], data['folder_ex2']), 'Everything is Ok'))

        for item in make_files:
            res.append(checkout("ls {}".format(data['folder_ex2']), item))

        res.append(checkout("ls {}".format(data['folder_ex2']), make_subfolder[0]))
        res.append(checkout("ls {}/{}".format(data['folder_ex2'], make_subfolder[0]), make_subfolder[1]))
        assert all(res), "test6 FAIL"

    def test_step7(self):
        assert checkout("cd {}; 7z d arh.7z".format(data['folder_out']), 'Everything is Ok'), 'test7 FAIL'

    def test_hash(self, clear_folders, make_files):
        res = []
        for item in make_files:
            res.append(checkout("cd {}; 7z h {}".format(data['folder_in'], item), 'Everything is Ok'))
            hash = getout("cd {}; crc32 {}".format(data['folder_in'], item)).upper()
            res.append(checkout("cd {}; 7z h {}".format(data['folder_in'], item), hash))
        assert all(res), 'test8 FAIL'
