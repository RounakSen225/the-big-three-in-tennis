# Group 12 ECE 143 Project - The Big three in tennis

## Project Overview

How are the Big Three (Roger Federer, Rafael Nadal, Novak Djokovic) in tennis dominant in ATP rankings against other players for the past 2 decades? What specific part of their gameplay allows them to keep on winning against other players?

We have visualized stats of the big three and compared them with other tennis players. We have then focused on the performance of the big three in certain categories by using diverse types of graphs. We have used NumPy and Sklearn to perform data analysis. The results are visualized using Matplotlib and seaborn. Finally, based on the most impactful categories, we have predicted a rising star(s) and compared his stats with the big three.

## Project file structure

### Datasets

The `data/` folder contains the dataset which has been collected by Jeff Sackmann / Tennis Abstract, and is licensed under a Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License.
The data contains information such as winner, loser, break points won, surface, aces, etc for every ATP match leading as far back as 1968. It also has ATP world rankings. However, we will only be using data from 2003 and onwards, as that is when tennis was really modernized and popularized.
Dataset link: [Link to source](https://github.com/JeffSackmann/tennis_atp)

### Source Code

Source code for all data scraping and data analysis files are within the `src/` folder. [Link to Folder](src/)

Data Processing file: [data_processing.py](src/data_processing.py) 
- Returns a dataframe with cleaned up data, i.e, unneccesary columns and rows without invalid data are removed
- Reads and processes the ranking data for future data analysis
- Removes the data of lost or won matches of given players

Data analysis and visualization related files:


- [sanky_chart.py](src/sanky_chart.py) - Generates a visualization to emphasize dominance of big 3
- [match_length.py](src/match_length.py) - Compares winning and losing match lengths among big 3 and other tennis players
- [serving_analysis.py](src/serving_analysis.py) - Compares aces, first & second serve and double fault stats among big 3 and other tennis players
- [mental_toughness.py](src/mental_toughness.py) - Calculates and compares mental toughness using break points
- [rising_star.py](src/rising_star.py) - Analyzes exisiting data to predict rising star(s) and compares his stats with big 3

### Jupyter Notebook

The [Jupyter Notebook](project.ipynb) has all the code for the data analysis.

### Graphs

The [`pics`](pics/) folder has images as `.png` of all the plots.

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

- Run [`project.ipynb`](project.ipynb) for viewing the plots.

## Presentation

Presentation - [Link to Presentation](presentation_group12.pdf)
