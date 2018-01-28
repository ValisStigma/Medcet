
class OnlineConfiguration(object):
    SQLALCHEMY_DATABASE_URI = ('postgresql://postgres:postgres@localhost:5432/oceancare')
    SQLALCHEMY_ECHO = True

class OfflineConfiguration(OnlineConfiguration):
    SQLALCHEMY_DATABASE_URI = ('sqlite:///offline_db')
    SQLALCHEMY_ECHO = True