import matplotlib.pyplot as plt
import pandas as pd 
import base64
from io import BytesIO

from pandas.core.frame import DataFrame

def get_graph():
    buffer=BytesIO()
    plt.savefig(buffer, fromat='png')
    buffer.seek(0)
    image_png=buffer.getvalue()
    graph=base64.b64encode(image_png)
    graph=graph.decode('utf-8')
    buffer.close()
    return graph

def get_plot(x):
    df = pd.read_csv('C:/Users/M. SAAD/Desktop/FYP 2020-2021/dataset_product_tracking.csv')
    df['date'] = pd.to_datetime(df['date'])
    item_df = df.set_index('date')
    plt.switch_backend('AGG')
    plt.figure(figsize=(10,5))
    plt.title('Weekly Sales')
    item_df.query('id==@x')[['weekly_sales']].plot()
    plt.xticks(rotation=45)
    plt.xlabel('dates')
    plt.ylabel('weekly sales')
    plt.tight_layout()
    graph=get_graph()
    return graph

def search_file(x):
    df = pd.read_csv('C:/Users/M. SAAD/Desktop/FYP 2020-2021/dataset_product_tracking.csv')
    asinss=df.loc[df['asins'].isin([x])]
    if asinss.shape[0]!=0:
        pid=asinss.iloc[1,3]
        return pid
    else:
        return 0
        
        




    

