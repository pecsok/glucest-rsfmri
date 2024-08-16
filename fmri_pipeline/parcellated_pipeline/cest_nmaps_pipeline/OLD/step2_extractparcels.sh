#!/bin/bash

#######################################################################################################
## DEFINE PATHS ##

post=$1 # Path to sliced nmaps and atlases in subject space (PREV $post)
outputpath=$2
nmaps=$3 # NMAPS path
case=$4
str=$5 # UNI or INV2

#######################################################################################################
## MAKE DIRS, DEFINE VARS ##

echo "Extracting nmap parcels for: $case"
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

declare -a maps=(
  "mGluR5"
  "NMDA"
  "GABA"
)

# Make output dir if necessary
if ! [ -d $outputpath/$str/nmaps ]; then
  mkdir -p $outputpath/$str/nmaps
fi

if ! [ -d $outputpath/$str/$case/nmaps ]; then
  mkdir -p $outputpath/$str/$case/nmaps
fi
 
#######################################################################################################
## APPLY ATLAS TO NEUROMAP AND EXTRACT DATA ##
   
for map in $maps; do # Loop through nmaps
    echo $map
    
    for atlas_name in "${atlases[@]}"; do # Loop through atlases
      if [ ! -d $outputpath/$str/nmaps/${atlas_name} ]; then
        mkdir $outputpath/$str/nmaps/${atlas_name}
      fi
      touch $outputpath/$str/nmaps/${atlas_name}/all-${map}-${atlas_name}-measures_$str.tsv
      echo "Subject	${atlas_name}_${map}_mean	${atlas_name}_${map}_numvoxels	${atlas_name}_${map}_SD" >> \
      $outputpath/$str/nmaps/${atlas_name}/all-${map}-${atlas_name}-measures_$str.tsv
          
      # quantify nmap value for each participant
      3dROIstats -mask $post/$case/atlases/$str/$case-cest-${atlas_name}.nii.gz \ # input the sliced atlas.
      -zerofill NaN -nomeanout -nzmean -nzsigma -nzvoxels -nobriklab -1DRformat \
      $post/$case/nmaps/$str/${case}-slice-${map}.nii.gz >> $outputpath/$str/$case/nmaps/$case-${map}-ROI-${atlas_name}-measures_$str.tsv
    # format participant-specific csv
      sed -i 's/name/Subject/g' $outputpath/$str/$case/nmaps/$case-${map}-ROI-${atlas_name}-measures_$str.tsv
      cut -f2-3 --complement $outputpath/$str/$case/nmaps/$case-${map}-ROI-${atlas_name}-measures_$str.tsv >> \
        $outputpath/$str/$case/nmaps/tmp.tsv
      mv $outputpath/$str/$case/nmaps/tmp.tsv $outputpath/$str/$case/nmaps/$case-${map}-ROI-${atlas_name}-measures_$str.tsv
    done
done
