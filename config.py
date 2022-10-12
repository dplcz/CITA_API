import configparser

# TODO ½âÎöÅäÖÃÎÄ¼ş

config = configparser.ConfigParser()

config.read('conf.ini')

print('http binding on {}:{} '.format(config['web.conf']['ip_bind'], config['web.conf']['port_bind']))
print('use sql by {}:{}'.format(config['mysqldb']['sql_host'], config['mysqldb']['sql_port']))
