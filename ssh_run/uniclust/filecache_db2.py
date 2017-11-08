#!/usr/bin/python
# -*- coding: utf-8 -*

try:
    import pymysql
    pymysql.install_as_MySQLdb()
except ImportError:
    pass

def db_connect( host, user, passwd, db ):
    return pymysql.connect(host, user, passwd, db)

def db_get_cursor ( db):
    return db.cursor();

def db_execute_query( curs, query ):
    return curs.execute( query );

def db_fetchall( curs ):
    return curs.fetchall();