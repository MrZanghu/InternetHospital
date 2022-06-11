#-*- coding: UTF-8 -*-
import unittest
import xlrd
import requests
import json
import Readini
from BeautifulReport import BeautifulReport
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
# 解决verify= False报错
# 在Run中选择运行，防止pycharm使用单元测试框架运行脚本，导致数据错误



print_log= 'Y'
# 是否打印请求参数

class ReplaceOrder(Readini.Config):
    '''
    1.重新下单
    2.form_data_post返回请求结果
    '''
    def __init__(self):
        super(ReplaceOrder,self).__init__()

    @staticmethod
    def checks():
        if print_log== 'Y':
            return True
        elif print_log== 'N':
            return False
        else:
            return False

    def form_data_post(self,params):
        super().cfg_general()
        self.headers= {
            "Content-Type":"application/json",
            "Authorization":"",
            "clientType":"X",
            "firmId":"dev",
            "hosId":"",
            "subjectType":"",
            "version":""
        }
        self.result= requests.post(url= self.BaseUrl + "/changmugu-order/medicineImgOrder/replaceOrder",
                                    data= json.dumps(params),
                                    headers= self.headers,
                                    verify= False)
        if self.checks():
            print("请求参数:")
            print(params)
            print("请求地址:")
            print(self.BaseUrl + "/changmugu-order/medicineImgOrder/replaceOrder")
            print()
        return self.result


class BeginROTest(Readini.ParametrizedTestCase,Readini.Config):
    '''使用unittest进行ReplaceOrder接口测试'''
    def setUp(self):
        super().cfg_general()
        self.t= ReplaceOrder()
        self.r= self.t.form_data_post(
            Readini.create_parameter_dict(
                orderId= self.param[1],
            ))
        self.formR= json.loads(self.r.text)
        print("返回参数:")
        print(self.formR)
        print()

        if self.param[0]== '0':
            with open("Temporary/005.txt", "a+") as f:
                f.write(str(self.formR) + "\n")
        else:
            pass
        # 将返回参数写入文件，便于之后接口调用

    def testX(self):
        self.doc= self.param[-1]  # 重写了源文件get_testcase_property，来读取我用例文档的title列
        if self.param[0]== '0':
            self.assertEqual(self.formR["code"],20000)
            self.assertEqual(Readini.get_expire_time(self.param[1],"3"),True) # 同时查询到1个过期时间
        elif self.param[0]== '1':
            self.assertNotEqual(self.formR["code"],20000)
            self.assertNotEqual(Readini.get_expire_time(self.param[1],"3"), True)
        else:
            raise Exception


def runners():
    '''
    读取测试用例文件，加载成list用于循环
    :return:
    '''
    suite= unittest.TestSuite()
    list_open= []
    file= "Cases_File/Case005_ReplaceOrder.xls"
    sheet1= xlrd.open_workbook(filename= file).sheet_by_index(0)
    for i in range(1,sheet1.nrows):
        rows= sheet1.row_values(i)
        list_open.append(rows)
    for i in list_open:
        suite.addTest(Readini.ParametrizedTestCase.parametrize(BeginROTest, param= i))
    result= BeautifulReport(suite)
    result.report(filename= "接口测试报告_Case005_ReplaceOrder",
                  description= "ReplaceOrder接口测试报告",
                  report_dir= "report",
                  theme= "theme_memories")


if __name__== '__main__':
    Readini.delete_temp("005.txt")
    runners()

