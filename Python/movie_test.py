import os
import glob
import shutil
import cv2



'''os.mkdir("inject_data/1")
os.mkdir("inject_data/2")
os.mkdir("inject_data/3")'''
files_0=glob.glob("inject_data/*_d0.png")
files_1=glob.glob("inject_data/*_d1.png")
files_2=glob.glob("inject_data/*_d2.png")



image_folder = './inject_data'  # make sure to use your folder
video_name = 'video_2.avi'


images = [img for img in os.listdir(image_folder)
          if img.endswith("d0.png")]
print(images)
frame = cv2.imread(os.path.join(image_folder, images[0]))
height, width, layers = frame.shape
print(frame)

video = cv2.VideoWriter(video_name, 0, 1, (width, height))

# Appending the images to the video one by one
for image in images:
  video.write(cv2.imread(os.path.join(image_folder, image)))


    # Deallocating memories taken for window creation
video.release()
cv2.destroyAllWindows()




