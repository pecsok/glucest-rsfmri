#!/bin/bash

#export SINGULARITYENV_FS_LICENSE=/project/bbl_roalf_pecsokphd/projects/glucest-rsfmri/images/license.txt
#export SINGULARITYENV_SURFER_SIDEDOOR=1

#subjs="114738 83068"
subjs="96465 20916"

for subject in ${subjs}
do

#project=/project/bbl_roalf_pecsokphd/projects/glucest-rsfmri

#SIF=${project}/images/fmriprep_21.0.1.sif

#echo $SIF

singularity run -B /project/bbl_roalf_pecsokphd/projects/glucest-rsfmri/:/mnt \
        --cleanenv fmriprep_21.0.1.sif \
        #--env /mnt/SURFER_SIDEDOOR=1
        /project/bbl_roalf_pecsokphd/projects/glucest-rsfmri/data/fmri/fw_data/3T/3T_${subject} /project/bbl_roalf_pecsokphd/projects/glucest-rsfmri/data/fmri/sandbox/preprocessed/3T participant \
        --participant-label sub-${subject} \
        --fs-license-file license.txt \
        --work-dir /mnt/tmp \
        --stop-on-first-crash \
        #--SURFER_SIDEDOOR=1 \
        --cifti-output \

done

