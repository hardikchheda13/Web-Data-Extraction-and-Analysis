from __future__ import division
import re
from scipy import stats
from scipy.stats import ttest_ind, ttest_ind_from_stats  #importin package to do t-test
def run(line,line1):
    #for line in mf:
        print line
        line=line.strip()
        f=open(line) #opening the text file containing paths of trip advisor reviews
        list1=[]
        for line in f:
            
            #Finding the lines in the reviews of restaurant's file containg Ratings
           
                if "Rating:" in line:
                    rating = re.findall(r'Rating: (.*)', str(line)) #extracting ratings from those files
                    try:
                        list1.append(int(rating[0])) #appending the rating to the list
                        print rating[0]
                    except:
                        print 1    
                   
    #for line in mg:
        line1=line1.strip()  
        f=open(line1) # #opening the text file containing paths of yelp reviews
        list2=[]
        for line1 in f:
            #Finding the lines in the reviews of restaurant's file containg Ratings
                if "Rating:" in line1:
                    rating= re.findall(r'Rating: (.*)', str(line1)) #extracting ratings from those files
                    try:
                        list2.append(int(rating[0]))  #appending the rating to the list
                        print rating[0]   
                    except:
                        print 1     
        a=str(ttest_ind(list1, list2, equal_var=False ))  #by passing the lists containng the ratings and doing T-test
        print a  
        w.write("ttest: "+a) # writing the output of T-test
        w.write("\n")
    

if __name__=='__main__':
     w=open('pvalue.txt','w')
     mf=open('F:\\trip advisor.txt') #opeing the file containg paths of trip advisor reviews
     mg=open('F:\\yelp.txt') #opeing the file containg paths of yelp of yelp reviews
     #for i in range(1,12):
       
     for line,line1 in zip(mf,mg):
          print line 
          print line1
          print run(line,line1) #passing path of file containing reviews of same restaurants in yelp and trip advisor