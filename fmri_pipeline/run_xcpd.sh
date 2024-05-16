
singularity run -B /project/bbl_roalf_pecsokphd/projects/glucest-rsfmri/:/mnt \
--cleanenv xcp_d-latest.simg \
/mnt/data/fmri/preprocessed/3T \
/mnt/data/fmri/postprocessed/3T \
participant  \
--participant_label 20902 93242 20754 127065 \
