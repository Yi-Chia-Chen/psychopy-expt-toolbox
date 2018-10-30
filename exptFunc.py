# -*- coding: utf-8 -*-
import math, string
from datetime import datetime
from psychopy import core, visual, info, event


#  ██████  ███████ ███    ██ ███████ ██████   █████  ██          ███████ ██    ██ ███    ██  ██████ ████████ ██  ██████  ███    ██ ███████
# ██       ██      ████   ██ ██      ██   ██ ██   ██ ██          ██      ██    ██ ████   ██ ██         ██    ██ ██    ██ ████   ██ ██
# ██   ███ █████   ██ ██  ██ █████   ██████  ███████ ██          █████   ██    ██ ██ ██  ██ ██         ██    ██ ██    ██ ██ ██  ██ ███████
# ██    ██ ██      ██  ██ ██ ██      ██   ██ ██   ██ ██          ██      ██    ██ ██  ██ ██ ██         ██    ██ ██    ██ ██  ██ ██      ██
#  ██████  ███████ ██   ████ ███████ ██   ██ ██   ██ ███████     ██       ██████  ██   ████  ██████    ██    ██  ██████  ██   ████ ███████

# polar coordinate to Cartesian coordinate
def polarToCart(r, theta):
    x = r*math.cos(math.radians(theta))
    y = r*math.sin(math.radians(theta))
    return [x,y]

# turn a list of variables to strings with tabs in between each item
def tabString(dataList):
    dataList = [str(x) for x in dataList]
    return '\t'.join(dataList)

# produce formatted current date and time
def formattedTime():
    nowDate = str(datetime.now()).split('.')[0].split(' ')[0]
    nowTime = str(datetime.now()).split('.')[0].split(' ')[1]
    return nowDate, nowTime

# get system, display, and psychopy information
def getSystemInfo(w):
    sysDic = info.RunTimeInfo(win=w, refreshTest=True)
    # sysDic['pythonVersion'] # version of python used
    # sysDic['psychopyVersion'] # version of psychopy used
    # sysDic['systemHostName'] # name of the computer
    # sysDic['windowRefreshTimeAvg_ms'] # mean of monitor refresh intervals
    # sysDic['windowRefreshTimeSD_ms'] # SD of monitor refresh intervals
    # sysDic['windowSize_pix'] # window size
    # sysDic['windowIsFullScr'] # whether window is fullscreen
    # full list of keys: ['psychopyVersion', 'systemRebooted', 'windowWinType', 'windowRgb', 'systemUserID', 'windowRefreshTimeMedian_ms', 'windowScreen', 'systemTimeNumpySD1000000_sec', 'windowSize_pix', 'systemUser', 'systemHaveInternetAccess', 'windowMonitor.name', 'systemMemFreeRAM', 'windowMonitor.getDistance_cm', 'psychopyHaveExtRush', 'windowRefreshTimeAvg_ms', 'windowUnits', 'systemLocale', 'systemPlatform', 'experimentRunTime', 'windowRefreshTimeSD_ms', 'experimentScript.directory', 'systemSec.pythonSSL', 'windowMonitor.getWidth_cm', 'experimentRunTime.epoch', 'experimentScript', 'experimentScript.digestSHA1', 'systemUsersCount', 'windowPos_pix', 'pythonVersion', 'windowMonitor.currentCalibName', 'systemMemTotalRAM', 'windowIsFullScr', 'systemHostName']
    return sysDic['pythonVersion'], sysDic['psychopyVersion'], sysDic['systemHostName'], sysDic['windowRefreshTimeAvg_ms'], sysDic['windowRefreshTimeSD_ms'], sysDic['windowSize_pix'], sysDic['windowIsFullScr']

# capitalize the first letter ONLY, instead of using string.capitalize() or string.capwords() where the rest of the letter will be .lower()
def capFirstLetter(stringText):
    return stringText[0].upper() + stringText[1:]


# ██ ███    ██ ███████ ████████ ██████  ██    ██  ██████ ████████ ██  ██████  ███    ██ ███████
# ██ ████   ██ ██         ██    ██   ██ ██    ██ ██         ██    ██ ██    ██ ████   ██ ██
# ██ ██ ██  ██ ███████    ██    ██████  ██    ██ ██         ██    ██ ██    ██ ██ ██  ██ ███████
# ██ ██  ██ ██      ██    ██    ██   ██ ██    ██ ██         ██    ██ ██    ██ ██  ██ ██      ██
# ██ ██   ████ ███████    ██    ██   ██  ██████   ██████    ██    ██  ██████  ██   ████ ███████

class instrObject:
    def __init__(self, w, fileName, color, beforeFormalText, restText, exptEndText, advancedKeyList=['backslash']):
        self.w = w
        self.list, self.length = self.readInstr(fileName)
        self.stim = visual.TextStim(self.w, text='', color=color, height=30, wrapWidth=900)
        self.restText = restText
        self.advancedKeyList = advancedKeyList
        self.exptEndText = exptEndText
        self.index = 0
        self.beforeFormalText = beforeFormalText

    def readInstr(self,fileName):
        tempFile = open(fileName, 'r')
        tempText = tempFile.readlines()
        tempFile.close()
        instrList = [] # even indexes store instructions, odd indexes store name of function to run before or during the instructions are shown
        thisPage = ''
        for line in tempText:
            if line[:3] == 'XXX':
                thisPage = thisPage[:-1] # remove the last line break in the page before adding to the list
                try:
                    if thisPage[-1] == '\r': # for Windows
                        thisPage = thisPage[:-1]
                except IndexError:
                    pass
                instrList.append(thisPage)
                thisPage = ''
                if line[3] == 'S': # line == 'XXXS[functionName-parameters]'
                    instrList.append(line[4:].rstrip('\r\n')) # append function name
                else: # line == 'XXXN', normal instructions page
                    instrList.append('') # no function to be run
            else:
                thisPage += line
        return instrList, len(instrList)/2 # number of instructions pages

    def formal(self):
        self.stim.setText(self.beforeFormalText)
        self.stim.draw()
        self.w.flip()

    def rest(self,b,blockN):
        self.restText.replace(  'XX__XX',  str(int(round(  100*(b-1)/(blockN-1)  )))  )
        self.stim.setText(self.restText)
        self.stim.draw()
        self.w.flip()

    def next(self):
        self.stim.setText(self.list[self.index])
        functionName = self.list[self.index+1]
        self.index += 2
        return functionName

    def endExpt(self):
        self.stim.setText(self.exptEndText)
        self.stim.draw()
        self.w.flip()
        event.waitKeys(keyList=self.advancedKeyList, maxWait=60)
        self.w.close()
        core.quit()


# ███████ ██    ██ ██████       ██ ███████  ██████ ████████
# ██      ██    ██ ██   ██      ██ ██      ██         ██
# ███████ ██    ██ ██████       ██ █████   ██         ██
#      ██ ██    ██ ██   ██ ██   ██ ██      ██         ██
# ███████  ██████  ██████   █████  ███████  ██████    ██

class subjObject:
    def __init__(self, checked, subjNo, w, fileName):
        self.checked = checked
        self.subjNo = subjNo
        self.w = w
        self.fileName = fileName
        self.titles = ['checked','subjNo','date','startTime','python','psychopy','system','frameD_M','frameD_SD','winWidth','winHeight','fullScreen']
        self.duration = 'X' # default value before completion
        self.getBasicInfo()

    def addTitles(self, titles):
        self.titles += titles
        for x in titles:
            setattr(self, x, '') # default values

    def getBasicInfo(self):
        self.date, self.startTime = formattedTime()
        self.python, self.psychopy, self.system, self.frameD_M, self.frameD_SD, (self.winWidth, self.winHeight), self.fullScreen = getSystemInfo(self.w)

    def save(self):
        self.titles.append('duration') # the duration will always be the last column
        with open(self.fileName, 'a') as subjFile:
            subjFile.write(tabString([capFirstLetter(x) for x in self.titles])+'\n')
            subjFile.write(tabString([getattr(self, x) for x in self.titles])+'\n')


# ████████ ██████  ██  █████  ██
#    ██    ██   ██ ██ ██   ██ ██
#    ██    ██████  ██ ███████ ██
#    ██    ██   ██ ██ ██   ██ ██
#    ██    ██   ██ ██ ██   ██ ███████

class dataObject:
    def __init__(self, subjNo, fileName, titles):
        self.subjNo = subjNo
        self.fileName = fileName
        self.titles = titles

    def openFile(self):
        self.file = open(self.fileName, 'a')
        self.file.write(tabString([capFirstLetter(x) for x in self.titles])+'\n')

    def saveTrial(self, clear=True):
        self.file.write(tabString([getattr(self, x) for x in self.titles])+'\n')
        if clear:
            for x in self.titles:
                if x != 'subjNo': # clear data after saving to prepare for the next trial, except for the subject number
                    setattr(self, x, '')

    def clearTrial(self):
        for x in self.titles:
            if x != 'subjNo':
                setattr(self, x, '') # clear data after saving to prepare for the next trial

    def closeFile(self):
        try:
            self.file.close()
        except AttributeError:
            print 'The data file is not opened yet.'
