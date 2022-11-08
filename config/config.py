# 更改配置文件格式
import json
# import configparser
import platform

plat = platform.system().lower()

if plat == 'windows':
    path = '\\'.join(__file__.split('\\')[:-1])
    file_path = '{}\{}'.format(path, 'conf.json')
elif plat == 'linux':
    path = '/'.join(__file__.split('/')[:-1])
    file_path = '{}/{}'.format(path, 'conf.json')

# TODO 解析配置文件

with open(file_path, 'r', encoding='utf-8') as f:
    config = json.load(f)
# config = configparser.ConfigParser()

# config.read_file(open(file_path, encoding='utf-8'))

print('http binding on {}:{} '.format(config['conf']['web']['ip'], config['conf']['web']['port']))
print('use sql by {}:{}'.format(config['conf']['mysqldb']['host'], config['conf']['mysqldb']['port']))
