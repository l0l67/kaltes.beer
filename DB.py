import sqlite3

db = sqlite3.connect('database.db', check_same_thread=False)

def newGuestbookEntry(ip, username, message, website):
    cursor = db.execute('insert into guestbook (ipAddress, username, message, website, entrydate) values (?, ?, ?, ?, CURRENT_TIMESTAMP)', [ip, username, message, website])
    db.commit()
    return cursor.lastrowid

def getMessages():
    cursor = db.execute('select username, website, message, entrydate from guestbook')
    return cursor.fetchall()

def setLastPost(ip):
    if _IPexists(ip):
        db.execute('update clients set postdate = CURRENT_TIMESTAMP where ipAddress = ?', [ip])
    else:
        db.execute('insert into clients (ipAddress, postdate) values (?, CURRENT_TIMESTAMP)', [ip])

def _IPexists(ip):
    cursor = db.execute('select exists(select 1 from clients where ipAddress = ?)', [ip]).fetchone()[0]
    return cursor == 1

def getLastEntry(ip):
    cursor = db.execute("select ipAddress, datetime(postdate, 'localtime') from clients where ipAddress = ?", [ip])
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

    db.execute('create table if not exists guestbook (id integer unique primary key AUTOINCREMENT, ipAddress not null references clients(ipAdress), username text not null, message text, website text, entrydate datetime not null)')
    db.execute('create table if not exists clients (id integer unique primary key AUTOINCREMENT, ipAddress text not null, postdate datetime not null)')

if __name__ == '__main__':
    createTable()