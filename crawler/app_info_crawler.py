from lib2to3.fixes.fix_imports import MAPPING
import urllib2
import os
import json
import simplejson
import pickle

def generate(filename, ids):
    print 'generating..........'
    base_url = 'http://graph.facebook.com/'
    fd = open(filename, 'w')
    dicts = list()
    size = 0
    for appid in ids:
        url = base_url + appid
        try:
	    response = urllib2.urlopen(url)
            jsondata = response.read()
            data = json.loads(jsondata)
            dicts.append(data)
            size += 1
            print size
        except:
            #print 'fail'
            pass
    encoded_data = simplejson.dumps(dicts, indent = 4, skipkeys = True)
    fd.write(encoded_data)

def read_id(filename):
    print 'reading.........'
    fid = open(filename, 'r')
    id_set = pickle.load(fid)
    return id_set

def main():
    os.chdir("/Users/karen/Desktop/project")
    json_file = 'app_information_full.json'
    id_file = 'appid'
    ids = read_id(id_file)
    generate(json_file,ids)


if __name__ == '__main__':
    main()
