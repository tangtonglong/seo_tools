
import json

from AmapAPICaller import AmapAPICaller
from common_fun import get_mysql_data, ssh_mysql2, save_item_to_file

GAODE_KEY = 'a010d5798fc1c5035f512f37d3d6c58f'

URL_PREFIX = 'https://restapi.amap.com/v3/geocode/geo?key=a010d5798fc1c5035f512f37d3d6c58f'

# http://api.map.baidu.com/geocoder/v2/?address=北京市海淀区上地十街10号&output=json&ak=您的ak&callback=showLocation
BAIDU_AK = 'A41NW3K8UUwGzSSjWPnjypteeo1snIPO'


def get_region(address):
    api_caller = AmapAPICaller(GAODE_KEY)
    item = api_caller.call_geo_lite(address, city='北京市')
    if 'info' in item and item['info'] == 'OK':
        print(item)
        if len(item['geocodes']) > 0:
            # print(item['geocodes'][0]['district'] + ' latlng: ' + str(item['geocodes'][0]['location']  ) )
            return item['geocodes'][0]['district']
        else:
            return None



def main():
    sqlstat = 'select shop_id,shop_name,shop_address,shop_latlng,shop_region from shop_detail where shop_region is null and shop_address is not null and shop_img is not null'



    columnlist = ['shop_id','shop_name','shop_address','shop_latlng','shop_region']


    item = get_mysql_data(sqlstat, columnlist)
    for ele in item:
        if 'shop_address' in ele and ele['shop_address'] is not None:
            tmp = ele['shop_address'].replace('地址：                 ', '').replace('地址：', '').replace('地址', '')
            ele['shop_address'] = tmp
            print(str(ele['shop_id']) + tmp)
            get_region(tmp)


def mab2():

    sqlstat3 = 'select region_code,region_name from seo_region where region_level = 2 and pid = 2'
    columnlist3 = ['region_code', 'region_name']

    region_dict = {}
    item3 = get_mysql_data(sqlstat3, columnlist3)

    region_list = []
    for ele in item3:
        # region_dict[ele['region_name']] = '2_' + ele['region_code']
        region_list.append(ele["region_name"])
    print(region_list)

    # sqlstat2 = 'select shop_id,shop_name,shop_address,shop_region from shop_detail t where t.shop_region is null and shop_address is not null '
    # columnlist2 = ['shop_id', 'shop_name', 'shop_address', 'shop_region']
    # item2 = ssh_mysql2(sqlstat2, columnlist2)
    # for ele in item2:
    #     if 'shop_address' in ele and ele['shop_address'] is not None:
    #         tmp = ele['shop_address'].replace('地址：                 ', '').replace('地址：', '').replace('地址', '')
    #         ele['shop_address'] = tmp
    #         # print(str(ele['shop_id']) + tmp)
    #         ele['district'] = get_region(tmp)
    #         if ele['district'] is not None:
    #             ele['shop_region'] = region_dict[ele['district']]
    #             tmpsql = 'update shop_detail set shop_region = "%s" where shop_id = %s;' %(ele['shop_region'], ele['shop_id'])
    #             save_item_to_file('new_update_shop_region.sql', tmpsql + '\n')



def mb3():
    sqlstat = "select sd.shop_id,sd.shop_name,ifnull(sd.shop_desc,'#####') as shop_desc, ifnull(cs.company_id, '#####') as company_id, ifnull(cd.company_name,'#####') as  company_name from shop_detail sd left join company_shop cs on (sd.shop_id = cs.shop_id) left join company_detail cd on cs.company_id = cd.company_id order by shop_name desc"

    columnlist = ['shop_id', 'shop_name', 'shop_desc', 'company_id', 'company_name']

    itemlist = ssh_mysql2(sqlstat, columnlist)

    for ele in itemlist:
        tmp = '店铺id: ' + str(ele['shop_id']) + ' 店铺名: ' + ele['shop_name'] + ' 店铺描述: ' + ele['shop_desc'] + ' 公司id: ' + ele['company_id'] + ' 公司名:' + ele['company_name']
        print(tmp)
        save_item_to_file('店铺简介信息公司名.txt', tmp + '\n')
    print(len(itemlist))

def mb4():
    region_dict = {'密云区': '2_c434', '延庆区': '2_c435', '怀柔区': '2_c4453', '门头沟区': '2_c4454', '平谷区': '2_c4455', '朝阳区': '2_r14', '东城区': '2_r15', '西城区': '2_r16', '海淀区': '2_r17', '丰台区': '2_r20', '石景山区': '2_r328', '昌平区': '2_r5950', '通州区': '2_r5951', '大兴区': '2_r5952', '房山区': '2_r9157', '顺义区': '2_r9158'}
    with open('./bdshop.json', 'r', encoding='utf-8') as f:
        file = f.readlines()
    for ele in file:
        item = json.loads(ele.replace('\n', ''))
        # print(item['shop_region_name'])
        region_code = region_dict[item['shop_region_name']]
        item['shop_region'] = region_code
        aaa = json.dumps(item, ensure_ascii=False) + '\n'
        save_item_to_file('./bdshop2.json', aaa)

if __name__ == '__main__':
    mb4()