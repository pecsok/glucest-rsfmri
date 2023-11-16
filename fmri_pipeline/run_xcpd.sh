
singularity run -B /project/bbl_roalf_pecsokphd/projects/glucest-rsfmri/:/mnt \
--cleanenv xcp_d-latest.simg \
/mnt/data/fmri/preprocessed/3T \
/mnt/data/fmri/postprocessed/3T \
participant  \
--participant_label 20303 19494 21874 88760
# 111720 115783 116354 125073 102041 19981 20011 85743 93274 94276 98831 120217 132179
