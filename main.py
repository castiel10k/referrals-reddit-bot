import praw
import datetime, time
import random
import os

def clearLog():
    os.remove("log.txt")

def printLog(title, newBody, subreddit_name):
    print(f"{title}\n{newBody}\n{subreddit_name}")
    f = open("log.txt",'a')
    print(f"{title}\n{newBody}\n{subreddit_name}\n", file=f)

def sleepRandom(): #delay between posts
    interval = random.randint(34, 480)
    print(f"time is currently at an interval of {interval}!")
    minutesToSleep = interval - datetime.datetime.now().minute % interval
    time.sleep(minutesToSleep * 60)
    

def submitPost(title,body,subreddit_name):
    
    sleepRandom() #delay between posts

    newBody = body.replace('~', '\n')
    printLog(title, newBody, subreddit_name)
    # Submit post
    
    subreddit = reddit.subreddit(subreddit_name)
    post = subreddit.submit(title, selftext=newBody)
    #print("\n")
    

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
    user_agent=config['user_agent']
)

print("start")
print("\n")
clearLog()
#print(config)


# Select subreddit and create post
subreddit_name=config['subreddit']

submitPost(config['neoTitle'],config['neoBody'],subreddit_name)
submitPost(config['eqTitle'],config['eqBody'],subreddit_name)
submitPost(config['kohoTitle'],config['kohoBody'],subreddit_name)
submitPost(config['wealthsimpleTitle'],config['wealthsimpleBody'],subreddit_name)
submitPost(config['amexTitle'],config['amexBody'],subreddit_name)
submitPost(config['shakepayTitle'],config['shakepayBody'],subreddit_name)
submitPost(config['newtonTitle'],config['newtonBody'],subreddit_name)
submitPost(config['tangerineTitle'],config['tangerineBody'],subreddit_name)
submitPost(config['rakutenTitle'],config['rakutenBody'],subreddit_name)
submitPost(config['timTitle'],config['timBody'],subreddit_name)

subreddit_name=config['subreddit2']
submitPost(config['tangerineTitle'],config['tangerineBody'],subreddit_name)

print("\n")
print("done")