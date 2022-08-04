#Jakob Coughlan
#TO DO
#COMMENT SIZE
#UPLOAD TO TIK TOK
#AUTOMATE
from ast import Not
from genericpath import exists
from selenium.webdriver import Firefox, FirefoxOptions
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import praw
from time import sleep
import tiktokvoices
import moviepy
import moviepy.editor as mp
import os

# enter your reddit username and password so bot
# can get reddit comments
redditUserName = ""
redditPassword = ""

subreddit = "AskReddit"

numOfComments = 5

voice = tiktokvoices
voicechoice = "en_us_002"

backgroundVideo = "backgroundvideo.mp4"

timeout = 10

if (redditUserName == None or redditUserName == "" \
    or redditPassword == None or redditPassword == ""):
    print("DID NOT ENTER REDDIT USERNAME AND PASSWORD INTO SCRIPT\
    \n please enter them now")
    redditUserName = input("Enter your reddit username:")
    redditPassword = input("Enter your reddit password:")

if exists(backgroundVideo) != True:
    print("ENTER BACKGROUND VIDEO INTO VARIABLE")
    exit()


#this logs into the Reddit API, helps navigate through reddit and find posts
print("logging into Reddit API")
r = praw.Reddit(    
    client_id="kSwWjkQzxcSxMRa5Pff4Qg",
    client_secret=None,#"	nO3j7r47crkRc-ERAnSRT9nFbwke2w",
    password="vnHN4VoNDewg",
    user_agent="get the top comments",
    username="lightwing22",)

#opens firefox using selinium, used for screenshotting reddit posts and comments
def startFireFox():
    print("starting firefox")
    opts = FirefoxOptions()
    opts.add_argument("--headless")
    opts.set_preference("dom.push.enabled", False)  # kill notification popup
    drv = Firefox(options=opts)
    drv.set_window_size(720,1920)
    print("loaded firefox")
    return drv

#logs into reddit in firefox
def login(drv):
    print("logging into reddit on firefox")

    drv.get("https://www.reddit.com/login")

    user = drv.find_element(By.ID, "loginUsername")
    user.send_keys(redditUserName)

    pwd = drv.find_element(By.ID, "loginPassword")
    pwd.send_keys(redditPassword)

    btn = drv.find_element(By.CSS_SELECTOR, "button[type='submit']")
    btn.click()

    sleep(timeout)

    print("logged in to reddit on firefox")

comments_in_order = []
#gets content from reddit
def getContent(drv,sub):
    for post in r.subreddit(sub).hot(limit=1):
        cmts = "https://www.reddit.com" + post.permalink
        print("Post:"+cmts)
        drv.get(cmts)

        # captures the post 
        id = f"t3_{post.id}"
        comments_in_order.append(id)
        try:
            print("post id:"+id)
            cmt = WebDriverWait(drv, timeout).until(
                lambda x: x.find_element(By.ID,id))
        except TimeoutException:
            print("Page load timed out...")
        else:
            print("----captured post----")
            print("author:"+str(post.author))
            print("score:"+str(post.score))
            print("title:"+str(post.title))

            cmt.screenshot(id + ".png")
            video = {(id+".png",id+".mp3")}
            voice.tts(voicechoice, str(post.title), id + ".mp3","true")

        # captures the comments
        loopnum = 0
        for comment in post.comments:
            loopnum = loopnum + 1

            if loopnum > numOfComments:
                break
                
            if len(comment.body)>200:
                print("skip comment")
                continue

            id = f"t1_{comment.id}"
            comments_in_order.append(id)

            try:
                print("comment id:"+id)
                cmt = WebDriverWait(drv, timeout).until(
                    lambda x: x.find_element(By.ID,id))
            except TimeoutException:
                print("Page load timed out...")
            else:
                cmt.screenshot(id + ".png")
                print("----captured comment----")
                print("author:"+str(comment.author))
                print("score:"+str(comment.score))
                print("comment:"+str(comment.body))

                voice.tts(voicechoice, str(comment.body), id + ".mp3","true")

#video edit
def videoEdit():
    print("starting making video")
    video = mp.VideoFileClip(backgroundVideo)
    video = video.subclip(52,130)
    video.set_start

    audio_together = []

    for sound_bit in comments_in_order:
        print(f"getting {sound_bit}.mp3")
        content = mp.AudioFileClip(f"{sound_bit}.mp3")
        print(content.duration)
        audio_together.append(content)

    video_together = [video]
    num = 0
    time_ellapsed = 0

    for pic in comments_in_order:
        
        print(f"getting {pic}.png")

        content = (mp.ImageClip(f"{pic}.png")
            .set_duration(video.duration)
            # .resize(width=1080) # if you need to resize...
            .margin(right=8, top=8, opacity=0) # (optional) logo-border padding
            .set_pos(("center")))
        
        content = content.subclip(0,audio_together[num].duration)
        content = content.set_start(time_ellapsed)
        time_ellapsed = time_ellapsed + audio_together[num].duration

        video_together.append(content)
        num = num + 1

    final = mp.CompositeVideoClip(video_together)
    final_audio = mp.concatenate_audioclips(audio_together)
    final = final.set_audio(final_audio)
    final = final.subclip(0,time_ellapsed)
    final.write_videofile("tiktok.mp4")
    print("combined")

def cleanUpFiles():
    print("clearing files")
    for files in comments_in_order:
        print(f"deleting:{files}")
        os.remove(f"{files}.mp3")
        os.remove(f"{files}.png")
    print("all done.")

browser = startFireFox()
login(browser)
getContent(browser,subreddit)            
print("closing firefox")
browser.close()
videoEdit()
cleanUpFiles()


