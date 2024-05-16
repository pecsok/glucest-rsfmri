#!/bin/bash

#export SINGULARITYENV_FS_LICENSE=/mnt/images/license.txt

subjs="100522 112126 118864"

for subject in ${subjs}
do

project=/project/bbl_roalf_pecsokphd/projects/glucest-rsfmri

SIF=${project}/images/fmriprep_21.0.1.sif

echo $SIF
singularity run --cleanenv \  
        -B ${project} \
        ${SIF} \
        /project/bbl_roalf_pecsokphd/projects/glucest-rsfmri/data/fmri/fw_data/3T/3T_${subject} /project/bbl_roalf_pecsokphd/projects/glucest-rsfmri/data/fmri/preprocessed/cifti/3T participant \
        --env SURFER_SIDEDOOR=1 \
        --participant-label sub-${subject} \
        --env FS_LICENSE=/project/bbl_roalf_pecsokphd/projects/glucest-rsfmri/images/license.txt \
        --fs-license-file /project/bbl_roalf_pecsokphd/projects/glucest-rsfmri/images/license.txt \
        --work-dir /project/bbl_roalf_pecsokphd/projects/glucest-rsfmri/tmp \
        --stop-on-first-crash \
	#--fs-no-reconall \
	--cifti-output \

done
