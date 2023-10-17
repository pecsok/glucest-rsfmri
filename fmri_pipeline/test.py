import subprocess as sub
import os
import flywheel
import json
import shutil
import re
import time
import pandas as pd

projects = ["GRMPY_822831", "MOTIVE", "PNC_LG_810336", "SYRP_818621"]
for proj in projects:
        print("Gathering subject list for "+proj+"...\n")
        subjects_all = pd.read_csv('glucest_fmri_acquisitions.csv') # List of all GluCEST and fMRI acquisitions for project
        subjects = subjects_all[(subjects_all['PROTOCOL_rs'] == proj) & (subjects_all['Transferred'] == 0)]['BBLID']
        print("Downloading subject data from ",proj)
        print(subjects)
