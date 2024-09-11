import praw
import datetime, time
import random

def sleepRandom():
    interval = random.randint(4, 26)
    print(f"time is currently at an interval of {interval}!")
    minutesToSleep = interval - datetime.datetime.now().minute % interval
    time.sleep(minutesToSleep * 60)
    

def submitPost(title,body,subreddit):
    sleepRandom()
    # Submit post
    # post = subreddit.submit(title, selftext=body)
    newBody = body.replace('~', '\n')
    print(f"{title}")
    print(f"{newBody}")
    print(f"{subreddit}")
    print("\n")

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
print("\n")
print("\n")
print("\n")
#print(config)


# Select subreddit and create post
subreddit=config['subreddit']

submitPost(config['tangerineTitle'],config['tangerineBody'],subreddit)
submitPost(config['neoTitle'],config['neoBody'],subreddit)
submitPost(config['eqTitle'],config['eqBody'],subreddit)
submitPost(config['kohoTitle'],config['kohoBody'],subreddit)
submitPost(config['wealthsimpleTitle'],config['wealthsimpleBody'],subreddit)
submitPost(config['amexTitle'],config['amexBody'],subreddit)
submitPost(config['shakepayTitle'],config['shakepayBody'],subreddit)
submitPost(config['newtonTitle'],config['newtonBody'],subreddit)

subreddit="OrangeKeys"
submitPost(config['tangerineTitle'],config['tangerineBody'],subreddit)

print("done")