# -*- coding: utf-8 -*-
"""
Created on Fri Mar  1 16:04:17 2024

@author: jcjea
"""

import numpy as np
import cv2

cap = cv2.VideoCapture(0)
face_det_model = cv2.dnn.readNetFromCaffe('./models/deploy.prototxt.txt','./models/res10_300x300_ssd_iter_140000_fp16.caffemodel')

def face_detectar_DNN(img):
    #passo 1 - blob from image
    #importante - o dnn foi treinado para imagens de 300x300
    blob = cv2.dnn.blobFromImage(img,1,(300,300),(104,177,123),swapRB=True)
    
    #passo 2: setar o blob como entrada
    
    face_det_model.setInput(blob)
    
    #passo 3: pegar a saida 
    detectar = face_det_model.forward()
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
        if confianca > 0.1: # verifica se o valor de confiança é maior que 50%
            #pontos diagonais 3:7
            #é necessario multiplicar o valor do detectar, pois o valores vem normalizados
            box = detectar[0,0,i,3:7]*np.array([w,h,w,h])
            box = box.astype('int') #trasforma o numero para inteiro
            pt1 = (box[0],box[1])
            pt2 = (box[2],box[3])
            # desenhar caixa
            cv2.rectangle(image,pt1,pt2, (0,255,0),1)
            text = 'score : {:.0f}'.format(confianca*100)
            cv2.putText(image,text,pt1,cv2.FONT_HERSHEY_SIMPLEX,1,(255,255,255),2)
            
    return image

while True:
    ret, frame = cap.read()
    
    if ret == False:
        break
    
    img_detectar = face_detectar_DNN(frame)
    
    cv2.imshow('Tempo Real',img_detectar)
    
    if cv2.waitKey(1) == ord("a"):
        break

cap.release()
cv2.destroyAllWindows()
