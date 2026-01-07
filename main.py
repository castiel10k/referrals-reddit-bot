import praw
import datetime, time
import random
import os
import sqlite3
from urllib.parse import urlparse
from urllib.parse import parse_qs
import configparser
import prawcore
import json

class referral:
  def __init__(self, information):
    self.title = information[0][0]
    self.body = information[0][1]
    self.subreddit = information[1]
  
  def to_dict(self):
    """Convert referral to dictionary for JSON serialization"""
    return {
        'title': self.title,
        'body': self.body,
        'subreddit': self.subreddit
    }
  
  def get_key(self):
    """Generate unique key for this referral"""
    return f"{self.title}|||{self.subreddit}"

def getInformation(row):
    query = "SELECT a.title, b.body FROM referralTitle a, referralBody b WHERE a.id = ? AND b.id = ?"
    cursor.execute(query, (row[0], row[1]))
    listTemp = cursor.fetchall()
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
    f = open("log.txt", 'a', encoding='utf-8')
    print(f"{title}\n{newBody}\n{subreddit_name}\n{url}\n", file=f)

def load_post_history():
    """Load the history of posted referrals"""
    if os.path.exists('post_history.json'):
        try:
            with open('post_history.json', 'r') as f:
                data = json.load(f)
                return set(data.get('posted', [])), data.get('queue', [])
        except:
            return set(), []
    return set(), []

def save_post_history(posted_set, queue):
    """Save the history of posted referrals and current queue"""
    with open('post_history.json', 'w') as f:
        json.dump({
            'posted': list(posted_set),
            'queue': queue,
            'last_updated': datetime.datetime.now().isoformat()
        }, f, indent=2)

def get_next_referrals_to_post(all_referrals, posted_set, saved_queue):
    """
    Get the next batch of referrals to post.
    If we have a saved queue, continue from there.
    Otherwise, create a new shuffled queue excluding already posted items.
    """
    # Convert all_referrals to list of dicts with keys
    all_refs_with_keys = [(ref, ref.get_key()) for ref in all_referrals]
    
    # If we have a saved queue, restore it
    if saved_queue:
        print(f"Resuming from saved queue with {len(saved_queue)} items remaining...")
        # Reconstruct referral objects from saved queue
        queue_refs = []
        for item in saved_queue:
            # Find matching referral in all_referrals
            for ref, key in all_refs_with_keys:
                if key == item['key']:
                    # Check if this referral is still enabled
                    if is_referral_enabled(ref.title):
                        queue_refs.append(ref)
                    else:
                        print(f"⊘ Removing disabled referral from saved queue: {ref.title}")
                    break
        
        # If queue is now empty after filtering disabled items, create a new queue
        if not queue_refs:
            print("Saved queue is empty after filtering disabled items. Creating new queue...")
            saved_queue = []  # Clear saved queue to trigger new queue creation below
        else:
            return queue_refs
    
    # Check if we've posted everything - if so, reset
    all_keys = set([key for _, key in all_refs_with_keys])
    if all_keys.issubset(posted_set):
        print("All referrals have been posted! Starting a new cycle...")
        posted_set.clear()
        save_post_history(posted_set, [])
    
    # Create new queue with unposted items (already filtered by is_referral_enabled earlier)
    unposted_refs = [ref for ref, key in all_refs_with_keys if key not in posted_set]
    
    # Optimize queue to avoid consecutive same subreddits
    optimized_queue = optimize_queue_for_subreddits(unposted_refs)
    
    print(f"Created new queue with {len(optimized_queue)} unposted items...")
    return optimized_queue

def optimize_queue_for_subreddits(queue):
    """
    Reorder queue to minimize consecutive posts to same subreddit.
    Uses a greedy algorithm to space out same-subreddit posts.
    """
    if len(queue) <= 1:
        return queue
    
    # Group by subreddit
    by_subreddit = {}
    for ref in queue:
        if ref.subreddit not in by_subreddit:
            by_subreddit[ref.subreddit] = []
        by_subreddit[ref.subreddit].append(ref)
    
    # Build optimized queue
    optimized = []
    last_subreddit = None
    
    while any(by_subreddit.values()):
        # Get available subreddits (those that still have posts and aren't the last one used)
        available = [sub for sub, posts in by_subreddit.items() 
                    if posts and sub != last_subreddit]
        
        # If no available subreddits (all remaining are same as last), use any
        if not available:
            available = [sub for sub, posts in by_subreddit.items() if posts]
        
        if not available:
            break
        
        # Pick a random available subreddit
        chosen_sub = random.choice(available)
        ref = by_subreddit[chosen_sub].pop(0)
        optimized.append(ref)
        last_subreddit = chosen_sub
        
        # Clean up empty lists
        if not by_subreddit[chosen_sub]:
            del by_subreddit[chosen_sub]
    
    return optimized

def sleepRandom():
    # Conservative delays to avoid bans
    # Minimum 48 hours, maximum 96 hours (2-4 days)
    interval = random.randint(48, 96)
    print(f"⏰ Waiting {interval} hours until next post...")
    print(f"Current time: {datetime.datetime.now()}")
    print(f"Next post at: {datetime.datetime.now() + datetime.timedelta(hours=interval)}")
    for x in range(interval*60):
        if x % 60 == 0:  # Print every hour
            hours_remaining = (interval*60 - x) // 60
            print(f"⏳ {hours_remaining} hours remaining... (Current: {datetime.datetime.now()})")
        time.sleep(60)

def submitPost(title, body, subreddit_name, posted_set, remaining_queue, last_subreddit, current_account):
    """Submit post and track it in history. Returns the subreddit posted to and postpone flag."""
    newBody = body
    ref_key = f"{title}|||{subreddit_name}"
    
    # Check if posting to same subreddit as last post
    if last_subreddit == subreddit_name:
        # Check if we can postpone this post
        different_subs_available = any(r.subreddit != subreddit_name for r in remaining_queue)
        
        if different_subs_available:
            print(f"⚠ Same subreddit as last post (r/{subreddit_name}), postponing this post...")
            # Don't post this one, signal to skip it for now
            return last_subreddit, True  # Signal that we postponed
        else:
            print(f"⏰ Posting to same subreddit (r/{subreddit_name}) - adding 18 hour delay")
            time.sleep(64800)  # 18 hours delay (18 * 3600 seconds)
    
    try:
        subreddit = reddit.subreddit(subreddit_name)
        post = subreddit.submit(title, selftext=newBody)
        printLog(f"[{current_account}] {title}", newBody, subreddit_name, post.shortlink if post.shortlink is not None else "N/A")
        
        # Mark as posted
        posted_set.add(ref_key)
        
        # Save updated history with remaining queue
        queue_to_save = [{'key': r.get_key(), 'title': r.title, 'subreddit': r.subreddit} 
                         for r in remaining_queue]
        save_post_history(posted_set, queue_to_save)
        
        print(f"✓ Posted and tracked: {title} to r/{subreddit_name} using account: {current_account}")
        
    except Exception as e:
        print(f"✗ Failed to post: {title} to r/{subreddit_name} - {e}")
        # Don't mark as posted if it failed
        return last_subreddit, False
    
    sleepRandom()
    return subreddit_name, False

def save_refresh_token(token, account_name):
    """Save refresh token to config file for specific account"""
    config[account_name]['refresh_token'] = token
    with open('config.ini', 'w') as configfile:
        config.write(configfile)

def get_available_accounts():
    """Get list of all configured Reddit accounts"""
    accounts = []
    for section in config.sections():
        if section.startswith('ACCOUNT_'):
            accounts.append(section)
    return accounts

def authenticate_reddit_account(account_name):
    """Handle Reddit authentication with refresh token for specific account"""
    global reddit
    
    if account_name not in config:
        print(f"❌ Account {account_name} not found in config.ini")
        return False, None
    
    account_config = config[account_name]
    
    # Check if refresh token exists
    if 'refresh_token' in account_config and account_config['refresh_token']:
        print(f"Using saved refresh token for {account_name}...")
        reddit = praw.Reddit(
            client_id=account_config['client_id'],
            client_secret=account_config['client_secret'],
            refresh_token=account_config['refresh_token'],
            user_agent=account_config['user_agent'],
        )
        try:
            username = str(reddit.user.me())
            print(f"✓ Logged in as: {username} ({account_name})")
            return True, username
        except Exception as e:
            print(f"Refresh token failed for {account_name}: {e}")
            print("Need to re-authenticate...")
    
    # No refresh token or it failed - do manual OAuth
    print(f"Performing manual authentication for {account_name}...")
    reddit = praw.Reddit(
        client_id=account_config['client_id'],
        client_secret=account_config['client_secret'],
        redirect_uri=account_config['redirect_uri'],
        user_agent=account_config['user_agent'],
    )
    
    try:
        # Use keyword arguments to avoid deprecation warning
        auth_url = reddit.auth.url(
            scopes=["identity", "submit"], 
            state="login-referral", 
            duration="permanent"
        )
        print(f"\nPlease go to the following URL to authenticate {account_name}:\n{auth_url}\n")
        authorization_code = input(f"Enter the full redirect URL or just the code for {account_name}: ")
        
        # Parse code from URL if full URL was provided
        if 'code=' in authorization_code:
            parsed_url = urlparse(authorization_code)
            captured_value = parse_qs(parsed_url.query)['code'][0]
        else:
            captured_value = authorization_code
        
        reddit.auth.authorize(captured_value)
        username = str(reddit.user.me())
        print(f"✓ Logged in as: {username} ({account_name})")
        
        # Extract refresh token from the authorized Reddit instance
        refresh_token = None
        
        # Method 1: Direct access (PRAW 7.8+)
        if hasattr(reddit.auth, 'refresh_token'):
            refresh_token = reddit.auth.refresh_token
        
        # Method 2: Access via _core._authorizer (PRAW 7.7)
        elif hasattr(reddit, '_core') and hasattr(reddit._core, '_authorizer'):
            if hasattr(reddit._core._authorizer, 'refresh_token'):
                refresh_token = reddit._core._authorizer.refresh_token
        
        # Method 3: Access via _core._authorizer._refresh_token (some PRAW versions)
        elif hasattr(reddit, '_core') and hasattr(reddit._core, '_authorizer'):
            if hasattr(reddit._core._authorizer, '_refresh_token'):
                refresh_token = reddit._core._authorizer._refresh_token
        
        if refresh_token:
            save_refresh_token(refresh_token, account_name)
            print(f"✓ Refresh token saved for {account_name}! You won't need to log in manually next time.")
        else:
            print(f"⚠ Warning: Could not extract refresh token for {account_name}. You'll need to log in again next time.")
            print("   However, the script will continue with this session.")
        
        return True, username
        
    except prawcore.exceptions.ResponseException as e:
        print(f"ResponseException for {account_name}: {e.response.text}")
        return False, None
    except Exception as e:
        print(f"Unexpected error for {account_name}: {e}")
        import traceback
        traceback.print_exc()
        return False, None

# Load credentials
config = configparser.RawConfigParser()
config.read('config.ini')
clearLog()

# ============================================================================
# REFERRAL TOGGLES - Set to False to disable posting specific referrals
# ============================================================================
ENABLED_REFERRALS = {
    'tangerine': True,
    'neo': True,
    'koho': True,
    'wealthsimple': True,
    'rakuten': True,
    'simplycash': True,
    'shakepay': True,
    'newton': True,
    'tims': True,
    'pc': True,
    'virgocx': True,
    'journie': True,
}
# ============================================================================

def is_referral_enabled(title):
    """Check if a referral should be posted based on ENABLED_REFERRALS"""
    title_lower = title.lower()
    for keyword, enabled in ENABLED_REFERRALS.items():
        if keyword in title_lower:
            return enabled
    return True  # If not in the list, enable by default

# Connect to database
try:
    sqlDB = sqlite3.connect("database.db")
    print("Connected to the database successfully!")
except sqlite3.Error as e:
    print(f"Failed to connect to the database: {e}")
    if sqlDB:
        sqlDB.close()
    exit(1)

# Create cursor
cursor = sqlDB.cursor()

# Initialize database tables if they don't exist
def initialize_database():
    """Create database tables if they don't exist"""
    try:
        # Create subreddit table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS subreddit (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL
            )
        """)
        
        # Create referralTitle table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS referralTitle (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL
            )
        """)
        
        # Create referralBody table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS referralBody (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                body TEXT NOT NULL
            )
        """)
        
        # Create linkTitleBody table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS linkTitleBody (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title_id INTEGER,
                body_id INTEGER,
                is_tangerine INTEGER DEFAULT 0,
                FOREIGN KEY (title_id) REFERENCES referralTitle(id),
                FOREIGN KEY (body_id) REFERENCES referralBody(id)
            )
        """)
        
        sqlDB.commit()
        print("Database tables verified/created successfully!")
        
        # Check if tables have data
        cursor.execute("SELECT COUNT(*) FROM subreddit")
        subreddit_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM referralTitle")
        title_count = cursor.fetchone()[0]
        
        if subreddit_count == 0 or title_count == 0:
            print("\n⚠ WARNING: Database tables are empty!")
            print("Please populate your database with:")
            print("  - Subreddits (subreddit table)")
            print("  - Referral titles (referralTitle table)")
            print("  - Referral bodies (referralBody table)")
            print("  - Links between them (linkTitleBody table)")
            print("\nExiting...")
            sqlDB.close()
            exit(1)
            
    except sqlite3.Error as e:
        print(f"Database initialization error: {e}")
        sqlDB.close()
        exit(1)

initialize_database()

# Get subreddits
listSubreddits = []
for row in cursor.execute("SELECT * FROM subreddit").fetchall():
    temp = row[1]
    listSubreddits.append(temp)

# Get referrals
listReferrals = []
for row in cursor.execute("SELECT * FROM linkTitleBody").fetchall():
    information = getInformation(row)
    information.append(row[3])
    tempSubreddits = listSubreddits[:]
    if information[1]!=1:
        tempSubreddits.remove("OrangeKeys")
    for p in tempSubreddits:
        information[1]=p
        temp = referral(information)
        if temp.subreddit !="OrangeKeys" and temp.subreddit!="CanadaReferralCodes":
            temp.title = "🍁[CANADA]🍁 " + temp.title
        listReferrals.append(temp)

# Filter referrals
i=0
listTemp = []
for p in listReferrals:
    # Check if referral is enabled
    if not is_referral_enabled(p.title):
        print(f"⊘ Skipping disabled referral: {p.title}")
        continue
        
    listTemp.append(p)
    if "newton" in p.title.lower() or "shakepay" in p.title.lower() or "virgocx" in p.title.lower():
        pass
    else: 
        if "referralcodescrypto" in p.subreddit.lower():
            listTemp.remove(p)
    i+=1
listReferrals = listTemp

# Close database
sqlDB.close()

# Load post history
posted_set, saved_queue = load_post_history()
print(f"Loaded history: {len(posted_set)} posts already made")

# Get the queue of referrals to post (either resume saved queue or create new one)
queue_to_post = get_next_referrals_to_post(listReferrals, posted_set, saved_queue)

# Print queue
print(f"\nQueue to post ({len(queue_to_post)} items):")
for i, p in enumerate(queue_to_post):
    printLog(i, p.title, p.subreddit, "N/A")

# Get all available accounts
accounts = get_available_accounts()
if not accounts:
    print("\n❌ No accounts found in config.ini!")
    print("Please add accounts in the format:")
    print("[ACCOUNT_1]")
    print("client_id = ...")
    print("client_secret = ...")
    print("user_agent = ...")
    print("redirect_uri = ...")
    print("refresh_token = ")
    exit(1)

print(f"\n📋 Found {len(accounts)} account(s) in config: {', '.join(accounts)}")

# Authenticate all accounts
authenticated_accounts = []
for account_name in accounts:
    success, username = authenticate_reddit_account(account_name)
    if success:
        authenticated_accounts.append((account_name, username))
    else:
        print(f"⚠ Skipping {account_name} - authentication failed")

if not authenticated_accounts:
    print("\n❌ No accounts successfully authenticated. Exiting.")
    exit(1)

print(f"\n✓ Successfully authenticated {len(authenticated_accounts)} account(s)")

# Wait until next interval
interval = 1
print(f"time is currently at an interval of {interval}! and it is {datetime.datetime.now()} and will be {datetime.datetime.now() + datetime.timedelta(minutes=interval)}")
minutesToSleep = interval - datetime.datetime.now().minute % interval
time.sleep(minutesToSleep * 60)

print("\n" + "="*60)
print("START POSTING")
print("="*60 + "\n")

# Post referrals from queue, rotating through accounts
last_subreddit_posted = None
postponed_items = []  # Track items we need to postpone
account_index = 0  # Track which account to use next

for i, p in enumerate(queue_to_post):
    # Rotate to next account
    current_account_name, current_username = authenticated_accounts[account_index % len(authenticated_accounts)]
    
    # Re-authenticate with the current account
    success, username = authenticate_reddit_account(current_account_name)
    if not success:
        print(f"⚠ Failed to authenticate {current_account_name}, skipping this post")
        continue
    
    print(f"\n🔄 Using account: {current_username} ({current_account_name})")
    
    remaining = queue_to_post[i+1:]  # Get remaining items after this one
    
    last_subreddit_posted, postponed = submitPost(
        p.title, p.body, p.subreddit, 
        posted_set, remaining, last_subreddit_posted, current_username
    )
    
    if postponed:
        # Add to postponed list and skip for now
        print(f"  → Added to end of queue: {p.title}")
        postponed_items.append(p)
    
    # Move to next account for next post
    account_index += 1

# Post any postponed items at the end
if postponed_items:
    print(f"\n📋 Processing {len(postponed_items)} postponed items...")
    for p in postponed_items:
        # Rotate to next account
        current_account_name, current_username = authenticated_accounts[account_index % len(authenticated_accounts)]
        
        # Re-authenticate with the current account
        success, username = authenticate_reddit_account(current_account_name)
        if not success:
            print(f"⚠ Failed to authenticate {current_account_name}, skipping this post")
            continue
        
        print(f"\n🔄 Using account: {current_username} ({current_account_name})")
        
        remaining = []  # No more items after these
        last_subreddit_posted, _ = submitPost(
            p.title, p.body, p.subreddit,
            posted_set, remaining, last_subreddit_posted, current_username
        )
        
        account_index += 1

print("\n" + "="*60)
print("DONE")
print("="*60)
print(f"Total posts attempted in this session: {len(queue_to_post)}")
print(f"Total posts in history: {len(posted_set)}")
print(f"Accounts used: {', '.join([username for _, username in authenticated_accounts])}")