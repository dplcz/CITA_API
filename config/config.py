import configparser

# TODO 解析配置文件
config = configparser.ConfigParser()

path = '\\'.join(__file__.split('\\')[:-1])

config.read_file(open('{}\{}'.format(path, 'conf.ini'), encoding='utf-8'))

print('http binding on {}:{} '.format(config['web.conf']['ip_bind'], config['web.conf']['port_bind']))
print('use sql by {}:{}'.format(config['mysqldb']['sql_host'], config['mysqldb']['sql_port']))
