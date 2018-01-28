'''
Created on 16.09.2014

@author: rafael
'''
class OnlineConfiguration(object):
    '''
    Basic configuration
    '''
    SQLALCHEMY_DATABASE_URI = ('postgresql://postgres:postgres@localhost:5432/oceancare')
    SQLALCHEMY_ECHO = True

class OfflineConfiguration(OnlineConfiguration):
    '''
    Debug configuration
    '''
    SQLALCHEMY_DATABASE_URI = ('sqlite:///offline_db')
    SQLALCHEMY_ECHO = True