import pandas as pd

def player_data(player, all_data):
    '''
    Fetch the data that certain player won and calculate the sum of data
    
    Args:
        player (str): name of a player
        all_data (pd.DataFrame): data of all matches

    Returns:
        The data that player won as a dataframe, and sum of data in pandas series format
    '''
    assert(isinstance(player, str))
    assert(isinstance(all_data, pd.DataFrame))
    data_player = all_data[all_data['winner_name'] == player]
    sum_player = data_player.sum()
    return data_player, sum_player

def player_group_data(all_data, entry):
    '''
    Group the data by given entry and sort the data
    
    Args:
        all_data (pd.DataFrame): data of all matches
        entry (str): the entry used to group the data

    Returns:
        Grouped and sorted data in dataframe format
    '''
    assert(isinstance(entry, str))
    assert(isinstance(all_data, pd.DataFrame))
    group_data = all_data[['winner_name', entry]].groupby('winner_name').sum()
    group_data = pd.DataFrame(group_data)
    group_data.sort_values(entry, ascending = False)
    return group_data

def serving_data(player_data):
    '''
    Calculate the number of different servings given the data of a player
    
    Args:
        player_data (pd.Series): data of a player

    Returns:
        Number of first serve, second serve and double faults in float
    '''
    assert(isinstance(player_data, pd.Series))
    data_f = player_data.w_1stWon + player_data.l_1stWon
    data_s = player_data.w_2ndWon + player_data.l_2ndWon
    data_d = player_data.w_df + player_data.l_df
    return data_f, data_s, data_d

def score_serving(i,j,k):
    '''
    Calculate the serving score of a player given the serving data
    
    Args:
        i (float): Number of first serve
        j (float): Number of second serve
        k (float): Number of doubel faults
    Returns:
        Serving score in float
    '''
    assert(isinstance(i, float))
    assert(isinstance(j, float))
    assert(isinstance(k, float))
    score = i/(i+j+k)+0.75*j/(i+j+k)-2*k/(i+j+k)
    return 100*score

def serve_percentage(data):
    '''
    Calculate the percentage of aces and double faults given the data of a player
    
    Args:
        data (pd.Series): data of a player

    Returns:
        Percentages of aces and double faults
    '''
    assert(isinstance(data, pd.Series))
    df_percentage = data.w_df/(data.w_1stWon+data.w_2ndWon+data.w_df)*100
    ace_percentage = data.w_ace/(data.w_1stWon+data.w_2ndWon+data.w_df)*100
    return [df_percentage, ace_percentage]