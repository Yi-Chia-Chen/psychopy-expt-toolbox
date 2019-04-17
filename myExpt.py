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
    sysDict = info.RunTimeInfo(win=w, refreshTest=True)
    # sysDict['pythonVersion'] # version of python used
    # sysDict['psychopyVersion'] # version of psychopy used
    # sysDict['systemHostName'] # name of the computer
    # sysDict['windowRefreshTimeAvg_ms'] # mean of monitor refresh intervals
    # sysDict['windowRefreshTimeSD_ms'] # SD of monitor refresh intervals
    # sysDict['windowSize_pix'] # window size
    # sysDict['windowIsFullScr'] # whether window is fullscreen
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
    return (sysDict['pythonVersion'], sysDict['psychopyVersion'],
            sysDict['systemHostName'], sysDict['windowRefreshTimeAvg_ms'],
            sysDict['windowRefreshTimeSD_ms'], sysDict['windowSize_pix'],
            sysDict['windowIsFullScr'])

# capitalize the first letter ONLY,
# instead of using string.capitalize() or string.capwords()
# where the rest of the letter will be .lower()
def capFirstLetter(stringText):
    return stringText[0].upper() + stringText[1:]

# convert RGB 256 scale to -1.0-1.0
def RGBConvert(rgb):
    return [(2.0*i/255.0)-1 for i in rgb]

# print error messages
def errorMessage(type, message):
    print os.path.basename(__file__) + '  --  ' + type + ': ' + message


# ███████ ██   ██ ██████  ████████
# ██       ██ ██  ██   ██    ██
# █████     ███   ██████     ██
# ██       ██ ██  ██         ██
# ███████ ██   ██ ██         ██

class exptObject(object):
    def __init__(self, subj=None, trial=None, instr=None, checked=False, exptName='Undefined',
                 screenColor='gray', pracBlockN=1, blockN=1, repeatBlockN=0,
                 restN=0, practiceTrialN=0, condN=1, condTrialN=1, condRepeatN=0):
        self.subj = subj
        self.trial = trial
        self.instr = instr
        self.checked = checked
        self.exptName = exptName
        self.screenColor = screenColor
        self.pracBlockN = pracBlockN
        self.blockN = blockN
        self.repeatBlockN = repeatBlockN # this is used to repeat a subset of trials
        self.restN = restN
        self.restCount = 0
        self.practiceTrialN = practiceTrialN
        self.condN = condN
        self.condTrialN = condTrialN
        self.condRepeatN = condRepeatN # number of trial repeating in each condition at the end
        self.trialNCal()
        self.restTimer = core.Clock()
        self.restD = []

    def trialNCal(self):
        self.totalBlockN = self.pracBlockN + self.blockN + self.repeatBlockN
        self.repeatN = self.condRepeatN * self.condN
        self.blockTrialN = self.condTrialN * self.condN
        self.trialN = self.blockTrialN * self.blockN + self.repeatN
        self.restTrialN = int(math.ceil(self.trialN/(self.restN+1.0)))
        if self.trialN % (self.restN+1.0) != 0:
            errorMessage('WARNING','Unequal trial numbers between rests due to trial number being non-divisible.')

    def exptCheck(self):
        checkDict = {'subject':self.subj, 'trial':self.trial, 'instructions':self.instr}
        for key, value in checkDict.iteritems():
            if value == None:
                errorMessage('BUG','Experiment object is not fully defined. The' + key + 'object is not assigned.')
            self.escapeExpt()

    def rest(self):
        self.restCount += 1
        completePerc = int(round(  100.0*self.restCount/(self.restN+1.0)  ))
        try:
            self.instr.stim.setText(self.instr.restText.replace('XX__XX', str(completePerc)))
            self.instr.stim.draw()
        except AttributeError:
            errorMessage('BUG','The instructions object is not assigned. Escape right before showing the rest instructions.')
            self.escapeExpt()
        self.w.flip()
        self.restTimer.reset()
        event.waitKeys(keyList=self.instr.restKey)
        self.w.flip()
        self.restD.append(self.restTimer.getTime())

    def escapeExpt(self):
        self.w.close()
        try:
            self.subj.save(complete=False)
        except AttributeError:
            errorMessage('NOTICE','Escape before assigning or creating the subject object.')
        try:
            self.trial.closeFile()
        except AttributeError:
            errorMessage('NOTICE','Escape before assigning or creating the trial object.')
        exit(0)

    def endExpt(self):
        try:
            self.instr.stim.setText(self.instr.exptEndText)
            self.instr.stim.draw()
        except AttributeError:
            errorMessage('BUG','The instructions object is not assigned. Escape right before showing the end instructions.')
            self.escapeExpt()
        self.w.flip()
        try:
            self.subj.save()
        except AttributeError:
            errorMessage('BUG','The subj object is not assigned. Escape right after showing the end instructions.')
            self.escapeExpt()
        try:
            self.trial.closeFile()
        except AttributeError:
            errorMessage('BUG','The trial object is not assigned. Escape right after showing the end instructions and saving the subject data.')
            self.escapeExpt()
        event.waitKeys(keyList=self.instr.advancedKeyList, maxWait=60)
        self.w.close()
        exit(0)


# ███████ ██    ██ ██████       ██ ███████  ██████ ████████
# ██      ██    ██ ██   ██      ██ ██      ██         ██
# ███████ ██    ██ ██████       ██ █████   ██         ██
#      ██ ██    ██ ██   ██ ██   ██ ██      ██         ██
# ███████  ██████  ██████   █████  ███████  ██████    ██

class subjObject(object):
    def __init__(self, expt, additionalVar=[]):
        self.expt = expt
        self.expt.subj = self
        self.checked = self.expt.checked
        self.exptName = self.expt.exptName
        self.getSubjNo()
        self.w = visual.Window(color=self.expt.screenColor, units='pix',
                    fullscr=True, allowGUI=False, autoLog=False)
        self.expt.w = self.w
        self.getBasicInfo()
        self.timer = core.Clock()
        self.titles = ['checked','num','replacement','date','startTime',
                       'python','psychopy','system',
                       'frameD_M','frameD_SD',
                       'winWidth','winHeight','fullScreen',
                       'instrD','duration']
        self.instrD = 'X' # default value before completion
        self.duration = 'X' # default value before completion
        if additionalVar != []:
            self.addTitles(additionalVar)

    def getBasicInfo(self):
        self.date, self.startTime = formattedTime()
        (self.python, self.psychopy, self.system,
        self.frameD_M, self.frameD_SD, (self.winWidth,
        self.winHeight), self.fullScreen) = getSystemInfo(self.w)

    def getSubjNo(self):
        while True:
            self.num = raw_input('Subj No.: ')
            try:
                int(self.num)
                break
            except ValueError:
                errorMessage('Error',"That's not an integer.")
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
                errorMessage('Error','Failed to convert to Boolean.')
        while True:
            self.replacement = raw_input('Replacement? ')
            if self.replacement in ['1','0']:
                self.replacement = bool(int(self.formal))
                break
            elif self.replacement in ['t','True','true','TRUE']:
                self.replacement = True
                break
            elif self.replacement in ['f','False','false','FALSE']:
                self.replacement = False
                break
            else:
                errorMessage('Error','Failed to convert to Boolean.')

        if self.formal:
            self.fileName = 'subj_'+self.exptName+'.txt'
        else:
            self.fileName = 'testingSubj_'+self.exptName+'.txt'

    def addTitles(self, additionalVar):
        for name, value in additionalVar:
            self.titles.append(name)
            setattr(self, name, value)

    def recordRestD(self, restD):
        for i in xrange(self.expt.restN):
            name = 'restD'+str(i+1)
            self.titles.append(name)
            try:
                setattr(self, name, restD[i])
            except IndexError:
                setattr(self, name, 'X')
                print os.path.basename(__file__) + "  --  WARNING: Actual rest number is less than defined rest number."

    def save(self, complete=True):
        self.duration = self.timer.getTime()/60.0 # experiment duration in minutes
        if not complete:
            self.duration = 'HALT_'+str(self.duration)
        self.recordRestD()
        with open(self.fileName, 'a') as subjFile:
            subjFile.write(tabString([capFirstLetter(x) for x in self.titles])+'\n')
            subjFile.write(tabString([getattr(self, x) for x in self.titles])+'\n')


# ████████ ██████  ██  █████  ██
#    ██    ██   ██ ██ ██   ██ ██
#    ██    ██████  ██ ███████ ██
#    ██    ██   ██ ██ ██   ██ ██
#    ██    ██   ██ ██ ██   ██ ███████

class trialObject(object):
    def __init__(self, expt, subj, titles):
        self.expt = expt
        self.expt.trial = self
        self.subj = subj
        self.subjNo = subj.num
        self.exptName = subj.exptName
        if subj.formal:
            self.fileName = 'data_'+self.exptName+'.txt'
        else:
            self.fileName = 'testingData_'+self.exptName+'.txt'
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
            print os.path.basename(__file__) + '  --  NOTICE: Closing the data file before it is created.'


# ██ ███    ██ ███████ ████████ ██████
# ██ ████   ██ ██         ██    ██   ██
# ██ ██ ██  ██ ███████    ██    ██████
# ██ ██  ██ ██      ██    ██    ██   ██
# ██ ██   ████ ███████    ██    ██   ██

class instrObject(object):
    def __init__(self, expt, subj, fileName='instructions.txt', color='black',
                 beforeFormalText='X', restText='X', restKey=['space'],
                 exptEndText='X', advancedKeyList=['backslash']):
        self.expt = expt
        self.expt.instr = self
        self.w = subj.w
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

    def next(self):
        self.stim.setText(self.list[self.index])
        functionName = self.list[self.index+1]
        self.index += 2
        return functionName
