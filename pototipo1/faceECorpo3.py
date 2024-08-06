import cv2
import numpy as np
import tkinter as tk
import datetime
import glob
import os
import shared_module
from threading import *
#import GUI3

def alert_trigger(frameCapturado):
    #print("entrou alert_trigger")
    #print(str(datetime.datetime.now()))

    

    shared_module.text_value = "Detectado!"
    #result_label.config(text=shared_module.text_value) 

    #confere se o sistema entrou aqui, seta como false e salva novo video caso nao detecte mais rostos
    shared_module.check_alert_trigger = True

    shared_module.count = 1 + shared_module.count

    if shared_module.count == 1:
        shared_module.starttime = datetime.datetime.now()
        shared_module.popuptime = datetime.datetime.now()

    shared_module.popuptimecontrol = datetime.datetime.now() - shared_module.popuptime

    

    if shared_module.count < 10:
        direct = "pototipo1/capturas/00000" + str(shared_module.count) + ".png"
    elif shared_module.count >= 10 and shared_module.count < 100:
        direct = "pototipo1/capturas/0000" + str(shared_module.count) + ".png"
    elif shared_module.count >= 100 and shared_module.count < 1000: 
        direct = "pototipo1/capturas/000" + str(shared_module.count) + ".png"
    elif shared_module.count >= 1000 and shared_module.count < 10000: 
        direct = "pototipo1/capturas/00" + str(shared_module.count) + ".png" 
    elif shared_module.count >= 10000 and shared_module.count < 100000: 
        direct = "pototipo1/capturas/0" + str(shared_module.count) + ".png" 
    elif shared_module.count >= 100000: 
        direct = "pototipo1/capturas/" + str(shared_module.count) + ".png"              

    # describe the font type
    font = cv2.FONT_HERSHEY_SIMPLEX

    #if shared_module.count != 1:
        #logica pra descobrir a framerate
    #    elapsedtime = datetime.datetime.now() - shared_module.elapsedtimesincelastiteration
    #    shared_module.elapsedtimesincelastiteration = datetime.datetime.now()
    #    shared_module.framerate = 1/(elapsedtime.total_seconds())

        # Get current date and time  
    #    date_time = str(datetime.datetime.now()) + "FPS: " + str(shared_module.framerate) 
    #elif  shared_module.count == 1:
    #    shared_module.elapsedtimesincelastiteration = datetime.datetime.now()
        # Get current date and time  
    date_time = str(datetime.datetime.now())    

    # write the date time in the video frame
    frameCapturado = cv2.putText(frameCapturado, date_time,(10, 30),font, 1,(210, 155, 155), 4, cv2.LINE_4)

    cv2.imwrite(direct, frameCapturado)

    if shared_module.popuptimecontrol.total_seconds() > 3.0:
        shared_module.popuptime = datetime.datetime.now()
        if shared_module.popupallow == True:
            shared_module.popuplog = True

    #shared_module.root = tk.Tk()
    #shared_module.root.title("Aperte para cancelar a detecção minimizada")

    #buttonCancel = tk.Button(shared_module.root, text="Cancelar", command=break_func)
    #buttonCancel.pack(side=tk.LEFT, padx=10, pady=10)

 # Inicia o processo de detecção
def execute_code_2():
    shared_module.butt2 = True
    shared_module.butt3 = False
    shared_module.popuplog = False
    
    exec(open(r'pototipo1\faceECorpo3.py').read())   


def break_func():

    img_array = []

    for filename in glob.glob('pototipo1/capturas/*.png'):
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

    #logica pra descobrir a framerate
    elapsedtime = datetime.datetime.now() - shared_module.starttime
    shared_module.framerate = 1/((elapsedtime.total_seconds())/len(img_array))


    #out = cv2.VideoWriter('project.avi',cv2.VideoWriter.fourcc(*'DIVX'), 15, size)
    #out = cv2.VideoWriter('project.avi',fourcc, 5, (640,480))
    out = cv2.VideoWriter(time_date,fourcc, shared_module.framerate, (640,480))

    print(str(shared_module.framerate))

    print(len(img_array))

    i = 0

    for i in range(len(img_array)):
        out.write(img_array[i])     
    out.release()

    files = glob.glob('pototipo1/capturas/*')
    for f in files:
        os.remove(f) #remove os png da pasta capturas

    

    shared_module.count = 0
    shared_module.count_no_detection = 0
    #shared_module.cap.release()
    #cv2.destroyAllWindows()

if shared_module.butt2 == False:
    # Load pre-trained Haar cascades for face and upper body detection
    #face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    #upper_body_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_upperbody.xml')
    #face_cascade = cv2.CascadeClassifier(r'pototipo1\haarcascade_frontalface_default.xml')
    #upper_body_cascade = cv2.CascadeClassifier(r'pototipo1\haarcascade_upperbody.xml')

    # Global variables for the line coordinates and segment selection
    line_coordinates = []
    ignore_above = False
 
# Function to draw a line on the frame
def draw_line(event, x, y, flags, param):
    global line_coordinates, ignore_above
    if event == cv2.EVENT_LBUTTONDOWN:
        if len(line_coordinates) < 4:
            line_coordinates.append((x, y))
            if len(line_coordinates) == 2:
                cv2.line(frame, line_coordinates[0], line_coordinates[1], (0, 255, 0), 2)
                cv2.imshow('Selecione a Margem (Q para Finalizar)', frame)
        elif len(line_coordinates) == 4:
            line_coordinates = [(x, y)]
            ignore_above = False



# shared_module.capture video stream (use your desired source)
shared_module.cap = cv2.VideoCapture(0) # Change to the appropriate camera index if needed
shared_module.face_det_model = cv2.dnn.readNetFromCaffe('./models/deploy.prototxt.txt','./models/res10_300x300_ssd_iter_140000_fp16.caffemodel')

def face_detectar_DNN(img):
    #passo 1 - blob from image
    #importante - o dnn foi treinado para imagens de 300x300
    blob = cv2.dnn.blobFromImage(img,1,(300,300),(104,177,123),swapRB=True)

    #passo 2: setar o blob como entrada
    
    shared_module.face_det_model.setInput(blob)
    
    #passo 3: pegar a saida 
    detectar = shared_module.face_det_model.forward()
    #detectar.shape - resulta em um vetor de 4 celulas;
    #sendo que a terceira celula é quantidade de faces encontradas
    #o valor de padrão que o algoritmo Caffe detecta é 200
    # o quarta celula pode ser 7 valores possiveis, e depende o valor resulta em um valor diferente
    # 0: numero da imagem
    # 1: binario (0 ou 1)
    # 2: pontuação de confiança (0 ate 1), quanto mais proximo de 1 maior certeza de ser uma face
    # 3: Inicio X
    # 4: Inicio Y
    # 5: Fim X
    # 6: Fim Y
    
    
    #passo 4: desenhaar uma caixa entorno da face

    image = img.copy() # cria uma copia
    h,w = image.shape[:2] # pega o tamanho da imagem.
    for i in range(0,detectar.shape[2]): # cria um for que começa em 0 e vai ate o numero de face encontradas, por isso que analisa a posição 2 (celula 3), onde tem as possiveis faces
        confianca = detectar[0,0,i,2] # acessa a confiança e salva   
        if confianca > 0.15: # verifica se o valor de confiança é maior que 15%
            #pontos diagonais 3:7
            #é necessario multiplicar o valor do detectar, pois o valores vem normalizados
            box = detectar[0,0,i,3:7]*np.array([w,h,w,h])
            box = box.astype('int') #trasforma o numero para inteiro
            pt1 = (box[0],box[1])
            pt2 = (box[2],box[3])
            if box[2] - box[0] < 60:
                # seta a flag para iniciar a gravação
                shared_module.frontal_face_detected = True
                # desenhar caixa
                cv2.rectangle(image,pt1,pt2, (0,255,0),1)
                text = 'Face Detectada {:.0f}'.format(confianca*100)
                cv2.putText(image,text,pt1,cv2.FONT_HERSHEY_SIMPLEX,1,(255,255,255),2)
            elif box[2] - box[0] < 90:
                # seta a flag para iniciar a gravação
                shared_module.frontal_face_detected = True
                # desenhar caixa
                cv2.rectangle(image,pt1,pt2, (0,255,255),1)
                text = 'Cuidado! {:.0f}'.format(confianca*100)
                cv2.putText(image,text,pt1,cv2.FONT_HERSHEY_SIMPLEX,1,(255,255,255),2) 
            elif box[2] - box[0] >= 90:
                # seta a flag para iniciar a gravação
                shared_module.frontal_face_detected = True
                # desenhar caixa
                cv2.rectangle(image,pt1,pt2, (0,0,255),1)
                text = 'Alerta! {:.0f}'.format(confianca*100)
                cv2.putText(image,text,pt1,cv2.FONT_HERSHEY_SIMPLEX,1,(255,255,255),2)    
            
    return image


    

if shared_module.butt2 == False and shared_module.regiao == False:

    #def window_CV():
    # Create a window to display the frame and allow the user to select the line
    cv2.namedWindow('Selecione a Margem (Q para Finalizar)')
    cv2.setMouseCallback('Selecione a Margem (Q para Finalizar)', draw_line)



    while True:
        ret, frame = shared_module.cap.read()
        

        # Draw the line
        if len(line_coordinates) == 2:
            cv2.line(frame, line_coordinates[0], line_coordinates[1], (0, 255, 0), 2)

        cv2.imshow('Selecione a Margem (Q para Finalizar)', frame)

        if cv2.waitKey(1) & 0xFF == ord('q') or len(line_coordinates) == 3:
            cv2.destroyAllWindows()
            break

    if len(line_coordinates) == 3:
            shared_module.hemisphere = line_coordinates[2]
   
            


# Define the line equation ax + by + c = 0
line = (line_coordinates[0][1] - line_coordinates[1][1],
        line_coordinates[1][0] - line_coordinates[0][0],
        line_coordinates[0][0] * line_coordinates[1][1] - line_coordinates[1][0] * line_coordinates[0][1])

#verfique se x hemisferio esta entre os dois x da linha
# e que o y hemisferio esta entre os dois y da linha
shared_module.arriba = False
if shared_module.hemisphere[0] > line_coordinates[0][0] or shared_module.hemisphere[0] < line_coordinates[1][0]:
    if shared_module.hemisphere[1] > line_coordinates[0][1] or shared_module.hemisphere[1] < line_coordinates[1][1]:
        shared_module.arriba = True

#demonstra a imagem selecionada
if len(line_coordinates) == 3 and shared_module.regiao == False:
    while True:
        ret, frame = shared_module.cap.read()
        
        #gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)    
        for y in range(frame.shape[0]):
            for x in range(frame.shape[1]):
                if shared_module.arriba == True:
                    if ignore_above and line[0] * x + line[1] * y + line[2] < 0:
                        frame[y, x] = 0
                    elif not ignore_above and line[0] * x + line[1] * y + line[2] > 0:
                        frame[y, x] = 0
                elif shared_module.arriba == False:
                    if not ignore_above and line[0] * x + line[1] * y + line[2] < 0:
                        frame[y, x] = 0
                    elif ignore_above and line[0] * x + line[1] * y + line[2] > 0:
                        frame[y, x] = 0 

        # describe the font type
        font = cv2.FONT_HERSHEY_SIMPLEX
        
        cv2.putText(frame, "Limites estabelecidos!",(10, 400),font, 1,(255, 255, 255), 1, cv2.LINE_4)
        cv2.putText(frame, "Pressione Q para sair.",(10, 440),font, 1,(255, 255, 255), 1, cv2.LINE_4)

        #cv2.imwrite(direct, frameCapturado)                
    
        cv2.imshow('Selecione a Margem (Q para Finalizar)', frame)

        if cv2.waitKey(1) & 0xFF == ord('q') or len(line_coordinates) == 4:
            shared_module.regiao = True
            cv2.destroyAllWindows()
            break

if shared_module.butt2 == True:

    while True:
        
        ret, frame = shared_module.cap.read()

        if ret == False:
            break
        
        #frame_sem_corte_de_regiao = frame

        # Define the area to ignore based on the line equation
        for y in range(frame.shape[0]):
            for x in range(frame.shape[1]):
                if ignore_above and line[0] * x + line[1] * y + line[2] < 0:
                   frame[y, x] = 0
                elif not ignore_above and line[0] * x + line[1] * y + line[2] > 0:
                    frame[y, x] = 0

        if shared_module.count == 0: 
            shared_module.check_alert_trigger = False

        if shared_module.count > 0:
            shared_module.count_no_detection = shared_module.count_no_detection + 1
        
        img_detectar = face_detectar_DNN(frame)

               
        if shared_module.frontal_face_detected == True:
           alert_trigger(img_detectar)
        
        cv2.imshow('Tempo Real',img_detectar)
        
        #if cv2.waitKey(1) == ord("a"):
        #    break


                
        shared_module.frontal_face_detected = False
        shared_module.profile_face_detected = False

        if shared_module.check_alert_trigger == True and shared_module.count > 0 and shared_module.count_no_detection > (shared_module.count + 5):
                break_func()

        if shared_module.popuplog == True and shared_module.popupallow == True:
            cv2.destroyAllWindows()
            shared_module.cap.release()
            execute_code_2()
            break

        if shared_module.butt3 == False:

            # Display the resulting frame
            #cv2.imshow('Câmera ativada (Q para finalizar)', frame)

            
            # Display the resulting frame
            #cv2.imshow('Vigilante9 ativado (Q para finalizar)', frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break_func()
                break

        #elif shared_module.butt3 == True & shared_module.cancelButt3 == True:

            
            
            #if cv2.waitKey(1) & 0xFF == ord('q'):
            #    break
                


        

                


# Release the shared_module.capture and close windows
       
shared_module.cap.release()
cv2.destroyAllWindows()

#permite alternar entre telas
shared_module.t2 = Thread(target=ret)


