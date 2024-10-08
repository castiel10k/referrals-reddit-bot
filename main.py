import praw
import datetime, time
import random
import os
import sqlite3
def getInformation(row):
    #print(row[0], row[1])
    query = "SELECT a.title, b.body FROM referralTitle a, referralBody b WHERE a.id = ? AND b.id = ?"
    cursor.execute(query, (row[0], row[1]))
    print(cursor.fetchall())
    return cursor.fetchall()


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
list = []
for row in cursor.execute("SELECT * FROM linkTitleBody"):
    information = getInformation(row)
    postObject.fillInformation(information)
    list.append(postObject)

result  = cursor.execute("SELECT * FROM linkTitleBody").fetchall()

#randomizeTable()
#cycleTable()

print(result)

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




submitPost(config['wealthsimpleTitle'],config['wealthsimpleBody'],config['subreddit'])

submitPost("[CANADA] "+config['wealthsimpleTitle'],config['wealthsimpleBody'],config['subreddit3'])

submitPost("[CANADA] "+config['wealthsimpleTitle'],config['wealthsimpleBody'],config['subreddit4'])


submitPost(config['amexTitle'],config['amexBody'],config['subreddit'])

submitPost("[CANADA] "+config['amexTitle'],config['amexBody'],config['subreddit3'])

submitPost("[CANADA] "+config['amexTitle'],config['amexBody'],config['subreddit4'])

submitPost(config['shakepayTitle'],config['shakepayBody'],config['subreddit'])

submitPost("[CANADA] "+config['shakepayTitle'],config['shakepayBody'],config['subreddit3'])

submitPost("[CANADA] "+config['shakepayTitle'],config['shakepayBody'],config['subreddit4'])


submitPost(config['newtonTitle'],config['newtonBody'],config['subreddit'])

submitPost("[CANADA] "+config['newtonTitle'],config['newtonBody'],config['subreddit3'])

submitPost("[CANADA] "+config['newtonTitle'],config['newtonBody'],config['subreddit4'])


submitPost(config['rakutenTitle'],config['rakutenBody'],config['subreddit'])

submitPost("[CANADA] "+config['rakutenTitle'],config['rakutenBody'],config['subreddit3'])

submitPost("[CANADA] "+config['rakutenTitle'],config['rakutenBody'],config['subreddit4'])


submitPost(config['pcTitle'],config['pcBody'],config['subreddit'])

submitPost("[CANADA] "+config['pcTitle'],config['pcBody'],config['subreddit4'])

submitPost("[CANADA] "+config['pcTitle'],config['pcBody'],config['subreddit3'])


submitPost(config['timTitle'],config['timBody'],config['subreddit'])

submitPost("[CANADA] "+config['timTitle'],config['timBody'],config['subreddit3'])

submitPost("[CANADA] "+config['timTitle'],config['timBody'],config['subreddit4'])


submitPost(config['virgoTitle'],config['virgoBody'],config['subreddit'])

submitPost("[CANADA] "+config['virgoTitle'],config['virgoBody'],config['subreddit3'])

submitPost("[CANADA] "+config['virgoTitle'],config['virgoBody'],config['subreddit4'])


submitPost(config['neoTitle'],config['neoBody'],config['subreddit'])

submitPost("[CANADA] "+config['neoTitle'],config['neoBody'],config['subreddit3'])

submitPost("[CANADA] "+config['neoTitle'],config['neoBody'],config['subreddit4'])


submitPost(config['eqTitle'],config['eqBody'],config['subreddit'])

submitPost("[CANADA] "+config['eqTitle'],config['eqBody'],config['subreddit3'])

submitPost("[CANADA] "+config['eqTitle'],config['eqBody'],config['subreddit4'])


submitPost(config['journieTitle'],config['journieBody'],config['subreddit'])

submitPost("[CANADA] "+config['journieTitle'],config['journieBody'],config['subreddit3'])

submitPost("[CANADA] "+config['journieTitle'],config['journieBody'],config['subreddit4'])

#submitPost(config['tangerineTitle'],config['tangerineBody'],config['subreddit'])

#submitPost(config['tangerineTitle'],config['tangerineBody'],config['subreddit2'])

#submitPost("[CANADA] "+config['tangerineTitle'],config['tangerineBody'],config['subreddit3'])

#submitPost("[CANADA] "+config['tangerineTitle'],config['tangerineBody'],config['subreddit4'])

submitPost(config['kohoTitle'],config['kohoBody'],config['subreddit'])

submitPost("[CANADA] "+config['kohoTitle'],config['kohoBody'],config['subreddit3'])

submitPost("[CANADA] "+config['kohoTitle'],config['kohoBody'],config['subreddit4'])

print("\n")
print("done")