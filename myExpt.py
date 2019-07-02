import math
import os
import string
from datetime import datetime

from psychopy import core, visual, info, event


######## ##     ## ##    ##  ######  ######## ####  #######  ##    ##  ######
##       ##     ## ###   ## ##    ##    ##     ##  ##     ## ###   ## ##    ##
##       ##     ## ####  ## ##          ##     ##  ##     ## ####  ## ##
######   ##     ## ## ## ## ##          ##     ##  ##     ## ## ## ##  ######
##       ##     ## ##  #### ##          ##     ##  ##     ## ##  ####       ##
##       ##     ## ##   ### ##    ##    ##     ##  ##     ## ##   ### ##    ##
##        #######  ##    ##  ######     ##    ####  #######  ##    ##  ######

def polar_to_cartesian(r, theta):
    X = r*math.cos(math.radians(theta))
    Y = r*math.sin(math.radians(theta))
    return [X, Y]

def turn_list_to_tabbed_string(data_list):
    data_list = [str(x) for x in data_list]
    return '\t'.join(data_list)

def produce_formatted_time_string():
    NOW_DATE = str(datetime.now()).split('.')[0].split(' ')[0]
    NOW_TIME = str(datetime.now()).split('.')[0].split(' ')[1]
    return [NOW_DATE, NOW_TIME]

def get_system_info(w):
    SYS_DICT = info.RunTimeInfo(win=w, refreshTest=True)
    return (SYS_DICT['pythonVersion'], SYS_DICT['psychopyVersion'],
            SYS_DICT['systemHostName'], SYS_DICT['windowRefreshTimeAvg_ms'],
            SYS_DICT['windowRefreshTimeSD_ms'], SYS_DICT['windowSize_pix'],
            SYS_DICT['windowIsFullScr'])

def capitalize_first_letter(string_text):
    return string_text[0].upper() + string_text[1:]

def RGB256_to_RGBn1to1(rgb):
    return [(2.0*i/255.0)-1 for i in rgb]

def print_error_message(error_type, file_name, message):
    print file_name + '  --  ' + error_type + ': ' + message
    return None

def check_string_as_boolean(string_text):
    result = None
    if string_text in ['1','t','T','True','true','TRUE']:
        result = True
    elif string_text in ['0','f','F','False','false','FALSE']:
        result = False
    return result


######## ##     ## ########  ######## ########  #### ##     ## ######## ##    ## ########
##        ##   ##  ##     ## ##       ##     ##  ##  ###   ### ##       ###   ##    ##
##         ## ##   ##     ## ##       ##     ##  ##  #### #### ##       ####  ##    ##
######      ###    ########  ######   ########   ##  ## ### ## ######   ## ## ##    ##
##         ## ##   ##        ##       ##   ##    ##  ##     ## ##       ##  ####    ##
##        ##   ##  ##        ##       ##    ##   ##  ##     ## ##       ##   ###    ##
######## ##     ## ##        ######## ##     ## #### ##     ## ######## ##    ##    ##

class exptObject(object):
    def __init__(self, checked=False, exptName='Undefined',
                 screenColor='gray', pracBlockN=1, blockN=1, recycleBlockN=0,
                 restN=0, practiceTrialN=0, condN=1, condUniqueTrialN=1, blockRepeatN=1, condRecycleTrialN=0):
        self.checked = checked
        self.exptName = exptName
        self.screenColor = screenColor
        self.pracBlockN = pracBlockN
        self.blockN = blockN
        self.recycleBlockN = recycleBlockN # this is used to run a subset of recycled trials
        self.restN = restN
        self.restCount = 0
        self.practiceTrialN = practiceTrialN
        self.condN = condN
        self.condUniqueTrialN = condUniqueTrialN
        self.blockRepeatN = blockRepeatN
        self.condRecycleTrialN = condRecycleTrialN # number of trial recycled in each condition at the end
        self.trialNCal()
        self.restTimer = core.Clock()
        self.restDuration = []

    def createSubjDataInstance(self, additionalVar=[]):
        self.subjData = subjDataObject(additionalVar)
        self.subjData.exptName = self.exptName
        self.subjData.checked = self.checked

    def createTrialDataInstance(self, titles):
        self.trialData = trialDataObject(titles)
        self.trialData.subjNo = self.subjData.num
        self.trialData.exptName = self.exptName
        self.trialData.checked = self.checked
        self.trialData.formal = self.subjData.formal

    def createInstrInstance(self, fileName='instructions.txt', color='black', beforeFormalText='X', restText='X', restKey=['space'], exptEndText='X', advancedKeyList=['backslash']):
        self.instr = instrObject(fileName, color, beforeFormalText, restText, restKey, exptEndText, advancedKeyList)
        self.instr.w = self.w
        self.instr.createTextObject()

    def trialNCal(self):
        self.uniqueTrialN = self.condUniqueTrialN * self.condN
        self.condTrialN = self.condUniqueTrialN * self.blockRepeatN
        self.totalBlockN = self.pracBlockN + self.blockN + self.recycleBlockN
        self.recycleTrialN = self.condRecycleTrialN * self.condN
        self.blockTrialN = self.condTrialN * self.condN
        self.trialN = self.blockTrialN * self.blockN + self.recycleTrialN
        self.restTrialN = int(math.ceil(self.trialN/(self.restN+1.0)))
        if self.trialN % (self.restN+1.0) != 0:
            print_error_message('WARNING', os.path.basename(__file__), 'Unequal trial numbers between rests due to trial number being non-divisible.')

    def openExptWin(self):
        self.w = visual.Window(color=self.screenColor, units='pix',
                    fullscr=True, allowGUI=False, autoLog=False)
        self.getBasicInfo()

    def getBasicInfo(self):
        self.subjData.date, self.subjData.startTime = produce_formatted_time_string()
        (self.subjData.python, self.subjData.psychopy, self.subjData.system,
        self.subjData.frameD_M, self.subjData.frameD_SD, (self.subjData.winWidth,
        self.subjData.winHeight), self.subjData.fullScreen) = get_system_info(self.w)
        self.winWidth = self.subjData.winWidth
        self.winHeight = self.subjData.winHeight

    # def exptCheck(self):
    #     checkDict = {'subjData':self.subjData, 'trialData':self.trialData, 'instructions':self.instr}
    #     for key, value in checkDict.iteritems():
    #         if value == None:
    #             print_error_message('BUG', os.path.basename(__file__),'Experiment object is not fully defined. The' + key + 'object is not assigned.')
    #         self.escapeExpt()

    def rest(self):
        self.restCount += 1
        completePerc = int(round(  100.0*self.restCount/(self.restN+1.0)  ))
        try:
            self.instr.stim.setText(self.instr.restText.replace('XX__XX', str(completePerc)))
            self.instr.stim.draw()
        except AttributeError:
            print_error_message('BUG', os.path.basename(__file__),'The instructions object is not created. Escape right before showing the rest instructions.')
            self.escapeExpt()
        self.w.flip()
        self.restTimer.reset()
        event.waitKeys(keyList=self.instr.restKey)
        self.w.flip()
        self.subjData.restDuration.append(self.restTimer.getTime())

    def escapeExpt(self):
        self.w.close()
        try:
            self.subjData.save(complete=False)
        except AttributeError:
            print_error_message('NOTICE', os.path.basename(__file__),'Escape before creating the subject object.')
        try:
            self.trialData.closeFile()
        except AttributeError:
            print_error_message('NOTICE', os.path.basename(__file__),'Escape before creating the trial object.')
        exit(0)

    def endExpt(self):
        try:
            self.instr.stim.setText(self.instr.exptEndText)
            self.instr.stim.draw()
        except AttributeError:
            print_error_message('BUG', os.path.basename(__file__),'The instructions object is not created. Escape right before showing the end instructions.')
            self.escapeExpt()
        self.w.flip()
        try:
            self.subjData.save()
        except AttributeError:
            print_error_message('BUG', os.path.basename(__file__),'The subjData object is not created. Escape right after showing the end instructions.')
            self.escapeExpt()
        try:
            self.trialData.closeFile()
        except AttributeError:
            print_error_message('BUG', os.path.basename(__file__),'The trial object is not created. Escape right after showing the end instructions and saving the subject data.')
            self.escapeExpt()
        event.waitKeys(keyList=self.instr.advancedKeyList, maxWait=60)
        self.w.close()
        exit(0)


 ######  ##     ## ########        ## ########  ######  ########
##    ## ##     ## ##     ##       ## ##       ##    ##    ##
##       ##     ## ##     ##       ## ##       ##          ##
 ######  ##     ## ########        ## ######   ##          ##
      ## ##     ## ##     ## ##    ## ##       ##          ##
##    ## ##     ## ##     ## ##    ## ##       ##    ##    ##
 ######   #######  ########   ######  ########  ######     ##

class subjDataObject(object):
    def __init__(self, additionalVar=[]):
        self.num = None
        self.timer = core.Clock()
        self.titles = ['checked','num','replacement','date','startTime',
                       'python','psychopy','system',
                       'frameD_M','frameD_SD',
                       'winWidth','winHeight','fullScreen',
                       'instrDuration','duration']
        self.addTitles(additionalVar)
        self.instrD = 'X' # default value before completion
        self.duration = 'X' # default value before completion
        self.restDuration = []

    def askForSubjInfo(self):
        while True:
            self.num = raw_input('Subj No.: (int) ')
            try:
                int(self.num)
                break
            except ValueError:
                print_error_message('Error', os.path.basename(__file__),"That's not an integer.")
        while True:
            self.formal = raw_input('Formal? (T/F) ')
            self.formal = check_string_as_boolean(self.formal)
            if self.formal == None:
                print_error_message('Error', os.path.basename(__file__),'Failed to convert to Boolean.')
            else:
                break
        while True:
            self.replacement = raw_input('Replacement? (T/F) ')
            self.replacement = check_string_as_boolean(self.replacement)
            if self.replacement == None:
                print_error_message('Error', os.path.basename(__file__),'Failed to convert to Boolean.')
            else:
                break
        if self.formal:
            self.fileName = 'subj_'+self.exptName+'.txt'
        else:
            self.fileName = 'testingSubj_'+self.exptName+'.txt'

    def addTitles(self, additionalVar):
        for name, value in additionalVar:
            self.titles.append(name)
            setattr(self, name, value)

    def recordRestDuration(self):
        for i, duration in enumerate(self.restDuration):
            name = 'restDuration'+str(i+1)
            self.titles.append(name)
            setattr(self, name, duration)

    def save(self, complete=True):
        self.duration = self.timer.getTime()/60.0 # experiment duration in minutes
        if not complete:
            self.duration = 'HALT_'+str(self.duration)
        self.recordRestDuration()
        with open(self.fileName, 'a') as subjFile:
            subjFile.write(turn_list_to_tabbed_string([capitalize_first_letter(x) for x in self.titles])+'\n')
            subjFile.write(turn_list_to_tabbed_string([getattr(self, x) for x in self.titles])+'\n')


######## ########  ####    ###    ##
   ##    ##     ##  ##    ## ##   ##
   ##    ##     ##  ##   ##   ##  ##
   ##    ########   ##  ##     ## ##
   ##    ##   ##    ##  ######### ##
   ##    ##    ##   ##  ##     ## ##
   ##    ##     ## #### ##     ## ########

class trialDataObject(object):
    def __init__(self, titles):
        self.titles = titles
        self.clearTrial() # to create all attributes and set default values

    def openFile(self):
        if self.formal:
            self.fileName = 'data_'+self.exptName+'.txt'
        else:
            self.fileName = 'testingData_'+self.exptName+'.txt'
        self.file = open(self.fileName, 'a')
        self.file.write(turn_list_to_tabbed_string([capitalize_first_letter(x) for x in self.titles])+'\n')

    def saveTrial(self, clear=True):
        # save and clear data (except for the subject numbers)
        self.file.write(turn_list_to_tabbed_string([getattr(self, x) for x in self.titles])+'\n')
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
            print_error_message('NOTICE', os.path.basename(__file__),'Closing the data file before it is created.')


#### ##    ##  ######  ######## ########  ##     ##  ######  ######## ####  #######  ##    ##  ######
 ##  ###   ## ##    ##    ##    ##     ## ##     ## ##    ##    ##     ##  ##     ## ###   ## ##    ##
 ##  ####  ## ##          ##    ##     ## ##     ## ##          ##     ##  ##     ## ####  ## ##
 ##  ## ## ##  ######     ##    ########  ##     ## ##          ##     ##  ##     ## ## ## ##  ######
 ##  ##  ####       ##    ##    ##   ##   ##     ## ##          ##     ##  ##     ## ##  ####       ##
 ##  ##   ### ##    ##    ##    ##    ##  ##     ## ##    ##    ##     ##  ##     ## ##   ### ##    ##
#### ##    ##  ######     ##    ##     ##  #######   ######     ##    ####  #######  ##    ##  ######

class instrObject(object):
    def __init__(self, fileName='instructions.txt', color='black',
                 beforeFormalText='X', restText='X', restKey=['space'],
                 exptEndText='X', advancedKeyList=['backslash']):
        self.list, self.length = self.readInstr(fileName)
        self.color = color
        self.restText = restText
        self.exptEndText = exptEndText
        self.index = 0
        self.beforeFormalText = beforeFormalText
        self.advancedKeyList = advancedKeyList
        self.restCount = 0
        self.restKey = restKey

    def createTextObject(self):
        self.stim = visual.TextStim(self.w, text='', color=self.color, height=30, wrapWidth=900)

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
