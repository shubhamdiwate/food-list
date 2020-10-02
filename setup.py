import sqlite3
import pymysql

#conn_pym=pymysql.connect('localhost','root','fbotdb.sqlite')
#pym=conn_pym.cursor()

conn=sqlite3.connect('foodbotdb.sqlite')
cur=conn.cursor()

def fdic():
    i=0
    abc={}
    foods= cur.execute('SELECT fname FROM fprice')
    for fname in foods:
        abc[i]=fname[0]
        i=i+1
    l=len(abc)
    return abc,l

cur.execute('DROP TABLE IF EXISTS users')
cur.execute('DROP TABLE IF EXISTS foodlist')
cur.execute('DROP TABLE IF EXISTS fprice')
cur.execute('DROP TABLE IF EXISTS host')
cur.execute('CREATE TABLE users(name TEXT,no TEXT,payed TEXT,total_amount FLOAT)')
cur.execute('CREATE TABLE foodlist(no TEXT)')
cur.execute('CREATE TABLE fprice(fname TEXT,price FLOAT)')
cur.execute('CREATE TABLE host(id INT,name TEXT,no TEXT)')
cur.execute('INSERT INTO host (id) VALUES (0) ')
conn.commit()

