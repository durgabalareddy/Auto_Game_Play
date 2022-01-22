import pickle
import os
import pyautogui as pag
import cv2
import pytesseract
import mss
import numpy as np
import time

pytesseract.pytesseract.tesseract_cmd = 'Tesseract-OCR/tesseract.exe'   # Set Pytesseract home

with open('questionBank','rb') as f:                                    # Read the questionBank as a dictionary
    questionBank = pickle.load(f) if os.path.getsize('questionBank') > 0 else {}   # if the file is empty, we will create a empty dictionary else dictionary contains the file contents

options = [0,(485,624),(484,700),(484,775),(484,853)]         # Coordinates of question options. These coordinates will change based on the screen size.

# Read the Computer Help Options Images

Computer_Help_Option_A = cv2.imread("Images/Computer_Help_Option_A.png")
Computer_Help_Option_B = cv2.imread("Images/Computer_Help_Option_B.png")
Computer_Help_Option_D = cv2.imread("Images/Computer_Help_Option_D.png")

Expert_option = 0

def captureQuestion():
    questionCoordinates = {"top": 494, "left": 266, "width": 430, "height": 60}
    with mss.mss() as sct:
        questionImage = np.array(sct.grab(questionCoordinates))
    question = pytesseract.image_to_string(questionImage)
    return question

def GetComputerHelp():
    answerCoordinates = {"top": 277, "left": 575, "width": 45, "height": 51}
    pag.click(428,931)
    time.sleep(1)
    pag.click(501,341)
    time.sleep(1)
    with mss.mss() as sct:
        answerImage = np.array(sct.grab(answerCoordinates))
    cv2.imwrite('answerImage.png',answerImage)
    answerImage = cv2.imread("answerImage.png")
    if not np.any(cv2.subtract(Computer_Help_Option_A, answerImage)):
        Answer = 1
    elif not np.any(cv2.subtract(Computer_Help_Option_B, answerImage)):
        Answer = 2
    elif not np.any(cv2.subtract(Computer_Help_Option_D, answerImage)):
        Answer = 4
    else:
        Answer = 3
    return Answer

def GetAudiencePollHelp():
    answerCoordinates = {"top": 231, "left": 435, "width": 261, "height":88 }
    pag.click(660,931)
    time.sleep(1)
    pag.click(501,341)
    time.sleep(3)
    with mss.mss() as sct:
        answerImage = np.array(sct.grab(answerCoordinates))
    cv2.imwrite('answerImage.png',answerImage)
    answerImage = cv2.imread("answerImage.png")
    answerImageWithEdges = cv2.Canny(answerImage,90,90)
    for i in range(0,696):
        if answerImageWithEdges[i,27] == 255:
            dist_A = i
            break
    for i in range(0,696):
        if answerImageWithEdges[i,91] == 255:
            dist_B = i
            break
    for i in range(0,696):
        if answerImageWithEdges[i,157] == 255:
            dist_C = i
            break
    for i in range(0,696):
        if answerImageWithEdges[i,222] == 255:
            dist_D = i
            break
    if dist_A < dist_B and dist_A < dist_C and dist_A < dist_D:
        Answer = 1
    elif dist_B < dist_C and dist_B < dist_D:
        Answer = 2
    elif dist_C < dist_D:
        Answer = 3
    else:
        Answer = 4
    return Answer

def saveAnswer(question,answer):
    questionBank[question] = answer
    with open('questionBank','wb') as f:
        pickle.dump(questionBank,f)

def GetAnswer(question):
    return questionBank[question]

def clickAnswer(answer,questionNumber):
    pag.click(options[answer][0],options[answer][1])
    pag.click(1444,920)
    time.sleep(3)
    if questionNumber < 13:
        pag.click(478,619)
        pag.click(1444,920)
    time.sleep(5)

def restartGame():
    pag.click(477,602)
    pag.click(1444,920)
    time.sleep(40)
    pag.click(482,914)
    pag.click(1444,920)
    time.sleep(40)
    pag.click(475,923)
    pag.click(1444,920)
    time.sleep(4)
    pag.click(477,602)
    pag.click(1444,920)
    time.sleep(40)
    time.sleep(5)
    pag.click(478,619)
    time.sleep(6)


while True:
    questionNumber = 1
    print("\n Question Number --- " + str(questionNumber))
    while questionNumber <= 13:
        question = captureQuestion()
        print("\n Question Number --- " + str(questionNumber))
        questionNumber = questionNumber + 1
        print("\n Question --- " + question)
        if question not in questionBank:
            if Expert_option == 0:
                Expert_option = 1
                Answer = GetComputerHelp()
                print("\n Answer --- " + str(Answer))
                saveAnswer(question,Answer)
                print("\n Added Question --- " + str(len(questionBank)))
                clickAnswer(Answer,questionNumber - 1)
            else:
                questionNumber = 1
                Expert_option = 0
                Answer = GetAudiencePollHelp()
                print("\n Answer --- " + str(Answer))
                saveAnswer(question,Answer)
                print("\n Added Question --- " + str(len(questionBank)))
                if Answer == 1:
                    pag.click(484,700)
                    pag.click(1444,920)
                else:
                    pag.click(485,624)
                    pag.click(1444,920)

                time.sleep(3)
                restartGame()
        else:
            Answer = GetAnswer(question)
            print("\n Answer --- " + str(Answer))
            clickAnswer(Answer,questionNumber - 1)
    
    restartGame()
