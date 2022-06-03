#!/usr/bin/python
import cgi
import cgitb;
cgitb.enable()
import pymysql
import json
import random
import os, sys
import binascii

DEBUG = False

if DEBUG:
    print("Status : 200 ok")
    print("Content-Type: text/plain;charset=utf-8")
    print("")
print("Content-Type: application/json\r\n\r\n")

#Connect to DB

servername  = "localhost"
username = "MyUserName" #Can't share this detail because other projects apis are also running on this server 
password = "MyDataBaseAccessPassword"
dbname = "price_module"
connection = pymysql.connect(host=servername,user=username,passwd=password,database=dbname,autocommit=True)
c = connection.cursor()
if c:
    try:
        form = cgi.FieldStorage()
        req = form['req'].value

        if req == 'updatePrice':
            response = {}
            type = form['type'].value
            price = form['price'].value
            if type == 'tbp':
                sql = "UPDATE price_list SET price = '{0}' WHERE type = 'tbp'".format(price)
            if type == 'dbp':
                sql = "UPDATE price_list SET price = '{0}' WHERE type = 'dbp'".format(price)
            c.execute(sql)
            connection.commit()
            if c.rowcount > 0:
                response['response'] = True
            else:
                response['response'] = False
            print(json.dumps(response))

        elif req == 'getPrice':
            response = {}
            sql = "SELECT price FROM price_list WHERE type = 'TBP'"
            c.execute(sql)
            data = c.fetchone()
            response['TBP']=data[0]
            sql = "SELECT price FROM price_list WHERE type = 'DBP'"
            c.execute(sql)
            data = c.fetchone()
            response['DBP']=data[0]
            print(json.dumps(response))

        elif req == 'clculatePrice':
            distance = form['distance'].value
            time = form['time'].value
            name = form['name'].value
            sql = "SELECT price FROM price_list WHERE type = 'TBP'"
            c.execute(sql)
            TBP = c.fetchone()[0]
            response = {}
            sql = "SELECT price FROM price_list WHERE type = 'DBP'"
            c.execute(sql)
            DBP = c.fetchone()[0]
            sql = "SELECT travalID FROM travel_detail"
            c.execute(sql)
            tt = c.fetchall()
            tid = []
            for point in tt:
                tid.append(point[0])

            price = (int(distance) * int(DBP)) + (int(time) * int(TBP))

            travalID = binascii.hexlify(os.urandom(5))
            while travalID in tid:
                travalID = binascii.hexlify(os.urandom(5))
            travalID = travalID.decode("utf-8")
            sql = "INSERT INTO travel_detail (name, Time, distance, totalprice, travalID) VALUES ('{0}', '{1}', '{2}', '{3}', '{4}')".format(name, time, distance, price, travalID)
            c.execute(sql)
            if c.rowcount > 0:
                response['response'] = True
                response['travalID'] = travalID
            else:
                response['response'] = False
            print(json.dumps(response))


        elif req == 'getDetails':
            response = {}
            travalID = form['travalID'].value
            sql = "SELECT * FROM travel_detail WHERE travalID = '{0}'".format(travalID)
            c.execute(sql)
            if c.rowcount > 0 :
                tmp = c.fetchone()
                response['response'] = True
                response['travalID'] = tmp[1]
                response['name'] = tmp[2]
                response['time'] = tmp[3]
                response['distance'] = tmp[4]
                response['totalPrice'] = tmp[5]
                response['timestamp'] = str(tmp[6])
            else:
                response['response'] = False
            print(json.dumps(response))

    except Exception as e:
        print("@@ERROR##",e)
else:
    print("Connection Failed")
c.close()
connection.close()
