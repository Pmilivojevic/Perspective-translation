import numpy as np
import imutils
import cv2

cap1= cv2.VideoCapture(0)
cap1.set(cv2.CAP_PROP_FRAME_WIDTH, 512)
cap1.set(cv2.CAP_PROP_FRAME_HEIGHT, 512)

cap2= cv2.VideoCapture(1)
cap2.set(cv2.CAP_PROP_FRAME_WIDTH, 512)
cap2.set(cv2.CAP_PROP_FRAME_HEIGHT, 512)

def perspectiveTrans(cap1, cap2):
    _, frameL= cap1.read()
    frameL = imutils.rotate(frameL, 270)
#    frameL= cv2.imread('dest.png')
    _, frameR= cap2.read()
    frameR = imutils.rotate(frameR, 270)
 #   frameR= cv2.imread('persp.png')
    #print(frameL)
    ret1, cornersDist = cv2.findChessboardCorners(frameL, (3, 3), None)
    #print(cornersDist)
    ret2, cornersPersp = cv2.findChessboardCorners(frameR, (3, 3), None)

    if ret1:
        cv2.drawChessboardCorners(frameL, (3, 3), cornersDist, ret1)
    if ret2:
        cv2.drawChessboardCorners(frameR, (3, 3), cornersPersp, ret2)

    cv2.imshow('win3', frameL)
    cv2.imshow('win4', frameR)

    ptsPersp = np.array([[cornersPersp[6][0][0], cornersPersp[6][0][1]], [cornersPersp[0][0][0], cornersPersp[0][0][1]],
                         [cornersPersp[8][0][0], cornersPersp[8][0][1]], [cornersPersp[2][0][0], cornersPersp[2][0][1]]])

    ptsDest = np.array([[cornersDist[0][0][0], cornersDist[0][0][1]], [cornersDist[2][0][0], cornersDist[2][0][1]],
                        [cornersDist[6][0][0], cornersDist[6][0][1]], [cornersDist[8][0][0], cornersDist[8][0][1]]])

    '''ptsPersp = np.array([[cornersPersp[6][0][0], cornersPersp[6][0][1]], [cornersPersp[3][0][0], cornersPersp[3][0][1]], [cornersPersp[0][0][0], cornersPersp[0][0][1]],
                         [cornersPersp[7][0][0], cornersPersp[7][0][1]], [cornersPersp[4][0][0], cornersPersp[4][0][1]], [cornersPersp[1][0][0], cornersPersp[1][0][1]],
                         [cornersPersp[8][0][0], cornersPersp[8][0][1]], [cornersPersp[5][0][0], cornersPersp[5][0][1]], [cornersPersp[2][0][0], cornersPersp[2][0][1]]])

    ptsDest = np.array([[cornersDist[0][0][0], cornersDist[0][0][1]], [cornersDist[1][0][0], cornersDist[1][0][1]], [cornersDist[2][0][0], cornersDist[2][0][1]],
                        [cornersDist[3][0][0], cornersDist[3][0][1]], [cornersDist[4][0][0], cornersDist[4][0][1]], [cornersDist[5][0][0], cornersDist[5][0][1]],
                        [cornersDist[6][0][0], cornersDist[6][0][1]], [cornersDist[7][0][0], cornersDist[7][0][1]], [cornersDist[8][0][0], cornersDist[8][0][1]]])'''
    print(ptsPersp)
    print(ptsDest)

    h, status = cv2.findHomography(ptsPersp, ptsDest)
    print(h)
    return h
h= perspectiveTrans(cap1, cap2)
while True:
    _, frame1= cap1.read()
    frame1= imutils.rotate(frame1, 270)
    _, frame2= cap2.read()
    frame2= imutils.rotate(frame2, 270)
    frame = cv2.warpPerspective(frame2, h, (frame1.shape[1], frame1.shape[0]))

    cv2.imshow('win1', frame1)
    cv2.imshow('win2', frame)
    #cv2.imshow('win3', frameL)
    #cv2.imshow('win4', frameR)

    if cv2.waitKey(1) == 27:
        break

cv2.destroyAllWindows()

cap1.release()
cap2.release()