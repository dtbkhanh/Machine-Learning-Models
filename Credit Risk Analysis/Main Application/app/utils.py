from os import environ


def get_db_url():
    user = environ.get('USER_DB', 'root')
    password = environ.get('PASS_DB', 'helloworld')
    host = environ.get('HOST_DB', 'localhost')
    database_name = environ.get('DATABASE_DB', 'KhanhDB')
    port = environ.get('PORT_DB', '3306')
    return f"mysql+pymysql://{user}:{password}@{host}:{port}/{database_name}"
