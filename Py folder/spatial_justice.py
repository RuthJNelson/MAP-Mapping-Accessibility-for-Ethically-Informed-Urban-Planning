import networkx as nx
import pandas as pd

def calculate_reach_centrality(G, source_vertices_list, target_vertices, threshold, Reach, weight_param, threshold2):
    """
    Calculate the Reach Centrality for vertices in a graph based on specific criteria.
    Note you have to create an empty list called Reach before implementing this function

    Parameters:
    G (networkx.Graph): The graph object.
    source_vertices_list (list): List of lists containing source vertices.
    target_vertices (list): List of target vertices.
    threshold (int): Maximum overall time threshold to consider for reach.
    Reach (list): This is the name of an empty list you have created to populate with the Reach values
    weight_param (str or func): this could be a string, which would be the name of the weight value in the graph or it could be a function
    threshold2 (int): Maximum overall walking threshold to consider for reach.
    Prints:
    A number of how long the Reach list is.
    """
    for source_vertices in source_vertices_list:
        # Compute shortest paths and distances once for the source node list
        shortest_distances = nx.multi_source_dijkstra_path_length(G, source_vertices, weight=weight_param)
        shortest_paths = nx.multi_source_dijkstra_path(G, source_vertices, weight=weight_param)

        # Filter targets by distance threshold and if they are actual targets
        reachable_targets = {k: v for k, v in shortest_distances.items() if v <= threshold and k in target_vertices}
        count = 0
        for target, distance in reachable_targets.items():
            path = shortest_paths[target]
                # Calculate total street weight for each path
            street_weight = sum(G[u][v]['time_cost'] for u, v in zip(path[:-1], path[1:]) if G[u][v]['vertex_type'] == 'street')
            # if it is less than the overall threshold count it   
            if street_weight <= threshold2:
                count += 1

        Reach.append(count)
        print(len(Reach))

def normalise(df,columns,new_names):
    """
    This function performs min/max normalisation on specific columns in your dataframe to prepare for calculating Rawl's Reach Centrality

    Parameters:
    df (pandas.DataFrame): dataframe that contains the existing Socio-economic values 
    columns (list): list of the column names to normalise
    new_names (dictionary): dictionary of the original column names and the names you will call the normalised columns i.e. new_names ={income:income_norm}

    Outputs:
    COLUMNS in the dataframe: normalised values in columns with their new names
    """
    n_norm = (df[columns]-df[columns].min())/(df[columns].max()-df[columns].min())
    n_norm = n_norm.rename(columns=new_names)
    norm_columns =  n_norm.columns.tolist()
    df[norm_columns] = n_norm[norm_columns]

def equality(r,df,n):
    """
    This function redistibutes existing Reach distribution of access to opportunities in a city by giving every neighbourhood/spatial unit an equal number of opportunities based on principles of Egalitarianism

    Parameters:
    r (str): name of the column with the existing Reach Centrality Value (i.e. Reach 15min, Reach 30min etc.) you will redistribute
    df (pandas.DataFrame): dataframe that contains the existing Reach Centrality Values
    n (int): number of neighbourhoods/spatial units included in the analysis

    Outputs:
    3 COLUMNS in the dataframe:
    df['ERC'+ r] (float)= Equality Reach Centrality
    df['ERG'+ r] (float)= Equality Reach Gap
    df['Eq'+r] (Boolean)= True if ERG>=0 and False if ERG<0

    Returns:
    Prints(number of neighbourhoods/spatial units with ERG<0;number of neighbourhoods/spatial units with ERG>=0; % neighbourhoods/spatial units with ERG>=0, % neighbourhoods/spatial units with ERG<0)
    """
    sum_reach = df[r].sum()
    equality_reach = (sum_reach/n).round(0) #calculate equality number
    df['ERC'+ r] = equality_reach
    df['ERG'+ r] = df[r] - equality_reach #difference between actual reach and equality reach
    df['Eq'+r] = 'True'#create a column and fill default with true
    df.loc[df['ERG'+ r] < 0, 'Eq'+r] = 'False' #if less than 0 means it did not meet crtieria of equality
    print(df['Eq'+r].value_counts())
    False_eq = df.loc[df['Eq'+r] == 'False'] #seperate those who do not make criteria
    True_eq = df.loc[df['Eq'+r] == 'True'] #seperate those who do  make criteria
    False_p = len(False_eq)*100/n
    True_p = len(True_eq)*100/n
    print('% neighbourhoods/spatial units with ERG>=0:',True_p, '% neighbourhoods/spatial units with ERG<0:',False_p)


def utility(r,df,n,w):
    """
    This function redistibutes existing Reach distribution of access to opportunities in a city by giving every neighbourhood/spatial unit a Reach value proportional to its working population.

    Parameters:
    r (str): name of the column with the existing Reach Centrality Value (i.e. Reach 15min, Reach 30min etc.) you will redistribute
    df(pandas.DataFrame): dataframe that contains the existing Reach Centrality Values
    n (int): number of neighbourhoods/spatial units included in the analysis
    w (str): name of the column with the number of available working population for each neighbourhood/spatial unit

    Outputs:
    3 COLUMNS in the dataframe:
    df['URC'+ r] (float)= Utilitarian Reach Centrality
    df['URG'+ r] (float)= Utilitarian Reach Gap
    df['Ut'+r] (Boolean)= True if UTG>=0 and False if UTG<0

    Returns:
    Prints(number of neighbourhoods/spatial units with URG<0;number of neighbourhoods/spatial units with URG>=0; % neighbourhoods/spatial units with URG>=0, % neighbourhoods/spatial units with URG<0)
    """
    sum_reach = df[r].sum() #the total amount with all the df added together
    sum_population = df[w].sum() #this is population above 18 - thus working pop
    Ratio_equality = sum_reach/sum_population #equal people to location
    df['URC'+ r] = df[w]*Ratio_equality #calculating utilitarian reach
    df['URG'+ r] = df[r] - df['URC'+ r] #calculating difference in actual reach and utilitarian reach
    df['Ut'+ r] = 'True' #creating a column to see if meets criteria and filling with default 'True'
    df.loc[df['URG'+r] < 0, 'Ut'+ r] = 'False' #If the actual reach is less than the utilitarian reach does not meet criteria
    print(df['Ut'+ r].value_counts())
    False_ut = df.loc[df['Ut'+r] == 'False'] #seperate those who do not make criteria
    True_ut = df.loc[df['Ut'+r] == 'True'] #seperate those who do  make criteria
    False_p = len(False_ut)*100/n
    True_p = len(True_ut)*100/n
    print('% neighbourhoods/spatial units with URG>=0:',True_p, '% neighbourhoods/spatial units with URG<0:',False_p)


def vul_score(df, columns):
    """
    Creates a vulnerability score for each neighbourhood/spatial unit

    Parameters:
    df(pandas.DataFrame): The DataFrame to modify.
    columns (list of str): List of column names with normalised vulnerability indicators.

    Outputs:
    df['vul_score']: a column with the vulnerability score of a neighbourhood/spatial unit
    df['vul_prop']: a column with the proportional value of vulnerability a neighbourhood/spatial unit has

    Returns:
    pandas.DataFrame: The DataFrame with an added column for the vulnerability score of the neighbourhood/spatial unit.
    """
    # Check if all columns in columns_to_sum exist in the DataFrame
    for col in columns:
        if col not in df.columns:
            raise ValueError(f"Column '{col}' not found in DataFrame")

    # Sum the specified columns
    df['vul_score'] = 1 - (df[columns].sum(axis=1)/len(columns))
    df['vul_prop']=df['vul_score']/(df['vul_score'].sum())
    
    return df


def rawls(r,df,n):
    """
    This function redistibutes existing Reach distribution of access to opportunities in a city by giving every neighbourhood/spatial unit a Reach value proportional to its vulnerability score.

    Parameters:
    r (str): name of the column with the existing Reach Centrality Value (i.e. Reach 15min, Reach 30min etc.) you will redistribute
    df (dataframe): dataframe that contains the existing Reach Centrality Values
    n (int): number of neighbourhoods/spatial units included in the analysis

    Outputs:
    3 COLUMNS in the dataframe:
    df['RRC'+ r] (float)= Rawls' Reach Centrality
    df['RRG'+ r] (float)= Rawls' Reach Gap
    df['Ra'+r] (Boolean)= True if RTG>=0 and False if UTG<0

    Returns:
    Prints(number of neighbourhoods/spatial units with RRG<0;number of neighbourhoods/spatial units with RRG>=0; % neighbourhoods/spatial units with RRG>=0, % neighbourhoods/spatial units with RRG<0)
    """
    sum_reach = df[r].sum()
    df['RRC'+r]= sum_reach*df['vul_prop'] ## Rawls reach
    df['RRG'+r]= df[r] - df['RRC'+r] #If Rawls dif is less than 0, it does not make the threshold
    df['Ra'+r] = 'True' #create a column to check if meets criteria, default value 'True'
    df.loc[df['RRG'+r] < 0, 'Ra'+r] = 'False'#for where each of the neighbourhoods have a negative value in Rawls dif, Rawls get a 'false' value
    print(df['Ra'+r].value_counts())
    False_r = df.loc[df['Ra'+r] == 'False'] #seperate those who do not make criteria
    True_r = df.loc[df['Ra'+r] == 'True'] #seperate those who do  make criteria
    False_p = len(False_r)*100/n
    True_p = len(True_r)*100/n
    print('% neighbourhoods/spatial units with RRG>=0:',True_p, '% neighbourhoods/spatial units with RRG<0:',False_p)
