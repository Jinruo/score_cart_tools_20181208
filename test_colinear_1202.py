import pandas as pd
import numpy as np
from varlable_filter_1125 import Varlable_filter
from io_function import *

#####################################################################
class Colinear_test(Varlable_filter):
    def __init__(self,df,col_name,threshold):
        Varlable_filter.__init__(self,df,col_name)
        self.threshold = threshold       
    def cor_dic(self,df_cov,col_list):
        cov_D = {}
        for x in col_list:
            df_x = df_cov[x]>self.threshold
            if df_x[df_x == True].index.tolist()!= [x]:
                cor = df_x[df_x == True].index.tolist()
                cor.remove(x)
                cov_D[x] = cor
        return cov_D
#做一个序列，由所有与其他变量有阈值内相关性的变量组成
    def coline_list(self,df_cov):
            co_list = []
            for x in df_cov.columns.tolist():
                df_x = df_cov[x]>self.threshold
                if df_x[df_x ==True].index.tolist() !=[x]:
                    co_list.extend(df_x[df_x ==True].index.tolist())
                    co_list.remove(x)
            co_list = list(set(co_list))
            return co_list
    
    def colinear_test(self,excelPath):
        import operator
        for x in self.col_list:
            self.df[x] = self.df[x].astype(float)       
        df_cov = self.df[self.col_list].corr().abs()
            #做一个字典，字典的值是与字典key相关性大于阈值的变量列表
        cov_D = self.cor_dic(df_cov,self.col_list)
            #做一个序列，由所有与其他变量有阈值内相关性的变量组成
        the_coline_list = self.coline_list(df_cov)
        #设置一个 IV字典的列表
		IV_dict_list = []
        for x in the_coline_list:
            print(x)
            if x in list(cov_D.keys()):
                print(x)
                list_tmp = cov_D[x]
                iv_dic = {}
                for x1 in list_tmp:
                    iv_dic[x1] = Varlable_filter.woe_IV(self,x1)
                iv_dic[x] = Varlable_filter.woe_IV(self,x)
				IV_dict_list.append(iv_dic)
                sorted_list = sorted(iv_dic.items(),key =operator.itemgetter(1),reverse = True)
                the_drop_list = [x[0] for x in sorted_list[1:]]
                for name in the_drop_list:
                    if name in self.col_list:
                        self.col_list.remove(name)
                    
                df_cov = self.df[self.col_list].corr().abs()#np.corrcoef(self.df[self.col_list].T)
                #df_cov = pd.DataFrame(cov,columns = self.col_list,index = self.col_list)
                cov_D = self.cor_dic(df_cov,self.col_list)  
                the_coline_list = self.coline_list(df_cov)
                if cov_D == {}:
                    break
        print(len(self.col_list))
        self.col_list.append(self.col)  
        colinear_df = self.df[self.col_list]
		#把这个字典变为df_list 
		df_list = [pd.Series(D).to_frame('Iv') for D in IV_dict_list]
		name_list = list(len(df_list))
		dataFrame2sheet(dataframe_list, excelPath, name_list, index_col=None)
        return colinear_df
	
################################################################################