from sshcheckers import ssh_checkout, upload_files
import yaml
import pytest

with open('config.yaml', 'r', encoding='utf-8') as f:
    data = yaml.safe_load(f)


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


def test_delete():
    assert ssh_checkout(f'{data.get("host")}',
                        f'{data.get("user")}',
                        f'{data.get("pswd")}',
                        f'echo {data.get("pswd")} | sudo -S dpkg -r p7zip-full',
                        "Удаляется")


if __name__ == '__main__':
    pytest.main(['-vv'])
