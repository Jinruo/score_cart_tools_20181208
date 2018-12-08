import pandas as pd
import numpy as np
class Nan_pro():
    def __init__(self,df_cuted,col_name):
        self.df = df_cuted
        self.col =  col_name
        tmp = list(df_cuted)
        tmp.remove(col_name)
        self.col_list = tmp
    def processing(self,nan_name = '空值'):
        df_cut_999 = self.df.copy()
        df_cut_nan = self.df.copy()
        for x in self.col_list:
            df_cut_999[x] = df_cut_999[x].astype('object')
            df_cut_nan[x] = df_cut_nan[x].astype('object')
            df_cut_999[x] = df_cut_999[x].fillna('999')
            if len(df_cut_999) != self.df[x].count():
                if len(self.df)-self.df[x].count()> int(len(self.df)*0.05):
                    df_cut_nan[x] = df_cut_nan[x].fillna(nan_name)
                else:
                    rate_se = self.df.groupby([x]).apply(lambda surf: surf[self.col].sum()/ surf[self.col].count())
                    rate_se999 = df_cut_999.groupby([x]).apply(lambda surf: surf[self.col].sum()/ surf[self.col].count())
                    index_list = list(rate_se.index)
                    value_list = list(rate_se.values)
                    the_999_rate = rate_se999['999']
                    diff_list = []
                    for i in value_list:
                        diff_list.append(abs(i- the_999_rate))
                    neatest_position = diff_list.index(min(diff_list))
                    df_cut_nan[x] = df_cut_nan[x].fillna(index_list[neatest_position])
        return df_cut_nan
        
    def CalcWOE(self,df_cut_999, target):
    
#    :param df: dataframe containing feature and target
#    :param target: the feature that needs to be calculated the WOE and iv, usually categorical type
#    :param col: good/bad indicator
#    :return: WOE and IV in a dictionary
    
        total = df_cut_999.groupby([target])[self.col].count()
        total = pd.DataFrame({'total': total})
        bad = df_cut_999.groupby([target])[self.col].sum()
        bad = pd.DataFrame({'bad': bad})
        regroup = total.merge(bad, left_index=True, right_index=True, how='left')
        regroup.reset_index(level=0, inplace=True)
        N = sum(regroup['total'])
        B = sum(regroup['bad'])
        regroup['good'] = regroup['total'] - regroup['bad']
        G = N - B
        regroup['bad_pcnt'] = regroup['bad'].map(lambda x: x*1.0/B)
        regroup['good_pcnt'] = regroup['good'].map(lambda x: x * 1.0 / G)
        regroup['WOE'] = regroup.apply(lambda x: np.log(x.bad_pcnt*1.0/x.good_pcnt),axis = 1)
        WOE_dict = regroup[[target,'WOE']].set_index(target).to_dict(orient='index')
        for k, v in WOE_dict.items():
            WOE_dict[k] = v['WOE']
        IV = regroup.apply(lambda x: (x.bad_pcnt-x.good_pcnt)*np.log(x.bad_pcnt*1.0/x.good_pcnt),axis = 1)
        IV = sum(IV)
        
        return {"WOE": WOE_dict, 'IV':IV}

    def woe_design(self,df_cut_999):
        IV_woe_D = {}
        for x in self.col_list:
            IV_woe_D[x] = self.CalcWOE(df_cut_999, x)
            df_cut_999[x] = df_cut_999[x].map(IV_woe_D[x]['WOE'].get)
        return df_cut_999