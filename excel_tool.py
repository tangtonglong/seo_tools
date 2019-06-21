# -*- coding: utf-8 -*-

import codecs
import json

import xlrd


def save_item_to_file(filename,item):
        with codecs.open(filename, 'a', encoding='utf8') as f:
                f.write(item)

def read_excel():

    #文件位置

    ExcelFile=xlrd.open_workbook(r'C:\Users\ttl\Desktop\001.xlsx')

    #获取目标EXCEL文件sheet名

    print(ExcelFile.sheet_names())

    #------------------------------------

    #若有多个sheet，则需要指定读取目标sheet例如读取sheet2

    #sheet2_name=ExcelFile.sheet_names()[1]

    #------------------------------------

    #获取sheet内容【1.根据sheet索引2.根据sheet名称】

    sheet=ExcelFile.sheet_by_index(4)

    # sheet=ExcelFile.sheet_by_name('TestCase002')

    #打印sheet的名称，行数，列数

    print(sheet.name,sheet.nrows,sheet.ncols)

    #获取整行或者整列的值

    # rows=sheet.row_values(2)#第三行内容

    # cols=sheet.col_values(1)#第二列内容

    # print(cols,rows)

    #获取单元格内容

    # print(sheet.cell(1,0).value)

    # print(sheet.cell_value(1,0))

    # print(sheet.row(1)[0].value)

    #打印单元格内容格式

    # print(sheet.cell(1,0).ctype)
    item_list = []
    for i in range(0,sheet.nrows):
        tmp = {}
        for j in range(0,sheet.ncols):
            tmp[sheet.cell(0,j).value] = sheet.cell(i,j).value
            # print(sheet.cell(0,j).value + ' : ' + sheet.cell(i,j).value)
        item_list.append(tmp)
    for ele in item_list:

        ele['shop_tag'] = ele['shop_tag'].strip().replace('"', '“').replace("'", "‘").replace(',', ' ')
        ele['shop_name'] = ele['shop_name'].replace('"', '“').replace("'", "‘")
        ele['shop_address'] = ele['shop_address'].replace('"', '“').replace("'", "‘")
        ele['shop_price'] = str(ele['shop_price']).replace('.0', '')
        ele['shop_star'] = str(ele['shop_star']).replace('.0', '').replace('.', '')
        if len(str(ele['shop_star']).strip()) < 1:
            ele['shop_star'] = '0'
        elif len(str(ele['shop_star']).strip()) == 1 and str(ele['shop_star']).strip() != '0':
            ele['shop_star'] += '0'
            
        item = json.dumps(ele, ensure_ascii=False) + '\n'
        save_item_to_file('./bdshop.json', item)


def xxx():
    ExcelFile=xlrd.open_workbook(r'C:\Users\ttl\Desktop\001.xlsx')

    #获取目标EXCEL文件sheet名

    print(ExcelFile.sheet_names())

    sheet=ExcelFile.sheet_by_index(5)

    print(sheet.name,sheet.nrows,sheet.ncols)

    
    for i in range(0,sheet.nrows):
        tmp = sheet.cell(i,0).value
        index = tmp.find('ty:2,uid:')
        if index > 0:
            stra = tmp[index+9:].replace(',', '').replace('\n', '')
            
            save_item_to_file('./uid', stra + '\n')
            
    # for ele in item_list:
    #     if len(str(ele['shop_star']).strip()) < 1:
    #         ele['shop_star'] = '0'
    #     ele['shop_tag'] = ele['shop_tag'].strip().replace('"', '“').replace("'", "‘").replace(',', ' ')
    #     ele['shop_name'] = ele['shop_name'].replace('"', '“').replace("'", "‘")
    #     ele['shop_address'] = ele['shop_address'].replace('"', '“').replace("'", "‘")
    #     ele['shop_price'] = str(ele['shop_price'])
    #     ele['shop_star'] = str(ele['shop_star']).replace('.0', '')
    #     item = json.dumps(ele, ensure_ascii=False) + '\n'
    #     save_item_to_file('./bdshop.json', item)

def yyy():
    with open('./uid', 'r', encoding='utf-8') as f:
        file = f.readlines()

    uid_set = set()
    for ele in file:
        uid_set.add(ele.replace('\n', ''))
    print(len(uid_set))

if __name__ =='__main__':
    yyy()
    # read_excel()