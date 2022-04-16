import pandas as pd
from pyecharts import options as opts
from pyecharts.charts import Timeline, Map
from pyecharts.globals import ThemeType
from pyecharts.datasets import register_url

register_url("https://echarts-maps.github.io/echarts-countries-js/")

dataset = pd.read_csv('sentiment_result.csv', lineterminator='\n')
#print(dataset['country'].value_counts())



us_tweet = dataset.loc[dataset['country'].str.contains('United States', na=False)]
df_Sep = us_tweet.loc[us_tweet['date'].str.contains('2021/9', na=False)]
#print(df_Sep['date'].head())
df_Oct = us_tweet.loc[us_tweet['date'].str.contains('2021/10', na=False)]
#print(df_Oct['date'].head())
df_Nov = us_tweet.loc[us_tweet['date'].str.contains('2021/11', na=False)]
#print(df_Nov['date'].head())
df_Jan = us_tweet.loc[us_tweet['date'].str.contains('2022/1', na=False)]
#print(df_Jan['predict_label'].head())

df_list = [df_Sep, df_Oct, df_Nov, df_Jan]

def map_tl() -> Timeline:
    timeline = Timeline(init_opts=opts.InitOpts(page_title='tweet sentiment map',
                                          theme=ThemeType.INFOGRAPHIC,
                                          width='1500px',
                                          height='800px'),
                  )

    month_list = ['September', 'October', 'November', 'January']

    for i in range(len(df_list)):
        state_series = df_list[i]['state'].value_counts()
        #print(len(state_series))
        state_list = []
        percentage_list = []
        for j in range(len(state_series)):
            state_name = state_series.index[j]
            state_list.append(state_name)
            df_state = df_list[i].loc[df_list[i]['state'].str.contains(state_name, na=False)]
            #print(df_state['predict_label'].value_counts())
            #print(df_state.shape[0])
            df_label0 = df_state.loc[df_state['predict_label'] == '0']
            df_label1 = df_state.loc[df_state['predict_label'] == '1']
            df_label2 = df_state.loc[df_state['predict_label'] == '2']
            if (df_label0.shape[0] + df_label1.shape[0] + df_label2.shape[0]) != 0:
                percentage = df_label0.shape[0] / (df_label0.shape[0] + df_label1.shape[0] + df_label2.shape[0])
            else:
                percentage = 0
            percentage_list.append(percentage)

        state_data_pair = zip(state_list, percentage_list)

        vi_map = (
            Map(init_opts=opts.InitOpts(width='1200px',
                                        height='700px',
                                        bg_color=None))
            .add(series_name='negative sentiment tweet percentage',
                 data_pair=[list(x) for x in state_data_pair],
                 maptype='美国',
                 is_map_symbol_show=False)
            .set_global_opts(
                title_opts=opts.TitleOpts(title='tweet sentiment map',
                                          subtitle=month_list[i],
                                          ),
                visualmap_opts=opts.VisualMapOpts(is_piecewise=True,
                                                  range_text=['high', 'low'],
                                                  pieces=[
                                                      {'min': 0.5, 'color': '#2a3058', 'label': '>50%'},
                                                      {'min': 0.4, 'max': 0.5, 'color': '#295886', 'label': '40%-50%'},
                                                      {'min': 0.3, 'max': 0.4, 'color': '#1983b0', 'label': '30%-40%'},
                                                      {'min': 0.2, 'max': 0.3, 'color': '#0cb1d1', 'label': '20%-30%'},
                                                      {'max': 0.2, 'color': '#3ddfe9', 'label': '<20%'},
                                                  ]),
            )
        )
        timeline.add(vi_map, month_list[i])
        timeline.add_schema(is_timeline_show=True,
                      play_interval=5000,
                      symbol=None,
                      is_loop_play=True
                      )
    return timeline


map_tl().render()
