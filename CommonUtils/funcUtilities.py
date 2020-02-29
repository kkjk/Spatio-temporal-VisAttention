import os
import scipy.io
from scipy.io import loadmat, savemat
import pandas as pd
import numpy as np
import json
import matplotlib.pyplot as plt
from PIL import Image
import time
import random
from scipy.interpolate import interp1d
import pandas as pd
from numpy import savetxt
import sys
from CommonUtils.classUtilities import *

FILTER_SIZE = 500


def readDataSet(userFile, taskName, datasetDir):
    """
    This function reads the mat files for the mentioned user and collects
    all the positions for mouse, cursor and fixations irrespective of timestamps,
    uniform samples, read data from random data points and save all the data
    into csv files - Input as well as Output csv files

    Parameters:
        userFile (string): name of the user whose data will be processed
        taskName (string): The name of the selected interface
        datasetDir (string): Dataset directory

    Returns:
        list: list of mouse data 
        list: list of cursor data 
        list: list of fixation data
    """

    mat = scipy.io.loadmat(datasetDir+userFile)
    totalInterfaces = len(mat['guidata'][0])

    intfList = []
    for i in range(totalInterfaces):
        intfList.append(mat['guidata'][0][i][0][0][0][0])
    
    try:
        intfListIndex = intfList.index(taskName)
    except ValueError:
        print("No interface %s for user %s" % (taskName, userFile))
        return [],[],[]

    #: Read: Mat file of the user to collect mouse, cursor and fixation positions
    ts_input_mouse = mat['guidata'][0][intfListIndex][0][0][2][0][0][0][0]
    ts_input_cursor = mat['guidata'][0][intfListIndex][0][0][2][0][0][3][0]
    ts_output_fixation = mat['guidata'][0][intfListIndex][0][0][3][0]


    mouse_list = []

    for i in ts_input_mouse: 
        if i['event'][0][0][0] == "move":  
                mouse_list.append((int(i['x'][0][0][0][0]),int(i['y'][0][0][0][0])))

    cursor_list = []

    for i in ts_input_cursor: 
        if i['type'][0][0][0] == "caret":
            cursor_list.append((int(i['x'][0][0][0][0]),int(i['y'][0][0][0][0])))

    fixation_list = []

    for i in ts_output_fixation: 
        fixation_list.append((int(np.uint16(i['x'][0][0][0])), int(np.uint16(i['y'][0][0][0]))))

    return mouse_list, cursor_list, fixation_list

def getValueAfterBlur(X, Y,posX,posY,filSize):
    """
    This function returns the value of the pixel corresponding to a blurred image
    The blur has been done in runtime from this function

    Parameters:
        X (int): location on x axis
        Y (int): location on y axis
        posX (int): location on x axis which indicates actual mouse/cursor/fixation position
        posY (int): location on y axis which indicates actual mouse/cursor/fixation position
        filSize (int): filter size for blurring

    Returns:
        int: pixel value corresponding to the blur
    """
    value = 0
    for i in range(0,filSize):
        if X-i <= posX and X+i >= posX and Y-i <= posY and Y+i >= posY:
            value = int(255.0*(filSize - i)/filSize)
            break
    return value

def normalize(dataList):
    """
    This function normalizes a data list to the range [0-1]

    Parameters:
        dataList (list): list of time points needing normalization

    Returns:
        List: normalized time list

    """
    min_time = dataList[0]
    max_time = dataList[-1]
    diff_time = max_time - min_time
    normTimeDict = {}
    for timeIter in range(len(dataList)-1):
        norm_time = (dataList[timeIter] - min_time)/ diff_time
        normTimeDict[norm_time] =  dataList[timeIter]
    return normTimeDict

def culminateDataPoints(sampledNormList, normDictionary, pMouse, pCursor, pFixation, dMouse, dCursor, dFixation, interfaceObj):
    """
    This function processed the data list and creates a normalized datalist

    Parameters:
        sampledNormList (list): Normalized time list which has been sampled and hence reduced entries
        normDictionary (Dictionary): Dictionary containing normalized and actual timestamps
        pMouse (func): interpolated mouse function
        pCursor (func): interpolated cursor function
        pFixation (func): interpolated fixation function
        dMouse (Dictionary): Dictionary of mouse points
        dCursor (Dictionary): Dictionary of cursor points
        dFixation (Dictionary): Dictionary of fixation points
        interfaceObj (InterfaceBbox) : Bounding box data

    Returns:
        normDataList: normalized data list
        actualTimeList: list containing the corresponding timestamps

    """
    normDataList = []
    actualTimeList = []
    for samTimeInst in sampledNormList:
        actualTime = normDictionary[samTimeInst]
        mouseIndex = int(pMouse(actualTime))
        cursorIndex =  int(pCursor(actualTime))
        fixationIndex = int(pFixation(actualTime))
        if mouseIndex != -1 and fixationIndex != -1:
            mousePred = dMouse[ list(dMouse.keys())[ mouseIndex ]]
            if(cursorIndex == -1):
                cursorPred = [(2000,2000)]
            else:
                cursorPred = dCursor[list(dCursor.keys())[ cursorIndex ]]
            fixationPred = dFixation[ list(dFixation.keys())[ fixationIndex ]]
            posDataInstance = PosData(samTimeInst, actualTime, mousePred, cursorPred, fixationPred, interfaceObj )
            normDataList.append(posDataInstance)
            actualTimeList.append(samTimeInst)
    return normDataList,actualTimeList


def getFeatureList(IntfDataList, time, posX, posY, dim, interfaceObj):
    """
    This function computes the input feature : [ Mouse , Cursor , Bounding box ] each of dimension 2*d+1

    Parameters:
        IntfDataList (list): Data list
        time (int): time index
        posX (int): location on x axis
        posY (int): location on y axis
        dim (int): dimension over time - 2*dim+1
        interfaceObj (InterfaceBbox) : Bounding box data

    Returns:
        list : containing the list of pixel values over time for mouse, cursor and bounding box

    """
    feature_list = getMouseFeatureList(IntfDataList, time, posX, posY, dim)
    feature_list = feature_list + getCursorFeatureList(IntfDataList, time, posX, posY, dim)
    feature_list = feature_list + getBboxFeatureList(IntfDataList, time, posX, posY, dim, interfaceObj)
    return feature_list


def getMouseFeatureList(IntfDataList, time, posX, posY, dim):
    """
    This function computes the input feature : [ Mouse ] of dimension 2*d+1

    Parameters:
        IntfDataList (list): Data list
        time (int): time index
        posX (int): location on x axis
        posY (int): location on y axis
        dim (int): dimension over time - 2*dim+1

    Returns:
        list : contains pixel values over time for mouse

    """
    feature_list = []
    for i in range(dim, len(IntfDataList) - dim):
        value = 0
        if IntfDataList[i].timestamp ==  time:
            for k in range(2*dim):
                actualX = IntfDataList[i - dim + k].mouse_data[0][0]
                actualY = IntfDataList[i - dim + k].mouse_data[0][1]
                value = getValueAfterBlur(actualX,actualY,posX,posY,FILTER_SIZE)
                feature_list.append(value)
            return feature_list
    return feature_list

def getCursorFeatureList(IntfDataList, time, posX, posY, dim):
    """
    This function computes the input feature : [ Cursor ] of dimension 2*d+1

    Parameters:
        IntfDataList (list): Data list
        time (int): time index
        posX (int): location on x axis
        posY (int): location on y axis
        dim (int): dimension over time - 2*dim+1

    Returns:
        list : contains pixel values over time for cursor

    """
    feature_list = []
    for i in range(dim, len(IntfDataList) - dim):
        value = 0
        if IntfDataList[i].timestamp ==  time:
            for k in range(2*dim):
                actualX = IntfDataList[i - dim + k].cursor_data[0][0]
                actualY = IntfDataList[i - dim + k].cursor_data[0][1]
                if actualX == 2000 or actualY == 2000:
                    value = 0
                else:
                    value = getValueAfterBlur(actualX,actualY,posX,posY,FILTER_SIZE)
                feature_list.append(value)
            return feature_list
    return feature_list

def getBboxFeatureList(IntfDataList, time, posX, posY, dim, interfaceObj):
    """
    This function computes the input feature : [ Bounding box ] of dimension 2*d+1

    Parameters:
        IntfDataList (list): Data list
        time (int): time index
        posX (int): location on x axis
        posY (int): location on y axis
        dim (int): dimension over time - 2*dim+1
        interfaceObj (InterfaceBbox) : Bounding box data

    Returns:
        list : contains pixel values over time for bounding box

    """
    feature_list = []
    for i in range(dim, len(IntfDataList) - dim):
        value = 0
        if IntfDataList[i].timestamp ==  time:
            for k in range(2*dim):
                if IntfDataList[i - dim + k].valBbox != "None" and IntfDataList[i - dim + k].valBbox == interfaceObj.whichBbox(posX, posY):
                    value = 255
                feature_list.append(value)
            return feature_list
    return feature_list

def getFixationFeatureList(IntfDataList, time, posX, posY):

    """
    This function computes the output feature : [ Fixation ]

    Parameters:
        IntfDataList (list): Data list
        time (int): time index
        posX (int): location on x axis
        posY (int): location on y axis

    Returns:
        list : contains pixel values each for time t of fixation

    """

    for i in range(len(IntfDataList) - 1):
        value = 0
        if IntfDataList[i].timestamp ==  time:
            actualX = IntfDataList[i].fixation_data[0][0]
            actualY = IntfDataList[i].fixation_data[0][1]
            value = getValueAfterBlur(actualX,actualY,posX,posY,FILTER_SIZE)
            return value
    return value

def getInterpolation(mouse, cursor, fixation):
    """
    This function interpolates the mouse, cursor, fixation with respect to time

    Parameters:
        mouse (list): mouse data list
        cursor (list): cursor data list
        fixation (list): fixation data list

    Returns:
        mousePlot: function for mouse interpolation
        cursorPlot: function for cursor interpolation
        fixationPlot: function for fixation interpolation

    """

    mouse_timestamp = np.asarray(list(mouse.keys()))
    mouse_index = np.linspace(0, len(mouse)-1, num=len(mouse), endpoint=True, dtype=np.int16)
    #mousePlot = interp1d(mouse_timestamp, mouse_index, kind='previous', fill_value="extrapolate")
    mousePlot = interp1d(mouse_timestamp, mouse_index, kind='previous', fill_value = -1, bounds_error=False)

    cursor_timestamp = np.asarray(list(cursor.keys()))
    cursor_index = np.linspace(0, len(cursor)-1, num=len(cursor), endpoint=True, dtype=np.int16)
    #cursorPlot = interp1d(cursor_timestamp, cursor_index, kind='previous', fill_value="extrapolate")
    cursorPlot = interp1d(cursor_timestamp, cursor_index, kind='previous', fill_value = -1, bounds_error=False)

    fixation_timestamp = np.asarray(list(fixation.keys()))
    fixation_index = np.linspace(0, len(fixation)-1, num=len(fixation), endpoint=True, dtype=np.int16)
    #fixationPlot = interp1d(fixation_timestamp, fixation_index, kind='previous', fill_value="extrapolate")
    fixationPlot = interp1d(fixation_timestamp, fixation_index, kind='previous', fill_value = -1, bounds_error=False)

    return mousePlot, cursorPlot, fixationPlot

def sampleTime(dictToSample):
    """
    This function samples the time list

    Parameters:
        dictToSample (dictionary): contains time points to be sampled

    Returns:
        Timestamp (list): list of sampled time stamps

    """
    Timestamp = []
    dictTimestamp = list(dictToSample.keys())

    tempTimestamp = dictTimestamp[0]
    while tempTimestamp < dictTimestamp[-1]:
        Timestamp.append(tempTimestamp)
        tempTimestamp = tempTimestamp + 20
    return Timestamp

def readPositiveData(dim, IntfDataList, actTime, intfObj):
    """
    This function creates the feature list for all the data points provided in the normalized data list

    Parameters:
        dim (int): dimension over time can be found by 2*dim+1
        IntfDataList (list): data list
        actTime (list): actual timestamp list
        intfObj (InterfaceBbox): Bounding box data

    Returns:
        InftFeatureList (list): Input feature list
        InftFixationFeatureList (list): Output feature list

    """
    InftFeatureList = []
    InftFixationFeatureList = []

    for i in range(dim, len(IntfDataList)-dim):

        InftFeatureList.append(getFeatureList(IntfDataList, actTime[i], IntfDataList[i].mouse_data[0][0], IntfDataList[i].mouse_data[0][1], dim, intfObj))
        InftFixationFeatureList.append(getFixationFeatureList(IntfDataList, actTime[i], IntfDataList[i].mouse_data[0][0], IntfDataList[i].mouse_data[0][1]))

        InftFeatureList.append(getFeatureList(IntfDataList, actTime[i], IntfDataList[i].cursor_data[0][0], IntfDataList[i].cursor_data[0][1], dim, intfObj))
        InftFixationFeatureList.append(getFixationFeatureList(IntfDataList, actTime[i], IntfDataList[i].cursor_data[0][0], IntfDataList[i].cursor_data[0][1]))

        InftFeatureList.append(getFeatureList(IntfDataList, actTime[i], int(IntfDataList[i].fixation_data[0][0]), int(IntfDataList[i].fixation_data[0][1]), dim, intfObj))
        InftFixationFeatureList.append(getFixationFeatureList(IntfDataList, actTime[i], int(IntfDataList[i].fixation_data[0][0]), int(IntfDataList[i].fixation_data[0][1])))

    return InftFeatureList, InftFixationFeatureList

############# Read Negative data #################

def readNegativeData(dim, intfDataList, timeList, intfObj):
    
    """
    This function creates the feature list for random data points in the interface of size 1920x1200

    Parameters:
        dim (int): dimension over time can be found by 2*dim+1
        IntfDataList (list): data list
        actTime (list): actual timestamp list
        intfObj (InterfaceBbox): Bounding box data

    Returns:
        InftFeatureList (list): Input feature list
        InftFixationFeatureList (list): Output feature list

    """

    InftFeatureList = []
    InftFixationFeatureList = []
    boundedTimeList = timeList[dim: len(timeList)-dim]
    customTimeList = random.sample(boundedTimeList,k= len(timeList) - 2*dim) + random.sample(boundedTimeList,k= len(timeList) - 2*dim) + random.sample(boundedTimeList,k= len(timeList) - 2*dim)
    #customTimeList = random.sample(boundedTimeList,k= len(timeList) - 2*dim)
    #customTimeList = random.sample(boundedTimeList,k= 3) + random.sample(boundedTimeList,k= 3) + random.sample(boundedTimeList,k= 3)
    xAxis = list(range(1920))
    yAxis = list(range(1200))
    xAxisRand = random.sample(xAxis,k=len(customTimeList))
    yAxisRand = random.sample(yAxis,k=len(customTimeList))
    for i in range(len(customTimeList)):
        InftFeatureList.append(getFeatureList(intfDataList, customTimeList[i], int(xAxisRand[i]), int(yAxisRand[i]), dim, intfObj))
        InftFixationFeatureList.append(getFixationFeatureList(intfDataList, customTimeList[i], xAxisRand[i], yAxisRand[i]))
    return InftFeatureList, InftFixationFeatureList

######################################################################################################

def getInterfacesList():
    
    """
    This function manages/returns the list of interfaces
    
    Returns:
        list : list of interfaces

    """
    listOfInterfaces = \
    [
        "Blogger_5","gmail","Blogger_2","FB_photo","gmail_4","Blogger_7","Blogger","FB_post",
        "Blogger_6","gmail_1","Blogger_9","gmail_8","DB_diary_8","Blogger_8","gmail_4","Blogger_10",
        "GitHub_8","Blogger_1","Amazon_review","Blogger_11","gmail_8","Blogger_3","GitHub",
        "gmail_1","Blogger_4","Tumblr_link"
    ]
    return listOfInterfaces

def getTrainingUserList():
    """
    This function manages/returns the list of users for training

    Returns:
        list : list of users

    """
    listOfUsersMatFiles = ["Alice.mat", "Charlotte.mat", "Irina.mat", "Konstantin.mat", "Lokesh.mat", "Mike.mat", "Russa.mat"]
    return listOfUsersMatFiles

def getValidationUserList():
    """
    This function manages/returns the list of users for validation

    Returns:
        list : list of users

    """
    listOfUsersMatFiles = ["Sampath.mat","Somendra.mat"]
    return listOfUsersMatFiles

def getTestingUserList():
    """
    This function manages/returns the list of users for testing

    Returns:
        list : list of users

    """
    listOfUsersMatFiles = []
    return listOfUsersMatFiles

