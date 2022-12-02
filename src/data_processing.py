import pandas as pd
import os
import glob

def read_csv_files(files):
    '''
    Read certain files that matches the given file name to a dataframe
    
    Args:
        files (str): all the files that matches the string will be read

    Returns:
        The dataframe contains all data from read CSV files
    '''
    assert(isinstance(files, str))
    path = os.getcwd()
    csv_files = glob.glob(os.path.join(path, files))
    all_data = pd.DataFrame()
    for f in csv_files:
        df = pd.read_csv(f)
        all_data = pd.concat([all_data, df])
    return all_data

def read_gslam_files(csv_files):
    '''
    Read and process the grand slam data for future data analysis
    
    Args:
        csv_files (str): all the files that matches the string will be read

    Returns:
        The dataframe contains the grand slam data for future data analysis
    '''
    assert(isinstance(csv_files, str))
    all_data = read_csv_files(csv_files)
    # Only take matches that are Grand Slams (G)
    all_data = all_data[all_data["tourney_level"] == "G"]

    # Reset the Index
    all_data.reset_index(inplace=True)

    # Drop Unused Collumns
    collumns_to_drop = [
        'tourney_id', 'tourney_date', 'index', 'draw_size', 'match_num', 
        'winner_id', 'winner_seed', 'winner_entry', 'winner_hand', 'winner_ht', 
        'winner_ioc', 'winner_age', 'loser_id', 'loser_seed', 'loser_entry', 
        'loser_hand', 'loser_ht', 'loser_ioc', 'loser_age', 'w_SvGms',
        'l_SvGms', 'winner_rank', 'winner_rank_points', 'loser_rank', 'loser_rank_points'
        ]

    all_data.drop(collumns_to_drop, axis=1, inplace=True)

    # Drop Rows with Na as values
    all_data.dropna(inplace=True)
    return all_data

def read_ranking_files(ranking_csv):
    '''
    Read and process the ranking data for future data analysis
    
    Args:
        ranking_csv (str): all the files that matches the string will be read

    Returns:
        The dataframe contains the ranking data for future data analysis
    '''
    assert(isinstance(ranking_csv, str))
    ranking_data = read_csv_files(ranking_csv)
    return ranking_data

def remove_player(player_list, data, status):
    '''
    Remove the data of lost or won matches of given players
    
    Args:
        player_list (list(str)): the list of givn players
        data (pd.DataFrame): data of all matches
        status (str): indicates whether the won or lost games to be remove

    Returns:
        The dataframe contains the remaining data
    '''
    assert(isinstance(player_list, list))
    assert(isinstance(data, pd.DataFrame))
    assert(isinstance(status, str))
    data_other  = data.copy()
    for player in player_list:
        data_other = data_other[~eval('data_other.'+status+'_name.str.contains(\''+player+'\')')]
    return data_other