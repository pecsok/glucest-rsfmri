#!/bin/bash

#This script calculates average nmap value for each parcel of data within the GluCEST slice

#######################################################################################################
## DEFINE PATHS ##

post=$1 # Path to sliced nmaps and atlases in subject space (PREV $post)
outputpath=$2
nmaps=$3 # NMAPS path
str=$4 # UNI or INV2

#######################################################################################################
## MAKE DIRS, DEFINE VARS ##

# Define array of atlases
declare -a atlases=(
  "Schaefer2018_1000Parcels_17Networks"
)

#  "Schaefer2018_100Parcels_17Networks"
#  "Schaefer2018_100Parcels_7Networks"
#  "Schaefer2018_400Parcels_17Networks"
#  "Schaefer2018_400Parcels_7Networks"
#  "HarvardOxford-cort-maxprob-thr25"
#  "HarvardOxford-sub-maxprob-thr25"
#  "destrieux2009_rois"
#  "Schaefer2018_1000Parcels_7Networks"


# Make output dir if necessary
if ! [ -d $outputpath/$str ]; then
  mkdir $outputpath/$str
fi


#######################################################################################################
## APPLY ATLAS TO NEUROMAP AND EXTRACT DATA ##

for i in $(ls $post); do # Loop through subjects
    case=${i##*/}
    echo "CASE: $case"
    mkdir $outputpath/$str/nmaps
    mkdir $outputpath/$str/$case/nmaps
    
    for nmap in nmaps; do # Loop through nmaps
        nmap_name="${nmap##*/}"
        
        for atlas_name in "${atlases[@]}"; do # Loop through atlases
          if [ ! -d $outputpath/$str/nmaps/${atlas_name} ]; then
            mkdir $outputpath/$str/${atlas_name}
          fi
          touch $outputpath/$str/nmaps/${atlas_name}/all-${nmap_name}-${atlas_name}-measures_$str.tsv
          echo "Subject	${atlas_name}_${nmap_name}_mean	${atlas_name}_${nmap_name}_numvoxels	${atlas_name}_${nmap_name}_SD" >> \
          $outputpath/$str/nmaps/${atlas_name}/all-${nmap_name}-${atlas_name}-measures_$str.tsv
              
          # quantify nmap value for each participant
          3dROIstats -mask $post/$case/atlases/$str/$case-cest-${atlas_name}.nii.gz \ # input the sliced atlas.
          -zerofill NaN -nomeanout -nzmean -nzsigma -nzvoxels -nobriklab -1DRformat \
          $post/$case/nmaps/$str/${case}-${nmap_name}.nii.gz >> $outputpath/$str/$case/nmaps/$case-${nmap_name}-ROI-${atlas_name}-measures_$str.tsv
        # format participant-specific csv
          sed -i 's/name/Subject/g' $outputpath/$str/$case/nmaps/$case-${nmap_name}-ROI-${atlas_name}-measures_$str.tsv
          cut -f2-3 --complement $outputpath/$str/$case/nmaps/$case-${nmap_name}-ROI-${atlas_name}-measures_$str.tsv >> \
            $outputpath/$str/$case/nmaps/tmp.tsv
          mv $outputpath/$str/$case/nmaps/tmp.tsv $outputpath/$str/$case/nmaps/$case-${nmap_name}-ROI-${atlas_name}-measures_$str.tsv
 





    