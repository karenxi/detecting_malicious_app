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

def search_ids(names, app_infos):
    ids = list()
    found_names = list()
    name_set = set(names)
    for app in app_infos:
        try:
            app_name = app['name']
            if app_name in name_set:
                ids.append(app['id'])
                found_names.append(app_name)
        except:
            pass
    found_set = set(found_names)
    missed_names = name_set.difference(found_set)
    return ids, list(missed_names)
            

def main():
    os.chdir("E:\\facebook project\\1130")
    #name_list = ["Wisdom", "Social Calendar", "blablabla"]
    app_infos = read_json('total_app_info.json')
    id_list, missed_names = search_ids(name_list, app_infos)
    write_json('installed_appids.json', id_list)
    write_json('missed_appnames.json', missed_names)

if __name__ == '__main__':
    main()
