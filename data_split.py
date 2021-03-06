# -*- coding: utf-8 -*-
"""
Created on Sun Dec  3 16:38:08 2017

@author: pro3
"""

from datetime import datetime
import numpy as np
import generateFeatures

def splitdata(df,startDatetime,endDatetime):
    startDatetime = datetime.strptime(startDatetime,'%Y-%m-%d').date()
    endDatetime = datetime.strptime(endDatetime,'%Y-%m-%d').date()
    
    train_set = df[df['voucher_received_date'].apply(lambda x: True if x>=startDatetime and x<=endDatetime else False)]
    if 'used?' in train_set.columns.tolist():
        print("N:{},P:{}, N/P:{}".format(train_set.shape[0]-sum(train_set['used?']==1),sum(train_set['used?']==1),(train_set.shape[0]-sum(train_set['used?']==1))/sum(train_set['used?']==1)))    
    
    indexes = train_set.reset_index()['index']
    if 'used?' in train_set.columns.tolist():
        train_set_target = train_set['used?'][indexes]
    else:
        train_set_target = 1
    return train_set,train_set_target
    
if __name__ == '__main__':
    #target_name = 'repurchase_15?'
    #target_name = 'repurchase_30?'
    #target_name = 'repurchase_60?'
    target_name = 'repurchase_90?'
    #target_name = 'used?' 
    
    #split into training sets
    ''' set 1: 
    ''' 
    ''' train '''
    train_startDatetime = '2017-04-01'
    train_EndDatetime = '2017-08-09'   
    train_set_1,train_set_1_target = splitdata(train_data,train_startDatetime,train_EndDatetime)
        
       
    ''' predict '''   
    startDatetime = '2017-08-10'
    endDatetime = '2017-08-16'
    predict_set,predict_set_target = splitdata(predict_data,startDatetime,endDatetime)
        

    #step 0
    #filter train_data select those users in all data
    common_users = list(set(train_set_1['userid']) & set(predict_set['userid']) ) #& set(validate_set_1['userid']) 
    #65350
    def filterByUserid(data,target):
        temp = data.copy()
        temp['target'] = target.values
        #temp = pd.concat([temp[temp['target']==0].sample(n=sum(Ytrain)*5),temp[temp['target']==1]])
        temp = temp[temp['userid'].isin(common_users)]
        data = temp.iloc[:,:-1]
        target = temp.iloc[:,-1]
        print("After filtering, P:{},N:{}, N/P:{}".format(sum(target),data.shape[0]-sum(target),(data.shape[0]-sum(target))/sum(target)))
        return data,target
    
    a=len(set(train_set_1['userid']))
    b=len(common_users)
    print('train old:{},new:{},new/old:{}'.format(a,b,b/a))
    
    a=len(set(predict_set['userid']))
    print('predict old:{},new:{},new/old:{}'.format(a,b,b/a))
    
    train_set_1,train_set_1_target = filterByUserid(train_set_1,train_set_1_target)
    
    
    #generate features
    train_set_1_features = generateFeatures.generateFeatureOfData(train_set_1,train_set_1,user_profiles_MY,
                                                        voucher_mechanics,transactions_MY[transactions_MY['order_date'].apply(lambda x: True if x<=datetime.strptime(train_EndDatetime,'%Y-%m-%d').date() else False)],
                                                        view_log_0,voucher_distribution_active_date,train_data)
    train_set_1_features.replace(np.inf,0,inplace=True)
    train_set_1_features.replace(np.nan,0,inplace=True)
    train_set_1_features.to_csv('train_set_1_features_'+target_name[:-2]+'_'+train_startDatetime+'_'+str(train_EndDatetime)+'.csv')
    train_set_1_target.to_csv('train_set_1_target_'+target_name[:-2]+'_'+train_startDatetime+'_'+str(train_EndDatetime)+'.csv')
            
    
#    validate_set_1_features = generateFeatures.generateFeatureOfData(validate_set_1,validate_set_1,user_profiles_MY,
#                                                        voucher_mechanics,transactions_MY[transactions_MY['order_date'].apply(lambda x: True if x<=datetime.strptime(validate_EndDatetime,'%Y-%m-%d').date() else False)],
#                                                        view_log_0,voucher_distribution_active_date)
#    validate_set_1_features.replace(np.inf,0,inplace=True)
#    validate_set_1_features.replace(np.nan,0,inplace=True)
#    validate_set_1_features.to_csv('validate_features_set_1_'+validate_StartDatetime+'_'+str(validate_EndDatetime)+'.csv')
#    validate_set_1_target.to_csv('validate_target_set_1_'+validate_StartDatetime+'_'+str(validate_EndDatetime)+'.csv')
#        
#    test_set_1_features = generateFeatures.generateFeatureOfData(test_set_1,train_set_1,user_profiles_MY,
#                                                        voucher_mechanics,transactions_MY[transactions_MY['order_date'].apply(lambda x: True if x<=datetime.strptime(test_EndDatetime,'%Y-%m-%d').date() else False)],
#                                                        view_log_0,voucher_distribution_active_date)
#    test_set_1_features.replace(np.inf,0,inplace=True)
#    test_set_1_features.replace(np.nan,0,inplace=True)
#    test_set_1_features.to_csv('test_set_1_features_'+test_StartDatetime+'_'+str(test_EndDatetime)+'.csv')
#    test_set_1_target.to_csv('test_set_1_target_'+test_StartDatetime+'_'+str(test_EndDatetime)+'.csv')
         
    ''' predict '''    
    #    predict_set = predict_set[predict_set['userid'].isin(common_users)]
    predict_features = generateFeatures.generateFeatureOfData(predict_set,train_set_1,user_profiles_MY,
                                                        voucher_mechanics,transactions_MY[transactions_MY['order_date'].apply(lambda x: True if x<=datetime.strptime(endDatetime,'%Y-%m-%d').date() else False)],
                                                        view_log_0,voucher_distribution_active_date,train_data)
    predict_features.replace(np.inf,0,inplace=True)
    predict_features.replace(np.nan,0,inplace=True)
    predict_features.to_csv('predict_features_'+target_name[:-2]+'_'+startDatetime+'_'+str(endDatetime)+'.csv')
                
    


    ''' set 2: 
    ''' 
    #    ''' train '''
    train_startDatetime = '2017-04-01'
    train_EndDatetime = '2017-08-09'   
    train_set_2,train_set_2_target = splitdata(train_data,train_startDatetime,train_EndDatetime)
        
       
    ''' test '''
    test_StartDatetime = '2017-08-10'
    test_EndDatetime = '2017-08-16'  
    test_set_2,test_set_2_target = splitdata(train_data,test_StartDatetime,test_EndDatetime)
 


    #step 0
    #filter train_data select those users in all data
    common_users = list(set(train_set_2['userid']) & set(test_set_2['userid']) ) #& set(validate_set_1['userid']) 
    #17691

    train_set_2,train_set_2_target = filterByUserid(train_set_2,train_set_2_target)

    #generate features
    train_set_2_features = generateFeatures.generateFeatureOfData(train_set_2,train_set_2,user_profiles_MY,
                                                        voucher_mechanics,transactions_MY[transactions_MY['order_date'].apply(lambda x: True if x<=datetime.strptime(train_EndDatetime,'%Y-%m-%d').date() else False)],
                                                        view_log_0,voucher_distribution_active_date,train_data)
    train_set_2_features.replace(np.inf,0,inplace=True)
    train_set_2_features.replace(np.nan,0,inplace=True)
    train_set_2_features.to_csv('train_set_2_features_'+target_name[:-2]+'_'+train_startDatetime+'_'+str(train_EndDatetime)+'.csv')
    train_set_2_target.to_csv('train_set_2_target_'+target_name[:-2]+'_'+train_startDatetime+'_'+str(train_EndDatetime)+'.csv')
             
    
    
    
    test_set_2,test_set_2_target = filterByUserid(test_set_2,test_set_2_target)
    
    test_set_2_features = generateFeatures.generateFeatureOfData(test_set_2,train_set_2,user_profiles_MY,
                                                        voucher_mechanics,transactions_MY[transactions_MY['order_date'].apply(lambda x: True if x<=datetime.strptime(test_EndDatetime,'%Y-%m-%d').date() else False)],
                                                        view_log_0,voucher_distribution_active_date,train_data)
    test_set_2_features.replace(np.inf,0,inplace=True)
    test_set_2_features.replace(np.nan,0,inplace=True)
    test_set_2_features.to_csv('test_set_2_features_'+target_name[:-2]+'_'+test_StartDatetime+'_'+str(test_EndDatetime)+'.csv')
    test_set_2_target.to_csv('test_set_2_target_'+target_name[:-2]+'_'+test_StartDatetime+'_'+str(test_EndDatetime)+'.csv')
             

    ''' set 4: 
        2017-04-01~2017-07-15
        2017-07-16~2017-08-15
    ''' 

    ''' set 5:  final train
    ''' 
    
   
    ''' set 6: 
        2017-05-15~2017-07-15
        2017-07-16~2017-08-16
    ''' 
    
    
    