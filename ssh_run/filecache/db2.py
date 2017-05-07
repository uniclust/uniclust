#!/usr/bin/python
# -*- coding: utf-8 -*

import global_vars2
import MySQLdb

def db_connect( host, user, passwd, db ):
    return MySQLdb.connect( host, user, passwd, db );

def db_get_cursor ( db):
    return db.cursor();

def db_execute_query( curs, query ):
    return curs.execute( query );

def db_fetchall( curs ):
    return curs.fetchall();

def db_escape_string( db ):
    return db.escape_string("'");
