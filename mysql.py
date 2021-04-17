import pymysql


# 连接数据库
class Database:
    def __init__(self, host='localhost',
                 port=3306,
                 user='root',
                 passwd='ld123456',
                 charset='utf8',
                 database=None):
        self.host = host
        self.port = port
        self.user = user
        self.passwd = passwd
        self.charset = charset
        self.database = database
        self.connect_database = self.connect_database()

    # 连接数据库
    def connect_database(self):
        self.db = pymysql.connect(host=self.host,
                                  port=self.port,
                                  user=self.user,
                                  password=self.passwd,
                                  charset=self.charset,
                                  database=self.database)

    # 关闭数据库
    def close(self):
        self.db.close()

    # 创建游标
    def create_cursor(self):
        self.cur = self.db.cursor()

    # 注册
    def register(self, name, passwd):
        sql = "select * from user where name='%s'" % name
        self.cur.execute(sql)
        r = self.cur.fetchone()
        if r:
            return False
        sql = "insert into user (name,password) values(%s,%s)"
        try:
            self.cur.execute(sql, [name, passwd])
            self.db.commit()
            return True
        except Exception:
            self.db.rollback()

    # 登录
    def do_sign_in(self, name, passwd):
        sql = "select * from user where name=%s and password=%s"
        self.cur.execute(sql, [name, passwd])
        r = self.cur.fetchone()
        if r:
            return True

    # 单词查询，并将用户查询添加到历史记录中
    def query(self, name, word):
        sql = "insert into hist (name,word) values(%s,%s)"
        # 将查询单词插入历史记录
        try:
            self.cur.execute(sql, [name, word])
            self.db.commit()
        except Exception:
            self.db.rollback()

        sql = "select * from words where word=%s"
        self.cur.execute(sql, [word])
        r = self.cur.fetchone()
        if r:
            return r[1] + ':' + r[2]
        else:
            return '没有找到该单词'

    # 查询历史记录
    def do_hist(self, name):
        sql = "select word from hist where name=%s"
        self.cur.execute(sql, [name])
        r = self.cur.fetchall()
        if r:
            return str(r)
        else:
            return '没有历史记录'
