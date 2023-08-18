# glucest-rsfmri
Repository for "Project 1" of PhD: GluCEST-rsfMRI

General Analysis Plan: 
1.  Re-run steps of MotorGluCEST with all BBLIDs, updated code, and using established Yeo Atlas functional networks. 
2.  Process rsfMRI data
3.  Repeat steps with subject-specific functional networks

Stage 1: BIDSify 3T and 7T Data 
- Add these to the repo

Stage 2: Run fMRI Prep
- Need to mount singularity node
- ssh singularity01 before running script

Stage 3: Run XCP
- Mount/install XCP image into singularity space. Do this using Screen to avoid connection timing out and interrupting installation.
  singularity pull docker://pennbbl/xcpengine:latest
  

