import pymysql
import h1
import datetime
import hashlib
#pymysql 默认开启事务

class bbs():
    def __init__(self,conn,cursor):
        self.conn=conn
        self.cursor=cursor

    def jiemian(self):
        print("""
        注册：①
        登录：②
        """)
        n=int(input())
        if n==1:
            return bbs.zhuce(self)
        elif n==2:
            return bbs.denglu(self)
        else:
            print("请重新输入")
            return bbs.jiemian(self)


    def denglu(self):
        self.username=input("请输入用户姓名：")
        self.password=input("请输入密码：")
        sql = """select password from user where username='%s' """%self.username
        cursor.execute(sql)
        records = cursor.fetchall()
        a=hashlib.sha1(self.password.encode('utf8')).hexdigest()
        if records[0]['password']==a:
            print("登陆成功")
            print(
                """
                返回初始界面 1
                查看用户信息 2
                
                """
            )
            a=int(input())
            if a==1:
                return bbs.jiemian(self)
            elif a==2:
                return bbs.chakan(self)
            else:
                print("输入无效默认返回初始界面")
                return bbs.jiemian(self)
        else:
            print("登录失败")
            return bbs.jiemian(self)

    def chakan(self):
        print(self.username)
        sql=" select username,usertype,password,regtime,email from user where username='%s' "%self.username
        cursor.execute(sql)
        records=cursor.fetchall()
        a=str(records[0]['username'])
        b=str(records[0]['usertype'])
        c=str(records[0]['password'])
        d=str(records[0]['regtime'])
        e=str(records[0]['email'])

       

        print('用户名：%s'%a)
        print('用户类型：%s'%b)
        print('密码：%s'%c)
        print('注册时间：%s'%d )
        print('email：%s'%e)
        




    def zhuce(self):
        self.username=input("请输入注册用户名：")
        string=self.username.strip(" ")
        s=list(string)
        if len(s)<=2:
            print("不符合要求")
            return bbs.zhuce(self)
        sql = 'select username from user'
        res = cursor.execute(sql)
        records = cursor.fetchall()
        a=len(records)

        if res > 0:
            for i in range(a):
                if records[i]['username']==self.username:
                    print("该名已存在。")
                    return bbs.zhuce(self)
        password = input("请输入您的密码：")
        self.password=hashlib.sha1(password.encode('utf8')).hexdigest()
        self.email=input("请输入您的邮箱：")
        self.regtime=datetime.datetime.now()
        sql="insert into user (username,password,regtime,email) values ('%s','%s','%s','%s')"%(self.username,self.password,self.regtime,self.email)
        cursor.execute(sql)
        conn.commit()
        return bbs.jiemian(self)





if __name__ == "__main__":
    conn = pymysql.Connect(**h1.parameters)
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    sql='create database bbs default charset=utf8'
    res = cursor.execute(sql)
    conn.commit()
    sql = 'use bbs'
    res = cursor.execute(sql)
    conn.commit()
    sql="""
    create table if not exists user(
        uid int primary key auto_increment,
         username  varchar(4)  unique,
         usertype  enum('普通用户','管理员') default '普通用户',
         password varchar(48),
         regtime datetime,
         email varchar(25));
    """
    res = cursor.execute(sql)
    conn.commit()
    t=datetime.datetime.now()
    sql = """
     insert into user(username,usertype,password,regtime,email) values('adn','1',sha1('123'),'%s','3883@qq.com')
     """%t
    res = cursor.execute(sql)
    conn.commit()

    b=bbs(conn,cursor)
    b.jiemian()
    cursor.close()
    conn.close()