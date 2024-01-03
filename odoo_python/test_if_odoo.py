import xmlrpc.client

                                                                                 
url = 'localhost'
db = 'base'
username = 'admin'
password = '2000'

info = xmlrpc.client.ServerProxy('https://demo.odoo.com/start').start()
url, db, username, password = info['host'], info['database'], info['user'], info['password']