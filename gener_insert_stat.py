import json
from common_fun import (get_mysql_data,
                        save_item_to_file)
import json

from common_fun import (get_mysql_data,
                        save_item_to_file)


def get_shopdetail_insert():
    timestr = str('')
    shopdetailsql = 'insert_Shop_Detail-'+timestr+'.txt'
    strList = []
    # file = open('shop_detail.json','r',encoding='utf-8')
    # itemList = json.load(file)
    with open('shop_detail_from_comment-2019-05-22-15-26-59.json', 'r') as f:
        file = f.readlines()
    # itemList = json.loads(file)
    # insertStr = []
    # insertStr = json.loads(itemList)
    for ele in file:
        # item = json.loads(ele)
        # itemStr='('
        # for key in ele:
        #     itemStr += str(ele[key]) + ','
        # itemStr += '),'

        strList.append(ele.replace("},", "}").replace("'{", "{"))

    itemlist= []
    for ele in strList:
        item = json.loads(ele)
        itemlist.append(item)

    tb= 'shop_detail'


    for ele in itemlist:
        ls = [(k, ele[k]) for k in ele if ele[k]]
        sentence = 'INSERT %s (' % tb + ','.join([i[0] for i in ls]) +\
                ') VALUES (' + ','.join(['%r' % i[1] for i in ls]) + ');'
        print(sentence)
        save_item_to_file(shopdetailsql,sentence+'\n')

def get_commentdetail_insert():
    strList = []

    with open('comment_list.json', 'r') as f:
        file = f.readlines()

    for ele in file:      
        strList.append(ele.replace("},", "}").replace("'{", "{"))
    
    itemlist= []
    for ele in strList:
        item = json.loads(ele)
        itemlist.append(item)

    insertlist = []
    for ele in itemlist:
        insertstr = '('
        for key in ele:
            if key != 'comment_follows':
                insertstr += ('"' + ele[key] + '", ')
            else:
                insertstr += ('"' + ele[key] + '" ), ')
            insertstr += '\n'
            insertlist.append(insertstr)
        print(insertstr)
        save_item_to_file('insert_comment.txt',insertstr)

def get_region_insert():
    with open('/Users/tangtonglong/Downloads/shop_id.txt', 'r',encoding='utf-8') as f:
        file = f.readlines()
    formated = []
    for ele in file:
        aa = str(ele.split("\t")[0]) + '\t2_' + str(ele.split("\t")[-1])
        formated.append(aa)
    print(formated)

def get_region_data():
    sqlstat = "select region_code, region_name, region_level, pid, pid_path from reigon"
    columnlist = [ 'region_code', 'region_name', 'region_level', 'pid', 'pid_path']
    resultdictlist = get_mysql_data(sqlstat,columnlist)
    print(resultdictlist)

def gener_bd_shop_sql():
    with open('./bdshop2.json', 'r', encoding='utf-8') as f:
        file = f.readlines()
    item_list = []
    item_set = set()
    for ele in file:
        item_set.add(ele.replace('\n', ''))

    for ele in item_set:
        item = json.loads(ele)
        item.pop('shop_region_name')
        item['data_from'] = 'baidu'
        item['shop_latlng'] = item['uid']
        item.pop('uid')
        item_list.append(item)

    for ele in item_list:
        ls = [(k, ele[k]) for k in ele if ele[k]]
        sentence = 'INSERT %s (' % 'shop_detail' + ','.join([i[0] for i in ls]) +\
                ') VALUES (' + ','.join(['%r' % i[1] for i in ls]) + ');'
        print(sentence)
        save_item_to_file('./bdshop2.sql', sentence + '\n')

def gener_bd_comment_sql():
    with open('./review4.sjon', 'r', encoding='utf-8') as f:
        file = f.readlines()

    item_list = []
    for ele in file:
        item = json.loads(ele.replace('\n', ''))
        item_list.append(item)

                


def main():
    # get_shopdetail_insert()
    # get_commentdetail_insert()
    # get_region_insert()
    # get_region_data()
    # get_all_shopId()
    gener_bd_shop_sql()

if __name__ == '__main__':
    main()