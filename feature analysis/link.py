import json
import simplejson
import os

def read_json(filename):
    f = open(filename, 'r')
    decoded_file = json.load(f)
    return decoded_file

def write_json(filename, data):
    fd = open(filename, 'w')
    json_data = simplejson.dumps(data, indent = 4)
    fd.write(json_data)
    fd.close()
    

def main():
    os.chdir("E:\\facebook project\\1201")
    data = read_json('installed_posts.json')
    link_dict = dict()
    for post in data:
        link_list = list()
        if post['application']['id'] not in link_dict.keys():
            link_dict[post['application']['id']] = list()
        link_dict[post['application']['id']].append(post['link'])
    links = dict()
    for app_id in link_dict.keys():
        link_set = set(link_dict[app_id])
        links[app_id] = list(link_set)
    write_json('post_links.json', links)

if __name__ == '__main__':
    main()
