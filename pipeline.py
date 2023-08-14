### Import packages
import os
import numpy as np
import pandas as pd
from scipy.stats import pearsonr

### Define paths and variables
# Main folder path
input_path = "xcp_d" 
output_path = "analyses"
# Initialize empty lists and vars 
bblids = []


# Loop through subjects for first-past analysis
for subj_path in os.listdir(input_path):
  # Extract numerical part of folder name
  bblid = subj_path.split('-')[1]
  subject_ids.append(bblid)


for n in range(len(subjs)):
    # Construct the file path for the subject file
    bblid = subjs['subj'][n]
    ses = subjs['session'][n]
    file_path = f"{reho_path}/sub-{bblid}_ses-{ses}_schaefer100x17_ts.1D"
    if os.path.exists(file_path):  # if file exists
        # Compile subject files into a list
        subj_data = pd.read_table(file_path, header=None)
        df_name = f"{bblid}_fcon"
        globals()[df_name] = subj_data
        fcon_list.append(subj_data)
        n_fcon += 1

# Make correlation matrices and store in list
fcon_list = [df for df in [sub_106057_fcon, sub_125511_fcon, sub_19981_fcon, sub_90077_fcon, sub_90281_fcon, sub_92211_fcon, sub_97994_fcon]]

cor_list = []
for i in range(len(fcon_list)):
    subj_matrix = fcon_list[i]
    subj_cor = np.corrcoef(subj_matrix, rowvar=False)
    cor_list.append(subj_cor)

# Convert the list of matrices to a 3D array
array_3d = np.array(cor_list)
array_3d = array_3d.transpose((1, 2, 0))

## Extract average within-network correlation values for each network
# Define rows containing network-specific information
dmn = list(range(37, 48))
ecn = list(range(30, 36))
sn = list(range(20, 26))

fcon_results = pd.DataFrame(columns=["dmn_dmn_mean", "dmn_dmn_sterr", "ecn_ecn_mean", "ecn_ecn_sterr", "ecn_dmn_mean", "ecn_dmn_sterr"])

for i in range(6):
    # Extract values for DMN-DMN 
    dmn_dmn_mean = np.mean(array_3d[dmn, dmn, i])
    dmn_dmn_sterr = np.var(array_3d[dmn, dmn, i])
    ecn_ecn_mean = np.mean(array_3d[ecn, ecn, i])
    ecn_ecn_sterr = np.std(array_3d[ecn, ecn, i]) / np.sqrt(len(ecn))
    ecn_dmn_mean = np.mean(array_3d[ecn, dmn, i])
    ecn_dmn_sterr = np.std(array_3d[ecn, dmn, i]) / np.sqrt(len(dmn))
    
    fcon_results.loc[i] = [dmn_dmn_mean, dmn_dmn_sterr, ecn_ecn_mean, ecn_ecn_sterr, ecn_dmn_mean, ecn_dmn_sterr]

# Create an empty DataFrame with the desired column names
output_df = pd.DataFrame(columns=["bblids", "dmn_dmn_mean", "dmn_dmn_std"])
