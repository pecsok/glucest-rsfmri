#!/bin/bash

path=$1

#for i in {1..100} #schaefer atlas
for i in {1..75} #Destrieux2009 atlas
do
parcel=$i
#lower = i
# Threshold atlas to include one parcel and name that parcel by its number

parcelmask="$path/destrieux2009_rois_${i}_mask.nii.gz"
fslmaths $path/destrieux2009_rois.nii.gz -thr ${parcel} -uthr ${parcel} ${parcelmask}
fslmaths ${parcelmask} -bin ${parcelmask}
done

#parcelmask="$path/3d-s100_7_${i}_mask.nii.gz"
#fslmaths $path/Schaefer2018_100Parcels_7Networks_order_FSLMNI152_1mm.nii.gz -thr ${parcel} -uthr ${parcel} ${parcelmask}
# Binarize mask
#fslmaths ${parcelmask} -bin ${parcelmask}
#done

