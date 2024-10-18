import praw
import datetime, time
import random
import os
import sqlite3
from urllib.parse import urlparse
from urllib.parse import parse_qs
import configparser
import prawcore

class referral:
  def __init__(self, information):
    self.title = information[0][0]
    self.body = information[0][1]
    self.subreddit = information[1]

def getInformation(row):
    #print(row[0], row[1]) isTangerine()
    query = "SELECT a.title, b.body FROM referralTitle a, referralBody b WHERE a.id = ? AND b.id = ?"
    cursor.execute(query, (row[0], row[1]))
    #print(cursor.fetchall())
    listTemp = cursor.fetchall()
    #listTemp.append(row[2])
    #print(listTemp)
    return listTemp 

def isTangerine():
    pass

def appendCanada():
    pass

def clearLog():
    try:
        os.remove("log.txt")
    except OSError:
        pass

def printLog(title, newBody, subreddit_name, url):
    print(f"{title}\n{newBody}\n{subreddit_name}\n{url}")
    f = open("log.txt",'a')
    print(f"{title}\n{newBody}\n{subreddit_name}\n{url}\n", file=f)

def sleepRandom(): #delay between posts
    interval = random.randint(36, 54)
    interval = 1
    print(f"time is currently at an interval of {interval}! and it is {datetime.datetime.now()} and will be {datetime.datetime.now() + datetime.timedelta(minutes=interval)}")
    time.sleep(interval * 60)
    

def submitPost(title,body,subreddit_name):
    newBody=body
    #newBody = body.replace('~', '\n\n')
    try:
        # Submit post
        subreddit = reddit.subreddit(subreddit_name)
        post = subreddit.submit(title, selftext=newBody)
        print("-------------------------------------------------------------")
        printLog(title, newBody, subreddit_name, post.shortlink if post.shortlink is not None else "N/A" )
        #printLog(title, newBody, subreddit_name, "N/A")
        #print("\n")
    except:
        pass
    #delay between posts
    sleepRandom()
    

# Function to read credentials from a text file
#def read_config_file(file_path):
#    config = {}
#    with open(file_path, 'r') as file:
#        for line in file:
#            if '=' in line:
#                key, value = line.strip().split('=', 1)
#                config[key] = value
#    return config

# Load credentials
#config = read_config_file('config.ini')
config = configparser.ConfigParser() #eventually TODO
config.read('config.ini')
clearLog()

# Initialize Reddit instance with credentials from file
reddit = praw.Reddit(
    client_id=config['DEFAULT']['client_id'],
    client_secret=config['DEFAULT']['client_secret'],
    username=config['DEFAULT']['username'],
    password=config['DEFAULT']['password'],
    user_agent=config['DEFAULT']['user_agent'],
    redirect_uri=config['DEFAULT']['redirect_uri'],
)
#connect


try:
    # Attempt to connect to the SQLite database
    sqlDB = sqlite3.connect("database.db")
    
    # If connection is successful, print success message
    print("Connected to the database successfully!")

except sqlite3.Error as e:
    # Print the error message if connection fails
    print(f"Failed to connect to the database: {e}")
    if sqlDB:
        sqlDB.close()

#finally:
    # Always close the connection if it was opened
    #if sqlDB:
    #    sqlDB.close()


#sqlDB = sqlite3.connect("database.db")
#------------------------------------
#if not exist create sample and crash
#------------------------------------
#create cursor
cursor = sqlDB.cursor()
#table = readSQL()

listSubreddits = []
for row in cursor.execute("SELECT * FROM subreddit").fetchall():
    #print(cursor.fetchall())
    #information = getInformation(row[1])
    #print(information)
    temp = row[1]
    #print(temp.title , temp.body)
    listSubreddits.append(temp)
#print(listSubreddits)

listReferrals = []
for row in cursor.execute("SELECT * FROM linkTitleBody").fetchall():
    #print(row)
    information = getInformation(row)
    information.append(row[3])
    #print(information)
    tempSubreddits = listSubreddits[:]
    if information[1]!=1:
            tempSubreddits.remove("OrangeKeys")
    for p in tempSubreddits:
        information[1]=p
        temp = referral(information)
        if temp.subreddit !="OrangeKeys" and temp.subreddit!="CanadaReferralCodes":
            temp.title = "[CANADA] " + temp.title
        listReferrals.append(temp)
    #print(temp.title , temp.body)

#tangerine toggle
listReferrals = [p for p in listReferrals if "tangerine" not in p.title.lower()]

i=0
listTemp = []
for p in listReferrals:
    listTemp.append(p)
    if "newton" in p.title.lower() or "shakepay" in p.title.lower() or "virgocx" in p.title.lower():
        pass
    else: 
        if "referralcodescrypto" in p.subreddit.lower():
            #printLog(i, p.title, p.subreddit, "N/A" )
            listTemp.remove(p)
    i+=1
listReferrals = listTemp

i=0
for p in listReferrals:
    printLog(i, p.title, p.subreddit, "N/A" )
    i+=1
#listReferrals = [p for p in listReferrals if "neo" not in p.title.lower()]

#listReferrals = [p for p in listReferrals if "koho" not in p.title.lower()]

#listReferrals = [p for p in listReferrals if "wealthsimple" not in p.title.lower()]

#listReferrals = [p for p in listReferrals if "rakuten" not in p.title.lower()]

#listReferrals = [p for p in listReferrals if "simplycash" not in p.title.lower()]

#listReferrals = [p for p in listReferrals if "shakepay" not in p.title.lower()]

#listReferrals = [p for p in listReferrals if "newton" not in p.title.lower()]

#listReferrals = [p for p in listReferrals if "tims" not in p.title.lower()]

#listReferrals = [p for p in listReferrals if "pc" not in p.title.lower()]

#listReferrals = [p for p in listReferrals if "virgocx" not in p.title.lower()]

#listReferrals = [p for p in listReferrals if "journie" not in p.title.lower()]

#i=0
# Check the filtered result
#for p in listReferrals:
#    print(p.title," ", i)
#    i+=1


#close db
sqlDB.close()

printLog("LIST BEFORE SHUFFLE", "", "", "N/A" )
i=0
for p in listReferrals:
    printLog(i, p.title, p.subreddit, "N/A" )
    i+=1

random.shuffle(listReferrals)


printLog("LIST AFTER SHUFFLE", "", "", "N/A" )
i=0
for p in listReferrals:
    printLog(i, p.title, p.subreddit, "N/A" )
    i+=1


#for p in listReferrals:
#    print("Title: ",p.title,"\r\nBody: ",p.body,"\r\nSubreddit: ",p.subreddit)
#    print("-------------------------------------------")

#result  = cursor.execute("SELECT * FROM linkTitleBody").fetchall()

#randomizeTable()
#cycleTable()

#print(result)
try:
    auth_url = reddit.auth.url(["identity", "submit"], "login-referral", "permanent")
    print(f"Please go to the following URL to authenticate: {auth_url}")
    authorization_code = input("Enter the code from the URL: ")
    parsed_url = urlparse(authorization_code)
    captured_value = parse_qs(parsed_url.query)['code'][0]
    print(captured_value,authorization_code)
    reddit.auth.authorize(captured_value)
    print(f"Logged in as: {reddit.user.me()}")       
except prawcore.exceptions.ResponseException as e:
    print(f"ResponseException: {e.response.text}")
except Exception as e:
    print(f"Unexpected error: {e}")
# Generate OAuth2 URL for user authorization
    
    

    # After the user authorizes your app and you get the code from the redirected URL:
    
    #print(captured_value)
    #config['DEFAULT']['secretkey'] = captured_value
    #with open('config.ini', 'w') as configfile:
    #    config.write(configfile)
    #config.read('config.ini')
    
    #updateConfig()

    #print(authorization_code)
    # Use the authorization code to get an access token
    

# Verify that the authorization was successful
print(f"Logged in as: {reddit.user.me()}")

interval = 1
print(f"time is currently at an interval of {interval}! and it is {datetime.datetime.now()} and will be {datetime.datetime.now() + datetime.timedelta(minutes=interval)}")
minutesToSleep = interval - datetime.datetime.now().minute % interval
time.sleep(minutesToSleep * 60)

print("start")
print("\n")

#print(config)
#while true:
for p in listReferrals:
    submitPost(p.title,p.body,p.subreddit)

print("\n")
print("done")