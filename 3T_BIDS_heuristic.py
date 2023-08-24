
# File:     3T_BIDS_heuristic.py
# Date:
# Desc:     heuristic file to curate the 3T fmri scans into BIDS format

import os

#################################################################################
####################  Create keys for each acquisition type  ####################
#################################################################################

def create_key(template, outtype=('nii.gz',), annotation_classes=None):
    if template is None or not template:
        raise ValueError('Template must be a valid format string')
    return template, outtype, annotation_classes

#anat
t1w = create_key(
    'sub-{bblid}/ses-{session}/anat/sub-{bblid}_ses-{session}_T1w')
#func
func = create_key(
    'sub-{bblid}/ses-{session}/func/sub-{bblid}_ses-{session}_task-rest_bold')
#fmap - which to include?
b0_phase = create_key(
   'sub-{bblid}/{session}/fmap/sub-{bblid}_{session}_phase_{item}')
b0_phase1 = create_key(
    'sub-{bblid}/{session}/fmap/sub-{bblid}_{session}_phase1')
b0_phase2 = create_key(
    'sub-{bblid}/{session}/fmap/sub-{bblid}_{session}_phase2')
b0_phasediff = create_key(
   'sub-{bblid}/{session}/fmap/sub-{bblid}_{session}_phasediff')
b0_mag = create_key(
   'sub-{bblid}/{session}/fmap/sub-{bblid}_{session}_magnitude{item}')
b0_mag1 = create_key(
   'sub-{bblid}/{session}/fmap/sub-{bblid}_{session}_magnitude1')
b0_mag2 = create_key(
   'sub-{bblid}/{session}/fmap/sub-{bblid}_{session}_magnitude2')
AP_epi = create_key(
   'sub-{bblid}/{session}/fmap/sub-{bblid}_acq-fMRI_dir-AP_epi')
PA_epi = create_key(
   'sub-{bblid}/{session}/fmap/sub-{bblid}_acq-fMRI_dir-PA_epi')
topup = create_key(
#    'sub-{bblid}/{session}/fmap/sub-{bblid}_acq-dMRI_topup_epi')

#################################################################################
###########  Define rules to map scans to the correct BIDS filename  ############
#################################################################################

#Institution name: PENN - HUP; NEUM - MPI for Human Development; UTMB - UTMB 3T SKYRA

def infotodict(seqinfo):
    """Heuristic evaluator for determining which runs belong where
    allowed template fields - follow python string module:
    item: index within category
    subject: participant id
    seqitem: run number during scanning
    subindex: sub index within group
    """

    info = {t1w: [],
        b0_phase: [], b0_phase1: [], b0_phase2: [],
        b0_mag: [], b0_mag1: [], b0_mag2: [], b0_phasediff: [],
        AP_epi: [], PA_epi: [], topup: [],
        rest: []
    }

## The get_latest_series function appends the series_id to correct key in info dictionary 
## based on the key and s parameters passed to it.
    def get_latest_series(key, s): 
        info[key].append(s.series_id)

## Start to loop through items in input folder
## Note project names next to corresponding file/series name format
    for s in seqinfo:
        protocol = s.protocol_name.lower()

        ## ANAT
        if "MPRAGE" in s.series_description and "MPRAGE_NAV" not in s.series_description:
            if s.dcm_dir_name.endswith("moco3_4.nii.gz"): # For project 810336-Go3, 815814-Conte, 818621-SYRP
                get_latest_series(t1w, s)
            elif "ipat2_2" in s.series_description: # Projects: 812481-22q, 822831-GRMPY, 818028-Effort
                get_latest_series(t1w, s)
        elif "anat-T1w_acq-vNavBC" in s.series_description: # Project: 833922 - EvolPsy
            get_latest_series(t1w, s)
        elif "ABCD_T1w_MPR_vNav_1" in s.series_description: # Project: 844685 - SSBC, MOTIVE
            get_latest_series(t1w, s)           

    ## FUNC 
        elif "restbold" in s.series_description:
            get_latest_series(func, s)
        elif "ABCD_fMRI_rest" in s.series_description: # Project: MOTIVE
            get_latest_series(func, s)
            
        #FMAPS
        elif "B0map_onesizefitsall_v3" in s.series_description:
            if s.dcm_dir_name.endswith("ph.nii.gz"):
                get_latest_series(b0_phase, s)
            if s.dcm_dir_name.endswith("_ph.nii.gz"):
                get_latest_series(b0_phase, s)
            if "ph" in s.dcm_dir_name:
                get_latest_series(b0_phase, s)
        
        elif "B0map" in s.series_description and "M" in s.image_type: # Ask Kahini which she input into fMRIPrep. Ask nick where im
            if "e1" in s.dcm_dir_name:
                get_latest_series(b0_mag1, s)
            elif "e2" in s.dcm_dir_name:
                get_latest_series(b0_mag2, s)
            #info[b0_mag].append(s.series_id)
        elif "B0map" in s.series_description and "P" in s.image_type: 
            if "e1" in s.dcm_dir_name:
                get_latest_series(b0_phase1, s)
            elif "e2" in s.dcm_dir_name:
                get_latest_series(b0_phase2, s)
            else:
                get_latest_series(b0_phasediff, s)
            #info[b0_phase].append(s.series_id)
        elif "B0map_onesizefitsall_v3" in s.series_description:
            if "e1" in s.dcm_dir_name:
        #        if "ph" in s.dcm_dir_name:
        #            get_latest_series(b0_phase, s)
        #        else:
        #            get_latest_series(b0_mag, s)
        #    elif "e2" in s.dcm_dir_name:
        #        if "ph" in s.dcm_dir_name:
        #            get_latest_series(b0_phase, s)
        #        else:
        #            get_latest_series(b0_mag, s)
        #    else:
        #        continue
            #else:
            #    continue
        #elif "fmap" in s.series_description:
        #    if "dir-AP" in s.series_description:
        #        get_latest_series(AP_epi, s)
        #    elif "dir-PA" in s.series_description:
        #        get_latest_series(PA_epi, s)
        elif "fmap-EPIdist_acq-fmri_dir-PA" in protocol: # Projects: 833922 - EvolPsy
            get_latest_series(AP_epi, s)
        elif "fmap-EPIdist_acq-fmri_dir-AP" in protocol: # Projects: 833922 - EvolPsy
            get_latest_series(PA_epi, s)
        #elif "fmap-ABCD_acq-dMRIdistmap_dir-PA" in s.series_description:
        #    get_latest_series(PA_epi, s)
        #elif "fmap-ABCD_acq-dMRIdistmap_dir-AP" in s.series_description:
        #    get_latest_series(AP_epi, s)
        elif "DistortionMap_AP" in s.series_description: # Projects: 844685 - SSBC and 829502 - MOTIVE
            get_latest_series(AP_epi, s)
        elif "DistortionMap_PA" in s.series_description: # Projects: 844685 - SSBC and 829502 - MOTIVE
            get_latest_series(PA_epi, s)
        elif "epi_singlerep_conte" in s.series_description:
            get_latest_series(???, s) # Accommodates conte 815814. What format is this???
        else:
            continue

    return info

#################################################################################
################     Additional metadata, Fieldmap intention,     ###############
################  Associated sidecars, Rename subject / session  ###############
#################################################################################

################### Hardcode required params in MetadataExtras ##################
##MetadataExtras = {
    # ToDo: If necessary, hardcode missing metadata fields for certain scan types.
    #       (Likely will need to do this if there is ASL data in the project!)

    # example: {
    #    "MetadataField_1": value_1,
    #    "MetadataField_2": value_2,
    #    ...
    #    "MetadataField_N: value_N"
    # }

##}

############ Dictionary mapping fieldmap to scans intended to correct ###########
IntendedFor = {
    gre: [
       'sub-{bblid}/ses-{session}/func/sub-{bblid}_ses-{session}_task-rest_bold',
       'sub-{bblid}/ses-{session}/func/sub-{bblid}_ses-{session}_task-ex_bold',
       'sub-{bblid}/ses-{session}/func/sub-{bblid}_ses-{session}_task-in_bold',
       'sub-{bblid}/ses-{session}/func/sub-{bblid}_ses-{session}_task-er_bold',
       'sub-{bblid}/ses-{session}/perf/sub-{bblid}_ses-{session}_asl',
       'sub-{bblid}/ses-{session}/perf/sub-{bblid}_ses-{session}_m0scan'
    ]
}


####################### Rename session and subject labels #######################
# This function queries Flywheel to generate a dictionary (session_labels) that
# maps the existing session label (sess.label) to a new session label in the
# form: <proj_abbreviation><session_index>.

#def gather_session_indices():
    #import flywheel
    #fw = flywheel.Client()
    #proj = fw.projects.find_first('label="{}"'.format("NSCOR_831353"))
    #subjects = proj.subjects()
    # Initialize session label dictionary where:
    #   Key:    existing session label
    #   Value:  new session label in form <proj_abbreb><session idx>.
    # session_labels = {}
    # Loop through all subjects in Flywheel project
    for s in range(len(subjects)):
        # Get a list of the subject's sessions
        sessions = subjects[s].sessions()
        if sessions:
            # Sort session list by timestamp
            sessions = sorted(sessions, key=lambda x: x.timestamp)
            # Loop through the subject's sessions, assign each session an index
            #for i, sess in enumerate(sessions):
            #    session_labels[sess.label] = "NSCOR" + str(i + 1)
    #return session_labels
    
# This line calls the above function.
##session_labels = gather_session_indices()

# Replace session label with <proj_abbrev><session_idx>
##def ReplaceSession(ses_label):
    ##return str(session_labels[ses_label])

#Replace subject label, e.g. Remove leading "0" from session label
##def ReplaceSubject(label):
    ##return label.lstrip("0")

    
    
    
    
    
    
    
    # Other notes
    
    # Script to convert files to BIDS format

# Pull latest heudiconv version from docker. If docker not set up, follow docker tutorial
docker pull nipy/heudiconv:latest

# Define input and output paths
inputpath = _____
outputpath = ____

# Generate heuristic file 
docker run --rm -it \ # rm means no modifications to container. it means interactive
-v inputpath:/data:ro \ # v means mounting directory. ro = read only. 
-v outputpath:/output \ 
nipy/heudiconv:latest \ # container being run
-d data 

# cd to input folder with all the dicoms we want 
import os
import shutil

def convert_to_bids(input_dir, output_dir, subject_id, session_id, task_name, datatype):
    # Create BIDS directory structure
    bids_subject_dir = os.path.join(output_dir, 'sub-' + subject_id)
    os.makedirs(bids_subject_dir, exist_ok=True)
    
    if session_id:
        bids_session_dir = os.path.join(bids_subject_dir, 'ses-' + session_id)
        os.makedirs(bids_session_dir, exist_ok=True)
    else:
        bids_session_dir = bids_subject_dir
    
    bids_data_dir = os.path.join(bids_session_dir, datatype)
    os.makedirs(bids_data_dir, exist_ok=True)
    
    # Rename and copy files to BIDS format
    for filename in os.listdir(input_dir):
        if filename.startswith(subject_id):
            source_path = os.path.join(input_dir, filename)
            _, ext = os.path.splitext(filename)
            
            bids_filename = f"sub-{subject_id}"
            if session_id:
                bids_filename += f"_ses-{session_id}"
            bids_filename += f"_task-{task_name}_{datatype}{ext}"
            
            bids_file_path = os.path.join(bids_data_dir, bids_filename)
            
            shutil.copy(source_path, bids_file_path)
            print(f"Converted {filename} to {bids_filename}")
    
    print("Conversion to BIDS format complete.")

# Example usage
input_directory = "/path/to/input/data"
output_directory = "/path/to/output/BIDS"
subject = "001"
session = "01"
task = "resting"
data_type = "anat"  # Replace with the actual datatype (e.g., anat, func, dwi, etc.)

convert_to_bids(input_directory, output_directory, subject, session, task, data_type)