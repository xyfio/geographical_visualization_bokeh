import os.path
import geopandas as gpd
import pandas as pd
import json

from bokeh.io import output_notebook, show, output_file
from bokeh.plotting import figure
from bokeh.models import GeoJSONDataSource, LinearColorMapper, ColorBar, CustomJS
from bokeh.palettes import brewer
from bokeh.io import curdoc, output_notebook
from bokeh.models import Slider, HoverTool
from bokeh.layouts import widgetbox, row, column

BASE_PATH = '/Users/fiona/Desktop/learn/machine_learning'

world_map = os.path.join(BASE_PATH, 'data/ne_110m_admin_0_countries/ne_110m_admin_0_countries.shp')
geo_df = gpd.read_file(world_map)[['ADMIN', 'ADM0_A3', 'geometry']]
geo_df.columns = ['country', 'country_code', 'geometry']
geo_df = geo_df.drop(geo_df.index[159])

datafile = 'data/COVID-19-geographic-disbtribution-worldwide-2020-04-08.csv'
df = pd.read_csv(datafile)[['month','cases','deaths','countryterritoryCode']]
df_month = df.groupby(['month','countryterritoryCode']).sum().reset_index(inplace=False,drop=False)
df_month.loc[df_month['month'] == 12, 'alpha_month'] = 'Dec_2019'
df_month.loc[df_month['month'] == 1, 'alpha_month'] = 'Jan_2020'
df_month.loc[df_month['month'] == 2, 'alpha_month'] = 'Feb_2020'
df_month.loc[df_month['month'] == 3, 'alpha_month'] = 'Mar_2020'
df_month.loc[df_month['month'] == 4, 'alpha_month'] = 'Apr_2020'

# Define function that returns json_data for month selected by user
def json_data(selectedMonth):
    mth = selectedMonth
    df_mth = df_month[df_month['alpha_month'] == mth]
    merged = geo_df.merge(df_mth, left_on='country_code', right_on='countryterritoryCode', how='left')
    merged.fillna('No data', inplace=True)
    merged_json = json.loads(merged.to_json())
    json_data_output = json.dumps(merged_json)
    return json_data_output

geosource = GeoJSONDataSource(geojson = json_data(4))

palette = brewer['RdYlGn'][8]
color_mapper = LinearColorMapper(palette = palette, low = 0, high = 40, nan_color = '#d9d9d9')
tick_labels = {'0': '10', '5': '50', '10':'100', '15':'500', '20':'1000', '25':'2000', '30':'3000','35':'5000', '40': '>10000'}
hover = HoverTool(tooltips = [ ('Country/region','@country'),('no of cases', '@cases'),('no of death', '@deaths')])
color_bar = ColorBar(color_mapper=color_mapper, label_standoff=8,width = 500, height = 20,
                     border_line_color=None,location = (0,0), orientation = 'horizontal', major_label_overrides = tick_labels)

p = figure(title = 'Number of Covid cases across the globe, Apr_2020', plot_height = 600 , plot_width = 1300, toolbar_location = None, tools = [hover])
p.xgrid.grid_line_color = None
p.ygrid.grid_line_color = None
p.patches('xs','ys', source = geosource, fill_color = {'field' :'cases', 'transform' : color_mapper},
          line_color = 'black', line_width = 0.25, fill_alpha = 1)
p.add_layout(color_bar, 'below')

    
def update_plot(attr, old, new):
    dt_dict = {1:'Jan_2020', 2: 'Feb_2020', 3:'Mar_2020', 4: 'Apr_2020', 12: 'Dec_2019'}
    num_mth = slider.value
    mth = dt_dict.get(num_mth)
    new_data = json_data(mth)
    geosource.geojson = new_data
    p.title.text = 'Number of Covid cases across the globe: {}'.format(mth)

# Make a slider object: slider
slider = Slider(title='Month', start=1, end=12, step=1, value=12)
slider.on_change('value', update_plot)
layout = column(p, widgetbox(slider))
curdoc().add_root(layout)

show(layout)
