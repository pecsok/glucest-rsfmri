# # Moving Data to New Project
# 3 Important rules to using the SDK:
# 1. Remember the data model: everything is either an object, or an attachment to an object.
# 2. Objects are nested hierarchically.
# 3. Operating on objects is different from operating on their attachments.


import subprocess as sub
import os
import flywheel
import json
import shutil
import re
import time
import pandas as pd

fw = flywheel.Client()


#def initialise_subject_list(source_proj):
#    source = fw.projects.find_first('label="{}"'.format(source_proj))
#    subs = source.subjects()
#    return [x.label for x in subs]


def wait_timeout(proc, seconds):
    """
    This function waits for a process to finish, or raise exception after timeout. Use it to kill and restart fw-heudiconv if it hangs
    Returns: True if it's been running longer than <seconds>, False otherwise
    """
    start = time.time()
    end = start + seconds
    interval = min(seconds / 1000.0, .25)
    while True:
        result = proc.poll()
        if result is not None:
            return False
        if time.time() >= end:
            proc.terminate()
            return True
        time.sleep(interval)

download_subject(subj, proj, '.', 'T1w', ['anat']) # anat

def download_subject(subj_label, source_proj, dest_path, acqs, folders):
    '''
    This function runs fw-heudiconv-export on a subject, using the wait_timeout function to kill and restart if it hangs.
    Modify the command as necessary
    '''
    command = ['fw-heudiconv-export', '--proj', source_proj, '--subject', subj_label, '--path', dest_path, '--folders']
    command.extend(folders)
    while True:
        print(command)
        print(folders)
        print("Trying fw-heudiconv...")
        p = sub.Popen(command, stdout=sub.PIPE, stdin=sub.PIPE, stderr=sub.PIPE, universal_newlines=True)
        p_is_hanging = wait_timeout(p, 120)
        if not p_is_hanging:
            break


def tidy(path):
    '''
    This function tidies the BIDS directory that was downloaded.
    In this case, we renamed every ses-<label>, kept only T1s, fmaps, and rest scans, and fixed IntendedFors accordingly
    '''
    # get names
    print("Tidying BIDS Directory...")
    fnames = [ os.path.join(parent, name) for (parent, subdirs, files) in os.walk('{}/bids_directory/'.format(path)) for name in files + subdirs ]
    #fnames2 = [f.replace("ses-1", "ses-PNC") for f in fnames]
    # copy all to new session label
    for n in range(len(fnames)):
        os.makedirs(fnames[n])
        #if not os.path.exists(fnames2[n]):
        #    if os.path.isdir(fnames[n]):
        #        os.makedirs(fnames2[n])
        #    else:
        #        shutil.copy2(fnames[n], fnames2[n])
    # delete old session label files
    #for f in fnames:
    #    if "ses-1" in f and os.path.exists(f):
    #        shutil.rmtree(f)
    # delete unwanted tasks, only keep rest
    for f in fnames2:
        if re.search(r"task-(?!rest)", f) is not None and os.path.isfile(f):
            os.remove(f)
    # fix json sidecars of fieldmaps to only have rest intendedfor
    for f in fnames2:
        if f.endswith('.json') and os.path.isfile(f):
            with open(f, 'r') as data:
                json_data = json.load(data)
            if 'IntendedFor' in json_data.keys():
                json_data['IntendedFor'] = [x.replace("ses-1", "ses-PNC") for x in json_data["IntendedFor"] if re.search(r"task-(?=rest)", x) is not None]
                with open(f, 'w') as fixed:
                    json.dump(json_data, fixed, indent = 4)


def upload_subject(path, dest_proj):
    #tidy(path) #optional of course
    print("Uploading subject data...")
    print(dest_proj)
    p2 = sub.Popen(['fw', 'import', 'bids', '--project', dest_proj, '{}/bids_directory/'.format(path), 'bbl'], stdout=sub.PIPE, stdin=sub.PIPE, stderr=sub.PIPE, universal_newlines=True)
    out, err = p2.communicate(input="yes\n")
    print(out)
    p3 = sub.Popen(['rm', '-rf', 'bids_directory/'], stdout=sub.PIPE, stdin=sub.PIPE, stderr=sub.PIPE, universal_newlines=True)


def main():
    projects = ["GRMPY_822831", "MOTIVE", "PNC_LG_810336", "SYRP_818621"]
    for proj in projects:
        print("Gathering subject list for "+proj+"...\n")
        subjects_all = pd.read_csv('glucest_fmri_acquisitions.csv') # List of all GluCEST and fMRI acquisitions for project
        subjects = subjects_all[(subjects_all['PROTOCOL_rs'] == proj]) & (subjects_all['Transferred' == 0)]['BBLID']
        print("Downloading subject data from ",proj)
        for subj in subjects:
            print("\n=============================")
            print("Processing subject {}".format(subj))
            subj=str(subj)
            # Download all desired files
            download_subject(subj, proj, '.', 'T1w', ['anat']) # anat
            download_subject(subj, proj, '.', 'task-rest', ['func']) # func
            # Download specific fmap used in corresponding study:
            if proj == 'MOTIVE':
                download_subject(subj, proj, '.', 'epi', ['fmap']) # fmap (Motive)
            elif proj == ['GRMPY_822831','PNC_LG_810336','SYRP_818621']:
                download_subject(subj, proj, '.', 'magnitude1', ['fmap']) # fmap (Motive)
                download_subject(subj, proj, '.', 'magnitude2', ['fmap']) # fmap (Motive)
                download_subject(subj, proj, '.', 'phasediff', ['fmap']) # fmap (Motive)
            upload_subject('.', 'Penn_GluCEST') # Upload to flywheel folder for re-BIDSing

if __name__ == '__main__':
    main()
