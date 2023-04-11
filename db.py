from sqlalchemy import *
import psycopg2

class dbconn():
    def __init__(self):  
        self.engine = create_engine("postgresql+psycopg2://kqkmyagt:E5xKSQqtnui4Yax4vNWwqEyjGZsJEyxY@babar.db.elephantsql.com/kqkmyagt")
        self.conn = self.engine.connect()

    def conexao(self, comandos):
        responsedb = self.conn.execute(text(comandos))
        return responsedb



