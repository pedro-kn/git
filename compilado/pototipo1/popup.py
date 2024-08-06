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
#import shared_module
import numpy as np
import glob



# Main function to create the GUI
def main():

    global canvas, result_label

    root = tk.Tk()
    root.title("Alerta!")
    

    # Create a frame to display the executed code result
    result_frame = tk.Frame(root, padx=10, pady=10)
    #result_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
    result_frame.grid(row=1,column=0,columnspan=3, padx=20, pady=10)
    

    # Create a label to display the result text

    result_label = tk.Label(result_frame, text="", font=("Helvetica", 14), wraplength=1000, name='frame1')
    #result_label.pack()
    result_label.grid()

    #exec(open(r'pototipo1\faceECorpo3.py').read())

    root.mainloop()

#def stop():
 #   event.set()
#    main()

#keyboard.add_hotkey("ctrl+alt+d", main()) 

if __name__ == "__main__":
    main()

