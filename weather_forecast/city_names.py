import pandas

city_data_df = pandas.read_excel('weather_forecast\static\cities_list.xlsx', sheet_name='cities_list')

def get_city_name():
    return city_data_df['name'].tolist()