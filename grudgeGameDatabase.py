# mysql.connector from https://dev.mysql.com/downloads/connector/python/
import mysql.connector

# creds to the TA led database lecture  https://scs.hosted.panopto.com/Panopto/Pages/Viewer.aspx?id=1e68b000-e15c-4e52-af04-ac6800f82ae8
# for its guidance on using mysql through python

# prior to running my game one needs to install mysql through https://dev.mysql.com/downloads/mysql/
# and then pip install mysql-connector-python
# then set up mysql using the setup interface and set the server user to root and password to password


grudgeGamedb = mysql.connector.connect(host= 'localhost', user='root', password= 'password')

cursor = grudgeGamedb.cursor()

cursor.execute("CREATE DATABASE IF NOT EXISTS GrudgeGame")

grudgeGamedb = mysql.connector.connect(host= 'localhost', user='root', password= 'password', database="GrudgeGame")

cursor = grudgeGamedb.cursor()


cursor.execute("CREATE TABLE IF NOT EXISTS Leaderboard(\
                ID int PRIMARY KEY AUTO_INCREMENT,\
                Username varchar(255) NOT NULL,\
                Score int NOT NULL)")

grudgeGamedb.commit()
    

def getLeaderboard():
    cursor.execute('SELECT Username, Score FROM Leaderboard ORDER BY Score DESC')
    leaderBoard = [row for row in cursor.fetchall()]
    return leaderBoard

def updateTable(username, score):
    cursor.execute('SELECT Username, Score FROM Leaderboard ORDER BY Score DESC')
    usersList = [row for row in cursor.fetchall()]
    cursor.execute('SELECT Username, Score FROM Leaderboard ORDER BY Score DESC')
    userNameList = [row[0] for row in cursor.fetchall()]

    for name, dbScore in usersList:
        if username == name and score > dbScore:
            cursor.execute('UPDATE Leaderboard SET Score ='+str(score)+' WHERE Username= "'+username+'"')
    
    if username not in userNameList:
        cursor.execute("INSERT INTO Leaderboard (Username, Score) VALUES ('"+username+"', "+str(score)+")")

    grudgeGamedb.commit()
    

    


