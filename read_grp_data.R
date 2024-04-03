read_grp_data <- function(fieldstrength,dataset) {
  ## Inputs: 
  ##         fieldstrength (3T or 7T)
  ##         dataset (grp_df_ or diag_df_)
  ## Actions:
  ##         Concat filenames and read in dataframes
  ## Outputs: 
  ##         Dataframe from desired fieldstrength dataset
  
  grp_path <- paste0('./fmri_pipeline/', fieldstrength, '.csv')
  diag_path <- paste0('./fmri_pipeline/diag_df_', fieldstrength, '.csv')
  grp_data <- read.csv(grp_path)
  diag_data <- read.csv(diag_path)
  return(grp_data)
}
