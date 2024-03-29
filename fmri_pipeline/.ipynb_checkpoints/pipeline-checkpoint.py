### Import packages
import os
import numpy as np
import pandas as pd
import network_fcon as fc
from scipy.stats import pearsonr

### Define paths and variables
# Main folder path
subjs = "subject_list.csv"
input_path = "xcp_d" 
output_path = "analyses"
# Initialize empty lists and vars Fix make object-oriented?
bblids = []
sesids = []
fcmats = []
# Choose what to analyse
networks_of_interest = ["SalVentAttn", "Default"] 
CNB_scores_of_interest = ["matrix", "verbal"]
clinical_scores_of_interest = ["BDI", "PROMIS-Anx"]
# Make dataframe based on metrics of interest
columns = ["BBLID"] + ["Session"] + networks_of_interest + CNB_scores_of_interest + clinical_scores_of_interest
grp_df = pd.DataFrame(columns=columns)

### INPUTS: 
## If source folder
## If Fcon
## If ALFF 
## If CNB data - probably CSV
## If Clinical data - probably CSV

###############################################################################
# Import data, loop through subjects, and establish file paths
# Add an if loop: If looping through folders, loop through folders. Else if only want to run one subj or use csv of subjs, hard-code subject and session ID
if folder_input:
    for subj_path in os.listdir(input_path):
        # Extract bblid and session id FIX how to extract session:
        bblid = subj_path.split('-')[1]
        # Assuming 'session' is the name of the daughter folder 
        # FIX These lines are definitely buggy
        daughter_folder = os.path.join(input_path, subj_path, 'session') 
        ses = daughter_folder.split('-')[1]
        subj_path = subj_path.append(daughter) # full path to session
        # Add to running list of bblids for grp analysis later:
        bblids.append(bblid)
        sesids.append(ses)
elif csv_input:
    for n in range(len(subjs)): # input csv of bblids and session ids
        # Construct the file path for the subject file FIX Make this correct
        bblid = subjs['subj'][n]
        ses = subjs['session'][n]
        subj_path = f"{input_path}/sub-{bblid}/ses-{ses}"
        # Add to running list of bblids for grp analysis later:
        bblids.append(bblid)
        sesids.append(ses)
        
###############################################################################
##### Network FCON: Call fcon function and calculate network-level connectivity measures for subject and whole group
    ### FIX Add IF statement: If FCON=TRUE so I only run this step if I want to
    # Import connectivity matrix 
    path_to_fcmat = f"{subj_path}/func/*Schaefer717_measure-pearsoncorrelation_conmat.tsv"
    fcmat = pd.read_csv(path_to_fcmat, sep='\t')
    # Add to 3D matrix for group analysis later
    fcmats = pd.concat([fcmats, fcmat], axis=2)

    # Call fcon function to compute network-level fcon for networks of interest
    avg_fcon = subj_fcon(correlation_matrix, networks_of_interest) 
    # Store output in dataframe for later group analyses
    
    
    # Fix. if OOP: Subj.fcmat = fc.subj_fcon(fmat)?
     
###############################################################################
##### Network ALFF: Call alff function and calculate network-level and node-specific alff measures for subject and whole group

for n in range(len(subjs)): # input csv of bblids and session ids
    # Construct the file path for the subject file FIX Make this correct
    bblid = subjs['subj'][n]
    ses = subjs['session'][n]
    fcmat = f"{reho_path}/sub-{bblid}_ses-{ses}_schaefer100x17_ts.1D" # FIx path
    if os.path.exists(file_path):  # if file exists
        # Compile subject files into a list
        subj_data = pd.read_table(file_path, header=None)
        df_name = f"{bblid}_fcon"
        globals()[df_name] = subj_data
        fcon_list.append(subj_data)
        n_fcon += 1

        
###############################################################################
##### CNB analysis

# Load CNB scores spreadsheet into a DataFrame
cnb_data = pd.read_excel('cnb_scores.xlsx')

# Create empty lists to store subject-specific correlation coefficients
correlation_coefficients = []

# Loop through subjects
# Loop through networks of interest
# Loop through CNB scores of interest
for subject_id, salventattn_values in avg_fcon.items():
    # Extract BDI score for the current subject (assuming a column named 'BDI')
    bdi_score = clinical_scores_df.loc[clinical_scores_df['Subject ID'] == bblid, 'BDI'].values[0]
    
    # Calculate the correlation between SalVentAttn and BDI scores
    correlation_coef, _ = pearsonr(salventattn_values, bdi_score)
    
    # Append the correlation coefficient to the list
    correlation_coefficients.append(correlation_coef)

# Calculate group-level summary statistics
mean_correlation = np.mean(correlation_coefficients)
std_deviation = np.std(correlation_coefficients)

# Print or visualize the group-level results
print(f"Mean Correlation: {mean_correlation:.4f}")
print(f"Standard Deviation: {std_deviation:.4f}")






########## OLD Code: 
# Make correlation matrices and store in list
# This is a comprehension that creates a new list more concisely
# General format: output_list = [output_exp for var in input_list if (var satisfies this condition)]
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
