#-*- coding: UTF-8 -*-
import time,os
import unittest
import configparser as cp
import pymysql



class Config(object):
    def cfg_general(self):
        '''
        读取ini配置文件
        :return: None
        '''
        self.cfg= cp.ConfigParser()
        self.cfg.read("Config.ini",encoding= "utf-8")
        self.BaseUrl= self.cfg.get("Parameter","BaseUrl")
        return [self.BaseUrl,]

    def cfg_db(self):
        '''general
        链接数据库参数
        :return:返回数据库参数
        '''
        self.cfg= cp.ConfigParser()
        self.cfg.read("Config.ini",encoding= "utf-8")
        self.dburl= self.cfg.get('Mysql', 'DBurl')
        self.username= self.cfg.get('Mysql', 'username')
        self.password= self.cfg.get('Mysql', 'password')
        self.dbname=self.cfg.get('Mysql', 'dbname')
        self.dbport= self.cfg.get('Mysql','port')
        return [self.dburl,self.username,self.password,self.dbname,self.dbport]


class ParametrizedTestCase(unittest.TestCase):
    '''
    1.可实现传入测试用例list自动创建用例集，
    2.不用手动根据用例进行，即 def testcase():pass,
    3.用例csv必须有标志位用于判断，如pass状态设置为0，
    4.继承时，必须以test开头，如testX()
    '''
    def __init__(self, methodName='runTest', param=None):
        super(ParametrizedTestCase, self).__init__(methodName)
        self.param= param

    @staticmethod
    def parametrize(testcase_klass, param=None):
        testloader= unittest.TestLoader()
        testnames= testloader.getTestCaseNames(testcase_klass)
        suite= unittest.TestSuite()
        for name in testnames:
            suite.addTest(testcase_klass(name, param= param))
        return suite


def create_parameter_dict(**kwargs):
    '''
    用例中如果某参数的值为no，则此参数进行不传输测试
    :param kwargs:调用时需自己加入key值
    :return:重新组成的dict
    '''
    empty_dict= {}
    for i in kwargs.items():
        if i[1]== 'no':
            pass
        else:
            empty_dict[i[0]]= i[1]
    return empty_dict


def create_parameter_dict_2(nesting):
    '''
    递归用于处理嵌套字典的接口参数
    用例中如果某参数的值为no，则此参数进行不传输测试
    :param nesting: 例字典{'a':1,'b':'no','c':[{'d':'no','e':2},{'d':1,'e':'no'}],'f':3,'g':'no'}
    :return:{'a': 1, 'c': [{'e': 2}, {'d': 1}], 'f': 3}
    '''
    for key in list(nesting.keys()):
        if type(nesting.get(key))== dict:
            create_parameter_dict_2(nesting.get(key))
        elif type(nesting.get(key))== list:
            for i in nesting.get(key):
                create_parameter_dict_2(i)
        else:
            if nesting.get(key)== 'no':
                del nesting[key]
    return nesting


def format_time(param):
    '''
    格式化时间
    :param para:
    :return:
    '''
    if param== 1:
        return (int(round(time.time() * 1000))) # 13位的时间戳
    elif param== 2:
        return (time.strftime("%X",time.localtime()))


def delete_temp(name:str):
    '''
    运行创建用例时，把历史文件删除
    :param name:
    :return:
    '''
    path= "Temporary/"+name
    if os.path.exists(path):
        os.remove(path)
    else:
        pass


def get_expire_time(orderId,Time_or_Status):
    '''
    根据orderId查询到是否存在过期时间或者订单状态
    :param orderId: 订单的id
    :return:
    '''
    cfg_db= Config().cfg_db()
    db= pymysql.connect(host= cfg_db[0],user= cfg_db[1],
                        password= cfg_db[2],database= cfg_db[3])
    cursor= db.cursor() # 使用cursor()方法获取操作游标

    if Time_or_Status== "Time":
        # 查询是否存在过期时间
        sql= "SELECT expire_time FROM medicine_img_order WHERE order_id= '%s'" % (orderId)
        try:
            cursor.execute(sql)
            results= cursor.fetchall()
            result_list= []
            for row in results:
                expire_time= row[0]
                if expire_time!= None:
                    result_list.append(expire_time)
            db.close()
            if len(result_list)== 1:    # 列表长度为1，才是正确的。其余长度都是错误
                return True
            else:
                return False
        except:
            db.close()
            return False
    elif Time_or_Status== "3":
        # 查询已关闭订单
        sql= "SELECT order_status FROM medicine_img_order WHERE order_id= '%s'" % (orderId)
        try:
            cursor.execute(sql)
            results= cursor.fetchall()
            result_list= []
            for row in results:
                status= row[0]
                if status== str(3): # 3为订单已关闭
                    result_list.append(status)
            db.close()
            if len(result_list)== 1:    # 列表长度为1，才是正确的。其余长度都是错误
                return True
            else:
                return False
        except:
            db.close()
            return False
    elif Time_or_Status== "1":
        # 查询待支付订单
        sql= "SELECT order_status FROM medicine_img_order WHERE order_id= '%s'" % (orderId)
        try:
            cursor.execute(sql)
            results= cursor.fetchall()
            result_list= []
            for row in results:
                status= row[0]
                if status== str(1): # 1为订单待支付
                    result_list.append(status)
            db.close()
            if len(result_list)== 1:    # 列表长度为1，才是正确的。其余长度都是错误
                return True
            else:
                return False
        except:
            db.close()
            return False



if __name__== '__main__':
    # print(create_parameter_dict_2({'a':1,'b':'no','c':[{'d':'no','e':2},{'d':1,'e':'no'}],'f':3,'g':'no'}))
    # delete_temp("005.txt")
    print(get_expire_time("F20220602-93558-018","1"))
    pass