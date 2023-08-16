import cv2
import numpy as np


# define a video capture object
vid = cv2.VideoCapture(1)
  
while(True):
      
    # Capture the video frame
    # by frame
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

        # Setting parameter values
    # t_lower = 50  # Lower Threshold
    # t_upper = 500  # Upper threshold
    
    # Applying the Canny Edge filter
    #edge = cv2.Canny(dilation, t_lower, t_upper)


    #contours, hierarchy = cv2.findContours(edge, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
  
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
            #cv2.drawContours(out, [contour], 0, (0, 0, 255), 5)
            cv2.drawContours(out, contour, -1, 255, 3)
            cv2.drawContours(img_output, [approx], -1, (255, 0, 0), 3)


            # finding center point of shape
            M = cv2.moments(contour)
      
            if M['m00'] != 0.0:
                x = int(M['m10']/M['m00'])
                y = int(M['m01']/M['m00'])

            print(len(approx))
                    # putting shape name at center of each shape
            if len(approx) == 3:
                cv2.putText(img_output, 'Triangle', (x, y),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        
            elif len(approx) == 4:
                cv2.putText(img_output, 'Quadrilateral', (x, y),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        
            elif len(approx) == 5:
                cv2.putText(img_output, 'Pentagon (OK)', (x, y),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
        
            elif len(approx) == 6:
                cv2.putText(img_output, 'Hexagon (NG)', (x, y),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
            
            elif len(approx) == 7:
                cv2.putText(img_output, '7', (x, y),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
            
            elif len(approx) == 8:
                cv2.putText(img_output, '8', (x, y),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
            
            elif len(approx) == 9:
                cv2.putText(img_output, '9', (x, y),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        
            else:
                cv2.putText(img_output, 'circle', (x, y),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
  


            #cv2.drawContours(out, contour, -1, 255, 3)

    
    
    
    # Create an output of all zeroes that has the same shape as the input
    # image
    

    # On this output, draw all of the contours that we have detected
    # in white, and set the thickness to be 3 pixels
    

    # Spawn new windows that shows us the donut
    # (in grayscale) and the detected contour

    cv2.imshow('Output Contour', out)



   
        
    #     if cv2.contourArea(contour) >1500 : # filter small contours
    #         print(cv2.contourArea(contour))
    #         cv2.drawContours(img_output, contours, -1, (0, 255, 0), -1)
           
#             cv2.drawContours(img_output, contour, -1, (0, 255, 0), 5)

    # circles  = cv2.HoughCircles(img_th,cv2.HOUGH_GRADIENT, 1, 15, param1 = 15,param2 = 16, minRadius = 5, maxRadius = 300)
    # if circles is not None:
    #     circles = np.round(circles[0, :]).astype("int")
    #     for (x, y, r) in circles:
        
    #         cv2.circle(img_output, (x, y), r, (0, 255, 0), 2)

    cv2.imshow('img_th', dilation)
 #   cv2.imshow('edge', edge)
    cv2.imshow('img_output', img_output)
 
 
    
   # cv2.imshow('img_output', img_output)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
  
# After the loop release the cap object
vid.release()
# Destroy all the windows
cv2.destroyAllWindows()
