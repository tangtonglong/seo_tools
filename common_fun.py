import codecs
import os
import time

import pymysql
import redis
from sshtunnel import SSHTunnelForwarder

REDIS_HOST = '127.0.0.1'
REDIS_PORT = 6379

def get_fold_name(file_dir):
        return os.listdir(file_dir)


def get_redis_conn():
        pool = redis.ConnectionPool(host=REDIS_HOST, port=REDIS_PORT)
        redis_cli = redis.StrictRedis(connection_pool=pool, port=6379, db=0, password=None, encoding='utf-8', decode_responses=True)
        return redis_cli

def save_item_to_file(filename,item):
        with codecs.open(filename, 'a', encoding='utf8') as f:
                f.write(item)

def get_cur_time_str():
        return time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime())

def get_mysql_data(sqlstat,columnlist):
        db = pymysql.connect("localhost", "root", "12345678", "testdb", charset='utf8' )
        # 使用cursor()方法获取操作游标 
        
        try:
                cursor = db.cursor()
                resultdictlist = []

                # 执行SQL语句
                cursor.execute(sqlstat)
                # 获取所有记录列表
                results = cursor.fetchall()

                for row in results:
                        itemdict = {}
                        for i in range(0, len(columnlist)):
                                itemdict[columnlist[i]] = row[i]
                                # print(itemdict[columnlist[i]])

                        resultdictlist.append(itemdict)
                # 打印结果
                # print ("region_Code=%s,region_Name=%s,regionLevel=%s,pid=%s,pid_path=%s" % (region_Code, region_Name, regionLevel, pid, pid_path )
                db.close()
                return resultdictlist
        except:
                db.close()
                print("Error: unable to fecth data")
                return None


def modify_mysql_data(sqlstat, table_name):
        db = pymysql.connect("localhost", "root", "12345678", "testdb", charset='utf8')
        # 使用cursor()方法获取操作游标
        cursor = db.cursor()
        try:
                # 执行sql语句
                cursor.execute(sqlstat)

                # 提交到数据库执行
                db.commit()


        except:
                print("Error: unable to fecth data")
                db.rollback()

        db.close()


def ssh_mysql2(sqlstat, columnlist):
        server = SSHTunnelForwarder(

                ssh_address_or_host=('192.144.190.227', 22),  # 指定ssh登录的跳转机的address

                ssh_username='root',  # 跳转机的用户

                ssh_password='ZhiXue@YG_t_Ct',  # 跳转机的密码

                remote_bind_address=('172.21.0.12', 3306)

        )

        server.start()

        db = pymysql.connect(

                host='127.0.0.1',

                port=server.local_bind_port,

                user='root',

                passwd='m6i1m2a3',

                db='seo'

        )


        try:
                cursor = db.cursor()
                resultdictlist = []

                # 执行SQL语句
                cursor.execute(sqlstat)
                # 获取所有记录列表
                results = cursor.fetchall()

                for row in results:
                        itemdict = {}
                        for i in range(0, len(columnlist)):
                                itemdict[columnlist[i]] = row[i]
                                # print(itemdict[columnlist[i]])

                        resultdictlist.append(itemdict)
                # 打印结果
                # print ("region_Code=%s,region_Name=%s,regionLevel=%s,pid=%s,pid_path=%s" % (region_Code, region_Name, regionLevel, pid, pid_path )
                return resultdictlist
        except:
                print("Error: unable to fecth data")
        db.close()

        server.close()

def ssh_mysql():
        server = SSHTunnelForwarder(

                ssh_address_or_host=('192.144.190.227', 22),  # 指定ssh登录的跳转机的address

                ssh_username='root',  # 跳转机的用户

                ssh_password='ZhiXue@YG_t_Ct',  # 跳转机的密码

                remote_bind_address=('172.21.0.12', 3306)

        )

        server.start()

        db = pymysql.connect(

                host='127.0.0.1',

                port=server.local_bind_port,

                user='root',

                passwd='m6i1m2a3',

                db='seo'

        )

        cur = db.cursor()
        sqlstat = 'select 1 '
        # sqlstat = '''INSERT INTO  comment_detail (shop_id, comment_user_name, comment_star, comment_score, comment_content, comment_user_img, comment_imgs) VALUES ('12306','dpuser_1588557440','5','课程：非常好 师资：非常好 环境：非常好 ','瑞思英语梨园校区的环境超级棒，老师非常热情，对孩子也特别耐心。去试听完觉得无论是从硬件条件还是软实力，不愧是教育培训行业的领头羊。','https://p0.meituan.net/userheadpic/bun.png',"['http://qcloud.dpfile.com/pc/5qkGbbUK-ouUxkskykmqc-4UiW_WfELml0M2hLy_yCLEvud6kpFOWKITUPDAZ-kDjoJrvItByyS4HHaWdXyO_DrXIaWutJls2xCVbatkhjUNNiIYVnHvzugZCuBITtvjski7YaLlHpkrQUr5euoQrg.jpg', 'http://qcloud.dpfile.com/pc/948v5vi5otZ8SAXI53hlXZi9ic_s1Zv-yGueWeIp3CcpJ36aly4bqURKSnWlKZwijoJrvItByyS4HHaWdXyO_DrXIaWutJls2xCVbatkhjUNNiIYVnHvzugZCuBITtvjski7YaLlHpkrQUr5euoQrg.jpg', 'http://qcloud.dpfile.com/pc/lz-WTnCstOM3YE9DuBnoxXDULVC-0i13snJISrX0xBF6lo_kpsFhbNx1yHyVDqGrjoJrvItByyS4HHaWdXyO_DrXIaWutJls2xCVbatkhjUNNiIYVnHvzugZCuBITtvjski7YaLlHpkrQUr5euoQrg.jpg']") ON DUPLICATE KEY UPDATE shop_id = "110418500", comment_user_name = "dpuser_1588557440", comment_star = "5", comment_score = "课程：非常好 师资：非常好 环境：非常好 ", comment_content = "瑞思英语梨园校区的环境超级棒，老师非常热情，对孩子也特别耐心。去试听完觉得无论是从硬件条件还是软实力，不愧是教育培训行业的领头羊。", comment_user_img = "https://p0.meituan.net/userheadpic/bun.png", comment_imgs = "['http://qcloud.dpfile.com/pc/5qkGbbUK-ouUxkskykmqc-4UiW_WfELml0M2hLy_yCLEvud6kpFOWKITUPDAZ-kDjoJrvItByyS4HHaWdXyO_DrXIaWutJls2xCVbatkhjUNNiIYVnHvzugZCuBITtvjski7YaLlHpkrQUr5euoQrg.jpg', 'http://qcloud.dpfile.com/pc/948v5vi5otZ8SAXI53hlXZi9ic_s1Zv-yGueWeIp3CcpJ36aly4bqURKSnWlKZwijoJrvItByyS4HHaWdXyO_DrXIaWutJls2xCVbatkhjUNNiIYVnHvzugZCuBITtvjski7YaLlHpkrQUr5euoQrg.jpg', 'http://qcloud.dpfile.com/pc/lz-WTnCstOM3YE9DuBnoxXDULVC-0i13snJISrX0xBF6lo_kpsFhbNx1yHyVDqGrjoJrvItByyS4HHaWdXyO_DrXIaWutJls2xCVbatkhjUNNiIYVnHvzugZCuBITtvjski7YaLlHpkrQUr5euoQrg.jpg']" '''

        try:
                # 执行sql语句
                cur.execute(sqlstat)

                # data = cur.fetchall()
                #
                # for ele in data:
                #         print(ele)
                # print(data)

                # 提交到数据库执行
                db.commit()
        except:
                # Rollback in case there is any error
                db.rollback()

        db.close()

        server.close()


def main():
        with open('/Users/tangtonglong/PycharmProjects/Tools/new_comment-sql.sql', 'r') as f:
                file = f.readlines()
        for ele in file:
                tmpsql = ele
                modify_mysql_data(ele, '')


if __name__ == '__main__':
        main()