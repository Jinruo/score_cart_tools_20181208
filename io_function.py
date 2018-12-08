import pandas as pd
import numpy as np
import pickle
import openpyxl
from openpyxl import load_workbook


def save_dol(file_dir, name_to_save, file_to_save, win=True):
    # 函数的作用是把list或者字典存上
    # file_dir是要存储的路径，是一个文件夹
    # name_to_save是要存储的名字
    if win:
        file_dir_name = file_dir+'\\'+name_to_save
    else:
        file_dir_name = file_dir+'/' + name_to_save
    output = open(file_dir_name, 'wb')
    pickle.dump(file_to_save, output)
    output.close()
    return
##################################


def load_dol(file_dir, name_to_load, win=True):
    # 从pickle文件里面去读字典或者序列
    if win:
        file_dir_name = file_dir + '\\' + name_to_load
    else:
        file_dir_name = file_dir + '/' + name_to_load
    output = open(file_dir_name, 'rb')
    result = pickle.load(output)
    output.close()
    return result


def dataFrame2sheet(dataframe_list, excelPath, name_list, index_col=None):
    # dataframe_list的长度与name_list要相等
    # DataFrame 转换成excel中的sheet表
    # excelPath 要写上完整的路径+Excel的名字，也就是说名字是事先起好的
    excelWriter = pd.ExcelWriter(excelPath, engine='openpyxl')
    for df_x, s_name in zip(dataframe_list, name_list):
        df_x.to_excel(excel_writer=excelWriter,
                      sheet_name=s_name, index=index_col)

    excelWriter.save()
    excelWriter.close()


def excelAddSheet(dataframe_list, excelPath, name_list, index_col=None):
    excelWriter = pd.ExcelWriter(excelPath, engine='openpyxl')
    book = load_workbook(excelWriter.path)
    excelWriter.book = book
    for df_x, s_name in zip(dataframe_list, name_list):
        df_x.to_excel(excel_writer=excelWriter,
                      sheet_name=s_name, index=index_col)
    excelWriter.close()
