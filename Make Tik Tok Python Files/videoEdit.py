import moviepy.editor as mp
import random
from functools import reduce

class videoEdit:
    
    def __init__(self):
        # self.videoDuration = None
        self.commentsInOrder = None
        self.CalltoAction = True
        self.splitVideoUp = False
        self.time_ellapsed = 0
        self.maxVideoLength = 30
        self.backgroundVideo = "Background Files\\backgroundvideovertical.mp4"
        self.videosToUpload = []
        return
    
    def makeVideo(self):

        video_together = []
        audio_together = []
        self.time_ellapsed = 0
        
        for comment in self.commentsInOrder:
            if self.time_ellapsed > self.maxVideoLength:
                break
            commentContent = self.audioVisual(comment)
            for a in commentContent[0]:
                audio_together.append(a)
            for v in commentContent[1]:
                video_together.append(v)

        if self.splitVideoUp:
            splits = self.findSplitsVideo(audio_together)

            splits[1].insert(0,0)
            for q in range(len(splits[1])):
                delParts = splits[1][q]-1
                audio_together_part = audio_together.copy()
                video_together_part = video_together.copy()
                for r in range(delParts):
                    print(r)
                    audio_together_part.pop(1)
                    video_together_part.pop(1)

                f = self.adjustAudioVisual(audio_together_part,video_together_part)

                self.createVideo(f[0],
                                    f[1],
                                    clipStart=0,
                                    clipStop=splits[0][q] + audio_together_part[0].duration,
                                    name=f"tiktok{q}.mp4")
                self.videosToUpload.append(f"tiktok{q}.mp4")

                audio_together_part = []
                video_together_part = []

            return
            
        if self.CalltoAction:
            c2a = self.createCallToAction()
            audio_together.append(c2a[0])
            video_together.append(c2a[1])

        self.createVideo(audio_together,video_together)
        
        self.videosToUpload.append("tiktok.mp4")

        return

    def audioVisual(self,comment):
        audio = self.getCommentAudio(comment)
        visual = self.getCommentVisual(comment)
        
        for sound, i in zip(audio,range(len(audio))):
            visual[i] = visual[i].subclip(0,sound.duration)
            visual[i] = visual[i].set_start(self.time_ellapsed)
            self.time_ellapsed = self.time_ellapsed + sound.duration

        return audio,visual

    def adjustAudioVisual(self,audio,visual):
        print("adjusting")
        self.time_ellapsed = 0
        for sound, i in zip(audio,range(len(audio))):
            # visual[i] = visual[i].subclip(0,sound.duration)
            visual[i] = visual[i].set_start(self.time_ellapsed)
            self.time_ellapsed = self.time_ellapsed + sound.duration

        return audio,visual

    def createVideo(self,audio_together, video_together,clipStart = 0, clipStop = None, name = "tiktok.mp4"):

        if clipStop == None:
            clipStop = self.time_ellapsed

        video = mp.VideoFileClip(self.backgroundVideo)
        totLeng = random.randrange(0,int(video.duration-240))
        video = video.subclip(totLeng,totLeng+240)
        video.set_start

        video_together.insert(0,video)

        final = mp.CompositeVideoClip(video_together)
        final_audio = mp.concatenate_audioclips(audio_together)
        final = final.set_audio(final_audio)
        final = final.subclip(clipStart,clipStop)
        final.write_videofile(name)
        print("combined")

    def getCommentAudio(self,comment):
        audio_together = []
        audio = comment.getAudio()
        if type(audio) == list:
            
            for audioParts in audio:
                print(f"getting list item:{audioParts}")
                content = mp.AudioFileClip(audioParts)
                audio_together.append(content)

            return audio_together
        
        print(f"getting {audio}")

        content = mp.AudioFileClip(audio)
        print(content.duration)
        audio_together.append(content)
        return audio_together

    def getCommentVisual(self,comment):
        visuals_together = []
        visual = comment.getImages()
            
        #list of images to go with list of audio
        if type(visual) == list:
            for picParts in visual:
                print(f"getting list item:{picParts}")
                #lays out how screenshot will look in video
                content = (mp.ImageClip(picParts)
                    .set_duration(120)
                    .resize(width=1080) # if you need to resize...
                    .margin(right=8, top=8, opacity=0) # (optional) logo-border padding
                    .set_pos(("center")))
                visuals_together.append(content)
            return visuals_together   

       #single image of pictures
        print(f"getting {visual}")

        #lays out how screenshot will look in video
        content = (mp.ImageClip(visual)
            .set_duration(120)
            .resize(width=1080) # if you need to resize...
            .margin(right=8, top=8, opacity=0) # (optional) logo-border padding
            .set_pos(("center")))
        visuals_together.append(content)
        return visuals_together

    def setCommentsInOrder(self,comments):
        self.commentsInOrder = comments

    def setMaxVideoLength(self,length):
        self.maxVideoLength = length

    def setBackgroundVideo(self,num):
        self.backgroundVideo = "Background Files\\backgroundvideovertical.mp4"

    def createCallToAction(self):
        c2aAudio = mp.AudioFileClip("Call To Action\\callToActionAudio.mp3")
        c2aVisual = (mp.ImageClip("Call To Action\\callToActionPicture.png")
                    .set_duration(120)
                    .resize(width=1080) # if you need to resize...
                    .margin(right=8, top=8, opacity=0) # (optional) logo-border padding
                    .set_pos(("center")))
        
        c2aVisual = c2aVisual.subclip(0,c2aAudio.duration)
        c2aVisual = c2aVisual.set_start(self.time_ellapsed)
        self.time_ellapsed = self.time_ellapsed + c2aAudio.duration

        return c2aAudio,c2aVisual

    def findSplitsVideo(self, audio_together):

        totalLength = self.time_ellapsed
        maxNumberOfParts = 5

        maxLength = 60
        minLength = 40

        possibleSplitsAudio = []
        possibleSplitsPositions = []
        for r in range(maxNumberOfParts):
            partsAudio = [0]
            positions = []
            position = 0
            partNum = 0
            for x in audio_together:
                position = position + 1
                partsAudio[partNum] =partsAudio[partNum] + x.duration

                if partsAudio[partNum]> totalLength/(r+1):
                    partNum = partNum + 1
                    partsAudio.append(0)
                    positions.append(position)

            print(partsAudio)
            if partsAudio[-1] >= minLength and partsAudio[-1] <= maxLength:
                print ("WINNNNERRR")
                print(partsAudio)
                print(positions)
                return partsAudio,positions
            possibleSplitsAudio.append(partsAudio)
            possibleSplitsPositions.append(positions)

        smallest = maxLength
        for t in range(len(possibleSplitsAudio)):
            w = 60 - int(possibleSplitsAudio[t][-1])
            if abs(w) < smallest:
                numOfSplits = t
                smallest = abs(w)

        print("WINNER")
        print(possibleSplitsAudio[numOfSplits])
        print(possibleSplitsPositions[numOfSplits])
        return possibleSplitsAudio[numOfSplits], possibleSplitsPositions[numOfSplits]

    def doCalltoAction(self, val):
        self.CalltoAction = val
    
    def doSplit(self, val):
        self.splitVideoUp = val

    def getVideos(self):
        return self.videosToUpload