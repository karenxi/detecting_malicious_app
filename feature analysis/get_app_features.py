# get app features for later analysis
import os
import re
import simplejson
import json
import sys
from operator import itemgetter

def read_ids(idsfile):
    f = open(idsfile, 'r')
    final_ids = json.load(f)
    return final_ids

def read_idinfo(filename,final_ids):
    tmp_id_info = {}
    id_info ={}
    rest = []
    f = open(filename, 'r')
    data = json.load(f)
    for individual_info in data:
        tmp_id_info[individual_info['id']] = individual_info
    for id in tmp_id_info:
        if id in final_ids:
            id_info[id] = tmp_id_info[id]
    for id in final_ids:
        if id not in id_info:
            rest.append(id)
    return id_info, rest

def get_feature(id_info):
    monthly_rank = {}
    daily_rank = {}
    monthly_users = {}
    weekly_users = {}
    daily_users = {}
    no_features = {}
    description = {}
    company = {}
    ids = []
    for id in id_info:
        ids.append(id)
        if 'monthly_active_users_rank' in id_info[id]:
            monthly_rank[id] = id_info[id]['monthly_active_users_rank']
        if 'daily_active_users_rank' in id_info[id]:
            daily_rank[id] = id_info[id]['daily_active_users_rank']
        if 'monthly_active_users' in id_info[id]:
            monthly_users[id] = id_info[id]['monthly_active_users']
        if 'weekly_active_users' in id_info[id]:
            weekly_users[id] = id_info[id]['monthly_active_users']
        if 'daily_active_users' in id_info[id]:
            daily_users[id] = id_info[id]['monthly_active_users']
        if 'monthly_active_users_rank' not in id_info[id] and 'daily_active_users_rank' not in id_info[id] and "monthly_active_users" not in id_info[id] and "weekly_active_users" not in id_info[id] and "daily_active_users" not in id_info[id]:
            no_features[id] = "no features"
        if 'description' in id_info[id]:
            description[id] = id_info[id]['description']
        if 'company' in id_info[id]:
            company[id] = id_info[id]['company']

    return description,company
    #ids, monthly_rank, daily_rank, monthly_users, weekly_users, daily_users, no_features

def company_hash(company):
    company_hash = {}
    for appid in company:
        name = company[appid]
        if name not in company_hash:
            company_hash[name] = []
        company_hash[name].append(appid)
    return company_hash


def toJson(Jfile, description):
    result = []
    f = open("app_description.json", "w")
    result.append(description)
    encoded = simplejson.dumps(result, indent = 4, skipkeys = True)
    f. write(encoded)


def combine(total_id, pre_id_info, id_info):
    result =[]
    f = open("total_app_info", "w")
    for id in id_info:
        if id not in pre_id_info:
            pre_id_info[id] = id_info[id]
    for new in pre_id_info:
        result.append(pre_id_info[new])
    encoded = simplejson.dumps(result, indent = 4, skipkeys = True)
    f. write(encoded)
    return pre_id_info


def change_to_urls(result, total_id_info):
    f = open("total_urls", 'w')
    urls = []
    base = "www.facebook.com/apps/application.php?id="
    for id in total_id_info:
        urls.append(base+id)
    encoded_data = simplejson.dumps(urls, indent = 4, skipkeys = True)
    f.write(encoded_data)

def get_last10(mr, dr, mu, wu, du, id_info):
    last_mr = sorted(mr.items(), key = itemgetter(1), reverse = True)[:10]
    last_dr = sorted(dr.items(), key = itemgetter(1), reverse = True)[:10]
    last_mu = sorted(mu.items(), key = itemgetter(1), reverse = True)[:10]
    last_wu = sorted(wu.items(), key = itemgetter(1), reverse = True)[:10]
    last_du = sorted(du.items(), key = itemgetter(1), reverse = True)[:10]
    last = set()
    for i in range(10):
         last.add(last_mr[i][0])
         last.add(last_dr[i][0])
         last.add(last_mu[i][0])
         last.add(last_wu[i][0])
         last.add(last_du[i][0])
    #base = "www.facebook.com/apps/application.php?id="
    #urls = []
    #for id in last:
    #    urls.append(base+id)
    return last

def main():
    os.chdir("/Users/karen/Desktop/project")
    idsfile = "final_ids.json"
    final_ids = read_ids(idsfile)

    filename = 'total_app_info'
    id_info,rest = read_idinfo(filename, final_ids)
    print "number of apps:", len(id_info)
    #ids = get_feature(id_info)
    #total_id = "total_app_info"
    #combine(total_id,pre_id_info, id_info)

    #result = 'total_urls.json'
    #change_to_urls(result, total_id_info)

    description, company = get_feature(id_info)
    
    #ids, monthly_rank, daily_rank, monthly_users, weekly_users, daily_users, no_features = get_feature(id_info)
    #print company
    print "number of apps that have company information:", len(company)
    print "number of apps that have description information:", len(description)

    result = company_hash(company)
    print "number of unique company:",len(result)
    #encoded_file = 'app_description.json'
    #toJson(encoded_file, description)
    
    #last = get_last10(monthly_rank, daily_rank, monthly_users, weekly_users, daily_users, id_info)
    #print len(urls)
    #print urls


if __name__ == "__main__":
    main()
