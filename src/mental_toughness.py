import matplotlib.pyplot as plt
import matplotlib
import pandas as pd

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