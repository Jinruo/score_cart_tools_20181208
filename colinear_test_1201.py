import pandas as pd
import os
import numpy as np


class Iv_cmt:
    def __init__(self,df,col):
        self.df = df
        self.col =  col
        tmp = list(df)
        tmp.remove(col)
        self.col_list = tmp
        
    def woe_IV(self,column_name): 
        small = pd.crosstab(self.df[column_name],self.df[self.col],margins = True)
        dele = small[small[1]<10]
        combin = list(dele.index)
        #print(column_name,"需要合并的字段有：",combin)  
        temp = small[small[1]<10].sum() 
        small.drop(combin,axis = 0,inplace = True)
        a = small.T
        a['AAA']=temp
        new = a.T
        al = new.ix['All']
        cou = new.drop('All',axis = 0) 
        bad_p = cou[1]/al[1]
        good_p = cou[0]/al[0]
        woe = np.log(bad_p/good_p)
        #print(woe)
        p = bad_p - good_p
        IV = (p*woe).sum()
        #return(pd.Series([woe,IV],index = ['woe','VI']) )
        return(IV)
        
    def cmt_iv(self,limited_value = -np.inf):
        woe_list = self.df.columns.tolist()
        woe_list.remove(self.col)
        times = 0
        iv_list = []
        for x in self.col_list:
            iv_v = self.woe_IV(x)
            if iv_v >limited_value:
                print(x,iv_v)  
                iv_list.append(x)
                times+=1
        print('the number of bigger then 0.02 if %f'%times)
        return iv_list
#####################################################################
class Colinear_test(Iv_cmt):
    def __init__(self,df,col_name,threshold):
        Iv_cmt.__init__(self,df,col_name)
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
    
    def colinear_test(self):
        import operator
        for x in self.col_list:
            self.df[x] = self.df[x].astype(float)       
        df_cov = self.df[self.col_list].corr().abs()
            #做一个字典，字典的值是与字典key相关性大于阈值的变量列表
        cov_D = self.cor_dic(df_cov,self.col_list)
            #做一个序列，由所有与其他变量有阈值内相关性的变量组成
        the_coline_list = self.coline_list(df_cov)
        #the_coline_list = ['add_total_inout_cut']
        for x in the_coline_list:
            print(x)
            if x in list(cov_D.keys()):
                print(x)
                list_tmp = cov_D[x]
                iv_dic = {}
                for x1 in list_tmp:
                    iv_dic[x1] = Iv_cmt.woe_IV(self,x1)
                iv_dic[x] = Iv_cmt.woe_IV(self,x)
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
        return colinear_df
################################################################################