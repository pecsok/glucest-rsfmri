#!/bin/bash

#export SINGULARITYENV_FS_LICENSE=/mnt/images/license.txt

#subjs="114738 83068"
subjs="22744"

for subject in ${subjs}
do

project=/project/bbl_roalf_pecsokphd/projects/glucest-rsfmri

SIF=${project}/images/fmriprep_21.0.1.sif

echo $SIF
singularity run --cleanenv \
        -B ${project} \
        -env SURFER_FRONTDOOR=1
        ${SIF} \
        /project/bbl_roalf_pecsokphd/projects/glucest-rsfmri/data/fmri/fw_data/3T/3T_${subject} /project/bbl_roalf_pecsokphd/projects/glucest-rsfmri/data/fmri/sandbox/preprocessed/3T participant \
        --participant-label sub-${subject} \
        --fs-license-file /project/bbl_roalf_pecsokphd/projects/glucest-rsfmri/images/license.txt \
        --work-dir /project/bbl_roalf_pecsokphd/projects/glucest-rsfmri/tmp \
        --stop-on-first-crash \
        --cifti-output \

done
