from math import dist
import MongoModule as MM
import cv2
import time
import HandTrackingModule as htm


def GetXPoints(hand):
    finger = []
    for point in hand:
        finger.append(point[1])
    return finger


def GetYPoints(hand):
    finger = []
    for point in hand:
        finger.append(point[2])
    return finger


def GetPoints(hand):
    fingerX = []
    fingerY = []
    for point in hand:
        fingerX.append(point[1])
        fingerY.append(point[2])
    return fingerX, fingerY


def DetermineMotor(p0, p1, p2):
    determine = abs(p0-p1)
    distance = p1 - p2
    motor = 180-(distance * (determine/180))
    if (motor > 180.0):
        motor = 180.0
    elif (motor < 0.0):
        motor = 0.0
    return motor


def DetermineXMotor(p0, p1, p2):
    determine = abs(p0 - p1)
    distance = p1 - p2
    motor = 20+(distance * (determine/180))
    if (motor > 180.0):
        motor = 180.0
    elif (motor < 0.0):
        motor = 0.0
    return motor


def MongoPost(fingerValue, collection):
    collection.update_one({"_id": "right"},
                          {"$set": {"thumb": fingerValue[0],
                                    "index": fingerValue[1],
                                    "middle": fingerValue[2],
                                    "ring": fingerValue[3],
                                    "pinky": fingerValue[4]}})
    return


client = MM.get_database()
database = client['RaspPiMotor']
collection = database['Motor']

width, height = 1280, 720

cap = cv2.VideoCapture(1)
cap.set(3, width)
cap.set(4, height)

pTime = 0
detector = htm.handDetector(detectionCon=0.85)
fingerValue = [0, 0, 0, 0, 0]
MongoPost(fingerValue, collection)

while True:
    ret, img = cap.read()
    img = detector.findHands(img)
    handList = detector.findPosition(img, draw=False)

    # https://google.github.io/mediapipe/solutions/hands.html
    if len(handList) != 0:
        fingerX, fingerY = GetPoints(handList)
        fingerValue[0] = DetermineXMotor(fingerX[0], fingerX[2], fingerX[4])
        fingerValue[1] = DetermineMotor(fingerY[0], fingerY[5], fingerY[8])
        fingerValue[2] = DetermineMotor(fingerY[0], fingerY[9], fingerY[12])
        fingerValue[3] = DetermineMotor(fingerY[0], fingerY[13], fingerY[16])
        fingerValue[4] = DetermineMotor(fingerY[0], fingerY[17], fingerY[20])

    MongoPost(fingerValue, collection)
    print(fingerValue)

    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime
    cv2.putText(img, f'FPS: {int(fps)}', (0, 40),
                cv2.FONT_HERSHEY_PLAIN, 3, (0, 0, 255), 3)

    cv2.imshow("Camera", img)

    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break

cap.release()
cv2.destroyAllWindows()
