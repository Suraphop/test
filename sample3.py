# Import required Libraries
from tkinter import *
from PIL import Image, ImageTk
import cv2
import numpy as np 
import sqlite3
#import RPi.GPIO as GPIO
import time

def create_table():
    try:
        sqliteConnection = sqlite3.connect('./db/sqlite_parameter.db')
        sqlite_create_table_query = '''CREATE TABLE parameter (
                                    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                                    ub_blue INTEGER NOT NULL,
                                    ub_green INTEGER NOT NULL,
                                    ub_red INTEGER NOT NULL,
                                    adaptive_param_2 INTEGER NOT NULL,
                                    kernel_param INTEGER NOT NULL,
                                    dilation_iter INTEGER NOT NULL,
                                    area_param INTEGER NOT NULL,
                                    approx_poly INTEGER NOT NULL
                                    );'''

        cursor = sqliteConnection.cursor()
        print("Successfully Connected to SQLite")
        cursor.execute(sqlite_create_table_query)
        sqliteConnection.commit()
        print("SQLite table created")

        cursor.close()

    except sqlite3.Error as error:
        print("Error while creating a sqlite table", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("sqlite connection is closed")

def insert_param(ub_blue,ub_green,ub_red,adaptive_param_2,kernel_param,dilation_iter,area_param,approx_poly):
    try:
        sqliteConnection = sqlite3.connect('./db/sqlite_parameter.db')
        cursor = sqliteConnection.cursor()
        print("Successfully Connected to SQLite")

        sqlite_insert_query = """INSERT INTO parameter
                            (ub_blue, ub_green, ub_red, adaptive_param_2, kernel_param,dilation_iter,area_param,approx_poly) 
                            VALUES 
                            ("""+str(ub_blue)+""","""+str(ub_green)+""","""+str(ub_red)+""","""+str(adaptive_param_2)+""","""+str(kernel_param)+""",
                            """+str(dilation_iter)+""","""+str(area_param)+""","""+str(approx_poly)+""")"""

        count = cursor.execute(sqlite_insert_query)
        sqliteConnection.commit()
        print("Record inserted successfully into table ", cursor.rowcount)
        cursor.close()

    except sqlite3.Error as error:
        print("Failed to insert data into sqlite table", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("The SQLite connection is closed")

def getParam():
    try:
        sqliteConnection = sqlite3.connect('./db/sqlite_parameter.db')
        cursor = sqliteConnection.cursor()
        print("Connected to SQLite")

        sql_select_query = """select * from parameter order by created_at desc limit 1"""

        cursor.execute(sql_select_query)
        records = cursor.fetchall()
        for row in records:
            print("ub_blue = ", row[1])
            print("ub_green  = ", row[2])
            print("ub_red  = ", row[3])
            print("adaptive_param_2  = ", row[4])
            print("kernel_param  = ", row[5])
            print("dilation_iter  = ", row[6])
            print("area_param  = ", row[7])
            print("approx_poly  = ", row[8])
        cursor.close()
        return row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8]

    except sqlite3.Error as error:
        print("Failed to read data from sqlite table", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("The SQLite connection is closed")

def result_ok():
    global result,color_result
    result = "OK"
    color_result = (0,255,0)

def result_ng():
    global result,color_result
    result = "NG"
    color_result = (255,0,0)

def ub_blue_value(val):
    global ub_blue
    ub_blue = val

def ub_green_value(val):
    global ub_green
    ub_green = val

def ub_red_value(val):
    global ub_red
    ub_red = val

def adaptive_param_2_value(val):
    global adaptive_param_2
    adaptive_param_2 = val

def kernel_value(val):
    global kernel_param
    kernel_param = val

def dilation_iter_value(val):
    global dilation_iter
    dilation_iter = val

def area_value(val):
    global area_param
    area_param = val

def approx_poly_value(val):
    global approx_poly
    approx_poly = val

def running():
    global mode
    mode = 0
    
def openColorMarkWindow():
    global mode,ub_blue,ub_green,ub_red
    mode = 1

    newWindow = Toplevel(master)
    newWindow.title("Color Mark")
    newWindow.geometry("400x200")

    Label(newWindow,text ="BLUE").pack()
    #Initialize a Horizontal Scale Widget
    ub_blue_slide=Scale(newWindow, from_=0, to=255, orient= HORIZONTAL, command=ub_blue_value)
    ub_blue_slide.set(int(ub_blue))
    ub_blue_slide.pack()

    Label(newWindow,text ="GREEN").pack()
    #Initialize a Horizontal Scale Widget
    ub_green_slide=Scale(newWindow, from_=0, to=255, orient= HORIZONTAL, command=ub_green_value)
    ub_green_slide.set(int(ub_green))
    ub_green_slide.pack()

    Label(newWindow,text ="RED").pack()
    #Initialize a Horizontal Scale Widget
    ub_red_slide=Scale(newWindow, from_=0, to=255, orient= HORIZONTAL, command=ub_red_value)
    ub_red_slide.set(int(ub_red))
    ub_red_slide.pack()

def openContoursWindow():
    global mode,adaptive_param_2,dilation_iter,kernel_value,area_param,approx_poly
    mode = 2

    newWindow = Toplevel(master)
    newWindow.title("Contours")
 
    # sets the geometry of toplevel
    newWindow.geometry("400x400")

    Label(newWindow,text ="ADAPTIVE PARAM 2").pack()
    adaptive_param_2_slide=Scale(newWindow, from_=1, to=10, orient= HORIZONTAL, command=adaptive_param_2_value)
    adaptive_param_2_slide.set(int(adaptive_param_2))
    adaptive_param_2_slide.pack()

    Label(newWindow,text ="KERNEL").pack()
    kernel_slide=Scale(newWindow, from_=1, to=13, orient= HORIZONTAL, command=kernel_value)
    kernel_slide.set(int(kernel_param))
    kernel_slide.pack()

    Label(newWindow,text ="DILATION INTER").pack()
    dilation_iter_slide=Scale(newWindow, from_=1, to=13, orient= HORIZONTAL, command=dilation_iter_value)
    dilation_iter_slide.set(int(dilation_iter))
    dilation_iter_slide.pack()

    Label(newWindow,text ="AREA").pack()
    area_slide=Scale(newWindow, from_=10000, to=100000, orient= HORIZONTAL, command=area_value)
    area_slide.set(int(area_param))
    area_slide.pack()

def openApproxPolysWindow():
    global mode,approx_poly
    mode = 3

    newWindow = Toplevel(master)
    newWindow.title("Approx poly")
    newWindow.geometry("400x100")

    Label(newWindow,text ="APPROX POLY").pack()
    area_slide=Scale(newWindow, from_=1, to=10, orient= HORIZONTAL, command=approx_poly_value)
    area_slide.set(int(approx_poly))
    area_slide.pack()

def save():
    global ub_blue,ub_green,ub_red,adaptive_param_2,kernel_param,dilation_iter,area_param,approx_poly
    insert_param(ub_blue,ub_green,ub_red,adaptive_param_2,kernel_param,dilation_iter,area_param,approx_poly)

def ticker_sensor():
    gpio = 0

    if int(gpio) == int(1):
        return True
    else:
        return False

def output_signal():
    global current_result
    if current_result == "OK":
        print("ok signal")
    elif current_result == "NG":
        print("ng signal")
    else:
        print('output signal error')

# Define function to show frame
def show_frames():
    # Get the latest frame and convert into Image
    global mode,ub_blue,ub_green,ub_red,adaptive_param_2,kernel_param,dilation_iter,area_param,approx_poly,result,current_result,color_result,current_color_result

    ret, img = vid.read()
    
    cv2image= cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    img_output = cv2image.copy()
    #img_resize = cv2.resize(cv2image,(720,960),interpolation = cv2.INTER_LINEAR)

    img_resize = cv2image

    img_hsv = cv2.cvtColor(img_resize, cv2.COLOR_BGR2HSV) #hsv

    lb = np.array([0, 0, 0])
    ub = np.array([int(ub_red), int(ub_green), int(ub_blue)])
    mask = cv2.inRange(img_hsv, lb, ub)
    img_mask = cv2.bitwise_and(img_resize, img_resize, mask=mask) #mask 

    img_gry = cv2.cvtColor(img_mask,cv2.COLOR_BGR2GRAY) #gray
    img_blr = cv2.blur(img_gry,(5,5)) #blur

    img_th = cv2.adaptiveThreshold(img_blr, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV,5,int(adaptive_param_2)) #theshold

    kernel = np.ones((int(kernel_param),int(kernel_param)),np.uint8)
    dilation = cv2.dilate(img_th,kernel,iterations = int(dilation_iter))

    contours, hierarchy = cv2.findContours(dilation, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    out = np.zeros_like(dilation)

    for contour in contours:
        area = cv2.contourArea(contour)

        if area >int(area_param) : 
       
            # cv2.approxPloyDP() function to approximate the shape
            approx = cv2.approxPolyDP(
                contour, (round(int(approx_poly)/100,2)) * cv2.arcLength(contour, True), True)
            
            # using drawContours() function
            cv2.drawContours(out, contour, -1, 255, 3)
            cv2.drawContours(img_output, [approx], -1, (0, 0, 255), 3)

            # finding center point of shape
            M = cv2.moments(contour)
      
            if M['m00'] != 0.0:
                x = int(M['m10']/M['m00'])
                y = int(M['m01']/M['m00'])

            if len(approx) == 5:
                result_ok()
                cv2.putText(img_output, 'Pentagon (OK)', (x, y),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
            elif len(approx) == 6:
                result_ng()
                cv2.putText(img_output, 'Hexagon (NG)', (x, y),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)
            else:
                result_ng()
                cv2.putText(img_output, 'cannot detect,please move the object a little bit', (x, y),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

    if mode == 0:
        img_show = img_output
        cv2.putText(img_show, 'RUNNING MODE', (10, 40),cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 0), 3)
        cv2.rectangle(img_show, (90,110), (550,360), (255,255,0), 3)
        cv2.putText(img_show, current_result, (550, 40),cv2.FONT_HERSHEY_SIMPLEX, 1.2, current_color_result, 3)
        img_show = cv2.resize(img_show,(1152,864),interpolation = cv2.INTER_LINEAR)

        if ticker_sensor() == True:
            current_result = result
            current_color_result = color_result
            output_signal()
    elif mode == 1:
        img_show = img_mask
        cv2.putText(img_show, 'COLOR MARK EDIT', (10, 40),cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 255), 3)
    elif mode == 2:
        img_show = out
        cv2.putText(img_show, 'CONTOURS EDIT', (10, 40),cv2.FONT_HERSHEY_SIMPLEX, 1.2, (255, 255, 255), 3)
    elif mode == 3:
        img_show = img_output
        cv2.putText(img_show, 'APPROX POLY EDIT', (10, 40),cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 255), 3)
    else:
        print('else')


    img = Image.fromarray(img_show)

    # Convert image to PhotoImage
    imgtk = ImageTk.PhotoImage(image = img)
    label.imgtk = imgtk
    label.configure(image=imgtk)

    
    # # Repeat after an interval to capture continiously
    label.after(1, show_frames)

if __name__ == "__main__":
    try:
        
        # ok_output = 33
        # ng_output = 35
        # ticker_sersor = 37
        #GPIO.setmode(GPIO.BOARD)
        #GPIO.setup(ok_output, GPIO.OUT)
        #GPIO.setup(ng_output, GPIO.OUT)
        #GPIO.setup(ticker_sersor, GPIO.IN)

        mode = 0
        current_result = 'init'
        result = 'init'

        current_color_result = (255,255,255)
        color_result = (255,255,255)

        create_table()

        ub_blue,ub_green,ub_red,adaptive_param_2,kernel_param,dilation_iter,area_param,approx_poly = getParam()
        
        # Create an instance of TKinter Window or frame
        master = Tk()
        master.title('COMPUTER VISION')
        master.attributes('-fullscreen', True)

        button1=Button(master, text="RUNNING MODE",height=2, width=54,command=running)
        button1.grid(row=0,column=0)

        button2=Button(master,text ="COLOR MARK",height=2, width=54,command=openColorMarkWindow)
        button2.grid(row=0,column=1)

        button3=Button(master, text="CONTOURS MARK",height=2, width=54,command=openContoursWindow)
        button3.grid(row=0,column=2)

        button4=Button(master, text="APPROX POLY",height=2, width=54,command=openApproxPolysWindow)
        button4.grid(row=0,column=3)

        button5=Button(master, text="SAVE",height=2, width=54,command=save)
        button5.grid(row=0,column=4)

        # Create a Label to capture the Video frames
        label =Label(master)
        label.grid(row=3,columnspan = 5)

        vid = cv2.VideoCapture(0, cv2.CAP_DSHOW) # this is the magic!
        vid.set(cv2.CAP_PROP_FRAME_WIDTH, 480)
        vid.set(cv2.CAP_PROP_FRAME_HEIGHT, 640)

        show_frames()
        master.mainloop()
    except Exception as e:
        print(f'error:{e}')
    finally:
        vid.release() 
        cv2.destroyAllWindows()
        print('quit the program')
   