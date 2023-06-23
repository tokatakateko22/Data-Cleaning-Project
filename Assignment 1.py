import pandas as pd
import numpy as np

'''
Load the energy data from the given file Energy Indicators.xls and exclude the
footer and header information from the datafile and change the column labels
'''
def energy():
    energy = pd.read_excel('Energy Indicators.xls', skiprows=17, skipfooter=38)
    energy=pd.DataFrame(energy)
    energy = energy.drop(['Unnamed: 0', 'Unnamed: 1'], axis=1)
    energy.columns = ['Country', 'Energy Supply', 'Energy Supply per Capita', 'Renewable']
    energy = energy.replace('...', np.NaN)
    energy['Energy Supply'] = energy['Energy Supply'] * 1000000  #convert energy supply to gigajoules
    energy['Country'] = energy['Country'].str.replace(r" \(.*\)","", regex=True)
    energy['Country'] = energy['Country'].str.replace(r"\d+","",regex=True)
    energy['Country'] = energy['Country'].str.strip()
    energy['Country'] = energy['Country'].replace({"Republic of Korea": "South Korea",
                                                   "United States of America": "United States",
                                                   "United Kingdom of Great Britain and Northern Ireland": "United Kingdom",
                                                   "China, Hong Kong Special Administrative Region": "Hong Kong"})
    return energy

print(energy())
print('\n\n')

def gdp():
    GDP = pd.read_csv('world_bank.csv', skiprows=4)
    GDP = pd.DataFrame(GDP)
    GDP['Country Name'] = GDP['Country Name'].replace({"Korea, Rep.": "South Korea",
                                                       "Iran, Islamic Rep.": "Iran",
                                                       "Hong Kong SAR, China": "Hong Kong"})
    GDP = GDP[['Country Name', '2010', '2011', '2012', '2013','2014', '2015']]
    GDP = GDP.rename(columns={'Country Name': 'Country'})
    
    return GDP

print(gdp())
print('\n\n')

#joining the two data sets
def merge():
    merged = pd.merge(gdp(),energy(), how='inner', left_on='Country', right_on='Country')
    merged = merged.set_index('Country')
    return merged

print(merge())
print('\n\n')

'''
function that returns the top 15 countries in terms of average GDP over
the previous six years. This function should produce an 'averageGDP' Series
containing 15 nations and their average GDP ordered in descending order
'''
def avgGDP():
    merged = merge()
    merged['avgGDP'] = merged.mean(axis=1)
    return merged['avgGDP'].sort_values(ascending=False)

print(avgGDP().head(15))
print('\n\n')

# function to return the mean energy supply per capita
def meanEnergy():
    merged = merge()
    return merged['Energy Supply per Capita'].mean()

print(meanEnergy())
print('\n\n')

def minRenewable():
    country = merge()['Renewable'].idxmin()
    value = merge().loc[country, 'Renewable']
    return country, value

print(minRenewable())


