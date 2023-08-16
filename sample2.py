import cv2
import numpy as np


# define a video capture object
vid = cv2.VideoCapture(1)
  
while(True):
      
    ret, img = vid.read()
    
    img_resize = cv2.resize(img,None,fx=1,fy=1,interpolation=cv2.INTER_LINEAR) #resize
    img_output = img_resize.copy()

    img_hsv = cv2.cvtColor(img_resize, cv2.COLOR_BGR2HSV) #hsv

    lb = np.array([0, 0, 0])
    ub = np.array([255, 80, 255])
    mask = cv2.inRange(img_hsv, lb, ub)
    img_mask = cv2.bitwise_and(img_resize, img_resize, mask=mask) #mask 
    img_gry = cv2.cvtColor(img_mask,cv2.COLOR_BGR2GRAY) #gray
    img_blr = cv2.blur(img_gry,(5,5)) #blur
    img_th = cv2.adaptiveThreshold(img_blr, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV,5,6) #theshold
   
    kernel = np.ones((7,7),np.uint8)
    dilation = cv2.dilate(img_th,kernel,iterations = 3)
  
    contours, hierarchy = cv2.findContours(dilation, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
 
    out = np.zeros_like(dilation)

    for contour in contours:
        area = cv2.contourArea(contour)
        #print(area)
        if area >40000 : 
       
            # cv2.approxPloyDP() function to approximate the shape
            approx = cv2.approxPolyDP(
                contour, 0.05 * cv2.arcLength(contour, True), True)
            
            # using drawContours() function
            cv2.drawContours(out, contour, -1, 255, 3)
            cv2.drawContours(img_output, [approx], -1, (255, 0, 0), 3)

            # finding center point of shape
            M = cv2.moments(contour)
      
            if M['m00'] != 0.0:
                x = int(M['m10']/M['m00'])
                y = int(M['m01']/M['m00'])

            if len(approx) == 5:
                cv2.putText(img_output, 'Pentagon (OK)', (x, y),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
            elif len(approx) == 6:
                cv2.putText(img_output, 'Hexagon (NG)', (x, y),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
            else:
                cv2.putText(img_output, 'cannot detect,please move the object a little bit', (x, y),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

    cv2.imshow('Output Contour', out)
    cv2.imshow('img_th', dilation)
    cv2.imshow('img_output', img_output) 

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

vid.release()
# Destroy all the windows
cv2.destroyAllWindows()