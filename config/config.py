import configparser
import platform

plat = platform.system().lower()

if plat == 'windows':
    path = '\\'.join(__file__.split('\\')[:-1])
    file_path = '{}\{}'.format(path, 'conf.ini')
elif plat == 'linux':
    path = '/'.join(__file__.split('/')[:-1])
    file_path = '{}/{}'.format(path, 'conf.ini')

# TODO 解析配置文件
config = configparser.ConfigParser()

config.read_file(open(file_path, encoding='utf-8'))

print('http binding on {}:{} '.format(config['web.conf']['ip_bind'], config['web.conf']['port_bind']))
print('use sql by {}:{}'.format(config['mysqldb']['sql_host'], config['mysqldb']['sql_port']))
