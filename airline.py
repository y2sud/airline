
# coding: utf-8

# In[193]:

#This program will solve first 3 questions from problem statement
# Depending on which answer is sought, one or all of below variables can be set to True

question1 = True
question2 = False
question3 = False


# In[34]:

import numpy as np
import pandas as pd
import os, sys, math, time
from collections import OrderedDict


# In[3]:

def read_files():
    global data, plane, airports, carriers
    
    data_2007 = pd.read_csv('2007.csv')
    data_2008 = pd.read_csv('2008.csv')
    data = pd.concat([data_2007, data_2008],axis=0)
    data.reset_index(inplace=True)
    plane = pd.read_csv('plane-data.csv')
    airports = pd.read_csv('airports.csv')
    carriers = pd.read_csv('carriers.csv')
    


# In[194]:

def main():
    global ans2_dict, ans3_dict
    
    start = time.time()
    
    if question1:
        print 'Solving answer 1..'
        # Get unique carriers
        all_carriers = data.ix[:,'UniqueCarrier']
        answer_1 = answer1(all_carriers)
        answer_1.solve()

    if question2:
        print 'Solving answer 2..'
        # Fetch subset of below columns
        subset = data.ix[:,['Month','DayofMonth','DayOfWeek','CRSDepTime','ArrDelay']]
        try:
            answer_2 = answer2(subset)
            ans2_dict = answer_2.solve()
        except:
            print 'error in solution 2'
        
        print 'Run time for question 2 = ', time.time() - start
        
    inter = time.time()
    
    if question3:
        print 'Solving answer 3..'
        #all_tail = data.ix[:,'TailNum']
        # Get unique tail numbers
        all_tail = data.ix[:,'TailNum'].drop_duplicates()
        all_tail.dropna()
        print len(all_tail)
        answer_3 = answer3(all_tail)
        ans3_dict = answer_3.solve()
        print 'Run time for question 3 = ', time.time() - inter
    
    print '\ntotal time ' , time.time() - start
    
    


# In[6]:

class answers:
    def __init__(self,data):
        pass
        #print self.all_carriers.ix
    
    def solve(self):
        pass        
    


# # Logic for question 1 ... carrier with least delay

# In[16]:

class answer1(answers):
    def __init__(self,all_carriers):
        #answers.__init__(self)
        self.all_carriers = all_carriers
    
    def solve(self):
        arr_delay = 999.0
        carrier_delay = ''
        for ind, carrier in enumerate(self.get_uniq_carrier()):            
            arrdelay_list = [data.ix[data.ix[:,'UniqueCarrier'] == carrier,'ArrDelay']]
            #if carrier == 'AQ':
            #    print 'list ', arrdelay_list
            avg_delay = np.nanmean(arrdelay_list)
            print 'Index. %d  carrier %s  delay  %f '  % (ind+1, carrier, avg_delay)
            if arr_delay > avg_delay:
                arr_delay = avg_delay
                carrier_delay = carrier
            
        print 'Carrier with minimum average Arrival delay is %s: %f mins average' % (carrier_delay, arr_delay)
        
    def get_uniq_carrier(self):
        uniq_carrier = self.all_carriers.drop_duplicates()
        #print 'uniq carr...' , uniq_carrier
        #print uniq_carrier
        return uniq_carrier
    


# # Logic for question 2 ... best time of year to fly - minimum delay

# In[8]:

class answer2(answers):
    def __init__(self,subset):
        #answers.__init__(self)
        self.subset = subset
    
    def build(self):
        period_dict = OrderedDict()
        
        for ind, row in self.subset.iterrows():

            mth, day, week, tim, arrdelay = row[0], row[1], row[2], row[3], row[4]

            if pd.isnull(arrdelay) or pd.isnull(mth) or pd.isnull(day) or pd.isnull(week) or pd.isnull(tim):
                continue
                
            if ind % 400000 == 0:
                print ind+1 , 'row ', mth, day, week, tim, arrdelay
                
            period_mth = math.ceil(day / float(7) )
            if tim <= 400:
                period_day = 1
            elif tim <= 800 and tim > 400:
                period_day = 2
            elif tim <= 1200 and tim > 800:
                period_day = 3
            elif tim <= 1600 and tim > 1200:
                period_day = 4
            elif tim <= 2000 and tim > 1600:
                period_day = 5
            else:
                period_day = 6
                
            key = ':'.join((str(mth),str(period_mth),str(week),str(period_day)))
            #print 'key ', key
            
            if period_dict.has_key(key):
                period_dict[key].append(arrdelay)
            else:
                period_dict[key] = [arrdelay]
                
            #if ind > 200:
            #    break
                
        return period_dict
            
        
    def solve(self):        
            period_dict = self.build()
            
            # iterate over period dictionary to find mean ArrDelay
            mindelay = 999
            for key, lst in period_dict.items():
                avgdelay = np.average(lst)
                if mindelay > avgdelay:
                    mindelay = avgdelay
                    period = key
                    
            mth, period_mth, week, period_day = key.split(':')
            if period_day == '1':
                duration = '00:00 - 04:00'
            elif period_day == '2':
                duration = '04:00 - 08:00'
            elif period_day == '3':
                duration = '08:00 - 12:00'
            elif period_day == '4':
                duration = '12:00 - 16:00'
            elif period_day == '5':
                duration = '16:00 - 20:00'
            else:
                duration = '20:00 - 00:00'
            
            #print '\nperiod dict ', period_dict
            
            print '\nBest time is month %s, week %s, day of week %s, time period %s; average Arrival delay %f '                 %(mth,period_mth,week,duration, mindelay )
        
            return period_dict
    


# # Logic for question 3 ... Do older planes suffer more delay?

# In[9]:

class answer3(answers):
    def __init__(self, all_tail):
        #answers.__init__(self)
        self.all_tail = all_tail
    

    def solve(self):
        year_dict = OrderedDict()
        temp_year_dict = self.build()
        print 'build over...'
        
        for year, lst in temp_year_dict.items():
            tot_cnt, tot_sm = 0, 0
            for tup in lst:
                sm, cnt = tup
                tot_sm += sm
                tot_cnt += cnt
                avg_delay = float(tot_sm) / tot_cnt
                
            year_dict[year] = avg_delay
            print 'year %s: average %f ' % (year, avg_delay)
        
        print year_dict
        return year_dict
            
    def build(self):
        year_dict = OrderedDict()
        for ind, tail in enumerate(self.all_tail):
            if ind % 100 == 0:
                print 'tail: ', ind+1,  tail
            
            # for a given tail num, find year from plane df
            year_series = plane.ix[plane.ix[:,'tailnum'] == tail, 'year']
            # for a given tail num, find list of all ArrDelays from data df
            lst = data.ix[data.ix[:,'TailNum'] == tail , 'ArrDelay']
            
            if year_series.empty:
                continue
                
            # find non-nan sum
            sm = np.nansum(lst)
            # find non-nan count
            cnt = len(np.where(~np.isnan(lst))[0])
            
            year = year_series.to_string(index=False)
            if pd.isnull(year) or year == '0000':
                continue
                
            #print 'year ', year_series
            if year_dict.has_key(year):
                year_dict[year].append((sm, cnt))
            else:
                year_dict[year] = [(sm, cnt)]
           
            #if ind > 20:
            #    break
                
        sorted_year = OrderedDict(sorted(year_dict.items(), key = lambda x:x[0]))
        return sorted_year
        
        


# In[195]:

if __name__ == "__main__":
    if sys.argv[0].find('airline') > -1:
        print 'Called from command line ..'
        error = False
        
        if len(sys.argv) == 1:
            print  'No path passed'
            error = True
        else:
            path = sys.argv[1]    
            if len(sys.argv) >= 3:
                question1 = sys.argv[2]
                if question1.lower() <> 'y':
                    print 'Invalid question 1 parm'
                    error = True
            if len(sys.argv) >= 4:
                question2 = sys.argv[3]
                if question2.lower() <> 'y':
                    print 'Invalid question 2 parm'
                    error = True                
            if len(sys.argv) == 5:
                question3 = sys.argv[4]
                if question3.lower() <> 'y':
                    print 'Invalid question 3 parm'
                    error = True

    	if len(sys.argv) > 5 or error:
        	print 'Previous error, or too many arguments passed... exit'
        	sys.exit()
    else:
        print 'Called from Jupyter ..'
        path = r'/home/test/prsnl/airline'

    os.chdir(path)
    print os.getcwd(), '\n'
    print 'reading files..'
    read_files()
        
    #print 'args ', sys.argv
    main()


# In[181]:

#bkup_dict = ans3_dict
#bkup_dict


# # Additional... plot manufacture year versus average arrival delay

# In[182]:

import matplotlib.pyplot as plt
import seaborn as sns


# In[183]:

#%matplotlib inline


# In[191]:

# ans3_dict contains average arrival delay for each manufacture year 
# plot a bar chart
fig, ax1 = plt.subplots(1,1,figsize=(30, 16))

try:
    x_ax = list(ans3_dict.keys())
    y_ax = list(ans3_dict.values())
    sns.barplot(x=x_ax, y=y_ax, ax=ax1)
except:
    print 'ans3 logic not executed.., so no plot'
#x_ax
#fig.savefig('years.png')


# In[ ]:



