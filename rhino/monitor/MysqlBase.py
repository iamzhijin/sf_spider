import pymysql.cursors
from datetime import datetime
import re


class MysqlBase:
    """python class to operation mysql for every project.

    Sometimes, a lot of project need operation mysql, such as add, delete, ` , select. I do not want to write code for every project.
    So, I create a class for all of the these needs
    """
    def __init__(self, connector):
        """init mysql class. Connect mysql sever defined by args.

        Args:
            connector: A config such like user, database.. That is a dict

        Returns:
            self.conncetion: A mysql conncet instance.
        """
        self.connection = pymysql.connect(**connector,  charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)

    def _execute(self, sql_query):
        """execute sql
        execute sql usually select sql
        Returns
            items: one line in sql by iterator
        """
        with self.connection.cursor() as cursor:
            dbcur = cursor.execute(sql_query)
            for items in cursor.fetchall():
                    yield items

    def _select(self, table, **kwargs):
        """select by args
        add fields to select, remember add limit otherwear pause for a long time

        Args:
            kwargs: fields,limit etc.

        Returns:
            items: one line in sql by iterator
        """
        limit = 0
        if 'limit' in kwargs:
            limit = kwargs.get('limit', 10)
            del kwargs['limit']

        keys = kwargs.keys()
        where = ' and '.join(['{}={}'.format(key, "'{}'".format(kwargs[key])) for key in keys])
        if where:
            sql = "select * from {table} where {where} limit {limit}".format(table=table, where=where, limit=limit)
        elif limit:
            sql = "select * from {table} limit {limit}".format(table=table, limit=limit)
        else:
            sql = "select * from {table}".format(table=table)
        with self.connection.cursor() as cursor:
            print(sql)
            cursor.execute(sql)
            for items in cursor.fetchall():
                    yield items

    def into_file(self, file, *fields, **result):
        """write into file
        writer into file, field delimited by '|', line delimited by '\n\r'

        Args:
            file: filename, use for write
            fields: database fields. if fields is list, parameters is *list
            results: database values. if result is dict, parameters is **dict

        Returns:
            write database values into file.
        """
        values = '|'.join([re.sub('\n\r', '', re.sub('|', '', str(result[f]).strip())) for f in fields])
        with open('{}'.format(file), 'a') as f:
            f.write('{}\n\r'.format(values))

    def _update(self, sql):
        """update database
        Args
            sql: sql sentence
        Returns
            r: line num
        """
        with self.connection.cursor() as cs:
            r = cs.execute(sql)
        self.connection.commit()
        return r if r else 0

    def into(self, table, **result):
        key = result.keys()
        fields = ','.join(key)
        values = ','.join(["'{}'".format(str(result[f])) for f in key])
        sql = "insert  IGNORE into  {table} ({fields}) values ({values});".format(table=table, fields=fields, values=values)
        with self.connection.cursor() as cs:
            print(sql)
            cs.execute(sql)
        self.connection.commit()

if __name__ == '__main__':
    from rhino.settings import PYSPIDER_DATABASE_HOST
    from rhino.settings import PYSPIDER_DATABASE_NAME
    from rhino.settings import PYSPIDER_DATABASE_PASSWORD
    from rhino.settings import PYSPIDER_DATABASE_USERNAME
    from rhino.settings import PYSPIDER_DATABASE_PORT


    connector = {
        'host': PYSPIDER_DATABASE_HOST,
        'user': PYSPIDER_DATABASE_USERNAME,
        'password': PYSPIDER_DATABASE_PASSWORD,
        'db': PYSPIDER_DATABASE_NAME
    }
    pyspider_mb = MysqlBase(connector)
    pyspider_name = 'aa'
    rst = [item for item in
     pyspider_mb._execute("select status, count(status) as num from `{}` group by status".format(pyspider_name))]
    print(rst)