#!/bin/bash

#export SINGULARITYENV_FS_LICENSE=/mnt/images/license.txt

subjs="19790 20180 90077 90281 92211 93292 93734 96659 97994 102041 105979 106057 106880 116019 119791 121085 125511 132641 89095 121407 19830 19981 80557"
for subject in ${subjs}
do

project=/project/bbl_roalf_pecsokphd/projects/glucest-rsfmri

SIF=${project}/images/fmriprep_21.0.1.sif

echo $SIF
singularity run --cleanenv \
        -B ${project} \
        ${SIF} \
        /project/bbl_roalf_pecsokphd/projects/glucest-rsfmri/data/fmri/fw_data/7T/7T_${subject} /project/bbl_roalf_pecsokphd/projects/glucest-rsfmri/data/fmri/preprocessed/7T participant \
        --participant-label sub-${subject} \
        --fs-license-file /project/bbl_roalf_pecsokphd/projects/glucest-rsfmri/images/license.txt \
        --work-dir /project/bbl_roalf_pecsokphd/projects/glucest-rsfmri/tmp \
        --stop-on-first-crash \
	--fs-no-reconall \

done
