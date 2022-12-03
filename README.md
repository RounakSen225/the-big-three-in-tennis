# Group 12 ECE 143 Project - The Big three in tennis

## Project Overview

How are the Big Three (Roger Federer, Rafael Nadal, Novak Djokovic) in tennis dominant in ATP rankings against other players for the past 2 decades? What specific part of their gameplay allows them to keep on winning against other players?

We have visualized stats of the big three and compared them with other tennis players. We have then focused on the performance of the big three by using diverse types of graphs, including relational plots for the surface and win rates, distribution plots for the winner and loser rank points, and regression plots for color palettes for nationalities and heights. We have used NumPy and Sklearn to perform data analysis. The results will are visualized using Matplotlib and seaborn. For continuous data, we have used regression analysis to check the impact of the factors collected from data and for categorical data we have evaluated the correlation between those factors and the players’ performances.

## Project file structure

### Datasets

The `data/` folder contains the dataset which has been collected by Jeff Sackmann / Tennis Abstract, and is licensed under a Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License.
The data contains information such as winner, loser, break points won, surface, aces, etc for every ATP match leading as far back as 1968. It also has ATP world rankings. However, we will only be using data from 2000 and onwards, as that is when tennis was really modernized and popularized.
Dataset link: [Link to source](https://github.com/JeffSackmann/tennis_atp)

### Source Code

Source code for all data scraping and data analysis files are within the `src/` folder. [Link to Folder](src/)

Pre-Processing file:

- [data_preprocessing.py](src/data_preprocessing.py) - Return a class object to load any dataset as a d_frame.

Data analysis and visualization related files:

- [match_length.py](src/match_length.py) - Obtains basic batsman stats from the data.
- [mental_toughness.py](src/mental_toughness.py) - Collates player statistics to plot graphs.
- [sanky_chart.py](src/sanky_chart.py) - Calculate teams W:L ratio and total auction spending per year and plot their graph.
- [rising_star.py](src/rising_star.py) - Extracts bowler statistics for the given bowler
- [serving_analysis.py](src/serving_analysis.py) - Extracts information about bowlers given a match and innings

### Jupyter Notebook

The [Jupyter Notebook](project.ipynb) has all the plotting code. All analyzed data is stored as one cell for easy reproducibility.

### Graphs

The [`Graphs`](pics/) folder has images as `.png` of all the analysis plots computed.

## Third Party Modules

The third party modules used are as listed below. They are included as [`requirements.txt`](requirements.txt).

- ipython==8.7.0
- matplotlib==3.5.2
- pandas==1.4.4
- plotly==5.9.0
- scikit_learn==1.1.3
- seaborn==0.12.1

## How to run the code

Install all required libraries -

```
pip install -r requirements.txt
```
Data Cleaning -

```
src % data_processing.py
```

Source Code for analysis -

- Run any python files from within `src/` folder

```
src % match_length.py
```

Jupyter Notebook -

- Run compete notebook or particular cells of [`project.ipynb`](project.ipynb) for viewing the plots.

## Presentation

Final Presentation - [Link to Presentation](presentation_group12.pdf)