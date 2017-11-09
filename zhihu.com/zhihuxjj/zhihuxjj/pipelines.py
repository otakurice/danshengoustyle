# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymysql

def dbHandle():
    conn = pymysql.connect(
        host='服务器IP',
        user='用户名',
        passwd='密码',
        charset='utf8',
        use_unicode=False
    )
    return conn

class ZhihuxjjPipeline(object):
    def process_item(self, item, spider):
        dbObject = dbHandle()  # 写入数据库
        cursor = dbObject.cursor()
        sql = "insert into xiaojiejie.zhihu(user_name,sex,user_sign,user_avatar,user_url,user_add) values(%s,%s,%s,%s,%s,%s)"
        param = (item['user_name'],item['sex'],item['user_sign'],item['user_avatar'],item['user_url'],item['user_add'])
        try:
            cursor.execute(sql, param)
            dbObject.commit()
        except Exception as e:
            print(e)
            dbObject.rollback()
        return item
