import sqlite3
import json
import xlrd
conn=sqlite3.connect('college_db.sqlite3')
cur=conn.cursor()

cur.executescript('''
drop table if exists Stream_Uni;
Drop table if exists College_Uni;
Drop table if exists College_PU;
Drop table if exists Area;
Drop table if exists Stream_pu;

Create table Stream_uni(
    id integer not null primary key autoincrement unique,
    stream  text unique);

Create table College_PU(
    rank integer not null primary key autoincrement unique,
    college text unique,
    link text unique,
    area_id integer,
    science integer,
    commerce integer,
    arts integer);
Create table College_Uni(
    rank integer not null primary key autoincrement unique,
    college text unique,
    link text unique,
    area_id integer,
    stream_uni_id integer);
Create table Area(
    id integer not null primary key autoincrement unique,
    name text unique);

    ''')
fname= "Uni_colleges.xlsx"
wb=xlrd.open_workbook(fname)#f=open(fname).readlines()
sheet=wb.sheet_by_index(0)
#json_data=json.loads(f)

for i in range(1,62):
    college=sheet.cell_value(i,0)
    link=sheet.cell_value(i,1)
    area=sheet.cell_value(i,2)
    rank=int(sheet.cell_value(i,3))
    stream=sheet.cell_value(i,4)
    print(college)
    cur.execute("insert or ignore into Area(name) values(?)",(area,))
    conn.commit()
    cur.execute("select id from Area where name= ?",(area,))
    area_id= int(cur.fetchone()[0])


    cur.execute("insert or ignore into Stream_uni(stream) values(?)", (stream,))
    conn.commit()
    cur.execute("select id from Stream_uni where stream= ?", (stream,))
    stream_uni_id = int(cur.fetchone()[0])

    cur.execute("Insert or replace into College_Uni (rank,college,link,area_id,stream_uni_id) values (?,?,?,?,?)",(rank,college,link,area_id,stream_uni_id))
    conn.commit()
fname= "PU colleges.xlsx"
wb=xlrd.open_workbook(fname)#f=open(fname).readlines()
sheet=wb.sheet_by_index(0)
#json_data=json.loads(f)

for i in range(1,22):
    college=sheet.cell_value(i,0)
    link=sheet.cell_value(i,1)
    area=sheet.cell_value(i,2)
    rank=int(sheet.cell_value(i,6))
    science=sheet.cell_value(i,3)
    commerce = sheet.cell_value(i, 4)
    arts = sheet.cell_value(i, 5)
    print(college)
    cur.execute("insert or ignore into Area(name) values(?)",(area,))
    cur.execute("select id from Area where name= ?",(area,))
    area_id= int(cur.fetchone()[0])
    conn.commit()

    cur.execute("Insert or replace into College_PU (rank,college,link,area_id, science, commerce, arts) values (?,?,?,?,?,?,?)",(rank,college,link,area_id,science,commerce,arts))
    conn.commit()
