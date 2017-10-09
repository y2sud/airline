
# coding: utf-8

# In[1]:

from sklearn import linear_model, svm
from sklearn.model_selection import train_test_split, cross_val_score
import os, sys, time
import pandas as pd, numpy as np
from sklearn.feature_selection import chi2


# In[2]:

# define models
ridgecv = linear_model.RidgeCV(alphas=[0.1,1,10])
lasso = linear_model.Lasso(alpha=0.1)
ridge = linear_model.Ridge(alpha=0.1, fit_intercept=False)
svr = svm.SVR()


# In[3]:

path = r'/home/test/prsnl/airline'
os.chdir(path)
os.getcwd()


# In[4]:

def read_files():
    global data2, plane, airports, carriers
    
    data_2007 = pd.read_csv('2007.csv')    
    print len(data_2007)
    data_2008 = pd.read_csv('2008.csv')
    print len(data_2008)
    data2 = pd.concat([data_2007, data_2008],axis=0)
    data2.reset_index(inplace=True)
    plane = pd.read_csv('plane-data.csv')

    


# In[5]:

read_files()


# In[6]:

# just take first 1 million rows from 2007 sheet
data = data2.ix[:1000000].copy()


# In[7]:

#sys.getsizeof(data) / 1000000
#del data2


# In[8]:

Y_all = data.ix[:,'ArrDelay'].copy()


# In[9]:

# Select below few columns

lst = ['Month', 'DayofMonth', 'DayOfWeek', 'UniqueCarrier', 'Origin', 'Dest']
out = pd.DataFrame()
type(out)

def create_dummies():
    out = pd.DataFrame()
    for col in lst:
        cat = pd.get_dummies(data.ix[:,col])
        #print cat.info()
        out = pd.concat([out,cat], axis=1)
    return out
        
# These are categorical columns. Transform them to dummy variables
# a df named out contains all these dummy variables
out = create_dummies()
out.info()


# In[10]:

# create df named out2 for elapsed time & distance, which are already in numeric format
out2 = data.ix[:,['CRSElapsedTime','Distance']]


# In[11]:

# Subset expected departure time into six 4-hour buckets
deptime = data.ix[:,'CRSDepTime']
per_series = []
for ind, row in deptime.iteritems():
    #print row
    if row < 400:
        period = 1
    elif row < 800:
        period = 2
    elif row < 1200:
        period = 3
    elif row < 1600:
        period = 4
    elif row < 2000:
        period = 5
    else:
        period = 6
    
    per_series.append(period)
    

# out3 will contain departure time dummy variables
out3 = pd.get_dummies(pd.Series(per_series))
    


# In[12]:

#uniq_tail = data.ix[:,'TailNum'].drop_duplicates().dropna()
#uniq_tail


# In[13]:

# This will identify unique tail numbers from 2007/2008 data; get year from plane-data, and build a list of years 
# for corresponding tail numbers
uniq_tail = data.ix[:,'TailNum'].drop_duplicates().dropna()
uniq_tail.reset_index()
print len(uniq_tail)
year_list = []
for ind, tail in uniq_tail.iteritems():
    #print 'ind ', ind
    year = plane.ix[plane.ix[:,'tailnum'] == tail,'year']
    year.reset_index(inplace=True,drop=True)
    #year = pd.to_numeric(year_ser)
    

    try:
        if year.empty:
            #print 'year1', year
            decade = '00-00'
            year_list.append(decade)
            continue
    except:
        print 'year2 ', year
        
    

    if year.item() < 1960:
        decade = '50-60'
    elif year.item() < 1970:
        decade = '60-70'
    elif year.item() < 1980:
        decade = '70-80'
    elif year.item() < 1990:
        decade = '80-90'
    elif year.item() < 2000:
        decade = '90-00'
    else:
        decade = '00-10'

        
    year_list.append(decade)


# In[14]:

# Combine tail number with corresponding year into a dataframe
year_series = pd.Series(year_list)
year_series.reset_index(inplace=True,drop=True)
uniq_tail.reset_index(inplace=True,drop=True)
print len(year_series)
tail_year = pd.concat([uniq_tail,year_series],axis=1)
#print year_series


# In[15]:

#x_train, x_test, y_train, y_test = train_test_split(X, Y, test_size=0.2, random_state=0.1, stratify=Y)


# In[36]:

# Memory error... reduce the count of rows
# Y is target
limit = 100000
Y = Y_all[:limit+1].copy()


# In[37]:

# Find whether there are any NaNs in target variable - Arrival delay
# There were few such rows...
Y_np = np.array(Y)
print 'Are any of the values Null for Y? ' ,  np.any(np.isnan(np.array(Y)))
print 'Are values finite for Y? ', np.any(np.isfinite(np.array(Y)))
print 'count of nulls in 3 diff approaches ', Y.isnull().sum().sum() , np.sum(np.isnan(Y_np)),         pd.isnull(Y_np).sum()


# In[38]:

# Find index of rows that contain NaN in target variable
null_inds = np.where(np.isnan(Y_np))[0]


# In[39]:

print null_inds, len(null_inds)


# In[40]:

# Remove rows Y where NaN was present in target variable
Y.drop(Y.index[null_inds], inplace=True)
Y_np = np.array(Y)


# In[41]:

Y_np.shape


# # This is where actual modeling happens

# In[42]:

# Modeling

# Concatenate all the feature data frames
new_temp_X = data.ix[:limit,['CarrierDelay','WeatherDelay', 'NASDelay', 'SecurityDelay']]
temp_X = pd.concat([new_temp_X, out3.ix[:limit,], out2.ix[:limit,], out.ix[:limit,]],axis=1)

print temp_X.shape
print 'Count of nulls ' , np.isnan(temp_X).sum().sum()

temp_X.drop(temp_X.index[null_inds], inplace=True)
print 'Count of nulls after processing..' , np.isnan(temp_X).sum().sum()
print temp_X.shape
#len(temp_X[temp_X[:] == 0.0])


# In[43]:

# print all column names
#temp_X.columns.values
#temp_X['CRSElapsedTime'].isnull().any()


# In[63]:

clf = ridge
#clf = lasso
#clf = svr


# In[ ]:

st = time.time()
temp_X_np = np.array(temp_X)
score = cross_val_score(clf, temp_X_np, Y_np, cv=5)
print 'duration: ', time.time() - st
print 'Score; average score ' , score, np.average(score)


# In[51]:

pred = lasso.fit(temp_X_np, Y_np)


# In[52]:

# Find linear regression coefficient. Second value is for weather delay
print pred.intercept_
pred.coef_[1]


# In[53]:

# Find pvalue for weather delay
scores, pvalues = chi2(temp_X_np, Y_np)

#pvalues[np.where(pvalues[:] > 0.05)]
pvalues[:1]


# In[ ]:




# # Find Pearson Correlation between weather & arrival delay

# In[54]:

from scipy.stats import pearsonr


# In[55]:

weather_vect = data.ix[:,'WeatherDelay'].copy()
arr_vect = data.ix[:,'ArrDelay'].copy()


# In[56]:

weather_vect.shape, arr_vect.shape


# In[60]:

print 'nulls in weather & arrival delay vectors? ' , weather_vect.isnull().any(), arr_vect.isnull().any()
null_inds = np.where(arr_vect.isnull())
print len(null_inds[0])

# drop rows that have null in arrival delay vector 
weather_vect.drop(weather_vect.index[null_inds], inplace=True)
arr_vect.drop(arr_vect.index[null_inds], inplace=True)


# In[61]:

pearsonr(weather_vect, arr_vect)


# In[ ]:



