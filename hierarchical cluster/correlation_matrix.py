
import json

def add_similairty(Matrix, appid_index_map, correlation, partial):
    for x in correlation:
        key = x
        value = correlation[x]
        pair = key.split('-')
        index1 = appid_index_map[pair[0]]
        index2 = appid_index_map[pair[1]]
    
        if index1 == index2:
            continue
        
        Matrix[index1][index2] += value
        if partial == True:
            Matrix[index2][index1] += value
    

if __name__ == '__main__':
    f1 = open('ids.json')
    f2 = open('../Similarity_Matrix/12.3_app_description_similarity.json')
    appid =  json.load(f1)
    correlation = json.load(f2)[0]
    
    appid_index_map = {}
    index_id_map = {}
    f3 = open("col_matrix.txt",'w')
    index = 0
    for i in appid:
        appid_index_map[i] = index
        index_id_map[index] = i
        index += 1

    # initialize the matrix
    dimension = len(appid)
    Matrix = [[0 for x in xrange(dimension)] for x in xrange(dimension)] 
    
    add_similairty(Matrix, appid_index_map, correlation, True);

    
    f2 = open('../Similarity_Matrix/company_similarity.json')    
    correlation = json.load(f2)
    add_similairty(Matrix, appid_index_map, correlation, False);

    f2 = open('../Similarity_Matrix/permissions_similarity.json')    
    correlation = json.load(f2)
    add_similairty(Matrix, appid_index_map, correlation, False);

    f2 = open('../Similarity_Matrix/post_similarity.json')    
    correlation = json.load(f2)
    add_similairty(Matrix, appid_index_map, correlation, False);

    f2 = open('../Similarity_Matrix/uri_similarity.json')    
    correlation = json.load(f2)
    add_similairty(Matrix, appid_index_map, correlation, False);
    
    s = ''
    for i in Matrix:
        s1 = ''
        for j in i:
            s1 += str(j) + ' '
        s1 = s1[:-1]
        s1 += '\n'
        s += s1
        
    f3.write(s)             

    f3.close()
    
    #print id
    #print correlation
