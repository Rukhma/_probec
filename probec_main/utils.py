import matplotlib.pyplot as plt
import pandas as pd 
#import base64
#from io import BytesIO
import plotly.graph_objects as go



def get_reviews_plot(x):
    df = pd.read_csv('C:/Users/tassa/Desktop/firstproject/dataset/reviews_labeled.csv')
    data = df.loc[df['id'] == x]
    y= [data.target.value_counts().positive,data.target.value_counts().negetive]
    rev_labels=['positive','negative']
    fig = go.Figure(data=go.Pie(labels = rev_labels, values = y))
    return fig
    


def search_file(x):
    df = pd.read_csv('C:/Users/tassa/Desktop/firstproject/dataset/fyp_product_tracking_ds.csv')
    asinss=df.loc[df['asins'].isin([x])]
    if asinss.shape[0]!=0:
        pid=asinss.iloc[1,5]
        return pid
    else:
        return 0



def search_reviews(x):
    df = pd.read_csv('C:/Users/tassa/Desktop/firstproject/dataset/reviews_labeled.csv')
    data = df.loc[df['asins'].isin([x])]
    if data.shape[0]!=0:
        pid=data.iloc[1,1]
        return pid
    else: 
        return 0



        
        
def make_graph(_x):
    df = pd.read_csv('C:/Users/tassa/Desktop/firstproject/dataset/fyp_product_tracking_ds.csv')
    df['date'] = pd.to_datetime(df['date'], format='%d/%m/%Y')
    item_df = df.set_index('date')
    item_df = item_df.loc[item_df['id'] == _x]
    fig = go.Figure(data=go.Scatter(x=item_df.index,y=item_df['weekly_sales']))
    
    data={
        "fig": fig,
        "name": item_df['name'][0], 
        "category": item_df['categories'][0],
        "brand": item_df['brand'][0],
        "price": item_df['price'][0]
    }
    return data

def make_graph_c(_x):
    df = pd.read_csv('C:/Users/tassa/Desktop/firstproject/dataset/fyp_current_sales_dataset.csv')
    df['date'] = pd.to_datetime(df['date'], format='%d/%m/%Y')
    item_df = df.set_index('date')
    item_df = item_df.loc[item_df['id'] == _x]
    fig = go.Figure(data=go.Scatter(x=item_df.index,y=item_df['weekly_sales']))
    
    data={
        "fig": fig,
        "name": item_df['name'][0]
    }
    return data


    

