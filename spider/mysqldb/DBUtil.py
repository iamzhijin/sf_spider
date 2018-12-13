import pymysql
import configparser
from DBUtils.PooledDB import PooledDB
from pymysql.cursors import DictCursor


class Config(object):
    ''' get the db config '''
    def __init__(self, config_path='/home/liuyun/pyfile/spider/config.ini', sectionname='dbconfig'):
        self.config = configparser.ConfigParser()
        self.config.read(config_path)
        self.sectionname = sectionname
        self.options = self.config.options(sectionname)

    def get_dbconfig(self):       
        dbconfig = {}
        for option in self.options:
            value = self.config.get(self.sectionname, option)
            dbconfig[option] = int(value) if value.isdigit() else value
        return dbconfig  


class MysqlPoll(object):
    ''' make the connect pool and operate mysql'''
    __pool = None

    def __init__(self):
        self.dbconfig = Config().get_dbconfig()
        self.host = self.dbconfig['host']
        self.port = self.dbconfig['port']
        self.db = self.dbconfig['db']
        self.user = self.dbconfig['user']
        self.password = self.dbconfig['password']
        self.charset = self.dbconfig['charset']
        self._conn = None
        self._conn = self.__getConnect()
        self.cursor = self._conn.cursor()

    def __getConnect(self):
        if MysqlPoll.__pool is None:
            __pool = PooledDB(
                creator=pymysql,
                mincached=1,
                maxcached=10,
                host=self.host,
                port=self.port,
                user=self.user,
                password=str(self.password),
                db=self.db,
                charset=self.charset,
                cursorclass=DictCursor
            )
        return __pool.connection() 

    def __query(self, sql, param=None):
        if param is None:
            count = self.cursor.execute(sql)
        else:
            count = self.cursor.execute(sql, param)
        self._conn.commit()    
        return count    

    def getAll(self, sql, param=None):
        '''
        sql 条件格式
        param tuple/list
        return 受影响行数
        '''
        count = self.__query(sql, param)
        if count > 0:
            result = self.cursor.fetchall()
        else:
            result = False
        return result 

    def update(self, sql, param=None):
        '''
        sql 条件格式 使用 (%s, %s), 
        param值为tuple/list, 
        return 受影响行数
        '''
        return self.__query(sql, param) 

    def insert(self, sql, param=None):
        count =  self.__query(sql, param)
        # self.cursor.commit()
        return count 

    def delete(self, sql, param=None):
        return self.__query(sql, param) 

    def dispose(self):
        self.cursor.close()
        self._conn.close()


# if __name__ == "__main__":
#     sql = "SELECT * FROM CLASSES WHERE ID=%s"
#     mysqlpool = MysqlPoll()
#     result = mysqlpool.getAll(sql, param="2")
#     print(result)
