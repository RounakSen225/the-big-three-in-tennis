import matplotlib.pyplot as plt
import matplotlib
import pandas as pd
import data_processing as dp
import serving_analysis as sa
import mental_toughness as mt

def get_percentage(bpS, bpF):
    '''
    Computes the percentage with the given values.
    
    Args:
        bpS (float): break points saved
        bpF (float): break points faced

    Returns:
        The percentage as a float
    '''
    assert(isinstance(bpS, float))
    assert(isinstance(bpF, float))
    if bpF == 0:
        return 0
    else:
        return round((float(bpS) / float(bpF)), 4) * 100


def add_mental_points_col(df, names, all_data):
    '''
    Computes mental points of each score and adds it into another collumn.
    
    Args:
        df (pd.DataFrame): The data frame with the tennis data (to add mental points data)
        names (list(str)): The list of names of all tennis players
        all_data (pd.DataFrame): The data frame with all data

    Returns:
        The new dataframe.
    '''
    assert(isinstance(df, pd.DataFrame))
    assert(isinstance(names, list))
    assert(isinstance(all_data, pd.DataFrame))
    # Add the new collumn
    df["mental_score"] = 0

    # Iterate through all the names
    for name in names:
        # Get the data of that name
        data_name = all_data[all_data['winner_name'] == name]
        mental_score = 0

        # For every match score, comput the mental score
        for _, row in data_name.iterrows():
            score = row['score']
            
            mental_score = int(mental_score + 0.5*score.count("7-"))

            if score.count('-') == 5:
                mental_score = mental_score + 2
            
            if score.rsplit("-",1).pop() == "6":
                mental_score = mental_score + 4
        
                
        # Add the mental score
        df.loc[[name],['mental_score']] = mental_score
    

def annotate_plot(ax, df, names, colors):
    '''
    Annotate the given plot and label the names from the given dataframe.
    
    Args:
        ax (matplotlib.axes.Axes): The axis of the plot
        df (pd.DataFrame): The data
        names (list(str)): The list of names of all tennis players to annotate
        colors (list(str)): The lost of colors used in the plot
    '''
    assert(isinstance(ax, matplotlib.axes.Axes))
    assert(isinstance(df, pd.DataFrame))
    assert(isinstance(names, list))
    assert(isinstance(colors, list))
    for name, colour in zip(names, colors):
        plt.scatter(int(df.loc[[name], ["mental_score"]].values[0]), int(df.loc[[name], ["percentage"]].values[0]), s=100, marker='s', color=colour, label=name)

def main():
    '''
    The main function of drawing plots for mental toughness analysis
    '''
    all_data = dp.read_gslam_files("data/atp_matches*.csv")
    data_federer = all_data[all_data['winner_name'] == "Roger Federer"].copy()
    data_federer.drop([ 'winner_name' ], axis=1, inplace=True)
    data_nadal = all_data[all_data['winner_name'] == "Rafael Nadal"].copy()
    data_nadal.drop([ 'winner_name' ], axis=1, inplace=True)
    data_djoker = all_data[all_data['winner_name'] == "Novak Djokovic"].copy()
    data_djoker.drop([ 'winner_name' ], axis=1, inplace=True)

    data_federer, _ = sa.player_data("Roger Federer", all_data)
    data_nadal, _ = sa.player_data("Rafael Nadal", all_data)
    data_djoker, _ = sa.player_data("Novak Djokovic", all_data)

    # Group the data by winner name and add all the break points
    mental_df = all_data[['winner_name', 'w_bpSaved', 'w_bpFaced']].groupby('winner_name').sum()

    # Add a percentage collumn with the breakpoint percentage
    mental_df['percentage'] = mental_df.apply(lambda x: mt.get_percentage(x['w_bpSaved'], x['w_bpFaced']), axis=1)

    # Add a mental points collumn with the mental point scores
    mt.add_mental_points_col(mental_df, list(mental_df.index), all_data)

    # Plot the scatterplot
    fig, ax = plt.subplots(figsize=(8,6))
    ax.scatter(mental_df['mental_score'], mental_df['percentage'], s=20)
    ax.set_title("Break Point Win Percentage vs. Mental Point Score")
    ax.set_xlabel('Mental Point Score')
    ax.set_ylabel('Break Point Win Percentage')
    mt.annotate_plot(ax, mental_df, ["Roger Federer", "Novak Djokovic", "Rafael Nadal"], ["r", "g", "y"])

    plt.legend(prop={'size': 15})

    plt.show()

    mental_df = mental_df.sort_values('mental_score',ascending=False)
    
    pd.set_option('display.max_rows',525)
    mental_df.head(30)

if __name__ == '__main__':
    main()