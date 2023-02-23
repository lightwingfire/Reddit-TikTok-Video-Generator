import sys
import json
import random
import datetime
sys.path.append('Make Tik Tok Python Files')
sys.path.append('Uploading Python Files')

from reddit_tiktok import reddit_tiktok
from TiktokBot import TiktokBot
import time

def goodHourToPost(x):
    times = [10,11,12,13,14,15,16,18,19]
    for r in times:
         if x == r:
              return True
         
    return False


tiktok_bot = TiktokBot()

with open("Config Files\\subredditConfig.json","r") as f:
            subredditConfigs = json.load(f)

subRedditKey = random.choice(list(subredditConfigs.keys()))

# subRedditKey = "askreddit"

subredditInfo = subredditConfigs[subRedditKey]

# tiktok_bot.upload.directUpload("tiktok.mp4")
print("Program starting")
while True:

    # subRedditKey = random.choice(list(subredditConfigs.keys()))
    subRedditKey = 'tifu'
    subredditInfo = subredditConfigs[subRedditKey]

    now = datetime.datetime.now()
    hour = now.hour
    x = hour
    print(subRedditKey)
    while x == hour and goodHourToPost(x):

        r = reddit_tiktok()
        r.setSubreddit(subRedditKey)
        r.setNumberOfComments(subredditInfo["Number of Comments"])
        r.readPost(subredditInfo["Read Post"])
        r.setVideoLength(subredditInfo["Length of Video"])
        r.setCallToAction(subredditInfo["Call to Action"])
        r.doCommentScreenshots(subredditInfo["Screenshot Comments"])
        r.setVideoSplitting(subredditInfo["Splitable"])
        r.setTesting(True)
        r.run()

        if r.succeedInMakingNewVideo():
            for video in r.getVideos():
                tiktok_bot.upload.directUpload(video)
                time.sleep(random.randint(61, 300))
                
            time.sleep(240)

        del r

        now = datetime.datetime.now()
        hour = now.hour
