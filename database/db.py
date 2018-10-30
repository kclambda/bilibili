import pymysql
from DBUtils.PooledDB import PooledDB

from utils.config import *


class MySQLPool(object):
    def __init__(self):
        self.pool = PooledDB(creator=pymysql, mincached=MySQL_MIN_CACHED, maxcached=MySQL_MAX_CACHED,
                             maxshared=MySQL_MAX_SHARED, maxconnections=MySQL_MAX_CONNECYIONS,
                             blocking=MySQL_BLOCKING, maxusage=MySQL_MAX_USAGE,
                             setsession=MySQL_SET_SESSION,
                             host=MySQL_HOST, port=MySQL_PORT,
                             user=MySQL_USER, passwd=MySQL_PASSWORD,
                             db=MySQL_DATABASE, use_unicode=False, charset=MySQL_CHARSET)

    def get_conn(self):
        """
        Get MySQL connection object
        :return:
        """
        return self.pool.connection()


class MySQLDB(object):
    @staticmethod
    def insert(sql, data=()):
        """
        Insert data to database
        :return:
        """
        conn = MySQLPool().get_conn()
        cursor = conn.cursor()

        try:
            result = cursor.execute(sql, data)  # data maybe tuple or list and so on
            conn.commit()
            print(f"----Insert data sucess {result}----")
        except Exception as e:
            print(f"----Insert data failure {e}----")
            conn.rollback()
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def insert_many(sql, data=()):
        """
        Insert data to database
        :return:
        """
        conn = MySQLPool().get_conn()
        cursor = conn.cursor()
        """
        insert_sql = "insert into aid(aid) values (%s)"
        data = [1, 2, 3, 4]
        sql = sql + ",(%s)"*(len(data)-1) + ";"
        print(sql)
        
        # According to this plan, we can implement multiple data insert to database at the same time
        # but if we set the field unique, we can choose the following plan
        """
        for content in data:
            try:
                result = cursor.execute(sql.format(content))  # data maybe tuple or list and so on
                conn.commit()
                print(f"----Insert data sucess {result}----")
            except Exception as e:
                # print(f"----Insert data failure {e}----")
                conn.rollback()
                continue
        cursor.close()
        conn.close()

    @staticmethod
    def delete(sql, data=()):
        """
        Insert data to database
        :return:
        """
        conn = MySQLPool().get_conn()
        cursor = conn.cursor()

        try:
            result = cursor.execute(sql)  # data maybe tuple or list and so on
            conn.commit()
            print(f"----Delete data from database sucess {result}----")
        except Exception as e:
            print(f"----Delete data failure {e}----")
            conn.rollback()
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def update(sql, data=()):
        """
        Update data to database
        :return:
        """
        conn = MySQLPool().get_conn()
        cursor = conn.cursor()

        try:
            result = cursor.execute(sql, data)  # data maybe tuple or list and so on
            conn.commit()
            print(f"----Update data sucess {result}----")
        except Exception as e:
            print(f"----Update data failure {e}----")
            conn.rollback()
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def create(sql):
        """
        On the basis of real situation create table
        :return:
        """
        aid_sql = "CREATE TABLE IF NOT EXISTS aid (id INT NOT NULL AUTO_INCREMENT, aid VARCHAR(10) NOT NULL, mark TINYINT UNSIGNED NOT NULL DEFAULT 0, PRIMARY KEY(id), CONSTRAINT aid_name UNIQUE (aid))ENGINE=InnoDB DEFAULT CHARSET=utf8;"

        user_sql = """
        CREATE TABLE IF NOT EXISTS userinfo (
        id INT NOT NULL AUTO_INCREMENT, 
        mid VARCHAR(10) NOT NULL, 
        name VARCHAR(50),
        sex VARCHAR(2),
        face VARCHAR(50),
        regtime VARCHAR(13),
        sign VARCHAR(100),
        birthday VARCHAR(13),
        place VARCHAR(50),
        current_level VARCHAR(5),
        fans VARCHAR(10),
        friends VARCHAR(10),
        attention VARCHAR(10),
        archive_count VARCHAR(10),
        article_count VARCHAR(10),
        mark TINYINT UNSIGNED NOT NULL DEFAULT 0, 
        PRIMARY KEY(id), 
        CONSTRAINT mid_name UNIQUE (mid)
        )ENGINE=InnoDB DEFAULT CHARSET=utf8;
        """

        conn = MySQLPool().get_conn()
        cursor = conn.cursor()

        try:
            result = cursor.execute(sql)  # data maybe tuple or list and so on
            conn.commit()
            print(f"----Update data sucess {result}----")
        except Exception as e:
            print(f"----Update data failure {e}----")
            conn.rollback()
        finally:
            cursor.close()
            conn.close()

    @ staticmethod
    def select(sql):
        """
        Select data from database
        :return:
        """
        conn = MySQLPool().get_conn()
        cursor = conn.cursor()

        try:
            result = cursor.execute(sql)  # data maybe tuple or list and so on
            if result > 0:
                print(f"----Select data success {result}----")
                data = cursor.fetchall()
                return data
        except Exception as e:
            print(f"----Select data failure {e}----")
            return None
        finally:
            cursor.close()
            conn.close()

    def run(self):
        """
        1. Execute self.create() function create table
        2. Execute self.insert() insert one video aid information
        :return:
        """
        pass


if __name__ == '__main__':
    db = MySQLDB()
    db.run()
