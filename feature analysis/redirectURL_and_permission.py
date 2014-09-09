'''
- app_sim.py

- Analyze redirect uri and permissions
'''

import json
import tldextract


def intersect(perm1, perm2):
    p1 = []
    for perm in perm1:
        perm = perm.strip()
        if perm != '':
            p1.append(perm)

    p2 = []
    for perm in perm2:
        perm = perm.strip()
        if perm != '':
            p2.append(perm)

    cnt = 0
    for perm in p1:
        if perm in p2:
            cnt += 1
            
    #if cnt != 0:
    #    print cnt
    
    return cnt


def compute_uri_similarity(uri1, uri2):
    #print uri1
    if uri1 == '' or uri1 == None or uri2 == '' or uri2 == None:
        return 0
    if is_internal(uri1) and is_internal(uri2):
        return 0.2
    elif ~is_internal(uri1) and ~is_internal(uri2):
        d1 = tldextract.extract(uri1).domain
        d2 = tldextract.extract(uri2).domain        
        if d1 == d2:
            #print d1 + ' and ' + d2
            return 1.0
        else:
            return 0.3
    else:        
        return 0    

    
def is_internal(uri):
    if uri.startswith('http://apps.facebook.com/') \
        or uri.startswith('https://apps.facebook.com/') \
        or uri.startswith('https://www.facebook.com/') \
        or uri.startswith('https://www.facebook.com/') \
        or uri.startswith('http://www.facebook.com/'):
        #or uri.startswith('https://facebook.previsite.net/'):
        return True
    else:
        return False

def redirect_uri_analysis(data):
    # redirect_uri analysis
    no_uri = 0
    internal = 0
    external = 0
    domain = []

    for record in data:        
        if record['redirect_uri'] == {} or record['redirect_uri'] == None:
            no_uri += 1
        elif is_internal(record['redirect_uri']):            
            internal += 1
        else:
            #print uri
            domain.append(tldextract.extract(record['redirect_uri']).domain)
            external += 1        

    print 'nouri: ' + str(no_uri)
    print 'internal: ' + str(internal)
    print 'external: ' + str(external)    
    print 'unique domain: ' + str(len(set(domain)))

    domain_map = {}

    for record in data:
        uri = record['redirect_uri']
        if uri == {} or uri == None:
            continue
        if not is_internal(uri):
            dom = tldextract.extract(uri).domain
            if dom in domain_map:
                domain_map[dom] += 1
            else:
                domain_map[dom] = 1
    
    for key, value in sorted(domain_map.iteritems(), key = lambda (k,v): (v,k)):
        print "%s: %d" % (key, value)

def permissions_analysis(data):
    # permissions analysis
    perms = []
    perm_uniq = 0
    perm_cnt = [0] * 65
    #print len(data)
    for record in data:
        perm_cnt[len(record['permissions'])] += 1
        #if (len(record['permissions']) == 35):
        #    print record['id']
        for perm in record['permissions']:
            perm = perm.strip()
            if perm != '' and perm not in perms:
                perm_uniq += 1
                perms.append(perm)

    # histogram of number of requested permissions
    for i in range(1, 65):
        print str(perm_cnt[i])

    print 'unique permissions: ' + str(perm_uniq)

def permissions_similarity(data):
    # permissions similarity
    perm_simi = {}
    for record1 in data:
        for record2 in data:
            perm_set = record1['id'] + record2['id']
            tot = len(set(perm_set));
            if tot != 0:
                perm_simi[record1['id'] + '-' + record2['id']] = \
                    1.0 * intersect(record1['permissions'], record2['permissions']) / tot
            else:
                perm_simi[record1['id'] + '-' + record2['id']] = 0

    # write to json file
    with open('permissions.json', 'w') as outfile:
        json.dump(perm_simi, outfile)


def redirect_uri_similarity(data):
    # redirect_uri similarity
    uri_simi = {}
    for record1 in data:
        for record2 in data:
            uri_simi[record1['id'] + '-' + record2['id']] = \
                compute_uri_similarity(record1['redirect_uri'], record2['redirect_uri'])            
    
    # write to json file
    with open('uri_similarity.json', 'w') as outfile:
        json.dump(uri_simi, outfile)


def company_similarity(app_id, data):
    company_simi = {}
    for id1 in app_id:
        for id2 in app_id:
            company_simi[id1 + '-' + id2] = 0
            if id1 in data and id2 in data:
                if data[id1] == data[id2]:
                    company_simi[id1 + '-' + id2] = 1
            elif id1 not in data and id2 not in data:
                company_simi[id1 + '-' + id2] = 0.876

    # write to json file
    with open('company_similarity.json', 'w') as outfile:
        json.dump(company_simi, outfile)


def post_similarity(app_id, data):
    post_simi = {}
    for id1 in app_id:
        for id2 in app_id:
            post_simi[id1 + '-' + id2] = 0
            if id1 in data and id2 in data:
                uri1 = data[id1]
                uri2 = data[id2]
                maxi = 0                
                for u1 in uri1:
                    for u2 in uri2:
                        maxi = max(maxi, compute_uri_similarity(u1, u2))
                post_simi[id1 + '-' + id2] = maxi
        
    # write to json file
    with open('post_similarity.json', 'w') as outfile:
        json.dump(post_simi, outfile)

def main():
    
    json_data = open('app_info.json')
    data = json.load(json_data)

    redirect_uri_analysis(data)
    permissions_analysis(data)

    permissions_similarity(data)
    redirect_uri_similarity(data)

    json_data = open('final_ids.json')
    app_id = json.load(json_data)

    json_data = open('app_company.json')
    data = json.load(json_data)
    
    company_similarity(app_id, data[0])

    json_data = open('post_links.json')
    data = json.load(json_data)
    post_similarity(app_id, data)
        
if __name__ == '__main__':
    main()

