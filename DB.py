import sqlite3

db = sqlite3.connect('database.db', check_same_thread=False)

def newMessage(username, message, website):
    db.execute('insert into guestbook (username, message, website, entrydate) values (?, ?, ?, CURRENT_TIMESTAMP)', [username, message, website])
    db.commit()

def getMessages():
    cursor = db.execute('select * from guestbook')
    return cursor.fetchall()

def setLastPost(ip):
    if _IPexists(ip):
        db.execute('update lastcomment set postdate = CURRENT_TIMESTAMP where ipAddress = ?', [ip])
    else:
        db.execute('insert into lastcomment (ipAddress, postdate) values (?, CURRENT_TIMESTAMP)', [ip])

def _IPexists(ip):
    cursor = db.execute('select exists(select 1 from lastcomment where ipAddress = ?)', [ip]).fetchone()[0]
    return cursor == 1

def getLastComment(ip):
    cursor = db.execute("select ipAddress, datetime(postdate, 'localtime') from lastcomment where ipAddress = ?", [ip])
    return cursor.fetchall()



def getPostIdFromPostName(postname):
    cursor = db.execute('select id, checksum from archive where postname = ?', [postname])
    return cursor.fetchall()

def getPostList():
    cursor = db.execute('select title, postname, postdate from archive')
    return cursor.fetchall()

def getPostByPostName(postname):
    cursor = db.execute('select id, title, html, postdate, lastchanged, checksum from archive where postname = ?', [postname])
    return cursor.fetchall()

def addPost(postname, title, checksum, html):
    db.execute('insert into archive (postname, title, checksum, postdate, lastchanged, html) values (?, ?, ?, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, ?)', [postname, title, checksum, html])
    db.commit()

def updatePost(id, postname, title, checksum, html):
    db.execute('update archive set postname = ?, title = ?, lastchanged = CURRENT_TIMESTAMP, checksum = ?, html = ? where id = ?', [postname, title, checksum, html, id])
    db.commit()




def closeDB():
    db.close()

#Stuff:
def createTable():
    db.execute('create table if not exists archive (id integer unique primary key AUTOINCREMENT, postname text unique not null, title text not null, checksum text not null, postdate datetime not null, lastchanged datetime not null, html text not null)')

    db.execute('create table if not exists guestbook (id integer unique primary key AUTOINCREMENT, username text not null, message text, website text, entrydate datetime not null)')
    db.execute('create table if not exists lastcomment (id integer unique primary key AUTOINCREMENT, ipAddress text not null, postdate datetime not null)')

if __name__ == '__main__':
    createTable()