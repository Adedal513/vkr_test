import pandas as pd
from utils import query_db

def get_main_metrics():
    kpi_total_preds = query_db('select sum(cnt) as totals from class_stats')['totals'].iloc[0]
    kpi_passed_moderation = query_db("select sum(cnt) as totals from class_stats where class='non-toxic'")['totals'].iloc[0]
    return kpi_total_preds, kpi_passed_moderation, kpi_total_preds - kpi_passed_moderation

def get_ts_df():
    time_series = query_db('select created_at, class as category, cnt from time_series;')
    time_series['created_at'] = time_series['created_at'].apply(lambda x: x.date())
    return time_series

def get_day_stats():
    day_stats = query_db('select * from day_stats;')
    return day_stats

def get_product_category_stats():
    cat_stats = query_db('select product_category, amount, class as pred from product_category_stats;')
    return cat_stats