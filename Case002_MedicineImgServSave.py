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

class MedicineImgServSave(Readini.Config):
    '''
    1.三维医学图像重建服务保存
    2.form_data_post返回请求结果
    '''
    def __init__(self):
        super(MedicineImgServSave,self).__init__()

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
        self.result= requests.post(url= self.BaseUrl + "/changmugu-basic/medicineImg/MedicineImgServSave",
                                    data= json.dumps(params),
                                    headers= self.headers,
                                    verify= False)
        if self.checks():
            print("请求参数:")
            print(params)
            print("请求地址:")
            print(self.BaseUrl + "/changmugu-basic/medicineImg/MedicineImgServSave")
            print()
        return self.result


class BeginMISSTest(Readini.ParametrizedTestCase,Readini.Config):
    '''使用unittest进行MedicineImgServSave接口测试'''
    def setUp(self):
        super().cfg_general()
        self.t= MedicineImgServSave()
        self.r= self.t.form_data_post(
            Readini.create_parameter_dict(
                directionId= self.param[1],
                docImp= self.param[2],
                isOpenInvoice= self.param[3],
                jointId= self.param[4],
                openId= self.param[5],
                patientId= self.param[6],
                userId= self.param[7],
                bankName= self.param[8],
                bankNum= self.param[9],
                coAddress= self.param[10],
                email= self.param[11],
                imgServCode= self.param[12],
                imgServMoney= self.param[13],
                imgServName= self.param[14],
                invoiceHead= self.param[15],
                invoiceName= self.param[16],
                invoiceNum= self.param[17],
                invoiceType= self.param[18],
                pcServCode= self.param[19],
                pcServCount= self.param[20],
                pcServMoney= self.param[21],
                pcServName= self.param[22],
                servId= self.param[23],
                telNo= self.param[24],
            ))
        self.formR= json.loads(self.r.text)
        print("返回参数:")
        print(self.formR)
        print()

        if self.param[0]== '0':
            with open("Temporary/002.txt", "a+") as f:
                f.write(str(self.formR) + "\n")
        else:
            pass
        # 将返回参数写入文件，便于之后接口调用

    def testX(self):
        self.doc= self.param[-1]  # 重写了源文件get_testcase_property，来读取我用例文档的title列
        if self.param[0]== '0':
            self.assertEqual(self.formR["code"],20000)
        elif self.param[0]== '1':
            self.assertNotEqual(self.formR["code"],20000)
        else:
            raise Exception


def runners():
    '''
    读取测试用例文件，加载成list用于循环
    :return:
    '''
    suite= unittest.TestSuite()
    list_open= []
    file= "Cases_File/Case002_MedicineImgServSave.xls"
    sheet1= xlrd.open_workbook(filename= file).sheet_by_index(0)
    for i in range(1,sheet1.nrows):
        rows= sheet1.row_values(i)
        list_open.append(rows)
    for i in list_open:
        suite.addTest(Readini.ParametrizedTestCase.parametrize(BeginMISSTest, param= i))
    result= BeautifulReport(suite)
    result.report(filename= "接口测试报告_Case002_MedicineImgServSave",
                  description= "MedicineImgServSave接口测试报告",
                  report_dir= "report",
                  theme= "theme_memories")


if __name__== '__main__':
    Readini.delete_temp("002.txt")
    runners()

