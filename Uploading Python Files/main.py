from TiktokBot import TiktokBot
if __name__ == "__main__":
    # Example Usage
    # pip install git+https://github.com/pytube/pytube
    
    tiktok_bot = TiktokBot()  # "VideosDirPath", is the default directory where images edited will be saved.

    # You can also choose to upload a file directly with no editing or cropping of the video.
    tiktok_bot.upload.directUpload("tiktok.mp4")

