# -*- coding: utf-8 -*-

import math
import os
import string
from datetime import datetime

from psychopy import core, visual, info, event


# ███████ ██    ██ ███    ██  ██████ ████████ ██  ██████  ███    ██ ███████
# ██      ██    ██ ████   ██ ██         ██    ██ ██    ██ ████   ██ ██
# █████   ██    ██ ██ ██  ██ ██         ██    ██ ██    ██ ██ ██  ██ ███████
# ██      ██    ██ ██  ██ ██ ██         ██    ██ ██    ██ ██  ██ ██      ██
# ██       ██████  ██   ████  ██████    ██    ██  ██████  ██   ████ ███████

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
    # full list of keys:
    #     ['psychopyVersion', 'systemRebooted', 'windowWinType', 'windowRgb',
    #     'systemUserID', 'windowRefreshTimeMedian_ms', 'windowScreen',
    #     'systemTimeNumpySD1000000_sec', 'windowSize_pix', 'systemUser',
    #     'systemHaveInternetAccess', 'windowMonitor.name', 'systemMemFreeRAM',
    #     'windowMonitor.getDistance_cm', 'psychopyHaveExtRush',
    #     'windowRefreshTimeAvg_ms', 'windowUnits', 'systemLocale',
    #     'systemPlatform', 'experimentRunTime', 'windowRefreshTimeSD_ms',
    #     'experimentScript.directory', 'systemSec.pythonSSL',
    #     'windowMonitor.getWidth_cm', 'experimentRunTime.epoch',
    #     'experimentScript', 'experimentScript.digestSHA1', 'systemUsersCount',
    #     'windowPos_pix', 'pythonVersion', 'windowMonitor.currentCalibName',
    #     'systemMemTotalRAM', 'windowIsFullScr', 'systemHostName']
    return (sysDic['pythonVersion'], sysDic['psychopyVersion'],
            sysDic['systemHostName'], sysDic['windowRefreshTimeAvg_ms'],
            sysDic['windowRefreshTimeSD_ms'], sysDic['windowSize_pix'],
            sysDic['windowIsFullScr'])

# capitalize the first letter ONLY,
# instead of using string.capitalize() or string.capwords()
# where the rest of the letter will be .lower()
def capFirstLetter(stringText):
    return stringText[0].upper() + stringText[1:]

# convert RGB 256 scale to -1.0-1.0
def RGBConvert(rgb):
    return [(2.0*i/255.0)-1 for i in rgb]


# ███████ ██    ██ ██████       ██ ███████  ██████ ████████
# ██      ██    ██ ██   ██      ██ ██      ██         ██
# ███████ ██    ██ ██████       ██ █████   ██         ██
#      ██ ██    ██ ██   ██ ██   ██ ██      ██         ██
# ███████  ██████  ██████   █████  ███████  ██████    ██

class subjObject(object):
    def __init__(self, checked, exptName, screenColor='gray', additionalVar=[]):
        self.checked = checked
        self.exptName = exptName
        self.timer = core.Clock()
        self.titles = ['checked','num','date','startTime',
                       'python','psychopy','system',
                       'frameD_M','frameD_SD',
                       'winWidth','winHeight','fullScreen',
                       'instrD','duration']
        self.instrD = 'X' # default value before completion
        self.duration = 'X' # default value before completion
        self.getSubjNo()
        self.screenColor = screenColor
        self.w = visual.Window(
                    color=self.screenColor, units='pix', fullscr=True,
                    allowGUI=False, autoLog=False)
        self.getBasicInfo()
        if additionalVar != []:
            self.addTitles(additionalVar)

    def getSubjNo(self):
        while True:
            self.num = raw_input('Subj No.: ')
            try:
                float(self.num)
                break
            except ValueError:
                print os.path.basename(__file__) + "  --  Error: That's not a number."
        while True:
            self.formal = raw_input('Formal? ')
            if self.formal in ['1','0']:
                self.formal = bool(int(self.formal))
                break
            elif self.formal in ['t','True','true','TRUE']:
                self.formal = True
                break
            elif self.formal in ['f','False','false','FALSE']:
                self.formal = False
                break
            else:
                print os.path.basename(__file__) + "  --  Error: Failed to convert to Boolean."

        if self.formal:
            self.fileName = 'subj_'+self.exptName+'.txt'
        else:
            self.fileName = 'testingSubj_'+self.exptName+'.txt'

    def addTitles(self, additionalVar):
        for name, value in additionalVar:
            self.titles.append(name)
            setattr(self, name, value)

    def getBasicInfo(self):
        self.date, self.startTime = formattedTime()
        (self.python, self.psychopy, self.system,
        self.frameD_M, self.frameD_SD, (self.winWidth,
        self.winHeight), self.fullScreen) = getSystemInfo(self.w)

    def save(self, complete=True):
        self.duration = self.timer.getTime()/60.0 # experiment duration in minutes
        if not complete:
            self.duration = 'HALT_'+str(self.duration)
        with open(self.fileName, 'a') as subjFile:
            subjFile.write(tabString([capFirstLetter(x) for x in self.titles])+'\n')
            subjFile.write(tabString([getattr(self, x) for x in self.titles])+'\n')


# ████████ ██████  ██  █████  ██
#    ██    ██   ██ ██ ██   ██ ██
#    ██    ██████  ██ ███████ ██
#    ██    ██   ██ ██ ██   ██ ██
#    ██    ██   ██ ██ ██   ██ ███████

class trialObject(object):
    def __init__(self, subj, titles):
        self.subj = subj
        self.subjNo = subj.num
        if subj.formal:
            self.fileName = 'data_'+subj.exptName+'.txt'
        else:
            self.fileName = 'testingData_'+subj.exptName+'.txt'
        self.exptName = subj.exptName
        self.titles = titles
        self.clearTrial() # to create all attributes and set default values

    def openFile(self):
        self.file = open(self.fileName, 'a')
        self.file.write(tabString([capFirstLetter(x) for x in self.titles])+'\n')

    def saveTrial(self, clear=True):
        # save and clear data (except for the subject numbers)
        self.file.write(tabString([getattr(self, x) for x in self.titles])+'\n')
        if clear:
            self.clearTrial()

    def clearTrial(self): # clear data (except for the subject numbers)
        for x in self.titles:
            if x != 'subjNo':
                setattr(self, x, '')

    def closeFile(self):
        try:
            self.file.close()
        except AttributeError:
            print os.path.basename(__file__) + '  --  Error: The data file is not opened yet.'

    def escapeExpt(self):
        self.subj.w.close()
        self.subj.save(complete=False)
        self.closeFile()
        exit(0)



# ██ ███    ██ ███████ ████████ ██████
# ██ ████   ██ ██         ██    ██   ██
# ██ ██ ██  ██ ███████    ██    ██████
# ██ ██  ██ ██      ██    ██    ██   ██
# ██ ██   ████ ███████    ██    ██   ██

class instrObject(object):
    def __init__(self, subj, trial, fileName='instructions.txt', color='black',
                 beforeFormalText='X', restText='X', restN=0, restKey=['space'],
                 exptEndText='X', advancedKeyList=['backslash']):
        self.subj = subj
        self.trial = trial
        self.w = self.subj.w
        self.list, self.length = self.readInstr(fileName)
        self.stim = visual.TextStim(
                                    self.w, text='', color=color,
                                    height=30, wrapWidth=900
                                   )
        self.restText = restText
        self.exptEndText = exptEndText
        self.index = 0
        self.beforeFormalText = beforeFormalText
        self.advancedKeyList = advancedKeyList
        self.restCount = 0
        self.restN = restN
        self.restKey = restKey

    def readInstr(self,fileName):
        tempFile = open(fileName, 'r')
        tempText = tempFile.readlines()
        tempFile.close()
        instrList = [] # even indices: instructions; odd indices: function name
        thisPage = ''
        for line in tempText:
            if line[:3] == 'XXX':
                thisPage = thisPage[:-1]
                # remove last line break in the page before adding to the list
                try:
                    if thisPage[-1] == '\r': # for Windows
                        thisPage = thisPage[:-1]
                except IndexError:
                    pass
                instrList.append(thisPage)
                thisPage = ''
                if line[3] == 'S': # line == 'XXXS[functionName-parameters]'
                    instrList.append(line[4:].rstrip('\r\n'))
                    # append function name
                else: # line == 'XXXN', normal instructions page
                    instrList.append('') # no function to run
            else:
                thisPage += line
        return instrList, len(instrList)/2 # number of instructions pages

    def formal(self):
        self.stim.setText(self.beforeFormalText)
        self.stim.draw()
        self.w.flip()

    def rest(self):
        self.restCount += 1
        completePerc = int(round(  100.0*self.restCount/(self.restN+1.0)  ))
        self.thisRestText = self.restText.replace('XX__XX', str(completePerc))
        self.stim.setText(self.thisRestText)
        self.stim.draw()
        self.w.flip()
        event.waitKeys(keyList=self.restKey)
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
        self.trial.closeFile()
        self.subj.save()
        event.waitKeys(keyList=self.advancedKeyList, maxWait=60)
        self.w.close()
        exit(0)
