import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import data_processing as dp
import match_length as ml
import serving_analysis as sa

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

def main():
    '''
    The main function of drawing match length violin plot
    '''
    all_data = dp.read_gslam_files("data/atp_matches*.csv")
    data_other = dp.remove_player(["Roger Federer", "Rafael Nadal", "Novak Djokovic"], all_data, 'winner')
    data_federer = all_data[all_data['winner_name'] == "Roger Federer"].copy()
    data_federer.drop([ 'winner_name' ], axis=1, inplace=True)
    data_nadal = all_data[all_data['winner_name'] == "Rafael Nadal"].copy()
    data_nadal.drop([ 'winner_name' ], axis=1, inplace=True)
    data_djoker = all_data[all_data['winner_name'] == "Novak Djokovic"].copy()
    data_djoker.drop([ 'winner_name' ], axis=1, inplace=True)

    data_federer, _ = sa.player_data("Roger Federer", all_data)
    data_nadal, _ = sa.player_data("Rafael Nadal", all_data)
    data_djoker, _ = sa.player_data("Novak Djokovic", all_data)
    # Fetch winning and losing match length for Roger Federer
    lose_federer, win_federer = ml.player_match_length("Roger Federer", data_other, data_federer)

    # Fetch winning and losing match length for Rafael Nadal
    lose_nadal, win_nadal = ml.player_match_length("Rafael Nadal", data_other, data_nadal)

    # Fetch winning and losing match length for Novak Djokovic
    lose_djoker, win_djoker = ml.player_match_length("Novak Djokovic", data_other, data_djoker)

    # Fetch winning and losing match length for other players
    win_other = data_other[data_other['minutes'] <= 400]
    win_other.insert(0, column = "Result", value = ['Win']*len(win_other))
    win_other.insert(0, column = "Name", value = ["Other"]*len(win_other))
    lose_other = dp.remove_player(["Roger Federer", "Rafael Nadal", "Novak Djokovic"], all_data, 'loser')
    lose_other = lose_other[lose_other['minutes'] <= 400]
    lose_other.insert(0, column = "Result", value = ['Lose']*len(lose_other))
    lose_other.insert(0, column = "Name", value = ["Other"]*len(lose_other))

    violin_data = pd.concat([win_federer, lose_federer, win_nadal, lose_nadal, win_djoker, lose_djoker, win_other, lose_other])
    violin_data = violin_data.rename(columns={"minutes": "Minutes"}, errors="raise")
    sns.set(style="darkgrid")
    sns.violinplot(x="Name", y="Minutes", hue="Result", data=violin_data, palette="Pastel1", split=True).set(title='Match Length of Big 3 and Other Players')
    plt.show()

if __name__ == '__main__':
    main()