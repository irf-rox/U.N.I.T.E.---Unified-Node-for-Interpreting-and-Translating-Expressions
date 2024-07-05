from tkinter import *
from PIL import ImageTk,Image
from tkinter import ttk
from tkinter import messagebox
import pickle
import time
import cv2
import mediapipe as mp
import numpy as np
from pyfirmata import Arduino, SERVO, util
from time import sleep
from gtts import gTTS  
from playsound import playsound
import speech_recognition as sr
import os

port='COM3'
global p0, p1, p2, p3, p4, p5, p
p0=8
p1=9
p2=10
p3=11
p4=12
p5=13
p=[p0, p1, p2, p5, p3, p4]
board=Arduino(port)
board.digital[p0].mode=SERVO
board.digital[p1].mode=SERVO
board.digital[p2].mode=SERVO
board.digital[p3].mode=SERVO
board.digital[p4].mode=SERVO
board.digital[p5].mode=SERVO

def rot(pin, ang):
    board.digital[pin].write(ang)
    sleep(0.5)

def all_off():
    rot(p0, 20)
    rot(p1, 0)
    rot(p2, 15)
    rot(p5, 0)
    rot(p3, 15)
    rot(p4, 8)
    sleep(2)

def all_on():
    rot(p0, 0)
    rot(p1, 18)
    rot(p2, 0)
    rot(p5, 20)
    rot(p3, 0)
    rot(p4, 20)
    sleep(2)

def on(pin):
    if pin==p0:
        rot(p0, 0)
    elif pin==p1:
        rot(p1, 18)
    elif pin==p2:
        rot(p2, 0)
    elif pin==p5:
        rot(p5, 20)
    elif pin==p3:
        rot(p3, 0)
    elif pin==p4:
        rot(p4, 20)

def off(pin):
    if pin==p0:
        rot(p0, 25)
    elif pin==p1:
        rot(p1, 0)
    elif pin==p2:
        rot(p2, 15)
    elif pin==p5:
        rot(p5, 0)
    elif pin==p3:
        rot(p3, 15)
    elif pin==p4:
        rot(p4, 8)

all_off()

model_dict = pickle.load(open('model1.p', 'rb'))
model = model_dict['model']



labels_dict = {0: 'A', 1: 'B', 2: 'C', 3: 'D', 4: 'E', 5: 'F', 6: 'G', 7: 'H', 8: 'I', 9: 'J', 10: 'K', 11: 'L', 12: 'M', 13: 'N', 14: 'O', 15: 'P', 16: 'Q', 17: 'R', 18: 'S', 19: 'T', 20: 'U', 21: 'V', 22: 'W', 23: 'X', 24: 'Y', 25: 'Z', 26: 'THANK YOU', 27: 'HELLO', 28: 'GOOD', 29: 'OKAY', 30:'NO', 31:'I LOVE YOU'}
letters={'a':[1,0,0,0,0,0],
        'b':[1,0,1,0,0,0],
        'c':[1,1,0,0,0,0],
        'd':[1,1,0,1,0,0],
        'e':[1,0,0,1,0,0],
        'f':[1,1,1,0,0,0],
        'g':[1,1,1,1,0,0],
        'h':[1,0,1,1,0,0],
        'i':[0,1,1,0,0,0],
        'j':[0,1,1,1,0,0],
        'k':[1,0,1,0,1,0],
        'l':[1,0,1,0,0,0],
        'm':[1,1,0,0,1,0],
        'n':[1,1,0,1,1,0],
        'o':[1,0,0,1,1,0],
        'p':[1,1,1,0,1,0],
        'q':[1,1,1,1,1,0],
        'r':[1,0,1,1,1,0],
        's':[0,1,1,0,1,0],
        't':[0,1,1,1,1,0],
        'u':[1,0,0,0,1,1],
        'v':[1,0,1,0,1,1],
        'w':[0,1,1,1,0,1],
        'x':[1,1,0,0,1,1],
        'y':[1,1,0,1,1,1],
        'z':[1,0,0,1,1,1],
        ' ':[0,0,0,0,0,0]}
l = []
def voice_input():
    global input_type
    input_type=2
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        messagebox.showinfo("showinfo", "Adjusting for ambient noise... Please wait.")
        recognizer.adjust_for_ambient_noise(source, duration=5)
        messagebox.showinfo("showinfo", "Listening...")
        audio = recognizer.listen(source)

    try:
        messagebox.showinfo("showinfo", "Recognizing...")
        global text
        text = recognizer.recognize_google(audio)
        print("You said: " + text)

    except sr.UnknownValueError:
        text=""
        messagebox.showerror("showerror", "Google Web Speech API could not understand the audio")
    except sr.RequestError as e:
        text=""
        messagebox.showerror("showerror", "Could not request results from Google Web Speech API; {0}".format(e))
    op()

def vid():
    flip_enabled = True
    global strng, l
    strng = ""
    l = []
    cap = cv2.VideoCapture(0)
    mp_hands = mp.solutions.hands
    mp_drawing = mp.solutions.drawing_utils
    mp_drawing_styles = mp.solutions.drawing_styles
    hands = mp_hands.Hands(static_image_mode=True, min_detection_confidence=0.3, max_num_hands=1)
    
    while True:
        if cv2.waitKey(1) & 0xFF == ord('x'):
            break
        key = cv2.waitKey(1)
        if key == ord('f'):
            flip_enabled = not flip_enabled

        data_aux = []
        x_ = []
        y_ = []

        ret, frame = cap.read()
        if not ret:
            messagebox.showerror("showerror", "Failed to capture image")
            break
        
        if flip_enabled:
            frame = cv2.flip(frame, 1)
        
        H, W, _ = frame.shape

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        predicted_character = ""
        results = hands.process(frame_rgb)
        
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(
                    frame,  # image to draw
                    hand_landmarks,  # model output
                    mp_hands.HAND_CONNECTIONS,  # hand connections
                    mp_drawing_styles.get_default_hand_landmarks_style(),
                    mp_drawing_styles.get_default_hand_connections_style())

            for hand_landmarks in results.multi_hand_landmarks:
                for i in range(len(hand_landmarks.landmark)):
                    x = hand_landmarks.landmark[i].x
                    y = hand_landmarks.landmark[i].y

                    x_.append(x)
                    y_.append(y)

                for i in range(len(hand_landmarks.landmark)):
                    x = hand_landmarks.landmark[i].x
                    y = hand_landmarks.landmark[i].y
                    data_aux.append(x - min(x_))
                    data_aux.append(y - min(y_))

            x1 = int(min(x_) * W) - 10
            y1 = int(min(y_) * H) - 10

            x2 = int(max(x_) * W) - 10
            y2 = int(max(y_) * H) - 10
            try:
                prediction = model.predict([np.asarray(data_aux)])

                predicted_character = labels_dict[int(prediction[0])]
            except ValueError:
                pass

            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 0), 4)
            cv2.putText(frame, predicted_character, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0, 0, 0), 3, cv2.LINE_AA)

        cv2.imshow('Press X to exit', frame)
        cv2.waitKey(1)
        
        time.sleep(0.5)
        
        recog = [0, 0, 0, 0, 0, 0]
        if predicted_character != '':
            recog = letters[predicted_character[0].lower()]
            if l == [] or l[-1] != predicted_character.lower():
                l.append(predicted_character.lower())
                strng += predicted_character.lower() + " "
                print(predicted_character.lower() + " ")

    cap.release()
    cv2.destroyAllWindows()

def braille_gen(stg):
    lis = stg.split()
    s = []
    for word in lis:
        for i in word:
            s.append(letters[i.lower()])
        s.append(letters[' '])
    print(s)
    for i in s:
        for j in range(len(i)):
            if i[j] == 1:
                on(p[j])
            else:
                off(p[j])
        sleep(1)
    all_off()

def say(text):
    language = 'en'
    tts_file = 'tts.mp3'
    if os.path.exists(tts_file):
        os.remove(tts_file)
    obj = gTTS(text=text, lang=language, slow=True)
    obj.save("tts.mp3")
    playsound('tts.mp3')
    
root=Tk()
root.title("UNITE.ai")
root.attributes('-fullscreen',True)
root.configure(bg='black')

landingbg="landing.png"
inputbg="input.png"
outputbg="output.png"
finalbg="next.png"
plainbg="plain.png"
pl="blnk.png"

input_type=0
output_type=0

def sup(*funcs):
    def combined_func(*args,**kwargs):
        for f in funcs:
            f(*args,**kwargs)
    return combined_func

def text_input():
    global input_type
    input_type=3
    def publish():
        global text_val
        text_val = entry.get()
        frame4.destroy()
        op()
    frame4 = Frame(root, width='1920', height='1080')
    frame4.pack(fill='both',expand=True)
    image9=ImageTk.PhotoImage(Image.open(plainbg))
    lblx=Label(frame4,image=image9)
    lblx.image=image9
    lblx.pack()
    global entry
    entry = Entry(frame4, width="41", bg="#282727", fg="white", relief="flat", font=('poppins',30))
    entry.place(relx=0.18,rely=0.454)

    button = Button(frame4, bg="#09D305", activebackground='#09D305', fg="white", width=25, height=2, relief="flat", text="Submit", font=('poppins',20), command=sup(publish))
    button.place(relx=0.5, rely=0.675, anchor='center')

    button = Button(frame4, bg="black", activebackground='red', activeforeground='white', fg="white", relief="flat", text="Exit", font=('poppins',15), command=sup(root.destroy))
    button.place(relx=0.95, rely=0.03)

def text_disp(tv):
    frame1 = Frame(root, width='1920', height='1080')
    frame1.pack(fill='both',expand=True)
    image9=ImageTk.PhotoImage(Image.open(pl))
    lblx=Label(frame1,image=image9)
    lblx.image=image9
    lblx.pack()
    button = Button(frame1, bg="#09D305", activebackground='#09D305', fg="white", width=25, height=2, relief="flat", text="Back to inputs", font=('poppins',20), command=sup(frame1.destroy, inp))
    button.place(relx=0.5, rely=0.645, anchor='center')
    ta = Label(frame1, width="41", height="5", bg="#282727", fg="white", relief="flat", text=tv, font=('poppins',30))
    ta.place(relx=0.5, rely=0.3, anchor='center')

def next():
    if input_type==1:
        vid()
        if output_type==1:
            text_disp(strng)
        elif output_type==2:
            say(strng)
        elif output_type==3:
            braille_gen(strng)
        elif output_type==4:
            braille_gen(strng)
            text_disp(strng)
        elif output_type==5:
            say(strng)
            braille_gen(strng)
            text_disp(strng)
        elif output_type==6:
            say(strng)
            text_disp(strng)

    elif input_type==2:
        # voice_input()
        if output_type==1:
            text_disp(text)
        elif output_type==2:
            say(text)
        elif output_type==3:
            braille_gen(text)
        elif output_type==4:
            text_disp(text)
            braille_gen(text)
        elif output_type==5:
            text_disp(text)
            say(text)
            braille_gen(text)
        elif output_type==6:
            text_disp(text)
            say(text)
    
    elif input_type==3:
        print(text_val)
        if output_type==1:
            text_disp(text_val)
        elif output_type==2:
            say(text_val)
        elif output_type==3:
            braille_gen(text_val)
        elif output_type==4:
            text_disp(text_val)
            braille_gen(text_val)
        elif output_type==5:
            text_disp(text_val)
            say(text_val)
            braille_gen(text_val)
        elif output_type==6:
            text_disp(text_val)
            say(text_val)
    frame1 = Frame(root, width='1920', height='1080')
    frame1.pack(fill='both',expand=True)
    image9=ImageTk.PhotoImage(Image.open(finalbg))
    lblx=Label(frame1,image=image9)
    lblx.image=image9
    lblx.pack()
    button = Button(frame1, bg="black", activebackground='red', activeforeground='white', fg="white", relief="flat", text="Exit", font=('poppins',15), command=sup(root.destroy))
    button.place(relx=0.95, rely=0.03)
    button = Button(frame1, bg="#09D305", activebackground='#09D305', fg="white", width=25, height=2, relief="flat", text="Proceed", font=('poppins',20), command=sup(frame1.destroy, inp))
    button.place(relx=0.5, rely=0.625, anchor='center')

def op():
    # print(text_val)
    frame3 = Frame(root, width='1920', height='1080')
    frame3.pack(fill='both',expand=True)
    
    def setop_text():
        global output_type
        output_type=1
        frame3.destroy()
        next()

    def setop_voice():
        global output_type
        output_type=2
        frame3.destroy()
        next()

    def setop_braille():
        global output_type
        output_type=3
        frame3.destroy()
        next()

    def setop_tb():
        global output_type
        output_type=4
        frame3.destroy()
        next()

    def setop_tvb():
        global output_type
        output_type=5
        frame3.destroy()
        next()

    def setop_tv():
        global output_type
        output_type=6
        frame3.destroy()
        next()

    image9=ImageTk.PhotoImage(Image.open(outputbg))
    lblx=Label(frame3,image=image9)
    lblx.image=image9
    lblx.pack()
    
    button = Button(frame3, bg="black", activebackground='red', activeforeground='white', fg="white", relief="flat", text="Exit", font=('poppins',15), command=sup(root.destroy))
    button.place(relx=0.95, rely=0.03)

    button = Button(frame3, bg="black", activebackground='blue', activeforeground='white', fg="white", relief="flat", text="Back", font=('poppins',15), command=sup(frame3.destroy, inp))
    button.place(relx=0.9, rely=0.03)

    button = Button(frame3, bg="#09D305", activebackground='#09D305', fg="white", width=25, height=2, relief="flat", text="Text", font=('poppins',20), command=sup(setop_text))
    button.place(relx=0.2, rely=0.335)

    button = Button(frame3, bg="#09D305", activebackground='#09D305', fg="white", width=25, height=2, relief="flat", text="Read Aloud", font=('poppins',20), command=sup(setop_voice))
    button.place(relx=0.2, rely=0.52)

    button = Button(frame3, bg="#09D305", activebackground='#09D305', fg="white", width=25, height=2, relief="flat", text="Generate Braille", font=('poppins',20), command=sup(setop_braille))
    button.place(relx=0.2, rely=0.708)
    
    button = Button(frame3, bg="#09D305", activebackground='#09D305', fg="white", width=25, height=2, relief="flat", text="Text and Braille", font=('poppins',20), command=sup(setop_tb))
    button.place(relx=0.535, rely=0.335)

    button = Button(frame3, bg="#09D305", activebackground='#09D305', fg="white", width=25, height=2, relief="flat", text="Text, Voice and Braille", font=('poppins',20), command=sup(setop_tvb))
    button.place(relx=0.535, rely=0.52)

    button = Button(frame3, bg="#09D305", activebackground='#09D305', fg="white", width=25, height=2, relief="flat", text="Text and Read Aloud", font=('poppins',20), command=sup(setop_tv))
    button.place(relx=0.535, rely=0.708)

def inp():
    frame2 = Frame(root, width='1920', height='1080')
    frame2.pack(fill='both',expand=True)
    
    def setip_sign():
        global input_type
        input_type=1
        frame2.destroy()
        op()

    def setip_speech():
        # global input_type
        # input_type=2
        frame2.destroy()
        voice_input()

    image9=ImageTk.PhotoImage(Image.open(inputbg))
    lblx=Label(frame2,image=image9)
    lblx.image=image9
    lblx.pack()
    
    button = Button(frame2, bg="black", activebackground='red', activeforeground='white', fg="white", relief="flat", text="Exit", font=('poppins',15), command=sup(root.destroy))
    button.place(relx=0.95, rely=0.03)

    button = Button(frame2, bg="#09D305", activebackground='#09D305', fg="white", width=25, height=2, relief="flat", text="Sign Language", font=('poppins',20), command=sup(setip_sign))
    button.place(relx=0.348, rely=0.327)

    button = Button(frame2, bg="#09D305", activebackground='#09D305', fg="white", width=25, height=2, relief="flat", text="Speak", font=('poppins',20), command=sup(setip_speech))
    button.place(relx=0.348, rely=0.515)

    button = Button(frame2, bg="#09D305", activebackground='#09D305', fg="white", width=25, height=2, relief="flat", text="Type", font=('poppins',20), command=sup(frame2.destroy, text_input))
    button.place(relx=0.348, rely=0.7)

def landing():
    frame1 = Frame(root, width='1920', height='1080')
    frame1.pack(fill='both',expand=True)
    image9=ImageTk.PhotoImage(Image.open(landingbg))
    lblx=Label(frame1,image=image9)
    lblx.image=image9
    lblx.pack()
    button = Button(frame1, bg="#09D305", activebackground='#09D305', fg="white", width=25, height=2, relief="flat", text="Get Started", font=('poppins',20), command=sup(frame1.destroy, inp))
    button.place(relx=0.5, rely=0.625, anchor='center')

landing()
root.mainloop()
