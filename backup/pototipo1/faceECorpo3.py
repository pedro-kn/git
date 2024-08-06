import cv2
import tkinter as tk
import shared_module
import GUI3

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
                cv2.imshow('Select Line', frame)
        elif len(line_coordinates) == 4:
            line_coordinates = [(x, y)]
            ignore_above = False



# shared_module.capture video stream (use your desired source)
shared_module.cap = cv2.VideoCapture(0) # Change to the appropriate camera index if needed

if shared_module.butt2 == False:
    # Create a window to display the frame and allow the user to select the line
    cv2.namedWindow('Select Line')
    cv2.setMouseCallback('Select Line', draw_line)



    while True:
        ret, frame = shared_module.cap.read()
        
        # Draw the line
        if len(line_coordinates) == 2:
            cv2.line(frame, line_coordinates[0], line_coordinates[1], (0, 255, 0), 2)

        cv2.imshow('Select Line', frame)

        if cv2.waitKey(1) & 0xFF == ord('q') or len(line_coordinates) == 3:
            cv2.destroyAllWindows()
            break



# Define the line equation ax + by + c = 0
line = (line_coordinates[0][1] - line_coordinates[1][1],
        line_coordinates[1][0] - line_coordinates[0][0],
        line_coordinates[0][0] * line_coordinates[1][1] - line_coordinates[1][0] * line_coordinates[0][1])


if shared_module.butt2 == True:

    while True:
        
        ret, frame = shared_module.cap.read()

        # Convert the frame to grayscale for detection
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Define the area to ignore based on the line equation
        for y in range(frame.shape[0]):
            for x in range(frame.shape[1]):
                if ignore_above and line[0] * x + line[1] * y + line[2] < 0:
                    gray[y, x] = 0
                elif not ignore_above and line[0] * x + line[1] * y + line[2] > 0:
                    gray[y, x] = 0

        # Detect shared_module.faces and upper bodies in the modified frame
        shared_module.faces = shared_module.face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)
        upper_bodies = shared_module.upper_body_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

        if shared_module.count == 0: 
            shared_module.check_alert_trigger = False

        if shared_module.count > 0:
                shared_module.count_no_detection = shared_module.count_no_detection + 1

        # Draw rectangles around the detected shared_module.faces and upper bodies
        for (x, y, w, h) in shared_module.faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 3)
            cv2.putText(frame, 'Face', (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 0), 2)
                
            GUI3.alert_trigger(frame)

        for (x, y, w, h) in upper_bodies:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)
            cv2.putText(frame, 'Upper Body', (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

        if shared_module.check_alert_trigger == True and shared_module.count > 0 and shared_module.count_no_detection > shared_module.count:
                GUI3.break_func()

        if shared_module.butt3 == False:

            # Display the resulting frame
            cv2.imshow('Câmera ativada (Q para finalizar)', frame)

            

            if cv2.waitKey(1) & 0xFF == ord('q'):
                GUI3.break_func()
                break

        #elif shared_module.butt3 == True & shared_module.cancelButt3 == True:

            
            
            #if cv2.waitKey(1) & 0xFF == ord('q'):
            #    break
            


            


# Release the shared_module.capture and close windows
       
shared_module.cap.release()
cv2.destroyAllWindows()
