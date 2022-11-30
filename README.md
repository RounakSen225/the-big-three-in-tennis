THE BIG THREE IN TENNIS

Introduction

How are the Big Three (Roger Federer, Rafael Nadal, Novak Djokovic) in tennis dominant in ATP rankings against other players for the past 2 decades? What specific part of their gameplay allows them to keep on winning against other players?

Dataset

Data: https://github.com/JeffSackmann/tennis_atp

The dataset we will be using has been collected by Jeff Sackmann / Tennis Abstract, and is licensed under a Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License.
The data contains information such as winner, loser, break points won, surface, aces, etc for every ATP match leading as far back as 1968. It also has ATP world rankings. However, we will only be using data from 2000 and onwards, as that is when tennis was really modernized and popularized.

Proposed Solution

We have visualized stats of the big three and compared them with other tennis players. We have then focused on the performance of the big three by using diverse types of graphs, including relational plots for the surface and win rates, distribution plots for the winner and loser rank points, and regression plots for color palettes for nationalities and heights. We have used NumPy and Sklearn to perform data analysis. The results will are visualized using Matplotlib and seaborn. For continuous data, we have used regression analysis to check the impact of the factors collected from data and for categorical data we have evaluated the correlation between those factors and the players’ performances.

