import pandas as pd
import os
import plotly.express as px
import plotly.graph_objects as go
import data_processing as dp
import match_length as ml
import serving_analysis as sa
import mental_toughness as mt

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

def match_length_score(ml_diff, smallest_ml, largest_ml):
    '''
    Computes score of match length for a player
    
    Args:
        ml_diff (float): Match length difference for this player
        smallest_ml (float): Smallest match length difference among all players
        largest_ml (float): Largest match length difference among all players

    Returns:
        The match length score of this player as a float
    '''
    assert(isinstance(ml_diff, float))
    assert(isinstance(smallest_ml, float))
    assert(isinstance(largest_ml, float))
    score = 100*(ml_diff - smallest_ml)/(largest_ml - smallest_ml)
    return score

def main():
    '''
    The main function of drawing plots for rising star analysis
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

    data_federer, sum_federer = sa.player_data("Roger Federer", all_data)
    data_nadal, sum_nadal = sa.player_data("Rafael Nadal", all_data)
    data_djoker, sum_djoker = sa.player_data("Novak Djokovic", all_data)


    #rising star match length t Alexander Zverev Dominic Thiem 
    data_zverev, sum_zverev = sa.player_data("Alexander Zverev", all_data)
    data_thiem, sum_thiem = sa.player_data("Dominic Thiem", all_data)
    
    
    lose_federer, win_federer = ml.player_match_length("Roger Federer", data_other, data_federer)

    # Fetch winning and losing match length for Rafael Nadal
    lose_nadal, win_nadal = ml.player_match_length("Rafael Nadal", data_other, data_nadal)

    # Fetch winning and losing match length for Novak Djokovic
    lose_djoker, win_djoker = ml.player_match_length("Novak Djokovic", data_other, data_djoker)
    
    win_other = data_other[data_other['minutes'] <= 400]
    win_other.insert(0, column = "Result", value = ['Win']*len(win_other))
    win_other.insert(0, column = "Name", value = ["Other"]*len(win_other))
    lose_other = dp.remove_player(["Roger Federer", "Rafael Nadal", "Novak Djokovic"], all_data, 'loser')
    lose_other = lose_other[lose_other['minutes'] <= 400]
    lose_other.insert(0, column = "Result", value = ['Lose']*len(lose_other))
    lose_other.insert(0, column = "Name", value = ["Other"]*len(lose_other))
    # Calculate the difference of losing and winning match length for different players
    dif_Federer = match_len_diff(lose_federer, win_federer)
    dif_Nadal = match_len_diff(lose_nadal, win_nadal)
    dif_Djoker = match_len_diff(lose_djoker, win_djoker)
    dif_Other = match_len_diff(lose_other, win_other)

    print(dif_Federer,dif_Nadal,dif_Djoker,dif_Other)
    group_win = all_data.groupby(['winner_name'])
    group_lose = all_data.groupby(['loser_name'])
    dif = []
    for name in group_win.groups.keys():
        player_win = group_win.get_group(name)
        win_length = player_win['minutes'].mean()
        player_lose = group_lose.get_group(name)
        lose_length = player_lose['minutes'].mean()
        dif.append(lose_length - win_length)

    dif.sort(reverse = True)
    dif_Largest = max(dif)
    dif_Least = min(dif)

    # Calculate the scores of match length for different players
    score_Federer_length = match_length_score(dif_Federer, dif_Least, dif_Largest)
    score_Nadal_length = match_length_score(dif_Nadal, dif_Least, dif_Largest)
    score_Djoker_length = match_length_score(dif_Djoker, dif_Least, dif_Largest)
    score_Other_length = match_length_score(dif_Other, dif_Least, dif_Largest)
    
    
    
    # Group the data by winner name and add all the break points
    mental_df = all_data[['winner_name', 'w_bpSaved', 'w_bpFaced']].groupby('winner_name').sum()
    # Add a percentage collumn with the breakpoint percentage
    mental_df['percentage'] = mental_df.apply(lambda x: mt.get_percentage(x['w_bpSaved'], x['w_bpFaced']), axis=1)
    # Add a mental points collumn with the mental point scores
    mt.add_mental_points_col(mental_df, list(mental_df.index), all_data)

    mental_df = mental_df.sort_values('mental_score',ascending=False)
   
    score_Federer_mental = mental_df.loc['Roger Federer','mental_score']
    score_Djoker_mental = mental_df.loc['Novak Djokovic','mental_score']
    score_Nadal_mental = mental_df.loc['Rafael Nadal','mental_score']
    score_Zverev_mental = mental_df.loc['Alexander Zverev','mental_score']
    score_Thiem_mental = mental_df.loc['Dominic Thiem','mental_score']
    mental_df_other = mental_df.drop(['Roger Federer','Novak Djokovic','Rafael Nadal'])
    score_Other_mental = mental_df_other['mental_score'].mean()
    
    categories = ['Serving Skills','Match Length','Mental Toughness','Serving Skills']

    fig = go.Figure()

    ff, fs, fd = sa.serving_data(sum_federer)
    nf, ns, nd = sa.serving_data(sum_nadal)
    df, ds, dd = sa.serving_data(sum_djoker) 
    of, os, od = sa.serving_data(sum_other) 
    tf, ts, td = sa.serving_data(sum_thiem) 
    zf, zs, zd = sa.serving_data(sum_zverev) 
    score_Federer_serving = sa.score_serving(ff,fs,fd)
    score_Nadal_serving = sa.score_serving(nf,ns,nd)
    score_Djoker_serving = sa.score_serving(df,ds,dd)
    score_Other_serving = sa.score_serving(of,os,od)
    score_Zverev_serving = sa.score_serving(zf,zs,zd)
    score_Thiem_serving = sa.score_serving(tf,ts,td)
    fig.add_trace(go.Scatterpolar(
        r=[score_Other_serving, score_Other_length,score_Other_mental,score_Other_serving],
        theta=categories,
        fill=None,
        name='Other player average'
      ))

    fig.update_layout(

        title=dict(
        text="Other player average",
        y=0.95,
        x=0.5,
        xanchor= 'center',
        yanchor= 'top',
        font=dict(size=20)
        ),
    polar=dict(
      radialaxis=dict(
        visible=True,
          range=[0, 100]
      )),
      showlegend=True
  )

    fig.show()
    
    categories = ['Serving Skills','Match Length','Mental Toughness','Serving Skills']

    fig = go.Figure()

    fig.add_trace(go.Scatterpolar(
        r=[score_Federer_serving, score_Federer_length,score_Federer_mental,score_Federer_serving],
        theta=categories,
        fill=None,
        name='Federer'
        ))

    fig.add_trace(go.Scatterpolar(
        r=[score_Djoker_serving, score_Djoker_length,score_Djoker_mental,score_Djoker_serving],
        theta=categories,
        fill=None,
        name='Djokovic'
        ))
    fig.add_trace(go.Scatterpolar(
        r=[score_Nadal_serving, score_Nadal_length,score_Nadal_mental,score_Nadal_serving],
        theta=categories,
        fill=None,
        name='Nadal'
        ))
    fig.update_layout(
        title=dict(
        text="Big 3",
        y=0.95,
        x=0.5,
        xanchor= 'center',
        yanchor= 'top',
        font=dict(size=20)
        ),
    polar=dict(
    radialaxis=dict(
      visible=True,
      range=[50, 100]
    )),
    showlegend=True
  )

    fig.show()
    average_Big3_serving = (score_Federer_serving + score_Nadal_serving + score_Djoker_serving)/3
    average_Big3_length = (score_Federer_length + score_Nadal_length + score_Djoker_length)/3
    average_Big3_mental = (score_Federer_mental + score_Nadal_mental + score_Djoker_mental)/3
    categories = ['Serving Skills','Match Length','Mental Toughness','Serving Skills']

    fig = go.Figure()

    fig.add_trace(go.Scatterpolar(
      r=[average_Big3_serving, average_Big3_length,average_Big3_mental,average_Big3_serving],
      theta=categories,
      fill=None,
      name='Big 3 average'
      ))

    fig.add_trace(go.Scatterpolar(
      r=[score_Other_serving, score_Other_length,score_Other_mental,score_Other_serving],
      theta=categories,
      fill=None,
      name='Other player average'
      ))
    fig.update_layout(
        title=dict(
        text="Big 3 average VS Other player average",
        y=0.95,
        x=0.5,
        xanchor= 'center',
        yanchor= 'top',
        font=dict(size=20)
    ),
    
  polar=dict(
    radialaxis=dict(
      visible=True,
      range=[0, 100]
    )),
      showlegend=True
  )

    fig.show()
    #rising star match length  Alexander Zverev Dominic Thiem 
    lose_zverev, win_zverev = ml.player_match_length("Alexander Zverev", data_other, data_zverev)
    lose_thiem, win_thiem = ml.player_match_length("Dominic Thiem", data_other, data_thiem)

    dif_Zverev = match_len_diff(lose_zverev, win_zverev)
    dif_Thiem = match_len_diff(lose_thiem, win_thiem)

    score_Zverev_length = match_length_score(dif_Zverev, dif_Least, dif_Largest)
    score_Thiem_length = match_length_score(dif_Thiem, dif_Least, dif_Largest)

    print(score_Zverev_length, score_Thiem_length)
    
    categories = ['Serving Skills','Match Length','Mental Toughness','Serving Skills']

    fig = go.Figure()

    fig.add_trace(go.Scatterpolar(
      r=[average_Big3_serving, average_Big3_length,average_Big3_mental,average_Big3_serving],
      theta=categories,
      fill=None,
      name='Big 3 average'
      ))

    fig.add_trace(go.Scatterpolar(
      r=[score_Zverev_serving, score_Zverev_length,score_Zverev_mental,score_Zverev_serving],
      theta=categories,
      fill=None,
      name='Zverev'
      ))
    fig.add_trace(go.Scatterpolar(
      r=[score_Thiem_serving, score_Thiem_length,score_Thiem_mental,score_Thiem_serving],
      theta=categories,
      fill=None,
      name='Thiem'
      ))
    fig.add_trace(go.Scatterpolar(
      r=[score_Other_serving, score_Other_length,score_Other_mental,score_Other_serving],
      theta=categories,
      fill=None,
      name='Other player average',
      marker={'color':'#FFA15A'}
      ))
    fig.update_layout(
    title=dict(
        text="Big 3 average VS Rising Star VS Other player average",
        y=0.95,
        x=0.5,
        xanchor= 'center',
        yanchor= 'top',
        font=dict(size=20)
    ),
    
  polar=dict(
    radialaxis=dict(
      visible=True,
      range=[0, 85]
    )),
  showlegend=True
  )

    fig.show()
    categories = ['Serving Skills','Match Length','Mental Toughness','Serving Skills']

    fig = go.Figure()

    fig.add_trace(go.Scatterpolar(
      r=[score_Federer_serving, score_Federer_length,score_Federer_mental,score_Federer_serving],
      theta=categories,
      fill=None,
      name='Federer'
      ))

    fig.add_trace(go.Scatterpolar(
      r=[score_Djoker_serving, score_Djoker_length,score_Djoker_mental,score_Djoker_serving],
      theta=categories,
      fill=None,
      name='Djokovic'
      
      ))
    fig.add_trace(go.Scatterpolar(
      r=[score_Nadal_serving, score_Nadal_length,score_Nadal_mental,score_Nadal_serving],
      theta=categories,
      fill=None,
      name='Nadal'
      ))

    fig.add_trace(go.Scatterpolar(
      r=[score_Zverev_serving, score_Zverev_length,score_Zverev_mental,score_Zverev_serving],
      theta=categories,
      fill=None,
      name='Zverev',
      marker={'color':'#7F7F7F'}
      ))
    fig.add_trace(go.Scatterpolar(
      r=[score_Thiem_serving, score_Thiem_length,score_Thiem_mental,score_Thiem_serving],
      theta=categories,
      fill=None,
      name='Thiem'
      ))

    fig.update_layout(
        title=dict(
        text="Big 3 VS Rising Star",
        y=0.95,
        x=0.5,
        xanchor= 'center',
        yanchor= 'top',
        font=dict(size=20)
    ),
  
  polar=dict(
    radialaxis=dict(
      visible=True,
      range=[0,100]
    )),
  showlegend=True
  )

    fig.show()
    ranking_data = dp.read_ranking_files("data/atp_rankings*.csv")
    ranking_data
    '''
    100644 Alexander Zverev
    106233 Dominic Thiem
    103819 Federer
    104745 Nadal
    104925 Djokovic
    '''
    ranking = ranking_data[(ranking_data['player'].isin([100644,106233,103819,104745,104925]))]
    ranking = ranking.sort_values(by=['ranking_date'])
    ranking['ranking_date'] = pd.to_datetime(ranking['ranking_date'], format='%Y%m%d')
    ranking = ranking.replace(100644,'Zverev')
    ranking = ranking.replace(106233,'Thiem')
    ranking = ranking.replace(103819,'Federer')
    ranking = ranking.replace(104745,'Nadal')
    ranking = ranking.replace(104925,'Djokovic')
    fig = px.line(ranking, x="ranking_date", y="rank", color="player")
 
    fig.update_yaxes(autorange="reversed")
    fig.update_layout(
    title=dict(
        text="Big 3 VS Rising Star Ranking",
        y=0.95,
        x=0.5,
        xanchor= 'center',
        yanchor= 'top',
        font=dict(size=20)
    ),
    )
    fig.show()

if __name__ == '__main__':
    main()