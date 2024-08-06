
import datetime
from os import remove
import os
import threading
import tkinter as tk
import sys
from tkinter import filedialog
from tkinter import *
import cv2
from PIL import Image, ImageTk
import threading
import time
import keyboard
import shared_module
import numpy as np
import glob

event = threading.Event()
frameCapturado = None
img_array = []


#while not event.is_set():
    #time.sleep(2)
    #print("Hello")
   # time.sleep(2)
    


# Executa a definição de limites para captura de rostos
def execute_code_1():
    shared_module.butt2 = False
    shared_module.text_value = "Limites de detecção estabelicidos!"
    result_label.config(text=shared_module.text_value)
    exec(open(r'pototipo1\faceECorpo3.py').read())

def label_code_2():
    shared_module.text_value = "Processo de detecção encerrado!"
    result_label.config(text=shared_module.text_value)
    execute_code_2()


# Inicia o processo de detecção
def execute_code_2():
    shared_module.butt2 = True
    shared_module.butt3 = False
    
    exec(open(r'pototipo1\faceECorpo3.py').read())
    

def execute_code_3():
    # Replace with the code you want to execute for Button 2
    shared_module.butt2 = True
    shared_module.butt3 = True
    
    if shared_module.cancelButt3 == False:
        shared_module.cancelButt3 = True
        shared_module.text_value = "Code 3 False executed"
        result_label.config(text=shared_module.text_value)
        exec(open(r'pototipo1\faceECorpo3.py').read())
    elif shared_module.cancelButt3 == True:
        shared_module.text_value = "Code 3 True executed"
        result_label.config(text=shared_module.text_value)
        shared_module.cancelButt3 = False
        shared_module.cap.release()

def execute_code_4():
    email = shared_module.entry1.get()

    print(email)
    shared_module.text_value = "E-mail " + email + " cadastrado!"
    result_label.config(text=shared_module.text_value)

    exec(open(r'pototipo1\e-mail.py').read())



def alert_trigger(frameCapturado):
    print("entrou alert_trigger")
    shared_module.text_value = "Detectado!"
    #result_label.config(text=shared_module.text_value) 

    #confere se o sistema entrou aqui, seta como false e salva novo video caso nao detecte mais rostos
    shared_module.check_alert_trigger = True

    shared_module.count = 1 + shared_module.count

    if shared_module.count < 10:
        direct = "pototipo1/capturas/0000" + str(shared_module.count) + ".png"
    elif shared_module.count >= 10 and shared_module.count < 100:
        direct = "pototipo1/capturas/000" + str(shared_module.count) + ".png"
    elif shared_module.count >= 100 and shared_module.count < 1000: 
        direct = "pototipo1/capturas/00" + str(shared_module.count) + ".png"
    elif shared_module.count >= 1000 and shared_module.count < 10000: 
        direct = "pototipo1/capturas/0" + str(shared_module.count) + ".png" 
    elif shared_module.count >= 10000: 
        direct = "pototipo1/capturas/" + str(shared_module.count) + ".png"           

    # describe the font type
    font = cv2.FONT_HERSHEY_SIMPLEX

    # Get current date and time  
    date_time = str(datetime.datetime.now())

    # write the date time in the video frame
    frameCapturado = cv2.putText(frameCapturado, date_time,(10, 100),font, 1,(210, 155, 155), 4, cv2.LINE_4)

    #cv2.imwrite("capturas/GeeksForGeeks.png", frameCapturado)

    cv2.imwrite(direct, frameCapturado)

    

    #shared_module.root = tk.Tk()
    #shared_module.root.title("Aperte para cancelar a detecção minimizada")

    #buttonCancel = tk.Button(shared_module.root, text="Cancelar", command=break_func)
    #buttonCancel.pack(side=tk.LEFT, padx=10, pady=10)

    

    #shared_module.root.mainloop() 

#movida para faceEcorpor3.py
def break_func():

    img_array = []

    for filename in glob.glob('capturas/*.png'):
        img = cv2.imread(filename)
        height, width, layers = img.shape
        size = (width,height)

        img_array.append(img)
    
    fourcc = cv2.VideoWriter_fourcc(*'XVID')

    time_date = str(datetime.datetime.now()) + '.avi'
    time_date = time_date.replace(" ", "_")
    time_date = time_date.replace(".", "", 1)
    time_date = time_date.replace(":", "-")
    #time_date = 'rec.avi'

    #out = cv2.VideoWriter('project.avi',cv2.VideoWriter.fourcc(*'DIVX'), 15, size)
    #out = cv2.VideoWriter('project.avi',fourcc, 5, (640,480))
    out = cv2.VideoWriter(time_date,fourcc, 5, (640,480))

    print(str(datetime.datetime.now()))

    print(len(img_array))

    i = 0

    for i in range(len(img_array)):
        out.write(img_array[i])     
    out.release()

    files = glob.glob('capturas/*')
    for f in files:
        os.remove(f) #remove os png da pasta capturas

    

    shared_module.count = 0
    shared_module.count_no_detection = 0
    #shared_module.cap.release()
    #cv2.destroyAllWindows()

# Main function to create the GUI
def main():

    global canvas, result_label

    shared_module.root = tk.Tk()
    shared_module.root.title("Vigilante 9")
    

    # Create a frame to display the executed code result
    result_frame = tk.Frame(shared_module.root, padx=10, pady=10)
    #result_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
    result_frame.grid(row=1,column=0,columnspan=3, padx=20, pady=10)
    

    # Create a label to display the result text

    result_label = tk.Label(result_frame, text="", font=("Helvetica", 14), wraplength=1000, name='frame1')
    #result_label.pack()
    result_label.grid()

    entry1_label = tk.Label(shared_module.root, text = 'E-mail:')
    entry1_label.grid(row=2,column=0, padx=10, pady=0)

    shared_module.entry1 = tk.Entry(shared_module.root)
    #entry1.pack(side=tk.LEFT, padx=10, pady=10)
    shared_module.entry1.grid(row=2,column=1, padx=0, pady=0)

    button3 = tk.Button(shared_module.root, text="Ativar Envio de Email", command=execute_code_4)
    #button1.pack(side=tk.LEFT, padx=10, pady=10)
    button3.grid(row=2,column=2, padx=10, pady=10)

    # Create two buttons
    button1 = tk.Button(shared_module.root, text="Configurar Detecção de Imagem", command=execute_code_1)
    #button1.pack(side=tk.LEFT, padx=10, pady=10)
    button1.grid(row=3,column=1, padx=10, pady=10)

    button2 = tk.Button(shared_module.root, text="Ativar Detecção", command=label_code_2)
    #button2.pack(side=tk.LEFT, padx=10, pady=10)
    button2.grid(row=3,column=2, padx=10, pady=10)

    

    #button3 = tk.Button(shared_module.root, text="Ativar/Desativar Detecção Minimizada", command=execute_code_3)
    #button3.pack(side=tk.LEFT, padx=10, pady=10)

    # Create a canvas to display OpenCV images
    canvas = tk.Canvas(shared_module.root, width=10, height=10)
    #canvas.pack(side=tk.BOTTOM, padx=10, pady=10)
    canvas.grid(padx=10, pady=10)

    shared_module.root.mainloop()

#def stop():
 #   event.set()
#    main()

#keyboard.add_hotkey("ctrl+alt+d", main()) 

if __name__ == "__main__":
    main()

