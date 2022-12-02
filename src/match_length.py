import pandas as pd

def player_match_length(player, data_other, data_player):
    '''
    Fetch the matches that a player won and lost to two dataframes
    
    Args:
        player (str): name of a player
        data_other (pd.DataFrame): data of players other than the big three
        data_player (pd.DataFrame): data winning matches of the player

    Returns:
        On dataframe of the lost matches of the player, and oneof the won matches of the player
    '''
    assert(isinstance(player, str))
    assert(isinstance(data_other, pd.DataFrame))
    assert(isinstance(data_player, pd.DataFrame))
    lose_player = data_other[data_other.loser_name.str.contains(player)]
    lose_player.insert(0, column = "Result", value = ['Lose']*len(lose_player))
    lose_player.insert(0, column = "Name", value = [player]*len(lose_player))
    win_player = data_player.copy()
    win_player.insert(0, column = "Result", value = ['Win']*len(win_player))
    win_player.insert(0, column = "Name", value = [player]*len(win_player))
    return lose_player, win_player