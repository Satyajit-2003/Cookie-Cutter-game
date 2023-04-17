"""
So, here is the logic of the game:

I HAVE REPLACED THE GIVEN COOKIE IMAGE WITH A TRANSPARENT PNG TO OVERLAY IT ON THE SCREEN
You have to cut the cookie in half by moving your hand in the cookie.
The cookie will be displayed on the screen and you have to cut it by moving your hand in the cookie.
The tip of your index finger will be used to cut the cookie.
Time limit is 40 seconds. (Assuming 30 FPS)
For every successful cut, the score will increase by 1.
If the score is greater than 500, you win the game.
If the time limit is reached, you lose the game.

ENJOY!
"""
#INITIAL SETUP
#----------------------------------------------------------------
import cv2
from cvzone import HandTrackingModule, overlayPNG
import numpy as np

# Loading the images
intro = cv2.imread(r"CookieCutter\frames\img1.jpeg")
kill = cv2.imread(r"CookieCutter\frames\img2.png")
winner = cv2.imread(r"CookieCutter\frames\img3.png")

# Initializing the camera and the hand detector with confidence level 0.77 and maximum number of hands 1
cam = cv2.VideoCapture(0)
detector = HandTrackingModule.HandDetector(maxHands=1,detectionCon=0.77)

#INITILIZING GAME COMPONENTS
#----------------------------------------------------------------
sqr_img = cv2.imread(r"CookieCutter\img\sqr(2).png", cv2.IMREAD_UNCHANGED)

#INTRO SCREEN WILL STAY UNTIL Q IS PRESSED
while True:
    cv2.imshow('Squid Game', cv2.resize(intro, (0, 0), fx=0.69, fy=0.69))
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

#destroying the intro screen and starting the game
cv2.destroyAllWindows()

# Defining the variables
NotWon = True
score = 0
time_s = 40 #time limit in seconds
timer = 30 * time_s #assumingg 30 FPS
cut_areas = [] #list of points that have been cut

#GAME LOGIC UPTO THE TEAMS
#-----------------------------------------------------------------------------------------
while True:
    # Get the current frame from the camera
    success, img = cam.read()

    # Flip the image horizontally for a more natural feel
    img = cv2.flip(img, 1)    

    # Detect the hand in the current frame
    hands, img = detector.findHands(img)
    if len(hands) > 0:
        hand1 = hands[0] # Get the first hand
        lmList = hand1["lmList"]  # List of 21 Landmark points

        if lmList:
            # Get the tip of the index finger
            x, y = lmList[8][:2] 
            # Check if the hand is in the cookie and increase the score if it is
            if (340 < x < 360 or 150 < x < 190) or (130 < y < 170 or 300 < y < 340):
                #checking if the point has been cut once 
                if (x,y) not in cut_areas:
                    #if not cut it and increse the score
                    cut_areas.append((x, y))
                    score += 1

    # Draw the score and timer on the screen
    cv2.putText(img, f"Score: {score}", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    cv2.putText(img, f"Time left: {int(timer/40)}s", (10, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    # Decrement the timer and end the game if time runs out
    timer -= 1
    if timer == 0:
        break

    # Increment the score and end the game if the score is high enough
    if score > 500:
        NotWon = False
        break
    
    # Draw the cookie on the screen
    img = overlayPNG(img, sqr_img, [10, 10])

    # Display the current frame
    cv2.imshow("Cookie Cutter Game", img)
    cv2.waitKey(1)



#LOSS SCREEN
if NotWon:
    while True:
        cv2.imshow('Squid Game', cv2.resize(kill, (0, 0), fx=0.69, fy=0.69))
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


#WIN SCREEN
else:
    while True:
        cv2.imshow('Squid Game', cv2.resize(winner, (0, 0), fx=0.69, fy=0.69))
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


#destroy all the windows
cv2.destroyAllWindows()
