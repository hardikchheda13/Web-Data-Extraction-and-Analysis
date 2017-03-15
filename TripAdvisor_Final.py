from BeautifulSoup import BeautifulSoup
import re
import urllib2
from operator import itemgetter
import time
import sys
import requests
import os

def run(url):
    newpath = r'TripAdv'                  #Creating a folder in the working directory
    if not os.path.exists(newpath):
           os.makedirs(newpath)
    
    pageNum=3                            #Page Number for Restraunts 
    for p in range(2,pageNum):  
	
		html=None
		print p

		if p==1: pageLink=url 
		else: 
		    print "hello"
		    pageLink='https://www.tripadvisor.com/RestaurantSearch-g60713-oa'+str(p*30)+'-San_Francisco_California.html#EATERY_OVERVIEW_BOX'
		
		for i in range(5): # try 5 times   #Opening Main trip Advisor Page
			try:
			        response=requests.get(pageLink,headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36', })
				html=response.content 
				break 
			except Exception as e:
				print 'failed attempt',i
				time.sleep(2)
				ss=input("No internet: Enter Anything")
			
		if not html:continue # couldnt get the page, ignore

		soup = BeautifulSoup(html) # parse the html 

		
		reviews= soup.findAll('a', {'class': re.compile('property_title')})     #Searching for the title of the restraunt
                #print reviews
                g=open('TripAdv\\RestruantList.txt','w')
                
                for review in reviews:
                    #print review
                    rev=review.contents[0]   #NAME OF THE RESTRAUNT
                    rev=rev.strip()
                    f=open('TripAdv''\\'+str(rev)+'.txt','w')      #Opening a file by the name of the Restaurant to save the reviews
                    g.write(str(rev))                              #Writing the titles to a new file to use it for SCrapping yelp reviews
                    g.write("\n")
                    
                    #print rev
                    link='https://www.tripadvisor.com'+review.get('href')     #Opening Restaurant
                    #print link
                    #title=re.findall("target(.*?)",str(review))
                    #title=re.findall(';">(.*)</a>',str(review))
                    #title=soup1.find_all('a')
                    
                    #print title.text
                    
                    
                    for q in range(0,5):  #Link of the restraunts
                        try: 
                            response=requests.get(link,headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36', })
                            Webcontent=response.content
                            break
                        except Exception as e:
				print 'failed attempt',i
				time.sleep(2) 
				ss=input("No internet: Enter Anything")
		    #print Webcontent
		    
		    #countPage=0
		    
		    revsoup=BeautifulSoup(Webcontent)
		    page=revsoup.findAll('a',{'class':'pageNum taLnk'})           #Finding page numbers till which the loop has to be run to scrape reviews and ratings
		    for p1 in page:
		        finalPage=p1.contents[0]                                 #FinalPage gives the page number
		    print finalPage
		    for p2 in range(0,int(finalPage)):                        #Loop for finding reviews,Rating and Date for each page in a restaurant
		    #rev=revsoup.findAll('div',{'class': re.compile('review-content')})
		        if p2==0:
                            revs=revsoup.findAll('a',{'href':re.compile('/ShowUserReviews')})
                    
		            for r in revs:
		                  title_review=re.findall(r'<span class="noQuotes">(.*?)</span>',str(r))  #NAME OF THE REVIEW
		                  print title_review
		                  try:
		                    
		                      f.write(title_review[0])                                         #Writing it to the file
		                      f.write("\n")
		                  except IndexError:
		                      print ""
		                  link_rev='https://www.tripadvisor.com/'+r.get('href')                #Creating link to go inside teh review 
		        #print link_rev
		                  for q in range(0,5):
                                        try: 
                                            response=requests.get(link_rev,headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36', })
                                            Webcontent_rev=response.content
                                            break
                                        except Exception as e:
			        	    print 'failed attempt',i
			        	    time.sleep(2)
			        	    ss=input("No internet: Enter Anything")
			          reviewPage=BeautifulSoup(Webcontent_rev)
			          rating=reviewPage.findAll('img',{'class':re.compile('sprite-rating_s_fill rating_s_fill s')})    #Scrapping rating from the review
			          reviewRating=rating[0].get('alt')
			          #reviewRating=reviewRating[0]
			          
			          f.write("Rating: ")
			          print reviewRating
			          i=0
			          while (reviewRating[i] != ' '):
			             print 'while'
			             f.write(reviewRating[i])             #Writing Rating in file
			             i=i+1 
			          f.write("\n")
			         # date1=reviewPage.findAll()
			          f.write("Date: ")
			          date=reviewPage.findAll('span',{'class':re.compile('ratingDate')})      #Scrapping date
			          #print date[0]
			          try:
			              reviewDate=date[0].get('title')
			              print reviewDate
			              f.write(reviewDate)                                                #Writing Date to the file
			              f.write("\n")
			          except Exception as e:    
			              p=re.compile(r'<.*?>')
			              datetest=p.sub('',str(date[0]))
			              dateTest=datetest.replace("Reviewed ","")
			              print dateTest
			              
			              f.write(dateTest)
			              f.write("\n")
			              
			          #datetest=re.findall('<span.*?>(.*?)</span>',str(date))
			          #print datetest
			          #reviewDate=date[0].get('title')
			          #f.write(reviewDate)
			          #f.write("\n")
			         
			          review_content=reviewPage.findAll('div',{'class':'entry'})             #Finding Review content
			          for div in review_content:
			             elem=div.find('p')
			             if elem:
			                 print elem.text
			                 try:
			                   
			                     f.write(elem.text)                                           #Writing review content to file
			                     
			                 except UnicodeEncodeError:
			                     print "123"
			             f.write("\n")
			             f.write("\n")
			             break
			else:                                                                            #To navigate to different pages inside the reviews
			    print "heelo"
			    link=link+'#REVIEWS'                                                          #To create link to Navigate in review pages
			    print link 
			    first=re.findall(r'(.*?)Reviews',str(link))
                            last=re.findall(r'Reviews(.*?)REVIEWS',str(link))
                            print first
                            print last
                            finalLink=first[0]+'Reviews-or'+str(p2*10)+last[0]+'REVIEWS'                  #To create link to Navigate in review pages
                            for q in range(0,5):
                                        try: 
                                            response=requests.get(finalLink,headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36', })
                                            Webcontent_rev=response.content
                                            break
                                        except Exception as e:
			        	    print 'failed attempt',i
			        	    time.sleep(2)
			        	    ss=input("No internet: Enter Anything")
			    reviewPage=BeautifulSoup(Webcontent_rev)
			    revs=reviewPage.findAll('a',{'href':re.compile('/ShowUserReviews')})
                            
		            for r in revs:
		                  title_review=re.findall(r'<span class="noQuotes">(.*?)</span>',str(r))
		                  print title_review
		                  try:
		                     
		                      f.write(title_review[0])
		                      f.write("\n")
		                  except IndexError:
		                      print ""
		                  link_rev='https://www.tripadvisor.com/'+r.get('href')
		        #print link_rev
		                  for q in range(0,5):
                                        try: 
                                            response=requests.get(link_rev,headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36', })
                                            Webcontent_rev=response.content
                                            break
                                        except Exception as e:
			        	    print 'failed attempt',i
			        	    time.sleep(2)
			        	    ss=input("No internet: Enter Anything")
			          reviewPage=BeautifulSoup(Webcontent_rev)
			          rating=reviewPage.findAll('img',{'class':re.compile('sprite-rating_s_fill rating_s_fill s')})
			          reviewRating=rating[0].get('alt')
			          #reviewRating=reviewRating[0]
			          print reviewRating
			          i=0
			          f.write("Rating: ")
			          while (reviewRating[i] != ' '):
			             #print 'while'
			             f.write(reviewRating[i])
			             i=i+1 
			          f.write("\n")
			          f.write("Date: ")
			          try:
			              date=reviewPage.findAll('span',{'class':re.compile('ratingDate')})
			          
			              try:
			                  reviewDate=date[0].get('title')
			                  print reviewDate
			                  f.write(reviewDate)
			                  f.write("\n")
			              except Exception as e:    
			                  p=re.compile(r'<.*?>')
			                  datetest=p.sub('',str(date[0]))
			                  dateTest=datetest.replace("Reviewed ","")
			                  print dateTest
			                  f.write(dateTest)
			                  f.write("\n")
			          except Exception as e:
			              print " No date"
			              f.write("\n") 
			              
			          
			          """date=reviewPage.findAll('span',{'class':re.compile('ratingDate')})
			          datetest=re.findall(r'>Reviewed (.*?)</span>',str(date))
			          print datetest
			          reviewDate=date[0].get('content')
			          f.write(reviewDate)
			          f.write("\n")"""
			         
			          review_content=reviewPage.findAll('div',{'class':'entry'})
			          for div in review_content:
			             elem=div.find('p')
			             if elem:
			                 print elem.text
			                 try:
			                    
			                     f.write(elem.text)
			                     
			                 except UnicodeEncodeError:
			                     print "123"
			             f.write("\n")
			             f.write("\n")
			             break    
			
		f.close()                                             #Close the restaurant file all the reviews,ratings and date of the of each restaurant has been saved in the file 
			
				
		      
                     
if __name__=='__main__':
	url='https://www.tripadvisor.com/Restaurants-g60713-San_Francisco_California.html'             #TripAdvisor URL for Restaurats in Calfornia
	print run(url)