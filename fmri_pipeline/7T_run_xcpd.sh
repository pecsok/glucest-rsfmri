singularity run -B /project/bbl_roalf_pecsokphd/projects/glucest-rsfmri/:/mnt \
--cleanenv xcp_d-latest.simg \
/mnt/data/fmri/preprocessed/7T \
/mnt/data/fmri/postprocessed/7T \
participant  \
--participant_label 20645 20642 20011 20543 112126 139272 93274 92155 90877 88608 87225
