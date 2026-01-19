import math


def thumbsup(hand): 
    hand4 = hand[4]

    for i in range(21): 
        difference = hand4.y - hand[i].y #finds the difference between the thumb tip y and the rest of the landmark y
        if difference > -0.03 and difference != 0.0: #checks if the thumbtip y is a decent bit bigger then the rest of the rest of the y
            return False
    return True

#function for comparing a list of landmarks to another
#hand is the list of landmarks taken from the live video
#gesture is a list of landmarks that is stored
def compareGesture(hand, gesture):
    #we want to find the difference between hand[0] through hand[0-20]
    # and compare it too the difference between gesture[0] through gesture[0-20]
    # do this for the enitre land marks
    #O(n^2)
    allowedDeviation = .048
    for landmark in range(21):
        handx = hand[landmark][0]
        handy = hand[landmark][1]
        handz = hand[landmark][2]
        gesturex = gesture[landmark][0]
        gesturey = gesture[landmark][1]
        gesturez = gesture[landmark][2]


        landmarkDist = math.sqrt((handx - gesturex)**2 + (handy - gesturey)**2 + (handz - gesturez)**2) #shortest distance from hand[landmark] to gesture[landmark]
        
        for otherlandmark in range(landmark+1, 21):
            
            
            otherLandmarkDist = math.sqrt((hand[otherlandmark][0] - gesture[otherlandmark][0])**2 
                                          + (hand[otherlandmark][1] - gesture[otherlandmark][1])**2 
                                          + (hand[otherlandmark][2] - gesture[otherlandmark][2])**2)
            
            
            if not checkDifference(landmarkDist, otherLandmarkDist, allowedDeviation):
                return False
    
    return True


def checkDifference(number, othernumber, allowed):
    lowerbound = othernumber - allowed
    upperbound = othernumber + allowed
    return (number - lowerbound >= 0) and (upperbound - number >= 0)
