import codecademylib3
import pandas as pd

ad_clicks = pd.read_csv('ad_clicks.csv')
# print(ad_clicks.head(10))

most_views = ad_clicks.groupby('utm_source').user_id.count().reset_index()
# print(most_views)

ad_clicks['is_click'] = ~ad_clicks\
   .ad_click_timestamp.isnull()

clicks_by_source = ad_clicks.groupby(['utm_source','is_click']).user_id.count().reset_index()
# print(clicks_by_source)

clicks_pivot = clicks_by_source.pivot(
  columns = 'is_click',
  index = 'utm_source',
  values = 'user_id'
).reset_index()
# print(clicks_pivot)

clicks_pivot['percent_clicked'] = clicks_pivot[True] / (clicks_pivot[True] + clicks_pivot[False])
# print(clicks_pivot)

# Were approximately the same number of people shown both ads? 
# Answer: They were even at 827
exp_grps = ad_clicks.groupby('experimental_group').user_id.count().reset_index()

# Did a greater percentage of users clicked on Ad A or Ad B? 
# Answer: Ad A
click_perc_ab = ad_clicks.groupby(['experimental_group','is_click']).user_id.count().reset_index()
# print(click_perc_ab)

# The Product Manager for the A/B test thinks that the clicks might have changed by day of the week.
a_clicks = ad_clicks[(ad_clicks.experimental_group == 'A') & (ad_clicks.is_click == True)]
a_clicks_per_day = a_clicks.groupby(['is_click','day']).user_id.count().reset_index()
a_clicks_per_day_pivot = a_clicks_per_day.pivot(
    columns = 'is_click',
    index = 'day',
    values = 'user_id'
).reset_index()
a_clicks_per_day_pivot['percent'] = \
  (a_clicks_per_day_pivot[True] / a_clicks_per_day_pivot[True].sum()) * 100
print(a_clicks_per_day_pivot)

b_clicks = ad_clicks[(ad_clicks.experimental_group == 'B') & (ad_clicks.is_click == True)]
b_clicks_per_day = b_clicks.groupby(['is_click','day']).user_id.count().reset_index()
b_clicks_per_day_pivot = b_clicks_per_day.pivot(
    columns = 'is_click',
    index = 'day',
    values = 'user_id'
).reset_index()
b_clicks_per_day_pivot['percent'] = \
  (b_clicks_per_day_pivot[True] / b_clicks_per_day_pivot[True].sum()) * 100
print(b_clicks_per_day_pivot)
