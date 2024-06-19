#!/bin/bash

## DEFINE PATHS ##
structural=$1
pre=$2
post=$3
atlas=$4
log=$5
case=$6
method=$7
reso=$8
str=$9

#######################################################################################################
## TRANSFORM NMAP TO SUBJECT SPACE ##

antsApplyTransforms -d 3 -r $structural/$case/${case}-${str}_masked.nii.gz \
  -i $atlas/Schaefer2018/Schaefer2018_100Parcels_17Networks_${reso}mm.nii.gz \
  -n MultiLabel \
  -o $post/$case/atlases/$str/${case}-Schaefer2018-100P-17N.nii.gz \
  -t [$structural/$case/MNI_transforms/${case}-${str}inMNI-0GenericAffine.mat,1] \
  -t $structural/$case/MNI_transforms/${case}-${str}inMNI-1InverseWarp.nii.gz