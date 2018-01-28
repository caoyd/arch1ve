### 1: 重庆出入境证件照片质量检测照相馆 [ MySQLHandler.py ]
    URL: http://www.cqcrj.gov.cn/article/10000492652/10000492652040.html
    MySQL: service_cq.exitentryphoto
    API: /api_cq/exitentryphoto?name=金纱&addr=李家沱一城&area=巴南&page=1&page_size=10

### 2: 重庆质监局状态查询 [ MySQLHandler.py ]
    URL: http://www.cqzj.gov.cn/ZJ_Page/SelectList.aspx
    MySQL service_cq.qualitystatus
    API: /api_cq/qualitystatus?name=耐德

### 3: 重庆地理标志查询 [ BrandCQ.py ]
    URL: http://www.cqgs.gov.cn/gzbs/sbxxcx/dlbzcq/39236.htm
    MySQL: service_cq.brandcq
    API: /api_cq/brandcq?area=奉节&name=脐橙

### 4: 重庆驰名商标 [ FamousBrandCQ.py ]
    URL: http://www.cqgs.gov.cn/gzbs/sbxxcx/cmsbcq/39235.htm
    MySQL: service_cq.famousbrand
    API: /api_cq/famousbrand?name=嘉陵&owner=嘉陵工业

### 5: 出入境受理大厅（点）地址和咨询电话 [ ExitEntryInfo.py ]
    URL: http://www.cqcrj.gov.cn/article/10000562978/10000562978010.html
    MySQL: service_cq.exitentryinfo
    API: /api_cq/exitentryinfo?name=渝中
   
### 6: 幼儿园信息查询
    URL: http://www.cqedu.cn/Category_167/Index.aspx
    MySQL: service_cq.kindergarten
    API: /api_cq/kindergarten?name=鱼洞幼儿园&area=巴南

### 7: 市级民办职业培训学校基本情况
    URL: http://www.cqhrss.gov.cn/c/2016-02-24/492819.shtml
    MySQL: service_cq.profschool
    API: /api_cq/profschool?name=新东方
    
### 8: 中职学校信息查询
    URL: http://www.cqedu.cn/Item/15325.aspx
    MySQL: service_cq.midprofschool
    API: /api_cq/midprofschool?area=万州&name=经济贸易

### 9: 在渝高校信息查询
    URL: http://www.cqedu.cn/Category_146/Index.aspx
    MySQL: service_cq.highschool
    API: /api_cq/highschool?name=文理学院&address=红河大道
    
### 10: 医院查询
    URL: http://www.cqwsjsw.gov.cn/Html/1/jyzn/index.html
    MySQL: service_cq.hospital
    API: /api_cq/hospital?name=人民医院&address=翠柏路&area=大渡口

### 11: 定点医疗机构查询(医院)
    URL: http://ggfw.cqhrss.gov.cn/QueryBLH_mainSmXz.do?code=033
    MySQL: service_cq.designatedmedical
    API: /api_cq/dm/hospital?area=巫山&name=白水村卫生室&addr=巫峡镇白水村

### 12: 定点医疗机构查询(药店)
    URL: http://ggfw.cqhrss.gov.cn/QueryBLH_mainSmXz.do?code=033
    MySQL: service_cq.designatedmedical
    API: /api_cq/dm/drugstore?area=巫溪&name=桐君阁大药房&addr=城厢镇先锋路227号

### 13: 疫苗接种点查询
    URL: http://www.cqwsjsw.gov.cn/Html/1/jbyf/index.html
    MySQL: service_cq.vaccination
    API: /api_cq/vaccination?area=万州&name=双河口街道社区卫生服务中心&addr=双河口富康路1号

### 14: 区县教委信息查询
    URL: http://www.cqedu.cn/Category_152/Index.aspx
    MySQL: service_cq.educommittee
    API: /api_cq/educommittee?name=永川区教委

### 15: 免费药具发放点查询
    URL: http://www.cqwsjsw.gov.cn/Html/1/mfyjff/index.html
    MySQL: service_cq.freemedicine
    API: /api_cq/freemedicine?area=南川区&street_town=神童镇&community_village=桂花村
    
### 16: 拟供应地块公告
    URL: http://jyzx.cqgtfw.gov.cn/ngytd/ngytd.asp 
    MySQL: service_cq.landannouncement
    API: /api_cq/landannouncement?location=李家沱

### 17: 律所查询
    URL: http://118.125.243.115/search/lawfirms.aspx
    MySQL: service_cq.lawoffice
    API: /api_cq/lawoffice?area=巴南区&name=典柯

### 18: 律师查询
    URL: http://118.125.243.115/search/lawyers.aspx
    MySQL: service_cq.lawyer
    API: /api_cq/lawyer?area=渝中区&name=朱荣&office=重庆智天

### 19: 重庆社保局
    URL: http://cq.bendibao.com/cyfw/wangdian/303.shtm
    MySQL: service_cq.socialsecurity
    API: /api_cq/socialsecurity?name=江津社保局
    
### 20: 重庆市ETC服务点
    URL: http://cq.bendibao.com/cyfw/wangdian/2253.shtm
    MySQL: service_cq.etc
    API: /api_cq/etc?name=农行双桥&addr=车城大道29号
    
### 21: 重庆市车管所
    URL: http://cq.bendibao.com/cyfw/wangdian/2085.shtm
    MySQL: service_cq.vehicleadmin
    API: /api_cq/vehicleadmin?name=巫溪县
    
### 22: 重庆市车辆检测站
    URL: http://cq.bendibao.com/cyfw/wangdian/2080.shtm
    MySQL: service_cq.vehicleinspect
    API: /api_cq/vehicleinspect?name=永川
    
### 23: 重庆民政局
    URL: http://cq.bendibao.com/cyfw/wangdian/2080.shtm
    MySQL: service_cq.civilaffair
    API: /api_cq/civilaffair?name=垫江


### 24: 重庆社保接口
URL: http://cqjy.cqhrss.gov.cn/cqwx/

#### 返回字段说明

字段 | 说明
------------ | ------------- 
name | 姓名
gender | 性别
nationality | 民族
birth_date | 出生日期
id | 身份证号
card_no | 社保卡号
personal_no | 个人编号
unit_no | 单位编号
unit_name | 单位名称
resident_type | 户口性质
work_type | 工种
insured_addr | 参保地
first_pay_date | 首次缴费时间/日期
first_insured_date | 首次参保日期
insured_status | 参保状态
account_status | 账户(卡)状态
retirement_date | 离退休时间
treatment_start_date | 待遇享受开始年月/领取失业金起始年月
insured_year | 社保年度/年度
total_month_of_year | 当年缴费月数
interest_of_year | 当年账户利息(元)
principal_of_year | 当年账户本金(元)
total_month | 累计缴费月数/缴费月数/失业前累计缴费月数/已缴费月数
total_unit_transfer | 累计单位划账存储额(元)
total_last_year | 上年末个人累计缴费本息(元)
payment_phase | 对应费款所属期/费用所属期/缴费年月
payment_base | 缴费基数/失业保险缴费基数/职工本人缴费基数
unit_payment | 单位缴纳金额(元)
personal_payment | 个人缴纳金额(元)
interest_over_year | 补缴个人跨年利息(元)
interest_this_year | 补缴个人本年利息(元)
payment_type | 缴费类型
payment_flag | 缴费标志
current_balance | 当前账户结余金额
total_account_payment | 当年账户累计支付金额
total_medical_fee | 本年医疗费累计
no_of_hospitalized | 本年住院次数
fee_item | 费款科目
unit_transfer_to_account | 单位缴费划账户金额
unit_transfer_to_plan | 单位缴费划统筹金额
medical_org_no | 医疗机构编号
medical_org_name | 医疗机构名称
medical_type | 医疗类别
large_payment | 大额支付
cash_payment | 现金支付
personal_account_payment | 个人账户支付
plan_payment | 统筹支付
other_amount | 其它补助金额
balance_date | 结算日期
injury_level | 伤残等级
certificate_no | 失业证书编号
month_remain | 失业保险金剩余月数
in_treatment | 是否享受待遇
month_of_treatment | 本次失业享受待遇月数
accounting_date | 到账日期
admin_org | 社保经办机构
unit_avg_wage | 单位上年度月平均工资


###### 登录接口
API: /api_cq/ss/login?id=身份证号&password=密码

`该API会返回名为"JSESSIONID_INVOICE"的cookie,用于后续请求`


###### 养老保险
* 参保信息

    ```
    API: /api_cq/ss/pension/info?JSESSIONID_INVOICE=cookie
    ```
* 账户信息

    ```
    API: /api_cq/ss/pension/account?JSESSIONID_INVOICE=cookie
    ```
* 缴费明细

    ```
    API: /api_cq/ss/pension/detail?JSESSIONID_INVOICE=cookie
    ```
    
###### 医疗保险
* 参保信息
    
    ```
    API: /api_cq/ss/medical/info?JSESSIONID_INVOICE=cookie
    ```
* 账户信息
    
    ```
    API: /api_cq/ss/medical/account?JSESSIONID_INVOICE=cookie
    ```
* 缴费明细
    
    ```
    API: /api_cq/ss/medical/detail?JSESSIONID_INVOICE=cookie
    ```
* 费用结算
    
    ```
    API: /api_cq/ss/medical/balance?JSESSIONID_INVOICE=cookie
    ```
    
###### 工伤保险
* 参保信息

    ````
    API: /api_cq/ss/injury/info?JSESSIONID_INVOICE=cookie
    ````
* 缴费明细

    ````
    API: /api_cq/ss/injury/detail?JSESSIONID_INVOICE=cookie
    ````
    
###### 失业保险
* 参保信息

    ````
    API: /api_cq/ss/unemployment/info?JSESSIONID_INVOICE=cookie
    ````
* 缴费明细

    ````
    API: /api_cq/ss/unemployment/detail?JSESSIONID_INVOICE=cookie
    ````
    
###### 生育保险
* 参保信息

    ````
    API: /api_cq/ss/maternity/info?JSESSIONID_INVOICE=cookie
    ````
* 缴费明细

    ````
    API: /api_cq/ss/maternity/detail?JSESSIONID_INVOICE=cookie
    ````
