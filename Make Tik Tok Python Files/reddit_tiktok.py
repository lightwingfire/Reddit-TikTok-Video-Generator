#Jakob Coughlan
import praw
import tiktokvoices
from videoEdit import videoEdit
from Screenshot import screenshot
import moviepy.editor as mp
import os
import json
from comment import Content
from PIL import ImageDraw
from PIL import ImageFont
import textwrap
import PIL
import re
import random

class reddit_tiktok:
    def __init__(self):
        
        self.pastIdPath = 'Config Files\\previous post id.json'
        self.dahFont = 'Config Files\\OpenSans-Regular.ttf'
        self.passwordPath = "Config Files\\passwords.json"
        self.doubleSpeakPath = 'Config Files\\doublespeakwords.json'

        with open(self.passwordPath,"r") as f:
            codes = json.load(f)

        self.subreddit = "AskReddit"

        #session id of a tik tok page
        self.session_id = codes["tikTokSessionId"]

        self.numOfComments = 5

        self.voice = tiktokvoices
        self.voicechoice = "en_us_006"

        self.doScreenshotsOfComments = False

        #this logs into the Reddit API, helps navigate through reddit and find posts
        print("logging into Reddit API")
        self.r = praw.Reddit(    
            client_id= codes["redditClientId"],
            client_secret=None,
            password= codes["redditPassword"],
            user_agent=codes["userAgent"],
            username=codes["redditUserName"],)
        
        self.content_in_order = []
        self.foundNewVideo = False
        self.madeNewVideo = False
        self.callToAction = False
        self.testing = False
        self.isReadPost = False
        self.doRandomTextColor = True
        self.videoSplitting = False

        self.videoLength = 30

        self.videosToUpload = []

        self.screenshotter = screenshot()

    #gets content from reddit
    def getContent(self,sub):

        #search for posts that have not been done yet
        for post in self.r.subreddit(sub).hot(limit=15):

            # get post id
            id = f"t3_{post.id}"
            print(id)

            if self.wasMadeBefore(id):
                print("---SKIPPING POST---")
                continue
            
            self.addIdToSkipList(id)
            self.foundNewVideo = True
            self.screenshotter.start()
            self.screenshotter.setRedditPost(post.permalink)

            self.capturePost(post,id)
            if self.isReadPost:
                self.capturePostWords(id)
            else:
                self.getContentImages(id)

            if self.readPost:
                self.capturePostWords(id)

            for comment, i in zip(post.comments,range(self.numOfComments)):
                if i == self.numOfComments:
                    break
                self.captureComment(comment)
                id =  self.content_in_order[-1].getId()
                if self.doScreenshotsOfComments:
                    self.content_in_order[-1].setAudio(self.voiceContentEditor(str(comment.body), id))
                    self.getContentImages(id)
                else:
                    self.content_in_order[-1].setAudio(self.voiceContentEditor(str(comment.body), id,combine=False))
                    self.getContentImages(id,words=str(comment.body))

            
            print(self.content_in_order)
            return
        self.foundNewVideo = False
        
    def capturePost(self,post,id):

        print("----captured post----")
        print("author:"+str(post.author))
        print("score:"+str(post.score))
        print("title:"+str(post.title))


        newContent = Content()
        self.content_in_order.append(newContent)

        self.content_in_order[-1].setId(id)
        # self.content_in_order[-1].setImages(f"{id}.png")
        self.content_in_order[-1].setWords(post.selftext)
        self.content_in_order[-1].setTitle(post.title)
        self.content_in_order[-1].setAudio(self.voiceContentEditor(str(post.title), id))

    def capturePostWords(self,id):
        
        words = self.content_in_order[-1].getWords()
        self.doScreenshotsOfComments = False

        self.content_in_order[-1].setAudio(self.voiceContentEditor(words, id,combine=False))
        self.getContentImages(id,words=words)

    def captureComment(self,comment):
                
        id = f"t1_{comment.id}"

        print("----captured comment----")
        print("author:"+str(comment.author))
        print("score:"+str(comment.score))
        print("comment:"+str(comment.body))

        newContent = Content()
        self.content_in_order.append(newContent)

        self.content_in_order[-1].setId(id)
        self.content_in_order[-1].setWords(comment.body)

        # if self.doScreenshotsOfComments:
        #     self.content_in_order[-1].setAudio(self.voiceContentEditor(str(comment.body), id))
        #     self.getContentImages(id)
        # else:
        #     self.content_in_order[-1].setAudio(self.voiceContentEditor(str(comment.body), id,combine=False))
        #     self.getContentImages(id,words=str(comment.body))

    def getContentImages(self,id, words = None):
        
        if words != None:
            parts = []
            numIteration = 0

            if self.doRandomTextColor:
                color = '#{:06x}'.format(random.randint(0, 0xFFFFFF))
            color = "#000000"

            for x in re.split(';|!|\?|\.', words):
                if x == "" or x =='\"' or x =="\'":
                    continue
                fileName = id + str(numIteration)
                self.makeTextImage(x,fileName,textColor=color)
                parts.append(fileName+".png")
                numIteration = numIteration + 1

            self.content_in_order[-1].setImages(parts)
            return
        
        #screenshotting
        if(self.screenshotter.getStarted() == False):
            # self.screenshotter.start()
            print("ble")
        self.screenshotter.screenshot(id)
        self.content_in_order[-1].setImages(f"{id}.png")
    
    def wasMadeBefore(self,postID):
        postsJson = open(self.pastIdPath)
        posts = json.load(postsJson)

        for x in posts:
            if x == postID:
                postsJson.close()
                return True

        postsJson.close()
        return False

    def addIdToSkipList(self,postID):
        if self.testing:
            print("TESTING SCRIPT, NOT SAVING POSTS")
            return
        postsJson = open(self.pastIdPath)
        posts = json.load(postsJson)
        posts.append(postID)
        print(posts)

        with open(self.pastIdPath, "w") as outfile:
            json.dump(posts, outfile)
        print("wrote to json")

    #replaces tos words with better words and makes longer audio clips
    def voiceContentEditor(self,content, fileName,combine = True):

        ModifiedContent = content.split()
        
        # list of words that get subsituted for other words
        with open(self.doubleSpeakPath,"r") as f:
            doubleSpeak = json.load(f)
        
        r = 0
        #checking for no no words and replacing them
        for x in ModifiedContent:
            
            if x.lower() in doubleSpeak:
                print("replacing",x,"in",fileName)
                ModifiedContent[r] = doubleSpeak[x.lower()]
            r = r + 1 
        
        ModifiedContent = ' '.join(ModifiedContent)

        #if text is too long, this splits it up per sentence
        if len(ModifiedContent)>200 or combine == False:
            numIteration = 0
            parts = []
            for x in re.split(';|!|\?|\.',ModifiedContent):
                if x == "" or x =='\"' or x =="\'":
                    continue
                self.voice.tts(self.session_id,self.voicechoice, x, fileName + str(numIteration)+".mp3","true")
                print(fileName + str(numIteration)+".mp3")
                parts.append(fileName + str(numIteration)+".mp3")
                numIteration = numIteration + 1

            #combines all the audio together
            if combine:
                audio_together = []
                for sound_bit in parts:
                    print(f"getting {sound_bit}")
                    content = mp.AudioFileClip(f"{sound_bit}")
                    print(content.duration)
                    audio_together.append(content)
                final_audio = mp.concatenate_audioclips(audio_together)
                final_audio.write_audiofile(fileName+".mp3")
            else:
                return parts

            print("clearing segmented audio files")
            for files in parts:
                print(f"deleting:{files}")
                os.remove(f"{files}")
            print("all done.")
            return fileName+".mp3"

        else:
            self.voice.tts(self.session_id,self.voicechoice, ModifiedContent, fileName + ".mp3","true")
            return fileName+".mp3"

    def makeTextImage(self,text, fileName, textColor = "#000000"):
        image = PIL.Image.new(mode = "RGBA",size = (1080,1920),color = (255,255,255,0))
        draw = ImageDraw.Draw(image)
        offset = 440
        font_path = self.dahFont
        font = ImageFont.truetype(font_path, 100)
        for line in textwrap.wrap(text, width=20):
            draw.text((10, offset), line, align = "center", font = font,fill=textColor,stroke_width= 10, stroke_fill="#FFFFFF")
            offset += 90

        image = image.save(f"{fileName}.png")
        return
    #video edit
    def videoEdit(self,videoMaxLength):
       print("new video editting")
       v = videoEdit()
       v.setMaxVideoLength(videoMaxLength)
       v.setCommentsInOrder(self.content_in_order)
       v.doSplit(self.videoSplitting)
       v.makeVideo()
       self.videosToUpload = v.getVideos()

    def cleanUpFiles(self):
        print("clearing files")
        for files in self.content_in_order:
            
            # try:
            if files == None:
                continue
            dell = False
            if type(files.getAudio()) == list:
                for parts in files.getAudio():
                    print(f"deleting list item:{parts}")
                    try:
                        os.remove(parts)
                    except:
                        print("failed")
                dell = True
            if type(files.getImages()) == list:
                for part2s in files.getImages():
                    print(f"deleting list item:{part2s}")
                    try:
                        os.remove(part2s)
                    except:
                        print("print")
                dell = True
            if dell:
                continue
            print(f"deleting:{files.getAudio()}")
            print(f"deleting:{files.getImages()}")
            try:
                os.remove(files.getAudio())
                os.remove(files.getImages())
            except:
                print("failed")
        print(self.content_in_order)
        del self.content_in_order[:]
        print("all done cleaning up files.")

    def run(self):

        # browser = self.startFireFox()
        # self.login(browser)
        self.getContent(self.subreddit)            
        print("closing firefox")
        # browser.close()
        if self.foundNewVideo:
            # self.videoEdit(30)
            try:
                self.videoEdit(self.videoLength)
                self.madeNewVideo = True
            except:
                print("An error has occurred during the video editing process.")
                self.madeNewVideo = False
            self.cleanUpFiles()






    def setSubreddit(self,sub):
        self.subreddit = sub

    def setNumberOfComments(self,num):
        self.numOfComments = int(num)

    def doCommentScreenshots(self, val):
        self.doScreenshotsOfComments = val

    def readPost(self, val):
        self.readPost = val

    def succeedInMakingNewVideo(self):
        return self.madeNewVideo

    def setCallToAction(self,toggle):
        self.callToAction = toggle

    def setTesting(self,toggle):
        self.testing = toggle
    
    def setReadPost(self, val):
        self.isReadPost = val

    def setRandomTextColor(self, val):
        self.doRandomTextColor = val
    
    def setVideoLength(self, val):
        self.videoLength = int(val)
    
    def setVideoSplitting(self,val):
        self.videoSplitting = val

    def getVideos(self):
        return self.videosToUpload