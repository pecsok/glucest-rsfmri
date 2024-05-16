#!/bin/bash

for i in {1..100}
do
parcel=$i
#lower = i
# Threshold atlas to include one parcel and name that parcel by its number
parcelmask="$path/3d-s100_17_${i}_mask.nii.gz"
fslmaths $path/Schaefer2018_100Parcels_17Networks_order_FSLMNI152_1mm.nii.gz -thr ${parcel} -uthr ${parcel} ${parcelmask}
# Binarize mask
fslmaths ${parcelmask} -bin ${parcelmask}
done

