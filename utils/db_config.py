from sqlalchemy import create_engine
def connect_mysql():
    return create_engine("mysql+mysqlconnector://root:@localhost/shopee_analytics")