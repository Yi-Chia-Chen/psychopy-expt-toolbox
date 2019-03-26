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

- 2.0.0 (2019.03.08): Adding experiment object and adjust roles of instructions, subject, and trial objects;
                      Adding rest duration recording to the experiment object;
                      Adding error message function
                      NOT TESTED YET

## Planned Improvements
- Create object controlling experimental blocks and trials with mixed and blocked design, different randomization units, etc.
