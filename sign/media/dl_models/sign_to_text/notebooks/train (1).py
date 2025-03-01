# -*- coding: utf-8 -*-
"""train.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1vI1qL3hHXxoDr5l6y_EVq49UrRxfp0Xy
"""

import shutil

# Commented out IPython magic to ensure Python compatibility.
import os
import cv2
#import pafy
import math
import random
import numpy as np
import datetime as dt
import tensorflow as tf
from collections import deque
import matplotlib.pyplot as plt

from moviepy.editor import *
# %matplotlib inline

from sklearn.model_selection import train_test_split

seed_constant = 27
np.random.seed(seed_constant)
random.seed(seed_constant)
tf.random.set_seed(seed_constant)

! pip install mediapipe
! pip install sk-video
! pip install keras-video-generators

from google.colab import drive
drive.mount('/content/drive')

shutil.copy("/content/drive/MyDrive/Three Classes.zip","/content")

! wget https://zenodo.org/record/4010759/files/Greetings_1of2.zip

! wget https://zenodo.org/record/4010759/files/Greetings_2of2.zip

!unzip "/content/Greetings_1of2.zip"

!unzip "/content/Greetings_2of2.zip"

shutil.rmtree("/content/Greetings/50. Alright")
shutil.rmtree("/content/Greetings/51. Good Morning")
shutil.rmtree("/content/Greetings/52. Good afternoon")
shutil.rmtree("/content/Greetings/53. Good evening")
shutil.rmtree("/content/Greetings/54. Good night")
shutil.rmtree("/content/Greetings/56. Pleased")

import os

source = '/content/Greetings/55. Thank you'
destination = '/content/Three Classes/Thank You'
os.makedirs(destination, exist_ok=True)
allfiles = os.listdir(source)

for f in allfiles:
    shutil.copy(source + "/" + f, destination + "/"+ f)

source = '/content/Greetings/49. How are you'
destination = '/content/Three Classes/How are you'
os.makedirs(destination, exist_ok=True)
allfiles = os.listdir(source)

for f in allfiles:
    shutil.copy(source + "/" + f, destination + "/"+ f)

source = '/content/Greetings/48. Hello'
destination = '/content/Three Classes/Hello'
os.makedirs(destination, exist_ok=True)
allfiles = os.listdir(source)

for f in allfiles:
    shutil.copy(source + "/" + f, destination + "/"+ f)

c=[]
for dirpathed,dirname,files in (os.walk("/content/Three Classes")):
  for class_name in dirname:
    i=0
    for dirpath,dirname,files in os.walk(os.path.join(dirpathed,class_name)):
     print(dirpath)
     print(files)
     print(len(files))
     for k in files:
        i=i+1
     c.append(class_name)
     c.append(i)

!git clone https://github.com/shayanalibhatti/Video-Augmentation-Code.git

!pip install vidaug

!python '/content/Video-Augmentation-Code/video_augmentation_code.py'  --main-folder-path "/content/Three Classes/Hello" --output-folder-path "/content/Input/Hello" --max-clips 3

!python '/content/Video-Augmentation-Code/video_augmentation_code.py'  --main-folder-path "/content/Three Classes/How are you" --output-folder-path "/content/Input/How are you" --max-clips 3
!python '/content/Video-Augmentation-Code/video_augmentation_code.py'  --main-folder-path "/content/Three Classes/Thank You" --output-folder-path "/content/Input/Thank You" --max-clips 3

source = '/content/Input/Hello'
destination = "/content/Three Classes/Hello"

allfiles = os.listdir(source)

for f in allfiles:
    shutil.copy(source + "/" + f, destination + "/"+ f)

source = '/content/Input/How are you'
destination = "/content/Three Classes/How are you"

allfiles = os.listdir(source)

for f in allfiles:
    shutil.copy(source + "/" + f, destination + "/"+ f)

source = '/content/Input/Thank You'
destination = "/content/Three Classes/Thank You"

allfiles = os.listdir(source)

for f in allfiles:
    shutil.copy(source + "/" + f, destination + "/"+ f)

c=[]
for dirpathed,dirname,files in (os.walk("/content/Output")):
  for class_name in dirname:
    i=0
    for dirpath,dirname,files in os.walk(os.path.join(dirpathed,class_name)):
     print(dirpath)
     print(files)
     print(len(files))
     for k in files:
        i=i+1
     c.append(class_name)
     c.append(i)

d=420+398+361
d

Hello=315
How_are_you=315
Thank_You=315

def mediapipe_detection(image,model):
    image = cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
    image.flags.writeable = False
    results = model.process(image)
    image.flags.writeable = True
    image = cv2.cvtColor(image,cv2.COLOR_RGB2BGR)
    return image,results

def draw_landmarks(image, results):
    mp_drawing.draw_landmarks(image,results.face_landmarks, mp_holistic.FACEMESH_TESSELATION)
    mp_drawing.draw_landmarks(image,results.pose_landmarks, mp_holistic.POSE_CONNECTIONS)
    mp_drawing.draw_landmarks(image,results.left_hand_landmarks, mp_holistic.HAND_CONNECTIONS)
    mp_drawing.draw_landmarks(image,results.right_hand_landmarks, mp_holistic.HAND_CONNECTIONS)

import mediapipe as mp

mp_drawing=mp.solutions.drawing_utils
mp_holistic=mp.solutions.holistic

def pose_estimation(image,results):

        # 1. Draw face landmarks
        #mp_drawing.draw_landmarks(image, results.face_landmarks, mp_holistic.FACE_CONNECTIONS,
        #                         mp_drawing.DrawingSpec(color=(80,110,10), thickness=1, circle_radius=1),
        #                         mp_drawing.DrawingSpec(color=(80,256,121), thickness=1, circle_radius=1)
        #                         )

        # 2. Right hand
        mp_drawing.draw_landmarks(image, results.right_hand_landmarks, mp_holistic.HAND_CONNECTIONS,
                                 mp_drawing.DrawingSpec(color=(102,255,51), thickness=3, circle_radius=4),
                                 mp_drawing.DrawingSpec(color=(255,255,255), thickness=2, circle_radius=2)
                                 )

        # 3. Left Hand
        mp_drawing.draw_landmarks(image, results.left_hand_landmarks, mp_holistic.HAND_CONNECTIONS,
                                 mp_drawing.DrawingSpec(color=(102,255,51), thickness=3, circle_radius=4),
                                 mp_drawing.DrawingSpec(color=(255,255,255), thickness=2, circle_radius=2)
                                 )

        # 4. Pose Detections
        mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_holistic.POSE_CONNECTIONS,
                                 mp_drawing.DrawingSpec(color=(255,255,0), thickness=2, circle_radius=4),
                                 mp_drawing.DrawingSpec(color=(255,255,255), thickness=2, circle_radius=2)
                                 )

        return image

os.makedirs("Output")

no_sequences=45

import skvideo.io

def extract_keypoints(results):
    pose = np.array([[res.x, res.y, res.z, res.visibility] for res in results.pose_landmarks.landmark]).flatten() if results.pose_landmarks else np.zeros(33*4)
    lh = np.array([[res.x, res.y, res.z] for res in results.left_hand_landmarks.landmark]).flatten() if results.left_hand_landmarks else np.zeros(21*3)
    rh = np.array([[res.x, res.y, res.z] for res in results.right_hand_landmarks.landmark]).flatten() if results.right_hand_landmarks else np.zeros(21*3)
    #face = np.array([[res.x, res.y, res.z] for res in results.face_landmarks.landmark]).flatten() if results.face_landmarks else np.zeros(468*3)
    return np.concatenate([pose,lh,rh])

os.makedirs("Mediapipe")

for dirpathed,dirnamed,file in os.walk("Input"):
    for class_  in dirnamed:
      os.makedirs(os.path.join("/content/Mediapipe",class_))

shutil.rmtree("/content/mp_results/Hello")

for dirpathed,dirnamed,file in os.walk("/content/mp_results"):
   for dirpath,dirname,files in os.walk(os.path.join(dirpathed,'Hello')):
     print(dirpath)
     print(dirname)
     print(len(dirname))

     for video in dirname:
       print(video)
       f = os.listdir(os.path.join(dirpathed,"Hello"))
       for file_name in sample(f,10):
          os.removedir(os.path.join(dirpath,file_name))

shutil.rmtree("/content/mp_results")

os.makedirs("mp_results")

DATA_PATH = os.path.join('/content/mp_results',"Hello")

#Actions
actions = np.array(['Hello','How are you','Thank You'])

#1179 videos worth of data
no_sequences = 1179

#45 frames
sequence_length = 45

for sequence in range(Hello):
        try:
            os.makedirs(os.path.join("/content/mp_results/Hello",str(sequence)))
        except:
            pass

DATA_PATH = os.makedirs(os.path.join("/content/mp_results","How are you"))

data_path="/content/mp_results/How are you"

for sequence in range(How_are_you):
        try:
            os.makedirs(os.path.join(data_path,str(sequence)))
        except:
            pass

DATA_PATH = os.makedirs(os.path.join("/content/mp_results","Thank you"))

data_path="/content/mp_results/Thank You"

for sequence in range(Thank_You):
        try:
            os.makedirs(os.path.join(data_path,str(sequence)))
        except:
            pass

for dirpathed,dirnamed,file in os.walk("Mediapipe"):
    for class_  in dirnamed:
      os.makedirs(os.path.join("/content/Output",class_))

def video_array_maker(pather,class_name, video_num,height=224,width=224,output_directory="./Output",output_folder=None,remove_input=False):
  """
    pather : location of video
    height,width (default : 224)
    output_directory :output main directory  (default : ./Output)
    output folder :output subdirectory
  """
  if output_folder is None:
    output_folder=pather.split("/")[3]
  elif output_folder == "No":
    output_folder=""
  videodata = skvideo.io.vread(pather)
  outpath=os.path.join(output_directory,output_folder,os.path.split(pather)[1])
  out = cv2.VideoWriter(outpath,cv2.VideoWriter_fourcc('M','J','P','G'), 10,(videodata.shape[2],videodata.shape[1]))
  k=0



  with mp_holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5) as holistic:

    actualframe=len(videodata)

    if actualframe >=45:
          for i in range (actualframe):
            x=round (actualframe/(45)  * i)
            if x >=actualframe:
                    break
            else:
                frame =videodata[x]


                #output=cv2.resize(frame,(videodata.shape[2],videodata.shape[1]),interpolation=cv2.INTER_NEAREST)
                output =cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
                out.write(output)


    else:
          s=0
          for i in range(actualframe):
              frame=videodata[i]



              #output=cv2.resize(frame,(videodata.shape[2],videodata.shape[1]),interpolation=cv2.INTER_NEAREST)
              output =cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
              out.write(output)

          for i in range(45-actualframe):

              newframe=np.zeros(shape=(videodata.shape[2],videodata.shape[1],3))
              #frame=videodata[i]




              out.write(np.uint8(newframe))

    out.release()

    if remove_input==True:
        os.remove(pather)

for dirpath,dirnamed,files in os.walk("/content/Three Classes"):
  for c in dirnamed:
    for i,j,k in os.walk(os.path.join(dirpath,c)):
      for index,m in enumerate(k):
        pather=os.path.join(i,m)
        video_array_maker(pather,c,index)

shutil.rmtree("/content/mp_results with zenordo")

shutil.rmtree("/content/Mediapipe")

shutil.rmtree("/content/Greetings")

shutil.rmtree("/content/71")

shutil.rmtree("/content/Input")

os.makedirs("Mediapipe videos")

for dirpathed,dirnamed,file in os.walk("Output"):
    for class_  in dirnamed:
      os.makedirs(os.path.join("/content/Mediapipe videos",class_))

def Mediapipe_converter(pather,class_name, video_num,output_directory="./Mediapipe videos",output_folder=None,remove_input=False):
  """
    pather : location of video
    height,width (default : 224)
    output_directory :output main directory  (default : ./Output)
    output folder :output subdirectory
  """
  if output_folder is None:
    output_folder=pather.split("/")[3]
  elif output_folder == "No":
    output_folder=""
  videodata = skvideo.io.vread(pather)
  print(videodata.shape)
  outpath=os.path.join(output_directory,output_folder,os.path.split(pather)[1])
  print(outpath)
  out = cv2.VideoWriter(outpath,cv2.VideoWriter_fourcc('M','J','P','G'), 10,(224,224))
  k=0

  with mp_holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5) as holistic:

    actualframe=len(videodata)

    for x in range(45):
                 frame=videodata[x]
                 image,results = mediapipe_detection(frame,holistic)

                 print(results)
                 output=pose_estimation(frame,results)
                 keypoints = extract_keypoints(results)
                 print(keypoints.shape)
                 npy_path = os.path.join("/content/mp_results",class_name,str(video_num), str(x))
                 np.save(npy_path,keypoints)
                 output=cv2.resize(output,(224,224),interpolation=cv2.INTER_AREA)
                 output =cv2.cvtColor(output,cv2.COLOR_BGR2RGB)
                 out.write(output)


    out.release()

    if remove_input==True:
        os.remove(pather)

k=0
for dirpathed,dirnamed,file in os.walk("/content/Output"):
  print(dirpathed)
  print(dirnamed)
  print(file)


  for dirpath,dirname,files in os.walk(os.path.join(dirpathed,'Hello')):
     print(dirpath)
     print(dirname)
     print(len(dirname))

     for index,video in enumerate(files):
       print(video)
       pather=os.path.join("/content/Output/Hello",video)
       #Mediapipe_converter(pather,c,index)
       #k=k+1

       if(index>=315):
         break
       else:
          Mediapipe_converter(pather,"Hello",index)
          print("videos completed:",index)
         #shutil.rmtree(os.path.join(dirpath,video))

k=0
for dirpathed,dirnamed,file in os.walk("/content/Output"):
  print(dirpathed)
  print(dirnamed)
  print(file)


  for dirpath,dirname,files in os.walk(os.path.join(dirpathed,'How are you')):
     print(dirpath)
     print(dirname)
     print(len(dirname))
     print(len(files))
     print(files)

     for index,video in enumerate(files):
       print(video)
       pather=os.path.join(dirpath,video)
       #Mediapipe_converter(pather,c,index)
       #k=k+1

       if(index>=315):
         break
       else:
           Mediapipe_converter(pather,"How are you",index)
           print("videos completed:",index)
         #shutil.rmtree(os.path.join(dirpath,video))

k=0
for dirpathed,dirnamed,file in os.walk("/content/Output"):
  print(dirpathed)
  print(dirnamed)
  print(file)


  for dirpath,dirname,files in os.walk(os.path.join(dirpathed,'Thank You')):
     print(dirpath)
     print(dirname)
     print(len(dirname))

     for index,video in enumerate(files):
       print(video)
       pather=os.path.join("/content/Output/Thank You",video)
       #Mediapipe_converter(pather,c,index)
       #k=k+1

       if(index>=315):
         break
       else:
          Mediapipe_converter(pather,"Thank You",index)
          print("videos completed:",index)
         #shutil.rmtree(os.path.join(dirpath,video))

for dirpath,dirnamed,files in os.walk("/content/Output"):
  for c in dirnamed:
    for i,j,k in os.walk(os.path.join(dirpath,c)):
      for index,m in enumerate(k):
        pather=os.path.join(i,m)
        Mediapipe_converter(pather,c,index)

for dirpathed,dirname,file in(os.walk("/content/Input")):
  print(dirpath)
  print(dirname)
  print(file)
  for class_ in dirname:
    for dirpath,dirname,files in os.walk(os.path.join(dirpathed,class_)):

       for i,j in enumerate(files):
          vid=skvideo.io.vread(os.path.join(dirpath,j))
          print(vid.shape)
          with mp_holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5) as holistic:

             for x in range(45):
                 frame=vid[x]
                 image,results = mediapipe_detection(frame,holistic)

                 print(results)
                 pose_estimation(image,results)
                 keypoints = extract_keypoints(results)
                 npy_path = os.path.join("/content/mp_results",class_,str(i), str(x))
                 np.save(npy_path,keypoints)

for dirpathed,dirname, files in os.walk(os.path.join("/content/Three Classes","Hello")):
  for i,j in enumerate(files):
     vid=skvideo.io.vread(os.path.join(dirpathed,j))
     print(vid.shape)
     with mp_holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5) as holistic:

             for x in range(45):
                 frame=vid[x]
                 image,results = mediapipe_detection(frame,holistic)

                 print(results)
                 pose_estimation(image,results)
                 keypoints = extract_keypoints(results)
                 npy_path = os.path.join("/content/mp_results","Hello",str(i), str(x))
                 np.save(npy_path,keypoints)

for dirpathed,dirname, files in os.walk(os.path.join("/content/Three Classes","How are you")):
  for i,j in enumerate(files):
     vid=skvideo.io.vread(os.path.join(dirpathed,j))
     print(vid.shape)
     with mp_holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5) as holistic:

             for x in range(45):
                 frame=vid[x]
                 image,results = mediapipe_detection(frame,holistic)

                 print(results)
                 pose_estimation(image,results)
                 keypoints = extract_keypoints(results)
                 npy_path = os.path.join("/content/mp_results","How are you",str(i), str(x))
                 np.save(npy_path,keypoints)

for dirpathed,dirname, files in os.walk(os.path.join("/content/Output","Thank you")):
  for i,j in enumerate(files):
     vid=skvideo.io.vread(os.path.join(dirpathed,j))
     print(vid.shape)
     with mp_holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5) as holistic:

             for x in range(45):
                 frame=vid[x]
                 image,results = mediapipe_detection(frame,holistic)

                 print(results)
                 pose_estimation(image,results)
                 keypoints = extract_keypoints(results)
                 npy_path = os.path.join("/content/mp_results","Thank you",str(i), str(x))
                 np.save(npy_path,keypoints)

from sklearn.model_selection import train_test_split
from tensorflow.keras.utils import to_categorical

label_map = {label:num for num, label in enumerate(actions)}

shutil.copytree("/content/mp_results with zenordo","/content/drive/MyDrive/Colab Notebooks/mp_results with zenordo")

shutil.move("/content/mp_results with zenordo/How are you/71","/content")

class_length=[315,315,315]
class_length

sequences, labels = np.array([]), np.array([])
k=0
for dirpath,dirname,files in (os.walk(("/content/mp_results"))):
      print(dirpath)
      print(dirname)
      print(files)
      for index,class_name in enumerate(dirname):
        for i,j,file in os.walk(os.path.join(dirpath,class_name)):

           print(i)
           print(j)
           print(file)


           for video_num in j:
             print(video_num)
             for path, sub_path, frames in os.walk(os.path.join(i,video_num)):
               print(path)
               print(sub_path)
               print(len(frames))
               print(frames)
               window=np.array([])
               for frame_num in (frames):
                  res = np.load(os.path.join("/content/mp_results",class_name, video_num,"{}".format(frame_num)))
                  print(res.shape)
                  window.append(res)
               if(frame_num==45):
                    k=k+1
                    print(k,"videos completed")
             sequences.append(np.asarray(window))
             labels.append(index)

x=np.asarray(sequences)

y=np.array(labels)

y = to_categorical(labels).astype(int)

x_train, x_test, y_train, y_test = train_test_split(x,y,test_size = 0.2)

X=np.expand_dims(x_train,axis=0)

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM,Dense
from tensorflow.keras.callbacks import TensorBoard

os.makedirs("checkpoint")

checkpoint_filepath = '/content/checkpoint'
model_checkpoint_callback = tf.keras.callbacks.ModelCheckpoint(
    filepath=os.path.join(checkpoint_filepath, "{epoch:02d}-{categorical_accuracy:.2f}.hdf5"),
    save_weights_only=True,
    monitor='loss',
    mode='min',
    save_best_only=False)

model = Sequential()

model.add(LSTM(64,return_sequences=True, activation='relu', input_shape=(45,258)))
model.add(LSTM(128,return_sequences=True, activation = 'relu'))
model.add(LSTM(256,return_sequences=True,activation="relu"))
model.add(LSTM(64, return_sequences = False,activation='relu'))
model.add(Dense(64,activation='relu'))
model.add(Dense(32,activation = 'relu'))
model.add(Dense(actions.shape[0],activation='softmax'))

model.summary()

model.compile(optimizer = 'Adam',loss='categorical_crossentropy',metrics=['categorical_accuracy'])

model.load_weights("/content/checkpoint/170-0.83.hdf5")

model_evaluation_history = model.evaluate(x_test, y_test)

Actual_class=[]
predicted_class=[]
predicted_label=[]
true_label=[]
count=0
for i in range(len(x_test)):
  predicted_label_probablities=model.predict(np.expand_dims(x_test[i],axis=0))
  predicted=np.argmax(predicted_label_probablities)
  predicted_label.append(predicted)
  c=np.argmax(y_test[i])
  true_label.append(c)
  print("Actual Class:",actions[c])
  Actual_class.append(c)
  print("predicted class:",actions[predicted])
  predicted_class.append(actions[predicted])
  print("########")
  if(actions[c]==actions[predicted]):
    count=count+1
print("No: of classes predicted correctly:",count)

shutil.copytree("/content/drive/MyDrive/Colab Notebooks/Aakash","/content/testing videos")

os.makedirs("mp_testing_results")

os.makedirs("mediapipe_testing_videos")

DATA_PATH = os.makedirs(os.path.join('/content/mp_testing_results',"actions"))
for action in actions:
   for sequence in range(3):
     try:
       os.makedirs(os.path.join("/content/mp_testing_results",action,str(sequence)))
     except:
            pass

def video_array_maker_testing(pather,class_name, video_num,height=224,width=224,output_directory="./Mediapipe_testing_videos",output_folder=None,remove_input=False):
  """
    pather : location of video
    height,width (default : 224)
    output_directory :output main directory  (default : ./Output)
    output folder :output subdirectory
  """
  if output_folder is None:
    output_folder=pather.split("/")[3]
  elif output_folder == "No":
    output_folder=""
  videodata = skvideo.io.vread(pather)
  outpath=os.path.join(output_directory,output_folder,os.path.split(pather)[1])
  out = cv2.VideoWriter(outpath,cv2.VideoWriter_fourcc('M','J','P','G'), 10,(videodata.shape[2],videodata.shape[1]))
  k=0



  with mp_holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5) as holistic:

    actualframe=len(videodata)

    if actualframe >=45:
          for i in range (actualframe):
            x=round (actualframe/(45)  * i)
            if x >=actualframe:
                    break
            else:
                frame =videodata[x]


                #output=cv2.resize(frame,(videodata.shape[2],videodata.shape[1]),interpolation=cv2.INTER_NEAREST)
                output =cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
                out.write(output)


    else:
          s=0
          for i in range(actualframe):
              frame=videodata[i]



              #output=cv2.resize(frame,(videodata.shape[2],videodata.shape[1]),interpolation=cv2.INTER_NEAREST)
              output =cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
              out.write(output)

          for i in range(45-actualframe):

              newframe=np.zeros(shape=(videodata.shape[2],videodata.shape[1],3))
              #frame=videodata[i]




              out.write(np.uint8(newframe))

    out.release()

    if remove_input==True:
        os.remove(pather)

for dirpath,dirnamed,files in os.walk("/content/testing videos"):
  for c in dirnamed:
    for i,j,k in os.walk(os.path.join(dirpath,c)):
      for index,m in enumerate(k):
        pather=os.path.join(i,m)
        video_array_maker_testing(pather,c,index)

os.makedirs("Real Time Mediapipe videos")

for dirpathed,dirnamed,file in os.walk("/content/testing videos"):
    for class_  in dirnamed:
      os.makedirs(os.path.join("/content/Real Time Mediapipe videos",class_))

def Mediapipe_converter_testing(pather,class_name, video_num,output_directory="./ Real Time Mediapipe videos",output_folder=None,remove_input=False):
  """
    pather : location of video
    height,width (default : 224)
    output_directory :output main directory  (default : ./Output)
    output folder :output subdirectory
  """
  if output_folder is None:
    output_folder=pather.split("/")[3]
  elif output_folder == "No":
    output_folder=""
  videodata = skvideo.io.vread(pather)
  print(videodata.shape)
  outpath=os.path.join(output_directory,output_folder,os.path.split(pather)[1])
  print(outpath)
  out = cv2.VideoWriter(outpath,cv2.VideoWriter_fourcc('M','J','P','G'), 10,(224,224))
  k=0

  with mp_holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5) as holistic:

    actualframe=len(videodata)

    for x in range(45):
                 frame=videodata[x]
                 image,results = mediapipe_detection(frame,holistic)

                 print(results)
                 output=pose_estimation(frame,results)
                 keypoints = extract_keypoints(results)
                 print(keypoints.shape)
                 npy_path = os.path.join("/content/mp_testing_results",class_name,str(video_num), str(x))
                 np.save(npy_path,keypoints)
                 output=cv2.resize(output,(224,224),interpolation=cv2.INTER_AREA)
                 output =cv2.cvtColor(output,cv2.COLOR_BGR2RGB)
                 out.write(output)


    out.release()

    if remove_input==True:
        os.remove(pather)

k=0
for dirpathed,dirnamed,file in os.walk("/content/Mediapipe_testing_videos"):
  print(dirpathed)
  print(dirnamed)
  print(file)


  for dirpath,dirname,files in os.walk(os.path.join(dirpathed,'Thank You')):
     print(dirpath)
     print(dirname)
     print(len(dirname))

     for index,video in enumerate(files):
       print(video)
       pather=os.path.join("/content/Mediapipe_testing_videos/Thank You",video)
       #Mediapipe_converter(pather,c,index)
       #k=k+1

       if(index>=315):
         break
       else:
          Mediapipe_converter_testing(pather,"Thank You",index)
          print("videos completed:",index)
         #shutil.rmtree(os.path.join(dirpath,video))

k=0
for dirpathed,dirnamed,file in os.walk("/content/Mediapipe_testing_videos"):
  print(dirpathed)
  print(dirnamed)
  print(file)


  for dirpath,dirname,files in os.walk(os.path.join(dirpathed,'How are you')):
     print(dirpath)
     print(dirname)
     print(len(dirname))

     for index,video in enumerate(files):
       print(video)
       pather=os.path.join("/content/Mediapipe_testing_videos/How are you",video)
       #Mediapipe_converter(pather,c,index)
       #k=k+1

       if(index>=315):
         break
       else:
          Mediapipe_converter_testing(pather,"How are you",index)
          print("videos completed:",index)
         #shutil.rmtree(os.path.join(dirpath,video))

for dirpathed,dirname, files in os.walk(os.path.join("/content/mp_testing_videos","Thank you")):
  for i,j in enumerate(files):
     vid=skvideo.io.vread(os.path.join(dirpathed,j))
     print(vid.shape)
     with mp_holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5) as holistic:

             for x in range(45):
                 frame=vid[x]
                 image,results = mediapipe_detection(frame,holistic)

                 print(results)
                 pose_estimation(image,results)
                 keypoints = extract_keypoints(results)
                 npy_path = os.path.join("/content/mp_testing_results","Thank you",str(i), str(x))
                 np.save(npy_path,keypoints)

for dirpathed,dirname, files in os.walk(os.path.join("/content/mp_testing_videos","How are you")):
  for i,j in enumerate(files):
     vid=skvideo.io.vread(os.path.join(dirpathed,j))
     print(vid.shape)
     with mp_holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5) as holistic:

             for x in range(45):
                 frame=vid[x]
                 image,results = mediapipe_detection(frame,holistic)

                 print(results)
                 pose_estimation(image,results)
                 keypoints = extract_keypoints(results)
                 npy_path = os.path.join("/content/mp_testing_results","How are you",str(i), str(x))
                 np.save(npy_path,keypoints)

for dirpathed,dirname, files in os.walk(os.path.join("/content/mp_testing_videos","Hello")):
  for i,j in enumerate(files):
     vid=skvideo.io.vread(os.path.join(dirpathed,j))
     print(vid.shape)
     with mp_holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5) as holistic:

             for x in range(45):
                 frame=vid[x]
                 image,results = mediapipe_detection(frame,holistic)

                 print(results)
                 pose_estimation(image,results)
                 keypoints = extract_keypoints(results)
                 npy_path = os.path.join("/content/mp_testing_results","Hello",str(i), str(x))
                 np.save(npy_path,keypoints)

sequences_test, labels_test = [], []
for action in actions:
    for sequence in range(2):
        window = []
        for frame_num in range(sequence_length):
            res = np.load(os.path.join("/content/mp_testing_results",action, str(sequence),"{}.npy".format(frame_num)))
            window.append(res)
        sequences_test.append(window)
        labels_test.append(label_map[action])

x_real=np.array(sequences_test)

y_real=np.array(labels_test)

y_real= to_categorical(labels_test).astype(int)

Actual_class=[]
predicted_class=[]
predicted_label=[]
true_label=[]
count=0
for i in range(len(x_real)):
  predicted_label_probablities=model.predict(np.expand_dims(x_real[i],axis=0))
  predicted=np.argmax(predicted_label_probablities)
  predicted_label.append(predicted)
  c=np.argmax(y_real[i])
  true_label.append(c)
  print("Actual Class:",actions[c])
  Actual_class.append(c)
  print("predicted class:",actions[predicted])
  predicted_class.append(actions[predicted])
  print("########")
  if(actions[c]==actions[predicted]):
    count=count+1
print("No: of classes predicted correctly:",count)

shutil.copytree("/content/mp_traininng_plain_results","/content/drive/MyDrive/Colab Notebooks/mediapipe_numpy_array on 24/01")

shutil.copytree("/content/checkpoint","/content/drive/MyDrive/Colab Notebooks/LSTM model checkpoints on 24/01")

shutil.copytree("/content/mp_testing_results","/content/drive/MyDrive/Colab Notebooks/mediapipe_real time_testing numpy array on 24/01")

shutil.copytree("/content/Real Time Mediapipe videos","/content/drive/MyDrive/Colab Notebooks/Real time mediapipe testing on 24/01")

model_evaluation_loss, model_evaluation_accuracy = model_evaluation_history

# Define the string date format.
# Get the current Date and Time in a DateTime Object.
# Convert the DateTime object to string according to the style mentioned in date_time_format string.
date_time_format = '%Y_%m_%d__%H_%M_%S'
current_date_time_dt = dt.datetime.now()
current_date_time_string = dt.datetime.strftime(current_date_time_dt, date_time_format)

# Define a useful name for our model to make it easy for us while navigating through multiple saved models.
model_file_name = f'_model___Date_Time_{current_date_time_string}___Loss_{model_evaluation_loss}___Accuracy_{model_evaluation_accuracy}.h5'

# Save the Model.
model.save(model_file_name)

shutil.copy("/content/_model with LSTM plain video 24jan22___Date_Time_2022_01_24__12_38_04___Loss_0.7315725684165955___Accuracy_0.7460317611694336.h5","/content/drive/MyDrive/Colab Notebooks/LSTM plain model on 24 jan 22")

shutil.copytree("/content/Output 24jan 45 frames per video","/content/drive/MyDrive/Colab Notebooks/45 frames per video 24 jan")

shutil.copytree("/content/Mediapipe videos","/content/drive/MyDrive/Colab Notebooks/mediapipe inscribed videos for training 24 jan")









