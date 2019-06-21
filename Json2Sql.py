import json

from common_fun import save_item_to_file


def commentJson2Sql():
    with open('/Users/tangtonglong/eclipse-workspace/mybatisgenerator/javaio-appendfile-5.json', 'r') as f:
        file = f.readlines()

    item_list = []
    for ele in file:
        item = json.loads(ele.replace('\n', ''))
        if 'comment_user_name' in item:
            tmp = item['comment_user_name'].replace('"','“').replace("'", "‘").replace('\n','')
            item['comment_user_name'] = tmp
        if 'comment_content' in item:
            tmp = item['comment_content'].replace('"','“').replace("'", "‘").replace('\n','')
            item['comment_content'] = tmp
        if 'comment_imgs' in item:
            tmp = '"' + item['comment_imgs'] + '"'
            item['comment_imgs'] = tmp
        item_list.append(item)

    table_name = 'comment_detail'

    for ele in item_list:

        ls = [(k,  ele[k]) for k in ele if ele[k]]
        ls2 = ['%s = "%s"'%(k, ele[k]) for k in ele if ele[k]]
        sentence = 'INSERT INTO  %s (' % table_name + ', '.join([i[0] for i in ls]) +\
                ') VALUES (' + ','.join(["%r" % i[1] for i in ls]) + ') ON DUPLICATE KEY UPDATE ' + ', '.join(j for j in ls2) + ';'
        print(sentence)
        save_item_to_file('new-comment-sql.sql',sentence + '\n')




def main():
    with open('/Users/tangtonglong/PycharmProjects/Tools/file1', 'r') as f:
        file = f.readlines()

    shop_region = {}
    for ele in file:
        tmpstr = ele.replace('\n', '')
        shop_region[tmpstr.split('$$')[0]] = '2_' + tmpstr.split('$$')[1]
        sentence = 'update shop_detail t set t.shop_region = "%s" where shop_id = %s and shop_region is null;'% (shop_region[tmpstr.split('$$')[0]], tmpstr.split('$$')[0])
        print(sentence)
        save_item_to_file('update-shop-region.sql', sentence + '\n')
    print(shop_region)

if __name__ == '__main__':
    main()