#!/usr/bin/env python 
#coding=utf-8
#
import pymysql
import time


class DB_MySQL:

    def __init__(self):
        pass

    pass    

def test():
    conn = pymysql.connect(host='localhost', user='root', passwd='', port=3306, db='test',charset='utf8')        
    try:
        cur = conn.cursor()

        stat = cur.execute('CREATE DATABASE IF NOT EXISTS test')
        print('CREATE  status:' + str(stat))
        cur.execute("USE test")

        cur.execute("SELECT VERSION()")
        data = cur.fetchone()
        print('Database version is %s' % data)

        cur.execute('DROP TABLE IF EXISTS tb_test')
        cur.execute('CREATE TABLE tb_test (id INT, info VARCHAR(20))')

        value = [1, 'hi rollen']
        cur.execute('INSERT INTO tb_test VALUES(%s, %s)', value)

        values = []
        for idx in range(20):
            values.append((idx, '你好, rollen' + str(idx)))    
        stat = cur.executemany('INSERT INTO tb_test VALUES(%s, %s)', values)
        print('executemany  status:' + str(stat))
        
        cur.execute('UPDATE tb_test SET info = "这是 roolen" WHERE id = 3')

        stat = cur.execute('DELETE FROM tb_test WHERE id = 20')
        print('DELETE status:%s' % stat) 

        conn.commit()
        
        cur.execute('SELECT * FROM tb_test')
        data = cur.fetchall()
        for row in data:
            print(str(row[1]))
        
        cur.close()

    except Exception as ex:
        print(ex)    
    finally:
        if conn:
            conn.close()
    pass

test()