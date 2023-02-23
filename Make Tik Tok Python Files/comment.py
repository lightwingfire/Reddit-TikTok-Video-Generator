class Content:

    def __init__(self):
        self.id = ""
        self.title = None
        self.mp3 = None
        self.words = ""
        self.image = None

    def __str__(self):
        return f"id:{self.id}\naudio:{self.mp3}\nwords:{self.words}\nimages{self.image}"

    def setId(self,newId):
        self.id = newId

    def setAudio(self,newmp3):
        if type(newmp3) == list:
            if self.mp3 == None:
                self.mp3 = newmp3
            else:
                self.mp3 = [self.mp3] + newmp3
        else:
            self.mp3 = newmp3

    def setWords(self,newWords):
        self.words = newWords

    def setTitle(self,newTitle):
        self.title = newTitle

    def setImages(self,newImage):
        if type(newImage) == list:
            if self.image ==None:
                self.image = newImage
            else:
                self.image = [self.image] + newImage
        else:
            self.image = newImage

    def getId(self):
        return self.id

    def getAudio(self):
        return self.mp3

    def getWords(self):
        return self.words

    def getTitle(self):
        return self.title
    
    def getImages(self):
        return self.image
    