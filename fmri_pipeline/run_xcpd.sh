
singularity run -B /project/bbl_roalf_pecsokphd/projects/glucest-rsfmri/:/mnt \
--cleanenv xcp_d-latest.simg \
/mnt/data/fmri/preprocessed/3T \
/mnt/data/fmri/postprocessed/sandbox_3T \
participant  \
--participant_label 94288
