import urllib2
import sys,re,pickle
"210831918949520"

def crawl():
    id_list = []
    result = urllib2.urlopen('http://www.socialbakers.com/facebook-applications/')
    l = re.findall("\d{15}", result.read())
    id_list = id_list + l
    
    for i in range(2,1506):
        try:
            result = urllib2.urlopen('http://www.socialbakers.com/facebook-applications/page-'+str(i))          
            l = re.findall("\d{15}", result.read())
            id_list = id_list + l
        except urllib2.URLError,e:
                print "url error"
        
    id_set = set(id_list)
    f = open("appid",'w') 
    pickle.dump(id_set,f)
    print id_set
    
crawl()
