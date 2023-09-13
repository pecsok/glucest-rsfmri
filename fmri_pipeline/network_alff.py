# --------------------------------------------------------------------------------------
# 4. Hub measures FIX Rework this to fit project 

# 4A
if step4_hubs:

    # a constant (already used for infomap, can't be changed) # Fix huh?
    thresholds = np.arange(0.01,0.11,0.01)
    
    # 1. Discuss infomap approach
    # Infomap: http://www.mapequation.org/code.html
    #    Rosvall & Bergstrom (2008). Maps of information flow reveal
    #    community structure in complex networks. PNAS, 105, 1118
    # 2. Discuss other approaches to network definition
    # 3. Discuss parameters that must be set
    
    # Start with a set of thresholded correlation matrices and network assignments for each threshold
    # [In the interest of time/ease, I am pre-computing network assignments and providing them here]
    # mat file has key = 'clrs' that lists network assignment across thresholds
    Group_infomapcomm = spio.loadmat(datadir + 'Allsubavg_333parcels_infomapassn.mat')

    # Compute hub measures - degree, PC, and WD - in the group across different thresholds
    # See formula from Guimera & Amaral (2005). Functional Cartography of Complex Metabolic
    #    Networks. Nature, 433, 895-900
    #     http://www.nature.com/nature/journal/v433/n7028/full/nature03288.html?foxtrotcallback=true
    # Practice writing code on your own for this [?]
    group_pc = np.empty((nrois,thresholds.size))
    group_wd = np.empty((nrois,thresholds.size))
    group_degree = np.empty((nrois,thresholds.size))
    for t in range(thresholds.size):
        adj_mat,adj_mat_sym = gfns.threshold_matrix_density(groupmat,thresholds[t]) # get a thresholded matrix
        [group_pc[:,t], group_wd[:,t], group_degree[:,t]] = gfns.hub_metrics(adj_mat_sym,Group_infomapcomm['clrs'][:,t])

    fig = gfns.figure_hubs(Parcel_params,thresholds,group_degree,group_wd,group_pc)
    fig.savefig(outdir + 'Hubmeasures_group.pdf')
    
    
    # 4B - IF TIME
if step4_hubs:

    # [If time], do this across subjects
    for sub in range(nsubs):
        subnum = 'MSC%02d' % (sub+1)
        sub_infomapcomm = spio.loadmat(datadir + subnum + '_333parcels_infomapassn.mat')

        sub_pc = np.empty((nrois,thresholds.size))
        sub_wd = np.empty((nrois,thresholds.size))
        sub_degree = np.empty((nrois,thresholds.size))
        for t in range(thresholds.size):
            adj_mat,adj_mat_sym = gfns.threshold_matrix_density(subavgmat[sub],thresholds[t]) # get a thresholded matrix
            [sub_pc[:,t], sub_wd[:,t], sub_degree[:,t]] = gfns.hub_metrics(adj_mat_sym,sub_infomapcomm['clrs'][:,t])

        fig = gfns.figure_hubs(Parcel_params,thresholds,sub_degree,sub_wd,sub_pc)
        fig.savefig(outdir + 'Hubmeasures_' + subnum + '.pdf')
    plt.close('all')
    # Discuss challenges of making hub measures per subject
    # See: Gordon, E, et al. (2018) "Three distinct sets of connector hubs integrate human brain function."
    #     Cell reports 24.7: 1687-1695.

    # [If time] Make a spring embedded plot, colored by hub measures rather than networks
    # Start with group and favorite threshold. Do other versions if time.
    t = 2;
    pc_hub_colors = gfns.hub_colormap(group_pc[:,t])
    node_data = gfns.make_gephi_node_inputfile(Parcel_params,nod_colors=pc_hub_colors)
    node_data.to_csv(outdir + 'Groupmat_gephi_nodedata_PC.csv',index=False)

    wd_hub_colors = gfns.hub_colormap(group_wd[:,t])
    node_data = gfns.make_gephi_node_inputfile(Parcel_params,nod_colors=wd_hub_colors)
    node_data.to_csv(outdir + 'Groupmat_gephi_nodedata_WD.csv',index=False)

    deg_hub_colors = gfns.hub_colormap(group_degree[:,t])
    node_data = gfns.make_gephi_node_inputfile(Parcel_params,nod_colors=deg_hub_colors)
    node_data.to_csv(outdir + 'Groupmat_gephi_nodedata_degree.csv',index=False)

    # For more work on hubs and their importance in brain function, in addition to the references above, see:
    # Gratton, C., et al., (2012). Focal brain lesions to critical locations cause widespread disruption of the
    #   modular organization of the brain. Journal of Cognitive Neuroscience, 24 (6), 1275-1285
    # Power, J.D. et al. (2013). Evidence for hubs in human functional brain networks. Neuron, 79 (4), 798-813
    # Warren, D.E., et al. (2014). Network measures predict neuropsychological outcome after brain injury. PNAS, 111 (39), 14247-14252

    # The following packages contain tools for graph theoretical analyses:
    # Brain Connectivity Toolbox (Sporns, Matlab/Python/C++): https://sites.google.com/site/bctnet/
    # NetworkX (Python): https://networkx.github.io/ 
    #   see also brainx extension: https://github.com/nipy/brainx