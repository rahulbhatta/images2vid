import cv2
import os

"""
Inputs to the class:

#mode:
#1. one image folder that contains all the images you want: "all_images"
#2. one image folder, and a pattern to match for the images that you want to include (such as "*.png"): "match_pattern"

image_folder_name

image_format
- .png, .jpeg, etc

output_video_name

speed: #we will input this to the function, so we dont have to keep changing the class variables
- the fps

"""

class VidMaker:
    def __init__(self, image_folder_name, image_format, codec_name, output_video_name, output_video_format):
        self.image_folder = image_folder_name
        self.video_name = output_video_name

        if "." in output_video_format:
            self.video_name = output_video_name + output_video_format
        else:
            self.video_name = output_video_name + "." + output_video_format

        if "." in image_format:
            self.image_format = image_format
        else:
            self.image_format = "." + image_format
        
        if "." in output_video_format:
            self.output_video_format = output_video_format
        else:
            self.output_video_format = "." + output_video_format

        self.codec_name = codec_name.lower() #must be lower case. for eg: "mp4v"
        self.initialize()
    
    def get_avg_height_width(self):
        #get all the heights and widths from the images
        heights = []
        widths = []

        for i in range(len(self.images)):
            frame = cv2.imread(os.path.join(self.image_folder, self.images[i]))
            height_, width_, layers = frame.shape
            heights.append(height_)
            widths.append(width_)

        #calculate the average height and width. This is because the images may have different heights and widths,
        # but we'll need to resize each image, for generating the video
        height = int(sum(heights)/len(heights))
        width = int(sum(widths)/len(widths))    
        return height, width
    
    def initialize(self):
        #get all the image filenames
        self.images = [img for img in os.listdir(self.image_folder) if img.endswith(self.image_format)]
        self.height, self.width = self.get_avg_height_width()
    
        #now we'll need to define the fourcc, and we're good to go
        self.fourcc = cv2.VideoWriter_fourcc(*(self.codec_name))         

    def generate_video(self, speed):
        video = cv2.VideoWriter(self.video_name, self.fourcc, speed, (self.width, self.height), True)
        for image in self.images:
            img = cv2.imread(os.path.join(self.image_folder, image))
            img = cv2.resize(img, (self.width, self.height))
            video.write(img)
        
        video.release()
        cv2.destroyAllWindows()
        print("Done!")