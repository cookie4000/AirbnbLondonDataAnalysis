import pandas as pd;
import matplotlib.pyplot as plot;

# Import the listings data
# Data From http://insideairbnb.com
df_listings = pd.read_csv('data/listings.csv')

# Filter to Columns of Interest
df_listings = df_listings[['id','neighbourhood', 'price','availability_365']]

# DQ - How many are in a price I dont think is possible
df_filtered = df_listings[(df_listings['price']<=19)]
#print(df_filtered.count())

# Remove these items - surely its not possible / bad data
df_listings = df_listings[df_listings.price >= 20]

################
## Analysis 
################

# cheapest room in area
df_cheapestByArea = df_listings.groupby(['neighbourhood'])['price'].min()


# average price in area
df_avgPriceByArea = df_listings.groupby(['neighbourhood'])['price'].mean()


# Calculate revnues for the next 365 days
df_listings['revenue'] = (df_listings['price'] * (365-df_listings['availability_365']))
df_RevbyArea = df_listings.groupby(['neighbourhood'])['revenue'].mean()
print (df_RevbyArea)


# Bring in new data - average house price per borough
# Data From https://www.statista.com/statistics/1029250/average-house-prices-in-london-united-kingdom-by-borough/
df_avg_house_price = pd.read_csv('data/averageHousePrice.csv')

# Convert the string imported (comma separated number) to a float
df_avg_house_price['average house price'] = df_avg_house_price['average house price'].str.replace(',', '').astype(float)

# Join the revenue by area to the average house price 
dfJoin = pd.merge(df_RevbyArea, df_avg_house_price, how='inner', left_on=['neighbourhood'], right_on=['borough'])
#print(dfJoin)

# Calculate the revenue to price ratio
dfJoin['Rev/Price'] = (dfJoin['revenue'] / dfJoin['average house price'])

# Create Results - Sort desc
df_Results = dfJoin[['borough', 'average house price','revenue','Rev/Price']]
print (df_Results.sort_values(by=['Rev/Price'],ascending=False))
#df_Results.to_csv('results.csv')

################
## Plot Graphs 
################

df_graph = df_Results[['borough', 'average house price','revenue']]

# average house price Vs Average Revenue Per borough
df_graph.plot(x="borough", kind="barh", title="Avergage House Price Vs Revenue",
        color={"green", "pink"})

#plot.show(block=True)

# Average Revenue to Average Price Ratio Graph
df_graph2 = df_Results[['borough', 'Rev/Price']]
df_graph2.plot(x="borough", kind="barh", title="Average Rev / Avg Price per borough",
        color={"green"})
plot.show(block=True)