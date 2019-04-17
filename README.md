# PsychoPy Experiment Toolbox (psychopy-expt-toolbox)

This is a tiny python toolbox for PsychoPy experiment by Yi-Chia Chen.

## Version History
- 1.0.0 (2018.10.18): First version with instructions controlling, subject data, and trial data objects
    - Used in Mazes Game Pilot 1

- 1.1.0 (2018.11.27): Passing experiment info between objects;
                      Adding rest counting to instructions, escape to trial, and get number to subject;
                      Fixing format
    - Used in Size Preference Adjustment Pilot 1

- 1.1.1 (2019.01.24): Fixing import format;
                      Fixing subj.addTitles bug and rest text % bug;
                      Included file name in error messages
    - Used in Size Preference 2IFC Pilot 1

- 1.1.2 (2019.01.28): Cleaning up trialObject.saveTrial();
                      Adding value check for subjObject formal question
    - Used in Scene Size Adjustment Pilot 1
    - Used in Scene Size Adjustment Pilot 2 (Blocked)

- 2.0.0b (2019.03.26): Adding experiment object and adjust roles of instructions, subject, and trial objects;
                       Adding rest duration recording to the experiment object;
                       Adding error message function

- 2.0.1b (2019.03.28): Fixing format and clean up redundancy;
                       Change the float subject number input to integer (to allow easier counter-balancing);
                       To allow replacing subject, add replacement count attribute and inquiry to the subject object

- 2.0.2b (2019.04.16): Fixing some bugs;


## Planned Improvements
- Fix the os path name error in error message printing (add a parameter to the function)
- Check rest count automatically and skip the rest at the end of the experiment
- Add trial count for rest (across blocks)
- Add check trial list length method in exptObject
- Create object controlling experimental blocks and trials with mixed and blocked design, different randomization units, etc. (nextTrial(), nextBlock() that update the trial.trialNo, .blockNo, & .restCount automatically)
