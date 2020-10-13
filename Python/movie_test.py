import os
import glob
import shutil
import cv2
from PIL import Image
import datetime

now = datetime.datetime.now()
time = now.strftime("%H_%M_%S_%MS")

### We might use these newly made direcories to store data but it is not integrated yet
'''os.mkdir("inject_data/1")
os.mkdir("inject_data/2")
os.mkdir("inject_data/3")
files_0=glob.glob("inject_data/*_d0.png")
files_1=glob.glob("inject_data/*_d1.png")
files_2=glob.glob("inject_data/*_d2.png")'''

# Define folder with images path
image_folder = './inject_data_2020-10-11'  # make sure to use your folder (folder containing png images)


#   GENERATING 3 VIDEOS; one for each frame (no image combining)
#   this part (line 24-48) takes pngs and makes 3 separate videos; each video corresponds to one of the frames (d0, d1 or d2)
''''
for i in range(0,3):

    video_name = 'video_'+str(i)+'.avi'


    images = [img for img in os.listdir(image_folder)
              if img.endswith("sqrt_d"+str(i)+".png")]
    #print(images)
    frame = cv2.imread(os.path.join(image_folder, images[0]))
    height, width, layers = frame.shape
    #print(frame)

    video = cv2.VideoWriter(video_name, 0, 1, (width, height))

    # Appending the images to the video one by one
    for image in images:
      video.write(cv2.imread(os.path.join(image_folder, image)))


        # Deallocating memories taken for window creation
    video.release()
    cv2.destroyAllWindows()
    print('Video '+str(i)+' complete')
'''

## THREE DIFFERENT WAYS OF COMBINING PNG FRAMES (d0+d1+d2) AND GENERATING VIDEOS

images = [img for img in os.listdir(image_folder)
          if img.endswith("sqrt_d0.png") or img.endswith("sqrt_d1.png")or img.endswith("sqrt_d2.png")] # tells the script which files to target
#print(images)
#print(images[0])

img_len=(int(len(images)/2))
print(img_len)
sets=int((img_len/3)+2) # chooses how many iterations (how many times pngs are used in the video)
                        # higher number of iterations gives better signal in the dark areas of
                         # images but lighter parts can get overexposed
#print(sets)

#1. Blending images with alpha value
'''for i in range(0,sets,3): #starts with image d0 and uses first 3 images in single composition (first frame of the video)
    print('THIS IS THE CURRENT STARTING IMAGE NUMBER: '+str(i))

    image_0= Image.open('./inject_data_2020-10-11/'+images[i]).convert("RGB") # d0 images
    #print(image_0)
    image_1 = Image.open('./inject_data_2020-10-11/'+images[i+1]).convert("RGB") # d1 images
    #print(image_1)
    image_2= Image.open('./inject_data_2020-10-11/'+images[i+2]).convert("RGB")  # d1 images
    #print(image_2)

    new_img = Image.blend(image_0,image_1, 0.5) # alpha value=0.5 (50% of the first image visibility; 50% second image) 
                                                # alpha values from 0.0-1.0; if alpha=0.0 output is 100% of the first image
                                                # (image_0) info, alpha=1.0 output is 100% of the second image (image_1) information
   
    new_img=Image.blend(new_img,image_2, 0.5) # bledning image_2 with blended image_0+image_1
    new_img.save("blended_channels_(0_1_2)"+str(i+10)+".png","PNG")
    print("Image "+ str(i)+ "saved")
    
    
# GENERATING A VIDEO FROM COMBINED IMAGES IN EACH TIME FRAME (blended images)

video_name = 'video_bleded_channels(0_1_2).avi'


images = [img for img in os.listdir('.')
          if img.startswith("blended_channels")]
images=sorted(images)
frame = cv2.imread(os.path.join('.', images[0]))
height, width, layers = frame.shape
#print(frame)

# Blank video file
video = cv2.VideoWriter(video_name, 0, 1, (width, height))

# Appending the images to the video one by one
for image in images:
  video.write(cv2.imread(os.path.join('.', image)))


# Deallocating memories taken for window creation
video.release()
cv2.destroyAllWindows()
print('Video complete')
'''

#2. Merging images with RGB bands; 3 at a time
for i in range(0,sets,3):
    print('THIS IS THE CURRENT STARTING IMAGE NUMBER: '+str(i))

    # Import images
    image_0= Image.open('./inject_data_2020-10-11/'+images[i]).convert("RGB") # d0
    #print(image_0)
    image_1 = Image.open('./inject_data_2020-10-11/'+images[i+1]).convert("RGB") # d1
    #print(image_1)
    image_2= Image.open('./inject_data_2020-10-11/'+images[i+2]).convert("RGB") # d2
    #print(image_2)

    #   define RGB bands for each image with function .split()
    r0, g0, b0, = image_0.split()
    r1, g1, b1, = image_1.split()
    r2, g2, b2, = image_2.split()

    # merge 3 images into 1 by combining band R form first, band G from second, and band B form third image
    merged = Image.merge("RGB", (r0, g1, b2)) # arbitrarely chosen order of bands; one can use for instance r1,g2,b0 or any other combination
    new_img = Image.blend(merged, image_1, 0.5)
    new_img.save("test_merged+blend_"+str(i+10)+".png")

    print("Image "+ str(i)+ "saved")
    

#   GENERATING A VIDEO FROM COMBINED IMAGES IN EACH TIME FRAME (merged images)
video_name = 'test_video_merge+blend_channels(0_and_1).avi' # file that we want to save video under (.avi)


images = [img for img in os.listdir('.')
          if img.startswith("merged+blend")] #define images used for the video (make sure os.listdir(<"folder">) <folder> contains images

images=sorted(images) #sort images
frame = cv2.imread(os.path.join('.', images[0])) # reads size of the first image
height, width, layers = frame.shape              # chooses size of the video based on image[0] size
#print(frame)

# Blank video file
video = cv2.VideoWriter(video_name, 0,1,(width, height))

# Appending the images to the video one by one
for image in images:
  video.write(cv2.imread(os.path.join('.', image)))

video.release()

# Deallocating memories taken for window creation
cv2.destroyAllWindows()
print('Video complete')



# 3. Compositing images using a mask
'''
for i in range(0,sets,2):
    print('THIS IS THE CURRENT STARTING IMAGE NUMBER: '+str(i))

    # Import images
    image_0= Image.open('./inject_data_2020-10-11/'+images[i]).convert("RGB")
    #print(image_0)
    image_1 = Image.open('./inject_data_2020-10-11/'+images[i+1]).convert("RGB")
    #print(image_1)
    image_2= Image.open('./inject_data_2020-10-11/'+images[i+2]).convert("RGB")
    #print(image_2)
    
    # Define a mask as a blank RGB image of the same size as data images
    mask = Image.new("RGBA", image_1.size, 128)
    
    # Compositing images
    composite=Image.composite(image_0,image_1, mask) # composite image_0 and image_1 
    composite=Image.composite(composite,image_2, mask) # composite image_2 with already composited image_0+image_1
    composite.save(str(i+20)+"_composite.png")

    print("Image "+ str(i)+ "saved")

# GENERATING A VIDEO FROM COMBINED IMAGES IN EACH TIME FRAME (composited images)

video_name = 'video_composite_channels(0_1_2).avi'


images = [img for img in os.listdir('.')
          if img.endswith("composite.png")]
images=sorted(images)
frame = cv2.imread(os.path.join('.', images[0]))
height, width, layers = frame.shape
#print(frame)

# Blank video file
video = cv2.VideoWriter(video_name, 0, 1, (width, height))

# Appending the images to the video one by one
for image in images:
  video.write(cv2.imread(os.path.join('.', image)))


# Deallocating memories taken for window creation
video.release()
cv2.destroyAllWindows()
print('Video complete')'''




