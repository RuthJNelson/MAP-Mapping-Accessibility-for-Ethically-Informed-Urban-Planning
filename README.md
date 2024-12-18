## MAP: Mapping Accessibility for Ethically Informed Urban Planning

DOI:10.5281/zenodo.14500637

<img width="379" alt="image" src="https://github.com/user-attachments/assets/b51c1773-f2e5-4070-8598-51964433f790" />

This Software Package contains the Python Notebooks associated with Nelson, Warnier and Verma’s paper, "Ethically informed urban planning: measuring distributive spatial justice for neighbourhood accessibility", 2024 (forthcoming). This software package corresponds to the Methodology as documented in their paper. It allows for:

- The creation of an urban network model, which links transport, streets and land use in one large graph
- The calculation of Neighbourhood Reach Centrality, a cumulative accessibility metric
- The calculation of three metrics of Spatial Justice

There are four folders in this Repository:

1. Metadata

This contains relevant Metadata for the project for each case study, which pertains to data structure and sources of data, as well as purposes of different notebooks. A description of the files are below:

**Data Dictionary.xlxs:**
This excel file contains data dictionarues of the variables that are included in the shape file which contains the nodes and the edges for the final Neighbourhood Reach Centrality calculations. It explains what each of the variables means as well as the format it is in, i.e. string, float etc.It also contains data dictionaries for the structure of each data set which would be required, specifically referencing the sample data sets of Cape Town, which can be downloaded from: https://data.4tu.nl/datasets/c34ff74b-30ce-4ed2-9e45-1910ca3e3470

**Notebook descriptions.xlxs:**
This excel file contains a list of all example notebooks and their descriptions

2. Notebooks

This contains the Notebooks for each case study which are in 3 sub-folders, with the processes visualised in Figure 2.

<img width="453" alt="image" src="https://github.com/user-attachments/assets/ab24da37-8ed1-42df-b79f-eb6679cf5d51" />

Figure 2: Processes followed by each notebook folder.

**Graph Preparation:**
This is a folder which contains jupyter notebooks which have code for preparing the Urban Network Model. Refer to the Notebook descriptions in the Metadata for a description of each notebook.

**Reach Calculations:**
This is a folder which contains a jupyter notebook which has code for calculating Neighbourhood Reach Centrality.

**Spatial Justice Calculations:**
This contains a jupyter notebook which has code for calculating the Spatial Justice Metrics.
To calculate the Spatial Justice metrics the Neighbourhood Reach Centrality for each neighbourhood needs to be known.

3.Py_folder

This contains the py file with the Reach and Spatial Justice functions, to be imported into the notebooks.

4. Libraries

This contains the list of Python libraries which need to be installed prior to running this software package.



