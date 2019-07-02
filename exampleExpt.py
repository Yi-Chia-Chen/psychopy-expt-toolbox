# Yi-Chia Chen

import glob
import random

from psychopy import core, visual, event
import pynput.mouse

import myExpt


##     ##    ###    ########  ####    ###    ########  ##       ########  ######
##     ##   ## ##   ##     ##  ##    ## ##   ##     ## ##       ##       ##    ##
##     ##  ##   ##  ##     ##  ##   ##   ##  ##     ## ##       ##       ##
##     ## ##     ## ########   ##  ##     ## ########  ##       ######    ######
 ##   ##  ######### ##   ##    ##  ######### ##     ## ##       ##             ##
  ## ##   ##     ## ##    ##   ##  ##     ## ##     ## ##       ##       ##    ##
   ###    ##     ## ##     ## #### ##     ## ########  ######## ########  ######

CHECKED = False # change to True only when everything is tested
SKIP_INSTRUCTIONS = False # skipping instructions for testing
EXPERIMENT_NAME = 'ExampleExpt'

# experiment structure
SIZE_CONDITION = ['big','small']
DIRECTION_CONDITION = ['left','right']
CONDITION_N = len(SIZE_CONDITION)*len(DIRECTION_CONDITION)

PRACTICE_BLOCK_N = 1
BLOCK_N = 2 # number of block for trial mixing (rests are controlled separately)
REST_N = 3 # number of rest
PRACTICE_TRIAL_N = 1
BLOCK_REPEAT_N = 1 # number of repetition in a block
CONDITION_UNIQUE_TRIAL_N = 13

# display
SCREEN_COLOR = 'gray'

# create experiment instance
expt = myExpt.exptObject(checked=CHECKED, exptName=EXPERIMENT_NAME, screenColor=SCREEN_COLOR,
                         pracBlockN=PRACTICE_BLOCK_N, blockN=BLOCK_N, restN=REST_N,
                         practiceTrialN=PRACTICE_TRIAL_N, condN=CONDITION_N,
                         condUniqueTrialN=CONDITION_UNIQUE_TRIAL_N, blockRepeatN=BLOCK_REPEAT_N)
                         # this object manages the experiment window, escaping and ending the experiment, blocks, rests, and trials

expt.createSubjDataInstance(additionalVar=[['exampleVar1',1],['exampleVar2',2]])
subjData = expt.subjData # just to make it shorter
# this object manage the subject data (as opposed to the trial data)

subjData.exampleVar1 = 2 # this is how you can save different values

subjData.askForSubjInfo() # command line questions
expt.openExptWin()

# duration
ITI = 0.485 # inter-trial interval; 500ms (60 Hz)
MOUSE_RESET_DURATION = 0.015 # time for mouse position reset (most of the module has a small delay in setting mouse position, including pynput used here)
WAIT_DURATION = ITI - MOUSE_RESET_DURATION # time
INITIAL_NO_CLICK_DURATION = 0.2 # accepting clicks only after this duration has passed

# timer
display_timer = core.Clock() # to control displays
rest_timer = core.Clock() # record rest durations


 ######  ######## #### ##     ## ##     ## ##       ####
##    ##    ##     ##  ###   ### ##     ## ##        ##
##          ##     ##  #### #### ##     ## ##        ##
 ######     ##     ##  ## ### ## ##     ## ##        ##
      ##    ##     ##  ##     ## ##     ## ##        ##
##    ##    ##     ##  ##     ## ##     ## ##        ##
 ######     ##    #### ##     ##  #######  ######## ####

STIM_PATH = 'Stimuli/'
PRACTICE_STIM_NAME = 'practiceStimulus.png'
practice_stim = visual.ImageStim(expt.w, image=STIM_PATH+PRACTICE_STIM_NAME, colorSpace='rgb')

img_dict = {}
for file_name in glob.glob(STIM_PATH+'*.png'): # get all png images in the specified folder
    if 'practice' not in file_name: # skip practice stimuli
        temp_name = file_name.replace('Stimuli/','').replace('Stimuli\\','').split('_') # strip the folder name (work in different os) and split into a list
        if temp_name[0] == 'b': # detect condition
            this_real_size = 'big'
        else:
            this_real_size = 'small'
        this_stim_name = ''.join(temp_name[1:]).replace('.png','') # strip the file extension
        img_dict[(this_stim_name,'right')] = [this_real_size, visual.ImageStim(expt.w, image=file_name)]
        img_dict[(this_stim_name,'left')] = [this_real_size, visual.ImageStim(expt.w, image=file_name, flipHoriz=True)]

if len(img_dict) != expt.uniqueTrialN:
    myExpt.errorMessage('BUG', 'Number of stimuli ('+len(img_dict)+') does not match the specified number of unique trials ('+str(expt.uniqueTrialN)+').')
    expt.escapeExpt()


########  ########  ######  ########   #######  ##    ##  ######  ########
##     ## ##       ##    ## ##     ## ##     ## ###   ## ##    ## ##
##     ## ##       ##       ##     ## ##     ## ####  ## ##       ##
########  ######    ######  ########  ##     ## ## ## ##  ######  ######
##   ##   ##             ## ##        ##     ## ##  ####       ## ##
##    ##  ##       ##    ## ##        ##     ## ##   ### ##    ## ##
##     ## ########  ######  ##         #######  ##    ##  ######  ########

CENTER_POSITION = (int(round(expt.winWidth/2.0)), int(round(expt.winHeight/2.0)))

# cursor
mouse = visual.CustomMouse(expt.w, clickOnUp=True, pointer=None)
controlled_mouse = pynput.mouse.Controller()


########     ###    ########    ###
##     ##   ## ##      ##      ## ##
##     ##  ##   ##     ##     ##   ##
##     ## ##     ##    ##    ##     ##
##     ## #########    ##    #########
##     ## ##     ##    ##    ##     ##
########  ##     ##    ##    ##     ##

DATA_TITLES = [
              'subjNo',
              'blockNo',
              'trialNo',
              'restCount',
              'size',
              'direction',
              'stimName',
              'clickPosX',
              'rt'
             ] # column labs to save for each trial

expt.createTrialDataInstance(titles=DATA_TITLES)
trialData = expt.trialData # just to make it shorter
# this object manage the trial data



######## ########  ####    ###    ##       ##       ####  ######  ########
   ##    ##     ##  ##    ## ##   ##       ##        ##  ##    ##    ##
   ##    ##     ##  ##   ##   ##  ##       ##        ##  ##          ##
   ##    ########   ##  ##     ## ##       ##        ##   ######     ##
   ##    ##   ##    ##  ######### ##       ##        ##        ##    ##
   ##    ##    ##   ##  ##     ## ##       ##        ##  ##    ##    ##
   ##    ##     ## #### ##     ## ######## ######## ####  ######     ##

trial_list = img_dict.keys() * BLOCK_REPEAT_N

if len(trial_list) != expt.blockTrialN:
    this_error = ('Trial number does not match. ' +
                  'The trial list contains ' + str(len(trial_list)) + ' elements, but the trial number per block is '+str(expt.blockTrialN)+'.')
    myExpt.errorMessage('BUG', this_error)
    expt.escapeExpt()


######## ##     ## ##    ##  ######  ######## ####  #######  ##    ##
##       ##     ## ###   ## ##    ##    ##     ##  ##     ## ###   ##
##       ##     ## ####  ## ##          ##     ##  ##     ## ####  ##
######   ##     ## ## ## ## ##          ##     ##  ##     ## ## ## ##
##       ##     ## ##  #### ##          ##     ##  ##     ## ##  ####
##       ##     ## ##   ### ##    ##    ##     ##  ##     ## ##   ###
##        #######  ##    ##  ######     ##    ####  #######  ##    ##

def run_trial(b,t):
    trialData.blockNo = b
    trialData.trialNo = t+1
    trialData.restCount = expt.restCount
    if b < expt.pracBlockN: # practice
        this_img = practice_stim
    else:
        this_trial = trial_list[t]
        this_size, this_img = img_dict[this_trial]
        trialData.size = this_size
        trialData.direction = this_trial[1]
        trialData.stimName = this_trial[0]

    while display_timer.getTime() < WAIT_DURATION:
        pass

    controlled_mouse.position = CENTER_POSITION
    while display_timer.getTime() < ITI:
        pass

    first_frame = True
    display_timer.reset() # to make sure the subject won't be able to click before the display is up
    event.clearEvents()
    while True:
        if not trialData.formal:
            key_press = event.getKeys(keyList='escape')
            if key_press != []:
                expt.escapeExpt()

        cursor_pos = mouse.getPos()
        clicks = mouse.getPressed()

        if clicks[0] != 0:
            if display_timer.getTime() >= INITIAL_NO_CLICK_DURATION: # only accepting clicks INITIAL_NO_CLICK_DURATION seconds after stimulus onset
                trialData.rt = display_timer.getTime()
                expt.w.flip()
                display_timer.reset()
                trialData.clickPosX = cursor_pos[0]
                if b >= expt.pracBlockN: # not practice
                    trialData.saveTrial()
                break
            else:
                event.clearEvents(eventType='mouse')

        cursor_x = cursor_pos[0]

        this_img.setPos( (cursor_x, this_img.pos[1]) )
        this_img.draw()
        expt.w.flip()
        if first_frame:
            display_timer.reset()
            first_frame = False


#### ##    ##  ######  ######## ########  ##     ##  ######  ######## ####  #######  ##    ##  ######
 ##  ###   ## ##    ##    ##    ##     ## ##     ## ##    ##    ##     ##  ##     ## ###   ## ##    ##
 ##  ####  ## ##          ##    ##     ## ##     ## ##          ##     ##  ##     ## ####  ## ##
 ##  ## ## ##  ######     ##    ########  ##     ## ##          ##     ##  ##     ## ## ## ##  ######
 ##  ##  ####       ##    ##    ##   ##   ##     ## ##          ##     ##  ##     ## ##  ####       ##
 ##  ##   ### ##    ##    ##    ##    ##  ##     ## ##    ##    ##     ##  ##     ## ##   ### ##    ##
#### ##    ##  ######     ##    ##     ##  #######   ######     ##    ####  #######  ##    ##  ######

AFTER_PRAC_TEXT = 'You are now ready for the experiment!\n\nWhen I leave the room, you may press SPACE to start.'
REST_TEXT = 'You have completed XX__XX% of the experiment. Feel free to take a break now. Press SPACE to continue whenever you are ready.'
END_TEXT = 'You have finished the experiment. Please find the experimenter.'

INSTRUCTIONS_FILE_NAME = 'instructions_exampleExpt.txt'

expt.createInstrInstance(fileName=INSTRUCTIONS_FILE_NAME, color='black',
                         beforeFormalText=AFTER_PRAC_TEXT, restText=REST_TEXT, exptEndText=END_TEXT)
instr = expt.instr # just to make it shorter
# this object manage instructions presentation

def showExample():
    this_img = practice_stim
    event.clearEvents()
    controlled_mouse.position = CENTER_POSITION
    while True:
        key_press = event.getKeys(keyList=instr.advancedKeyList)
        if key_press != []:
            break
        cursor_pos = mouse.getPos()
        cursor_x = cursor_pos[0]

        this_img.setPos( (cursor_x, this_img.pos[1]) )
        this_img.draw()
        instr.stim.draw()
        expt.w.flip()

if not SKIP_INSTRUCTIONS:
    for i in xrange(instr.length):
        functionName = instr.next() # set text without drawing and flipping
        if functionName != '': # need to draw instructions text stim in these functions too at proper time
            paramIndex = functionName.find('-')
            if paramIndex == -1:
                eval(functionName)()
            else:
                eval(functionName[:paramIndex])(eval(functionName[paramIndex+1:]))
        else: # text-only pages
            instr.stim.draw()
            expt.w.flip()
            if i == instr.length-1:
                event.waitKeys(keyList=['space']) # last page of instructions
                expt.w.flip()
                display_timer.reset()
            else:
                event.waitKeys(keyList=instr.advancedKeyList)


######## ##     ## ########  ######## ########  #### ##     ## ######## ##    ## ########
##        ##   ##  ##     ## ##       ##     ##  ##  ###   ### ##       ###   ##    ##
##         ## ##   ##     ## ##       ##     ##  ##  #### #### ##       ####  ##    ##
######      ###    ########  ######   ########   ##  ## ### ## ######   ## ## ##    ##
##         ## ##   ##        ##       ##   ##    ##  ##     ## ##       ##  ####    ##
##        ##   ##  ##        ##       ##    ##   ##  ##     ## ##       ##   ###    ##
######## ##     ## ##        ######## ##     ## #### ##     ## ######## ##    ##    ##

subjData.instrDuration = subjData.timer.getTime()/60.0 # in minutes

trial_count = -expt.practiceTrialN
trialData.openFile()
for b in xrange(expt.totalBlockN):
    if b == 0:
        this_trial_n = expt.practiceTrialN
    else: # formal blocks
        this_trial_n = expt.blockTrialN
        random.shuffle(trial_list)
        if b == 1: # before formal blocks start
            instr.formal() # instructions after practice and before formal
            event.waitKeys(keyList=['space'])
            expt.w.flip()
            display_timer.reset()
    for t in xrange(this_trial_n):
        run_trial(b,t)
        trial_count += 1
        if trial_count == expt.restTrialN and expt.restCount < expt.restN:
            trial_count = 0
            expt.rest()
            display_timer.reset()
expt.endExpt()
