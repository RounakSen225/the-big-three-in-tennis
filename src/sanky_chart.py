import pandas as pd

def sanky_chart_data(sanky_data):
    '''
    Computes data and layout information for the sanky chart
    
    Args:
        sanky_data (pd.DataFrame): Sanky data in dataframe format

    Returns:
        Sanky data in dictionary format and layout of the sanky chart
    '''
    assert(isinstance(sanky_data, pd.DataFrame))
    # First, we get a list of all of sources, remove duplicates, and make this a list
    sources = sanky_data['total_grand_slams'].drop_duplicates().tolist()
    
    # Then, we get a list of all of platforms (our targets), remove duplicates, and make this a list
    platforms = sanky_data['winner_name'].drop_duplicates().tolist()
    
    # Finally, create a list of all our nodes. We will use this for giving an id to each node for plot.ly
    all_nodes = sources + platforms
    
    # Keeping the size of our dataframes, this would be useful for applying the same color for each "node" and "link" of our sankey diagram, if we so choose to do so
    n = len(all_nodes)
    n2 = len(sanky_data['total_grand_slams'])
    
    # Create a dataframe that has all of the node ids. We will join this to the original data frame to reference later
    df1 = pd.DataFrame(all_nodes, columns = ['node'])
    df1 = df1.reset_index()
    df2 = pd.merge(pd.merge(sanky_data, df1, how = 'inner', left_on = "total_grand_slams", right_on ="node"), df1, how = 'inner', left_on = "winner_name", right_on ="node", suffixes = ('_source','_target'))
    # Setting up the data in the plotly "data" argument.
    # The nodes are described in the "node" dictionary (these are the vertical rectangles in the diagram)
    # The links are described in the "link" dictionary. These have 3 attributes, the "source" (the index of the node they start at), the "target" (the index of the node they end at), and the "value" the thickness of the band. Additional attributes, such as color can also be specified.
    data = dict(
        type='sankey',
        node = dict(
        pad = 15,
        thickness = 20,
        line = dict(
            color = "#435951",
            width = 0.5
        ),
        label = all_nodes,
        color = ["#84baa6"] * n
        ),
        link = dict(
        source = df2["index_source"],
        target = df2["index_target"],
        value = df2["size"],
        color = ['#bdf9e5'] * n2
    ))
    
    # Setting up the layout settings in the "layout" argument
    layout =  dict(
        title = dict(
            text = 'Distribution of Grand Slam match winners (top 20)',
            y = 0.95,
            x = 0.5,
            xanchor = 'center',
            yanchor = 'top',
            font = dict(
            size = 20
            )
        )
    )
    return data, layout