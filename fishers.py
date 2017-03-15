from __future__ import division
import re
from scipy import stats
from scipy.stats import ttest_ind, ttest_ind_from_stats
import scipy.stats as stats
from nltk.corpus import stopwords
from itertools import izip
stopLex = set(stopwords.words('english')) 
ta=open('F:\\trip advisor.txt') #opening file containg paths of files containg reviews of trip advisor
yp=open('F:\\yelp.txt')#opening file containg paths of files containg reviews of yelp
'''word = open('F:\\trip advisor.txt','r').readlines()
word1 = open('F:\\yelp.txt','r').readlines()'''
for line in ta:
    print ta
    break
for line,line1 in izip(ta,yp): #for each path in the files containg path do as follows
    
    line=line.strip()
    line1=line1.strip()
    restaurant=re.sub(r"F:\Yelp\\",'',str(line1))
    res=open(str(restaurant)+'_fisher.txt','w') #opening file to write output of fisher test
    print str(restaurant)
    t=open(line)
    y=open(line1)
    treq={}
    yreq={}
    creq={}
    #for each line in Trip advisor review file of restaurant
    for l in t:
                        if "Rating:" in l or "Date:" in l: #Avoiding lnes containing dates and ratings
                            continue
                        l = l.lower().strip()  # loewr case and strip
    
                        l = re.sub('[^a-z]', ' ', l)  # replace all non-letter characters  with a space

                        words = l.split(' ')  # split to get the words in the sentence
                        for word in words:  # for each word in the sentence
    
                            if word == '' or word in stopLex:
                                continue  # ignore empty words and stopwords

                            else:
                                treq[word] = treq.get(word, 0) + 1 #find the frequency of each word
    #for each line in Yelp review file of restaurant and doing same as done for trip advisor                           
    for l1 in y:
                        if "Rating:" in l1 or "Date:" in l1:
                            continue
                        l1 = l1.lower().strip()  # loewr case and strip
    
                        l1 = re.sub('[^a-z]', ' ', l1)  # replace all non-letter characters  with a space

                        words = l1.split(' ')  # split to get the words in the sentence
                        for word in words:  # for each word in the sentence
    
                            if word == '' or word in stopLex:
                                continue  # ignore empty words and stopwords

                            else:
                                yreq[word] = yreq.get(word, 0) + 1
    #find word that are common in trip advisr and yelp                            
    for key in treq:
        if key in yreq:
            creq[key]=[treq[key],yreq[key]] #creq contains word as key and list containg frequency of that word in trip advisor and in yelp as value
         
    for key1 in creq:
        list1=[]
        list2=[]
        list1.append(creq[key1][0])
        list1.append(creq[key1][1])
        
        sum_t=0
        sum_y=0
        for key2 in creq:
            if key2 !=key1:
                sum_t=sum_t+creq[key2][0]
                sum_y=sum_y+creq[key2][1]
        list2.append(sum_t) 
        list2.append(sum_y)
        
        stat,pvalue=stats.fisher_exact([list1, list2])#performing fisher test on each word with other words   
        if float(pvalue)<0.05:
            print list1
            print list2
            print str(pvalue)
            res.write(key1+":"+'pvalue='+str(pvalue))    #writing the pvalue of fishers test which are greater than 0.05        
            res.write("\n")        
                

