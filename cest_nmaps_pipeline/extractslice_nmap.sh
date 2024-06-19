#!/bin/bash

## DEFINE PATHS ##
structural=$1
outpath=$2
case=$3
nmap=$4

#######################################################################################################
## TRANSFORM NMAP TO SUBJECT SPACE ##


antsApplyTransforms -d 3 -r $structural/$case/${case}-UNI_masked.nii.gz \
  -i $nmap \
  -n MultiLabel \
  -o $outpath/$case \
  -t [$structural/$case/MNI_transforms/${case}-UNIinMNI-0GenericAffine.mat,1] \
  -t $structural/$case/MNI_transforms/${case}-UNIinMNI-1InverseWarp.nii.gz

  
