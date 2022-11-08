#!/usr/bin/python3

feed_url = "http://feeds.feedburner.com/crunchyroll/rss/anime"
from time import sleep
from datetime import datetime
import feedparser
feed = None
import numpy as np
from trycourier import Courier
client = Courier(auth_token="pk_prod_70EE2WDWN0MQZ7PNJJNJD97C92WB")

titles = ["Black Summoner", "Overlord", "Parallel World Pharmacy", "The World's Finest Assassin Gets Reincarnated in Another World as an Aristocrat", "Skeleton Knight in Another World", "That Time I Got Reincarnated as a Slime", "I've Been Killing Slimes For 300 Years And Maxed Out My Level", "So I'm a Spider, So What?", "The Hidden Dungeon Only I Can Enter", "The Misfit of Demon King Academy"]

def get_time():
    time = datetime.now().strftime(r'%Y-%m-%d %H:%M:%S')
    return time

def get_new_entries(li1, li2):
    new_entries = []
    for entry in li1.entries:
        if entry not in li2.entries:
            new_entries.append(entry)
    return new_entries

def get_feed():
    new_feed = feedparser.parse(feed_url)
    if new_feed == feed:
        return None
    elif feed == None:
        return (new_feed, new_feed)
    else:
        return (new_feed, get_new_entries(new_feed, feed))

feeds = get_feed()
new_entries = None
if feeds != None:
    feed = feeds[0]
    new_entries = feeds[1]

new_notifications = []
if new_entries != None:
    if not type(new_entries) == list:
        new_entries = new_entries.entries 
    for entry in new_entries:
        for title in titles:
            if title in entry.title and "English" in entry.title:
                new_notifications.append(entry)
                print("New entry: " + entry.title)

if len(new_notifications) > 0:
    print(f"Notice: New notifications; {get_time()}")
    notification_list = ""
    for entry in new_notifications:
        notification = entry.title + ": " + entry.link + "\n"
        notification_list += notification
    resp = client.send_message(
        message={
            "to": {
            "discord": {
                "user_id": "632326478394032128",
            },
            },
            "template": "KZH15646DZ4KHMQBW514AT3QN7N6",
            "data": {
            "notification_block": f"{notification_list}",
            },
        }
    )
else: 
    print(f"Notice: No new notifications; {get_time()}")
