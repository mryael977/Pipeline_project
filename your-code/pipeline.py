import pandas as pd
import opendatasets as od
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

name_of_report = str(input('Introduce the name you want to asign to this report:'))

def aquire():
    od.download('https://www.kaggle.com/datasets/thedevastator/unlock-profits-with-e-commerce-sales-data')
    data = pd.read_csv('./unlock-profits-with-e-commerce-sales-data/Amazon Sale Report.csv',encoding= 'unicode_escape')
    return data

def wrangle(data):
    data['Date'] = pd.to_datetime(data['Date'])
    data['day'] = data['Date'].dt.day_name()
    return data

def visualize(data):
    #Most wanted categories.
    fig, ax = plt.subplots(figsize = (10,6))
    most_wanted_categories = sns.countplot(x='Category', data= data).set(title= 'Orders by Categories')
    most_wanted_categories = ax
    #Categories with more oders cancelled.

    cancelled = data[data['Status']== 'Cancelled']
    fig, ax = plt.subplots(figsize = (10,6))
    more_categories_canceled = sns.countplot(x='Category', data= cancelled).set(title= 'Categories with More Cancelled Orders')
    more_categories_canceled = ax


    #Sizes with more orders 

    data.Size.value_counts()
    fig, ax = plt.subplots(figsize = (10,6))
    sizes_orders = sns.countplot(x='Size', data= data).set(title= 'Orders by Size')
    sizes_orders = ax

    #most orders cancelled by size 
    fig, ax = plt.subplots(figsize = (10,6))
    most_cancelled_size = sns.countplot(x='Size', data= cancelled).set(title= 'Orders Cancelled by Size')
    most_cancelled_size = ax

    #whatss the ship-state with more orders 

    fig, ax = plt.subplots(figsize = (15,10))
    plt.xticks(rotation=45)
    ship_state_orders = sns.barplot(x=data['ship-state'].value_counts()[:25].index, y=data['ship-state'].value_counts()[:25]).set(title= 'Ship State with More Orders')
    ship_state_orders = ax

    #amount spended by category


    fig, ax = plt.subplots(figsize = (15,10))
    plt.xticks(rotation=45)
    plt.ticklabel_format(style='plain', axis='y')

    amount_by_category = sns.barplot(x=data.groupby('Category')['Amount'].sum().sort_values(ascending=False).index, y=data.groupby('Category')['Amount'].sum().sort_values(ascending=False)).set(title= 'Amount sold by category ')
    amount_by_category = ax
    

    #Amount by Size
    fig, ax = plt.subplots(figsize = (15,10))
    plt.xticks(rotation=45)
    plt.ticklabel_format(style='plain', axis='y')
    amount_by_size = sns.barplot(x=data.groupby('Size')['Amount'].sum().sort_values(ascending=False).index, y=data.groupby('Size')['Amount'].sum().sort_values(ascending=False)).set(title= 'Amount sold by size')
    amount_by_size = ax

    #Amount by Ship City
    fig, ax = plt.subplots(figsize = (15,10))
    plt.xticks(rotation=45)
    plt.ticklabel_format(style='plain', axis='y')
    amount_by_city = sns.barplot(x=data.groupby('ship-city')['Amount'].sum().sort_values(ascending=False)[:10].index, y=data.groupby('ship-city')['Amount'].sum().sort_values(ascending=False)[:10]).set(title= 'Amount sold by city')
    amount_by_city = ax

    #amount by day total
    fig, ax = plt.subplots(figsize = (15,10))
    plt.xticks(rotation=45)
    plt.ticklabel_format(style='plain', axis='y')
    amount_by_day = sns.barplot(x=data.groupby('day')['Amount'].sum().sort_values(ascending=False).index, y=data.groupby('day')['Amount'].sum().sort_values(ascending=False)).set(title= 'Amount sold by day')
    amount_by_day = ax

    #AMount by category by day
    fig, ax = plt.subplots(figsize = (15,10))
    data_by_day = data.groupby(['day', 'Category'])['Amount'].sum().sort_values(ascending=False)
    data_by_day =data_by_day.reset_index()
    plt.ticklabel_format(style='plain', axis='y')
    amount_category_day = sns.barplot(x= 'day', y = 'Amount', hue = 'Category', data = data_by_day).set(title= 'Amount sold by category by day')
    amount_category_day =ax

    return (most_wanted_categories, more_categories_canceled, sizes_orders, most_cancelled_size,ship_state_orders, amount_by_category, amount_by_size, amount_by_city, amount_by_day, amount_category_day)

def safe_viz(barchart):
    
    with PdfPages( name_of_report+ '.pdf') as pp:
        for plot in barchart:
            pp.savefig(plot.figure)


if __name__ == '__main__':
    data = aquire()
    filtered = wrangle(data)
    charts = visualize(filtered)
    
    safe_viz(charts)
