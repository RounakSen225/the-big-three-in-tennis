
import pandas as pd

def match_len_diff(lose_data, win_data):
    '''
    Computes difference between losing and winning matchlength of a player
    
    Args:
        lose_data (pd.DataFrame): dataframe contains the winning matches of a player
        win_data (pd.DataFrame): dataframe contains the losing matches of a player

    Returns:
        Average difference between losing and winning match length as a float
    '''
    assert(isinstance(lose_data, pd.DataFrame))
    assert(isinstance(win_data, pd.DataFrame))
    average_lose = lose_data["minutes"].mean()
    average_win = win_data["minutes"].mean()
    return average_lose - average_win

def match_length_score(i, j, k):
    '''
    Computes score of match length for a player
    
    Args:
        i (float): Match length difference for this player
        j (float): Smallest match length difference among all players
        k (float): Largest match length difference among all players

    Returns:
        The match length score of this player as a float
    '''
    assert(isinstance(i, float))
    assert(isinstance(j, float))
    assert(isinstance(k, float))
    score = 100*(i - j)/(k - j)
    return score
