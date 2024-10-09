import praw
import datetime, time
import random
import os
import sqlite3

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
    print(f"time is currently at an interval of {interval}! and it is {datetime.datetime.now()} and will be {datetime.datetime.now() + datetime.timedelta(minutes=interval)}")
    time.sleep(interval * 60)
    

def submitPost(title,body,subreddit_name):
    newBody=body
    #newBody = body.replace('~', '\n\n')
    try:
        # Submit post
        subreddit = reddit.subreddit(subreddit_name)
        #post = subreddit.submit(title, selftext=newBody)
        print("-------------------------------------------------------------")
        printLog(title, newBody, subreddit_name, post.shortlink if post.shortlink is not None else "N/A" )
        #printLog(title, newBody, subreddit_name, "N/A")
        #print("\n")
    except:
        pass
    #delay between posts
    sleepRandom()
    

# Function to read credentials from a text file
def read_config_file(file_path):
    config = {}
    with open(file_path, 'r') as file:
        for line in file:
            if '=' in line:
                key, value = line.strip().split('=', 1)
                config[key] = value
    return config

# Load credentials
config = read_config_file('config.txt')

# Initialize Reddit instance with credentials from file
reddit = praw.Reddit(
    client_id=config['client_id'],
    client_secret=config['client_secret'],
    username=config['username'],
    password=config['password'],
    user_agent=config['user_agent'],
    redirect_uri="http://localhost:8080"
)
#connect
sqlDB = sqlite3.connect("database.db")

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
    



#close db
sqlDB.close()
random.shuffle(listReferrals)

for p in listReferrals:
    print("Title: ",p.title,"\r\nBody: ",p.body,"\r\nSubreddit: ",p.subreddit)
    print("-------------------------------------------")

#result  = cursor.execute("SELECT * FROM linkTitleBody").fetchall()

#randomizeTable()
#cycleTable()

#print(result)

# Generate OAuth2 URL for user authorization
auth_url = reddit.auth.url(["identity", "submit"], "login-referral", "permanent")
print(f"Please go to the following URL to authenticate: {auth_url}")

# After the user authorizes your app and you get the code from the redirected URL:
authorization_code = input("Enter the code from the URL: ")
if authorization_code == '':
    authorization_code = config['secretkey']

# Use the authorization code to get an access token
reddit.auth.authorize(authorization_code)

# Verify that the authorization was successful
print(f"Logged in as: {reddit.user.me()}")

interval = 1
print(f"time is currently at an interval of {interval}! and it is {datetime.datetime.now()} and will be {datetime.datetime.now() + datetime.timedelta(minutes=interval)}")
minutesToSleep = interval - datetime.datetime.now().minute % interval
time.sleep(minutesToSleep * 60)

print("start")
print("\n")
clearLog()
#print(config)

for p in listReferrals:
    submitPost(p.title,p.body,p.subreddit)

print("\n")
print("done")