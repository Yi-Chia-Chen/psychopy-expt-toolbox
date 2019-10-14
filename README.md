# PsychoPy Experiment Toolbox (psychopy-expt-toolbox)

This is a tiny python toolbox for PsychoPy experiment by Yi-Chia Chen.

## Version History
- 3.1.0 (2019.06.17): rename a few attributes;
                       clear up the trial number calculation;
                       rename trialDataObject instance to trialData, and subjDataObject instance to subjData;
                       Fix some bugs;
                       Add an example experiment
    - Used in Size Preference Expt 2 2IFC

- 3.0.0b (2019.06.17): create instr, subj, trial objects within expt object;
                       Open the experiment window with method not with the constructor;
                       Fix the os path name bug in error message printing

- 2.0.3 (2019.04.18): Fix a bug
    - Used in Size Preference Expt 2 2IFC Intact Images Pretest

- 2.0.2b (2019.04.16): Fix some bugs;

- 2.0.1b (2019.03.28): Fix format and clean up redundancy;
                       Change the float subject number input to integer (to allow easier counter-balancing);
                       To allow replacing subject, add replacement count attribute and inquiry to the subject object

- 2.0.0b (2019.03.26): Add experiment object and adjust roles of instructions, subject, and trial objects;
                       Add rest duration recording to the experiment object;
                       Add error message function

- 1.1.2 (2019.01.28): Clean up trialObject.saveTrial();
                      Add value check for subjObject formal question
    - Used in Scene Size Adjustment Pilot 1
    - Used in Scene Size Adjustment Pilot 2 (Blocked)

- 1.1.1 (2019.01.24): Fix import format;
                      Fix subj.addTitles bug and rest text % bug;
                      Includ file name in error messages
    - Used in Size Preference 2IFC Pilot 1

- 1.1.0 (2018.11.27): Pass experiment info between objects;
                      Add rest counting to instructions, escape to trial, and get number to subject;
                      Fix format
    - Used in Size Preference Adjustment Pilot 1

- 1.0.0 (2018.10.18): First version with instructions controlling, subject data, and trial data objects
    - Used in Mazes Game Pilot 1


## Planned Improvements

### Cleaning-up
- Add check trial list length method in exptObject
- Use assert
- Develop testing tool sets
- update the rest instructions to use str.format()
- update to Python 3 (use f-strings instead of str.format())

### Features
- Allow a parameter of separator in subjDataObject and trialDataObject
- Add trial count for rest (across blocks)
- Check rest count automatically and skip the rest at the end of the experiment
- Create object controlling experimental blocks and trials with mixed and blocked design, different randomization units, etc. (nextTrial(), nextBlock() that update the trial.trialNo, .blockNo, & .restCount automatically)