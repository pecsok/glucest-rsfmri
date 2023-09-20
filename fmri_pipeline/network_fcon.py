# network_fcon.py
# This function calculates network-level connectivity metrics for the individual subjects and for all subjects processed so far.

define avg connectivity as list 
def subj_fcon(fcmat, networks_of_interest):
    """
    Calculate average within-network connectivity for specified networks from a correlation matrix.

    Parameters:
    - fcmat (pd.DataFrame): A Pandas DataFrame representing the correlation matrix.
    - networks_of_interest (list): A list of network names to calculate averages for.

    Returns:
    - average_connectivity (dict): A dictionary where keys are network names and values are average connectivity values.
    
    """
    # Initialize a dictionary to store average connectivity for each network
    average_connectivity = []
    # Loop through the networks
    for network in networks_of_interest:
        # Select rows and columns corresponding to the network
        network_indices = [index for index in fcmat.index if network in index]
        network_connectivity = fcmat.loc[network_indices, network_indices]

        # Calculate the average connectivity within the network
        average_connectivity.append(network_connectivity.values.mean())

    return average_connectivity






    # Initialize a dictionary to store average connectivity for each network
    average_connectivity = {network: None for network in networks_of_interest}
    # Loop through the networks
    for network in networks_of_interest:
        # Select rows and columns corresponding to the network
        network_indices = [index for index in fcmat.index if network in index]
        network_connectivity = fcmat.loc[network_indices, network_indices]

        # Calculate the average connectivity within the network
        average_connectivity[network] = network_connectivity.values.mean()

    return average_connectivity
    
def grp_fcon(subj):
    """
    Calculates avg network-level fcon for group

    Parameters
    ----------
    list of fcon matrices for group of subjects
    
    Returns
    -------
    vis : nifti?
        fcon of visual network
    som : nifti?
        fcon of somatomotor network
    dattn : nifti?
        fcon of dorsal attention network
    vattn : nifti?
        fcon of ventral attention network    
    limb : nifti?
        fcon of limbic network
    dmn : nifti?
        fcon of default mode network
    ecn : nifti?
        fcon of executive control network
    sal : nifti?
        fcon of salience network    
                
    """