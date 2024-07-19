# network_fcon.py
# This function calculates network-level connectivity metrics for the individual subjects and for all subjects processed so far.
# Import Packages
import pandas as pd
import glob


# define avg connectivity as list 
def subj_fcon(ses_path, subj, ses, grp_df, networks_of_interest):
    """
    Calculate average within-network connectivity for specified networks from a correlation matrix.

    Parameters:
    - ses_path (pd.DataFrame): A Pandas DataFrame representing the correlation matrix.
    - networks_of_interest (list): A list of network names to calculate averages for.

    Returns:
    - updated grp_df    
    """
 #   import pandas as pd
    
    fcmat_glob = f"{ses_path}/func/*Schaefer717_measure-pearsoncorrelation_conmat.tsv"
    fcmat = pandas.read_csv(glob.glob(fcmat_glob)[0], sep='\t') # read in fcmat
    fcmat.set_index('Node', inplace = True)
    # Loop through the networks
    for network in networks:
        # Select rows and columns corresponding to the network
        network_fc = fcmat.loc[fcmat.index.str.contains(network), fcmat.columns[fcmat.columns.str.contains(network)]]
        # Calculate avg network fc and add value to proper column in grp_df
        grp_df.loc[len(grp_df)-1, network] = network_fc.values.mean()
        
    return(grp_df)
    
        ##### Troubleshooting: Add to 3D matrix for group analysis later FIX.
        #####fcmats = df
        #####fcmats = pd.concat([fcmats, fcmat], level='Matrix')
        #####fcmats.shape