# pip install pymysql
# pip install sqlalchemy
import pymysql
from sqlalchemy import create_engine
import pandas as pd

def data_save(df, table_nm, index=False):
    user_nm = 'root'
    user_pw = '1234'
    host_nm = 'localhost'
    host_address = '3306'
    db_nm = 'multi_pjt1'
    # 데이터 베이스 연결
    db_connection_path = f"mysql+mysqldb://{user_nm}:{user_pw}@{host_nm}:{host_address}/{db_nm}"
    db_connection = create_engine(db_connection_path, encoding='utf-8')
    conn = db_connection.connect()
    # 데이터 프레임 저장
    df.to_sql(name=table_nm, con=db_connection, if_exists='replace', index=index)
    # 데이터 저장 확인
    df = pd.read_sql_table(table_nm, con=conn)
    print(df)

def data_load(table_nm):
    user_nm = 'root'
    user_pw = '1234'
    host_nm = 'localhost'
    host_address = '3306'
    db_nm = 'multi_pjt1'
    # 데이터 베이스 연결
    db_connection_path = f"mysql+mysqldb://{user_nm}:{user_pw}@{host_nm}:{host_address}/{db_nm}"
    db_connection = create_engine(db_connection_path, encoding='utf-8')
    conn = db_connection.connect()
    # 데이터 가져오기
    df = pd.read_sql_table(table_nm, con=conn)
    return df