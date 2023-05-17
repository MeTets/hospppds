from sqlalchemy import *
from sqlalchemy.orm import sessionmaker
import psycopg2

class dbconn():
    def __init__(self):  
        self.engine = create_engine("postgresql+psycopg2://kqkmyagt:E5xKSQqtnui4Yax4vNWwqEyjGZsJEyxY@babar.db.elephantsql.com/kqkmyagt")
        self.conn = self.engine.connect()
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()

    def conexao(self, comandos):
        responsedb = self.conn.execute(text(comandos))
        return responsedb
    
    def conexaoInsert(self, comandos):
        responsedb = self.conn.execute(text(comandos))
        self.conn.commit()
        return responsedb



