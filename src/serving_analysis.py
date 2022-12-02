import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import data_processing as dp
import serving_analysis as sa

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

def main():
    '''
    The main function of drawing plots for serving analysis
    '''
    all_data = dp.read_gslam_files("data/atp_matches*.csv")
    data_other = dp.remove_player(["Roger Federer", "Rafael Nadal", "Novak Djokovic"], all_data, 'winner')
    sum_other = data_other.sum()
    data_federer = all_data[all_data['winner_name'] == "Roger Federer"].copy()
    data_federer.drop([ 'winner_name' ], axis=1, inplace=True)
    data_nadal = all_data[all_data['winner_name'] == "Rafael Nadal"].copy()
    data_nadal.drop([ 'winner_name' ], axis=1, inplace=True)
    data_djoker = all_data[all_data['winner_name'] == "Novak Djokovic"].copy()
    data_djoker.drop([ 'winner_name' ], axis=1, inplace=True)

    data_federer, sum_federer = player_data("Roger Federer", all_data)
    data_nadal, sum_nadal = player_data("Rafael Nadal", all_data)
    data_djoker, sum_djoker = player_data("Novak Djokovic", all_data)

    # Counting number of ace point played by every winning player
    ace_winner = player_group_data(all_data, 'w_ace')
    # Counting number of firstserve played by every winning player
    firstserve_winner = player_group_data(all_data, 'w_1stWon')
    # Counting number of secondserve played by every winning player
    secondserve_winner = player_group_data(all_data, 'w_2ndWon')
    # Counting number of double faults by every player
    df_winner = all_data[['winner_name', 'w_df']].groupby('winner_name').sum()
    df_winner = pd.DataFrame(df_winner)
    df_winner.head()
    # Data
    r = [0,1,2,3]
    ff, fs, fd = serving_data(sum_federer)
    nf, ns, nd = serving_data(sum_nadal)
    df, ds, dd = serving_data(sum_djoker) 
    of, os, od = serving_data(sum_other) 

    raw_data = {'greenBars': [ff, nf, df, of], 'orangeBars': [fs, ns, ds,os], 'blueBars': [fd, nd, dd, od]}
    df = pd.DataFrame(raw_data)
 
    # From raw value to percentage
    totals = [i+j+k for i,j,k in zip(df['greenBars'], df['orangeBars'], df['blueBars'])]
    greenBars = [i / j * 100 for i,j in zip(df['greenBars'], totals)]
    orangeBars = [i / j * 100 for i,j in zip(df['orangeBars'], totals)]
    blueBars = [i / j * 100 for i,j in zip(df['blueBars'], totals)]
    # plot
    barWidth = 0.85
    names = ('Federer','Nadal','Djokovic','Others')
    # Create green Bars
    plt.bar(r, greenBars, color='#b5ffb9', edgecolor='white', width=barWidth, label="First serve win")
    # Create orange Bars
    plt.bar(r, orangeBars, bottom=greenBars, color='#f9bc86', edgecolor='white', width=barWidth, label="Second serve win")
    # Create blue Bars
    plt.bar(r, blueBars, bottom=[i+j for i,j in zip(greenBars, orangeBars)], color='#a3acff', edgecolor='white', width=barWidth, label="Double fault")

    # Custom x axis
    plt.xticks(r, names)
    plt.xlabel("Name")
    plt.ylabel("Percent of all serves")
    plt.title("Serve proportion")
    # Add a legend
    plt.legend(loc='upper left', bbox_to_anchor=(1,1), ncol=1)
 
    # Show graphic
    plt.show()

    fig, axis = plt.subplots(figsize=(15,10))
    # Grid lines, Xticks, Xlabel, Ylabel

    axis.yaxis.grid(True)
    axis.xaxis.grid(True)
    axis.set_title('Correlation between ace and double fault',fontsize=25, pad=25.0)
    axis.set_xlabel('Double faults per Serve Point(%)',fontsize=20, labelpad= 25.0)
    axis.set_ylabel('Aces per Serve Point(%)',fontsize=20, labelpad=25.0)

    ace_data = (ace_winner['w_ace']).values.reshape(-1, 1)
    df_data = (df_winner['w_df']).values.reshape(-1, 1)
    firstserve_win = firstserve_winner['w_1stWon'].values.reshape(-1, 1)
    secondserve_win = secondserve_winner['w_2ndWon'].values.reshape(-1, 1)
    X = df_data/(firstserve_win+secondserve_win+df_data)*100
    Y = ace_data/(firstserve_win+secondserve_win+df_data)*100

    linear_regressor_one = LinearRegression()  # create object for the class
    linear_regressor_one.fit(X, Y)  # perform linear regression
    Y_pred = linear_regressor_one.predict(X)  # make predictions


    plt.plot(X, Y_pred, color='red')
    plt.xticks(fontsize=15)
    plt.yticks(fontsize=15)

    axis.scatter(X, Y)
    plt.scatter (*sa.serve_percentage(sum_federer), s=200, marker = 's', color='r', label = 'Roger Federer')
    plt.scatter (*sa.serve_percentage(sum_nadal), s=200, marker = 's', color='g', label = 'Novak Djokovic')
    plt.scatter (*sa.serve_percentage(sum_djoker), s=200, marker = 's', color='y', label = 'Rafael Nadal')
    plt.legend(prop={'size': 20})

    plt.show()

if __name__ == '__main__':
    main()