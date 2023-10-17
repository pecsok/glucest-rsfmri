#!/bin/bash

#export SINGULARITYENV_FS_LICENSE=/mnt/images/license.txt

subjs="20011 80557 83835 85743 90077 90281 121407 17621 132641 106880 119791"
for subject in ${subjs}
do

project=/project/bbl_roalf_pecsokphd/projects/glucest-rsfmri

SIF=${project}/images/fmriprep_21.0.1.sif

echo $SIF
singularity run --cleanenv \
        -B ${project} \
        ${SIF} \
        /project/bbl_roalf_pecsokphd/projects/glucest-rsfmri/data/fmri/fw_data/3T/3T_${subject} /project/bbl_roalf_pecsokphd/projects/glucest-rsfmri/data/fmri/preprocessed/3T participant \
        --participant-label sub-${subject} \
        --fs-license-file /project/bbl_roalf_pecsokphd/projects/glucest-rsfmri/images/license.txt \
        --work-dir /project/bbl_roalf_pecsokphd/projects/glucest-rsfmri/tmp \
        --stop-on-first-crash \
	--fs-no-reconall \

done
