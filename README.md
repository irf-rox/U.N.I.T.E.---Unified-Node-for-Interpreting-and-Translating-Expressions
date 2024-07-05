**_U.N.I.T.E. - Unified Node for Interpreting and Translating Expressions_**

Accessibility and integration are important in today's world, but visually impaired people often face frustration when they need information printed in Braille. Historically, the process of creating Braille documents has been a time-consuming and often bureaucratic process. Blind people have to deal with long wait times, administrative problems, and heavy reliance on external resources to transcribe text in Braille. The proposed system offers a solution to tackle this challenge by introducing a device that instantly converts texts to Braille information. Sign Language electronic devices represent technological devices designed to improve accessibility and communication for the visually impaired and hearing impaired. The most important innovation of the proposed system is the ability to convert text input into reproducible Braille format. Users do not need to go through the labyrinthine bureaucracy of Braille document production. Instead, they can enter the desired text into the device and instantly print it out in Braille. The device can also convert text to audio, sign language to text, sign language to braille, audio to braille etc. The impact of this revolutionary process is far-reaching and is leading to freedom and access to information for the visually impaired.

This project mainly focusses on bridging the communication gap between differently abled people.

There are basically 3 phases, the Braille phase, the Sign Language phase and the Text-to-Speech phase.

A new phase where handwritten text can be converted to the other mentioned phases is under developement


This project is done using python, and the libraries which we used are:
1. cv2
2. mediapipe
3. pyfirmata
4. gtts
5. playsound
6. sklearn
7. numpy


To access the recognizer program, go to /Code/signlang.py and run it.
If you want to start from scratch, i.e. from a new custom dataset, run the following modules in order
1. collect_imgs.py
2. create_dataset.py
3. train_classifier.py
4. signlang.py


The collect_imgs.py captures 100 images of your hand symbols within a few seconds.
Then the create_dataset.py converts the coordinates of the symbols to arrays and converts them to data.pickle file.
The train_classifier.py trains the model using RandomForest classifier and generates the model.p file.
The signlang.py opens a webcam prompt where you can show the symbols and it would display the text and when the _Hush.braille_ bot is connected, the braille letters of the corresponding recognized words would be embosed on the bot.


The HUSH.braille bot is runs on an Arduino UNO board, with 6 sg90 micro servo motors, powered by a 9V battery, it's circuit connection is as follows:
![image](https://github.com/irf-rox/Hush.AI/assets/94896261/9f12c3a4-dd40-427c-8ccc-006c561f44ef)


The sg90 micro servo has 3 pins - vcc, gnd and signal.
The +ve and -ve terminals of the battery are connected to the bread board's +ve and -ve line and all the vcc and gnd pins of the servos are connected to the +ve and -ve line of the bread board respectively. A connection from the -ve line to the gnd pin of the arduino must be established to equalize the ground.
Each signal pin of the servos are connected to Digital pins 8, 9, 10, 11, 12 and 13 (as per the code, can be changed to any pin from 2 to 13 and change in signlang.py lines 12-17)

**_THANK YOU_**
