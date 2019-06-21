import json

from common_fun import ssh_mysql2, save_item_to_file


def dumpShopId():
    sqlstat3 = 'select shop_id,shop_name from shop_detail where shop_region is not null'
    columnlist3 = ['shop_id', 'shop_name']

    shop_dict = {}
    item3 = ssh_mysql2(sqlstat3, columnlist3)

    for ele in item3:
        shop_dict[ele['shop_id']] = ele['shop_name']
    print(shop_dict)
    for ele in shop_dict:
        save_item_to_file('shop_id', 'http://www.yytvip.com/company/' + str(ele) + '\n')


def dumpCompany():
    sqlstat3 = 'select distinct cd.company_id,cd.company_name from shop_detail t join company_shop cs on (t.shop_id = cs.shop_id) join company_detail cd on (cs.company_id = cd.company_id) order by company_name desc'
    columnlist3 = ['company_id', 'company_name']

    com_dict = {}
    item3 = ssh_mysql2(sqlstat3, columnlist3)

    for ele in item3:
        com_dict[ele['company_id']] = ele['company_name']
    print(com_dict)
    for ele in com_dict:
        save_item_to_file('com_id', 'http://www.yytvip.com/companyDetail/' + str(ele) + '\n')

def dumpbaidu():
    sqlstat3 = "select shop_id, shop_latlng as uid from shop_detail t where t.data_from = 'bd_beijing'"
    columnlist3 = ['shop_id', 'uid']

    com_dict = {}
    item3 = ssh_mysql2(sqlstat3, columnlist3)

    for ele in item3:
        com_dict[ele['uid']] = ele['shop_id']
    with open('./review3.json', 'r', encoding='utf-8') as f:
        file = f.readlines()
    item_list = []
    for ele in file:
        tmp = ele.replace('\n', '')
        item = json.loads(tmp)
        item_list.append(item)
    error = 0
    for ele in item_list:
        if ele['uid'] in com_dict:
            ele['shop_id'] = str(com_dict[ele['uid']])
        else:
            error += 1
            ele['shop_id'] = 'error!!!'
            print('failed :' + ele['uid'])
        taa = json.dumps(ele, ensure_ascii=False) + '\n'
        save_item_to_file('./review4.json', taa)
    print(error)
    print('End !!!')



if __name__ == '__main__':
    dumpbaidu()