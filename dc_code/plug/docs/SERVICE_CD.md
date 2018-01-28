### 0: 空气质量查询 [ AirQuality.py ]
    URL: http://www.cdepb.gov.cn/cdepbws/Web/gov/airquality.aspx
    API: /api/aq
    
### 1: 成都市城乡房产管理局 - 维修服务机构查询 [ MySQLHandler.py ]
    URL: http://www.cdfgj.gov.cn/WXZJ/FixServeOrg.aspx
    MySQL: service_cd.fixserveorg
    API: /api/fixserveorg?org_name=名称&service_type=类型&page=1&page_size=20

### 2: 发行单位查询 [ MySQLHandler.py ]
    URL: http://www.gapp.gov.cn/zongshu/serviceList3.shtml
    MySQL: service_cd.issueorg
    API: /api/issueorg?org_name=名称&issue_type=类型&page=1&page_size=20
    
### 3: 出版物单位查询(图书,音像,电子出版物, 3个接口) [ MySQLHandler.py ]
    URL: http://www.gapp.gov.cn/zongshu/serviceSearchListbve.shtml
    MySQL: service_cd.publishingorg
    API: /api/publishingorg?name=电子科大&region=四川&admin_unit=教育部&host_unit=电子科技大学&type=图书
    
### 6: 成都市小学新生入学划片区域 [ MySQLHandler.py ]
    URL: http://www.chengdu.gov.cn/servicelist/xxjy04/
    MySQL: service_cd.elemschool
    API: /api/elemschool?school=泡桐&district=高新区&page=1

### 7: 国家环境保护标准 [ MySQLHandler.py ]
    URL: http://datacenter.mep.gov.cn/trs/query.action
    MySQL: service_cd.env_protection_std
    API: /api/envstd?std_no=HJ 799-2016&std_name=水溶性阴离子&page=1
    
### 8: 司法鉴定收费项目和收费标准基准价 [ MySQLHandler.py ]
    URL: http://www.chengdu.gov.cn/servicelist/jdgz04/
    MySQL: service_cd.judicialfee
    API: /api/judicialfee?name=尸表检验

### 9: 成都市因私出入境办证地点及咨询电话 [ MySQLHandler.py ]
    URL: http://www.chengdu.gov.cn/servicelist/hz01/
    MySQL: service_cd.exitentry
    API: /api/exitentry?name=崇州

### 10: 成都市预防接种疫苗门诊 [ MySQLHandler.py ]
    URL: http://www.cdwjw.gov.cn/art/2016/4/25/art_74_28280.html
    MySQL: service_cd.vaccine
    API: /api/vaccine?name=石羊&area=高新
   
### 11: 律师事务所查询 [ MySQLHandler.py ]
    URL: http://www.cdslsxh.org/lszx/index.html
    MySQL: service_cd.lawoffice
    API: /api/lawoffice?name=志众&area=金牛

### 12: 律师查询 [ MySQLHandler.py ]
    URL: http://www.cdslsxh.org/lszx/index.html
    MySQL: service_cd.lawyer
    API: /api/lawyer?name=舒婷梅&office=北京中伦

### 13: 犬伤处置医疗机构 [ MySQLHandler.py ]
    URL: http://www.cdwjw.gov.cn/art/2013/11/20/art_64_5389.html
    MySQL: service_cd.dogbite
    API: /api/dogbite?name=人民医院&area=青羊&addr=一环路
    
### 14: 住房保障机构 [ MySQLHandler.py ]
    URL: http://www.cdfgj.gov.cn/IHProject/ShowIHAgency.aspx?ClassID=05
    MySQL: service_cd.housingguarantee
    API: /api/housingguarantee?name=锦江
    
### 15: 成都旅行社查询  [ MySQLHandler.py ]
    URL: http://www.tsichuan.com/travellist.htm?type=&region=510100
    MySQL: service_cd.travelagency
    API: /api/travelagency?name=光大国际&addr=龙腾东路

### 16: 成都贷款楼盘查询 [ MySQLHandler.py ]
    URL: http://www.cdzfgjj.gov.cn/index.php?m=content&c=index&a=lists&catid=85
    MySQL: service_cd.loanablebuilding
    API: /api/loanablebuilding?name=万锦城&addr=华府大道&year=2016

### 17: 预防性健康检查体检机构 [ MySQLHandler.py ]
    URL: http://www.cdwjw.gov.cn/art/2016/1/5/art_74_17062.html
    MySQL: service_cd.pre_health_exam
    API: /api/prehealth?name=疾病预防控制&area=锦江&addr=锦华路
    
### 18: 公证机构查询 [ MySQLHandler.py ]
    URL: http://www.cdjustice.chengdu.gov.cn/cdssfj/gzcxc/cxfw.shtml
    MySQL: service_cd.notaryorg
    API: /api/notaryorg?name=蜀都公证&addr=东城根&area=青羊区

### 19: 司法鉴定机构查询 [ MySQLHandler.py ]
    URL: http://www.cdjustice.chengdu.gov.cn/cdssfj/sfjdjgcx1/cxfw.shtml
    MySQL: service_cd.judicial_org
    API: /api/judicialorg?name=嘉汇工程&business=工程造价鉴定&addr=太升南路
    
### 20: 成都疾控中心查询 [ MySQLHandler.py ]
    URL: http://www.cdwjw.gov.cn/art/2013/11/20/art_64_5391.html
    MySQL: service_cd.diseasecontrol
    API: /api/diseasecontrol?name=武侯

### 21: 成都公积金服务网点查询 [ MySQLHandler.py ]
    URL: http://www.cdzfgjj.gov.cn/index.php?m=content&c=index&a=lists&catid=56
    MySQL: service_cd.fund_service_network
    API: /api/fundnetwork?name=崇州

### 22: 成都应急避难场所 [ MySQLHandler.py ]
    URL: http://www.chengdu.gov.cn/servicelist/csyj01/
    MySQL: service_cd.shelter
    API: /api/shelter?name=青羊

### 23: 房屋安全鉴定机构 [ MySQLHandler.py ]
    URL: http://www.cdfgj.gov.cn/BusinessQuery/BusSearch.aspx?action=ucHouseSafeOrg
    MySQL: service_cd.housingsec
    API: /api/housingsec?name=西南勘察

### 24: 知识产权维权援助与举报投诉 [ MySQLHandler.py ]
    URL: http://www.sipo.gov.cn/wqyz/12330ym/201310/t20131025_862540.html
    MySQL: service_cd.intellectualproperty
    API: /api/intellectualproperty?name=成都

### 25: 就业培训定点机构 [ MySQLHandler.py ]
    URL: http://www.cdhrss.gov.cn/detail.jsp?id=662151
    MySQL: service_cd.employmenttraining
    API: /api/employmenttraining?name=艾米丽

### 26: 成都档案信息查询 [ FileInfo.py 在线查询]
    URL: http://i.rc114.com/InfoQuery_ArcInfo_Pub.aspx
    API: /api/fileinfo?name=姓名&id=510888888888888888

### 27: 地税发票查询 [ Invoice.py 在线查询,验证码]
    URL: http://182.151.197.163:7002/FPCY_SCDS_WW/
    API: 
    验证码 - /api/invoicecaptcha
    调用接口 - /api/invoicecheck?invoice_code=251011480175&invoice_num=00226598&invoice_psd=04083602&captcha=4934&JSESSIONID_INVOICE=xxxxxxxxx

### 28: 夜间施工查询 [ MySQLHandler.py ]
    URL: http://www.cdcc.gov.cn/QualitySafeShow/NightWorkList.aspx
    MySQL: service_cd.nightwork
    API: /api/nightwork?addr=北站

### 29: 物业管理执业查询 [ MySQLHandler.py ]
    URL: http://zy.cdpma.cn/C_staffSearch/EnterPriseInfo.aspx
    MySQL: service_cd.propertymng
    API: /api/propertymng?name=九峰

### 30: 房地产服务机构查询 [ RealEstateSrvOrg.py 在线查询,验证码 ]
    URL: http://www.cdfgj.gov.cn/BusinessQuery/BusSearch.aspx?action=ucEnterpriseQuery&Class=13
    API:
    验证码:/api/realestatecaptcha 
    调用接口: /api/realestate?type=物业服务企业&name=昊邦&captcha=56453&JSESSIONID_INVOICE=XXXXXX

### 31: 宗教查询 [ MySQLHandler.py ]
    URL: http://www.cdmzzj.gov.cn/news.do?method=getTWebCoreArticlePageQuery&channelId=channelId201308271454054502532096
    MySQL: service_cd.religion
    API: /api/religion?type=佛教&name=开化寺

### 32: 国内商品条码信息查询 [ Barcode.py 在线查询 ]
    URL1: http://www.ancc.org.cn/Service/queryTools/Internal.aspx
    URL2: http://search.anccnet.com/searchResult2.aspx?keyword=6904724022468
    API: /api/barcode?code=6930159563023

### 33: 四川名牌查询 [ MySQLHandler.py ]
    URL: http://www.zjj.chengdu.gov.cn/cdzj/xxcx/mpcpcx/list/
    MySQL: service_cd.famousbrand
    API: /api/famousbrand?name=双清牌螺旋钢管&ent=四川双清螺旋钢管有限公司&area=崇州

### 34: 产品质量监督抽查不良记录查询 [ MySQLHandler.py ]
    URL: http://www.zjj.chengdu.gov.cn/cdzj/xxcx/cpzlbljlcxfw/list/ 
    MySQL: service_cd.badrecord
    API: /api/badrecord?name=检查井盖&ent=崇州&time=2015

### 35: 厂商信息查询 [ Manufacturer.py 在线查询 ]
    URL: http://www.ancc.org.cn/Service/queryTools/Internal.aspx
    API: /api/manufacturer?name=冯老汉科技
   
### 36: 成都房屋“预/现售项目” [ PreForSale.py 在线查询 ]
    URL: http://www.cdfgj.gov.cn/SCXX/ShowNew.aspx
    API: /api/preforsale?page=1&name=保利&region=金牛&from=2015-01-01&to=2016-07-20 

### 37: 房地产企业查询 [ MySQLHandler.py ]
    URL: http://www.cdcc.gov.cn/webNew/aspx/EnterpriseLst.aspx?st=%B7%BF%B5%D8%B2%FA%C6%F3%D2%B5
    MySQL: service_cd.realestateent
    API: /api/realestateent?name=蜀山

### 38: 二级建造师信息查询 [ AssociateConstructor.py 在线查询 ]
    URL: http://jzsgl.coc.gov.cn/archisearch/cxejjzs/rylist.aspx
    API: /api/constructor?ent=九寨建设&name=陈心乐&reg_no=川251070811612&cer_no=00321147&qua_no=00022451
    参数:
    ent - 企业名称
    name - 姓名
    reg_no - 注册号
    cer_no - 注册证书编号
    qua_no - 执业资格证书编号

### 39: 成都出租车失物登记 [ TaxiLostFound.py ]
    URL: http://www.cdtaxi.cn/shiwudj
    API:
    /api/lostfoundcaptcha 
    /api/lostfoundrecord?page=1
    /api/lostfound?name=李女士&tel=13800125134&pickup=鹭岛国际社区&pickup_time=18&getoff=九眼桥&getoff_time=18:30&lost_item=钱包一个&msg=粉色,内有身份证证，招商银行卡&captcha=6522&JSESSIONID_INVOICE=0ab69aee52d01d3c6cfcac9443a553b5&HIDDEN_FORM_HASH=bf3640e7ce3f5c3f79a79144572c386f
    参数:
    name - 姓名
    tel - 联系电话
    pickup - 上车地点(18:30)
    pickup_time - 上车时间(9:20)
    getoff - 下车地点
    getoff_time - 下车时间
    company - 公司名称
    car_type - 车型
    plate_no - 车牌号码
    invoice_sum - 发票金额
    invoice_code - 发票代码
    invoice_no - 发票号码
    lost_item - 遗失物品
    msg - 留言备注
    time - 乘车时间(2016-07-25)
    captcha - 验证码
    JSESSIONID_INVOICE - 会话ID(后台处理)
    HIDDEN_FORM_HASH - 表单隐藏Hash(后台处理)

### 40 成都出租车失物招领 [ TaxiFound.py ]
    URL: http://www.cdtaxi.cn/zhaolingxx
    API: /api/taxifound?page=1
    
### 41 住房保障项目查询 [ MySQLHandler.py ]
    URL: http://www.cdfgj.gov.cn/IHProject/ShowIHProjectList.aspx
    MySQL: service_cd.housingensuring
    API: /api/housingensuring?project=海棠路&area=锦江

### 42 食品生产许可获证企业(SC) [ FoodDrugAdmin.py ]
    URL: http://app1.sfda.gov.cn/datasearch/face3/base.jsp?tableId=120&tableName=TABLE120&title=%CA%B3%C6%B7%C9%FA%B2%FA%D0%ED%BF%C9%BB%F1%D6%A4%C6%F3%D2%B5(SC)&bcId=145275419693611287728573704379
    API: /api/fda/food/sc?query=永兴大米&page=1
    
### 43 食品生产许可获证企业(QS) [ FoodDrugAdmin.py ]
    URL: http://app1.sfda.gov.cn/datasearch/face3/base.jsp?tableId=91&tableName=TABLE91&title=%CA%B3%C6%B7%C9%FA%B2%FA%D0%ED%BF%C9%BB%F1%D6%A4%C6%F3%D2%B5(QS)&bcId=137413698768984683499699272988
    API: /api/fda/food/qs?query=永兴大米&page=1
    
### 44 食品添加剂生产许可获证企业 [ FoodDrugAdmin.py ]
    URL: http://app1.sfda.gov.cn/datasearch/face3/base.jsp?tableId=89&tableName=TABLE89&title=%CA%B3%C6%B7%CC%ED%BC%D3%BC%C1%C9%FA%B2%FA%D0%ED%BF%C9%BB%F1%D6%A4%C6%F3%D2%B5&bcId=137403916083811026153735196207
    API: /api/fda/food/addictive?query=河南科恩
    
### 45 食品添加剂生产许可检验机构承检产品及相关标准 [ FoodDrugAdmin.py ]
    URL: http://app1.sfda.gov.cn/datasearch/face3/base.jsp?tableId=90&tableName=TABLE90&title=%CA%B3%C6%B7%CC%ED%BC%D3%BC%C1%C9%FA%B2%FA%D0%ED%BF%C9%BC%EC%D1%E9%BB%FA%B9%B9%B3%D0%BC%EC%B2%FA%C6%B7%BC%B0%CF%E0%B9%D8%B1%EA%D7%BC&bcId=137395392579976004904078921814
    API: /api/fda/food/addictivecheck?query=上海市质量

### 46 国产保健食品 [ FoodDrugAdmin.py ]
    URL: http://app1.sfda.gov.cn/datasearch/face3/base.jsp?tableId=30&tableName=TABLE30&title=%B9%FA%B2%FA%B1%A3%BD%A1%CA%B3%C6%B7&bcId=118103385532690845640177699192
    API: /api/fda/healthfood/domestic?query=鲨力精粉&page=1
    
### 47 进口保健食品 [ FoodDrugAdmin.py ]
    URL: http://app1.sfda.gov.cn/datasearch/face3/base.jsp?tableId=31&tableName=TABLE31&title=%BD%F8%BF%DA%B1%A3%BD%A1%CA%B3%C6%B7&bcId=118103387241329685908587941736
    API: /api/fda/healthfood/import?query=加拿大冷水鱼&page=1

### 48 进口化妆品 [ FoodDrugAdmin.py ]
    URL: http://app1.sfda.gov.cn/datasearch/face3/base.jsp?tableId=69&tableName=TABLE69&title=%BD%F8%BF%DA%BB%AF%D7%B1%C6%B7&bcId=124053679279972677481528707165
    API: /api/fda/cosmetic/importcosmetic?query=香奈儿&page=1
   
### 49 国产非特殊用途化妆品备案检验机构 [ FoodDrugAdmin.py ]
    URL: http://app1.sfda.gov.cn/datasearch/face3/base.jsp?tableId=83&tableName=TABLE83&title=%B9%FA%B2%FA%B7%C7%CC%D8%CA%E2%D3%C3%CD%BE%BB%AF%D7%B1%C6%B7%B1%B8%B0%B8%BC%EC%D1%E9%BB%FA%B9%B9&bcId=131474662666676136335027594407
    API: /api/fda/cosmetic/inspectionorg?query=重庆市食品药品&page=1

### 50 化妆品生产许可获证企业 [ FoodDrugAdmin.py ]
    URL: http://app1.sfda.gov.cn/datasearch/face3/base.jsp?tableId=93&tableName=TABLE93&title=%BB%AF%D7%B1%C6%B7%C9%FA%B2%FA%D0%ED%BF%C9%BB%F1%D6%A4%C6%F3%D2%B5&bcId=124053671285715992005675373538
    API: /api/fda/cosmetic/productionent?query=重庆杏林&page=1
    
### 51 化妆品行政许可检验机构 [ FoodDrugAdmin.py ]
    URL: http://app1.sfda.gov.cn/datasearch/face3/base.jsp?tableId=108&tableName=TABLE108&title=%BB%AF%D7%B1%C6%B7%D0%D0%D5%FE%D0%ED%BF%C9%BC%EC%D1%E9%BB%FA%B9%B9&bcId=141403272796679344681283623477
    API: /api/fda/cosmetic/admininspectionorg?query=四川省食品&page=1

### 52 互联网药品信息服务 [ FoodDrugAdmin.py ]
    URL: http://app1.sfda.gov.cn/datasearch/face3/base.jsp?tableId=28&tableName=TABLE28&title=%BB%A5%C1%AA%CD%F8%D2%A9%C6%B7%D0%C5%CF%A2%B7%FE%CE%F1&bcId=118715637133379308522963029631
    API: /api/fda/drug/infosrv?query=大连美创&page=1

### 53 互联网药品交易服务 [ FoodDrugAdmin.py ]
    URL: http://app1.sfda.gov.cn/datasearch/face3/base.jsp?tableId=33&tableName=TABLE33&title=%BB%A5%C1%AA%CD%F8%D2%A9%C6%B7%BD%BB%D2%D7%B7%FE%CE%F1&bcId=118715801943244717582221630944
    API: /api/fda/drug/tradesrv?query=老百姓药品&page=1 

### 54 网上药店 [ FoodDrugAdmin.py ]
    URL: http://app1.sfda.gov.cn/datasearch/face3/base.jsp?tableId=96&tableName=TABLE96&title=%CD%F8%C9%CF%D2%A9%B5%EA&bcId=139468294509280829793942689586
    API: /api/fda/drug/onlinestore?query=巴中怡和&page=1

### 55 国家保健食品安全监督抽检（不合格产品） [ FoodDrugAdmin.py ]
    URL: http://app1.sfda.gov.cn/datasearch/face3/base.jsp?tableId=112&tableName=TABLE112&title=%B9%FA%BC%D2%B1%A3%BD%A1%CA%B3%C6%B7%B0%B2%C8%AB%BC%E0%B6%BD%B3%E9%BC%EC%A3%A8%B2%BB%BA%CF%B8%F1%B2%FA%C6%B7%A3%A9&bcId=143106783126582192766779995431
    API: /api/fda/foodinspect/unqualifiedhf?query=龙涎减压茶&page=1

### 56 国家保健食品安全监督抽检（合格产品） [ FoodDrugAdmin.py ]
    URL: http://app1.sfda.gov.cn/datasearch/face3/base.jsp?tableId=113&tableName=TABLE113&title=%B9%FA%BC%D2%B1%A3%BD%A1%CA%B3%C6%B7%B0%B2%C8%AB%BC%E0%B6%BD%B3%E9%BC%EC%A3%A8%BA%CF%B8%F1%B2%FA%C6%B7%A3%A9&bcId=143106780679359099093230607567
    API: /api/fda/foodinspect/qualifiedhf?query=金日牌西洋参&page=1

### 57 国家食品安全监督抽检（不合格产品） [ FoodDrugAdmin.py ]
    URL: http://app1.sfda.gov.cn/datasearch/face3/base.jsp?tableId=114&tableName=TABLE114&title=%B9%FA%BC%D2%CA%B3%C6%B7%B0%B2%C8%AB%BC%E0%B6%BD%B3%E9%BC%EC%A3%A8%B2%BB%BA%CF%B8%F1%B2%FA%C6%B7%A3%A9&bcId=143106776907834761101199700381
    API: /api/fda/foodinspect/unqualifiedfood?query=张家川回族自治&page=1

### 58 国家食品安全监督抽检（合格产品） [ FoodDrugAdmin.py ]
    URL: http://app1.sfda.gov.cn/datasearch/face3/base.jsp?tableId=110&tableName=TABLE110&title=%B9%FA%BC%D2%CA%B3%C6%B7%B0%B2%C8%AB%BC%E0%B6%BD%B3%E9%BC%EC%A3%A8%BA%CF%B8%F1%B2%FA%C6%B7%A3%A9&bcId=143106772371776780261602322547
    API: /api/fda/foodinspect/qualifiedfood?query=长白山牌全汁&page=1

### 59 四川省地税办税日历 [ MySQLHandler.py ]
    URL: http://12366.sc-l-tax.gov.cn/resource/html/swzj/001001005/001005003/bsrl.htm
    MySQL: service_cd.sctaxcal
    API: /api/sctaxcal?year=2016

### 60 博物馆查询 [ MySQLHandler.py ]
    URL: http://huigu.chengdu.gov.cn/special/template3.jsp?ClassID=02020616
    MySQL: service_cd.cdmuseum
    API: /api/cdmuseum?name=建川
    
### 61 成都市殡仪馆服务项目及收费标准 [ MySQLHandler.py ]
    URL: http://www.chengdu.gov.cn/servicelist/swbz07/
    MySQL: service_cd.funeralfee
    API: /api/funeralfee?item=出租花圈

### 62 成都市各区（县）消防大队联系电话 [ MySQLHandler.py ]
    URL: http://www.chengdu.gov.cn/servicelist/xfaq01/
    MySQL: service_cd.firebrigadetel
    API: /api/firebrigadetel?name=锦江

### 63 中心城区居民用水阶梯价格表 [ RedisHandler.py ]
    URL: http://www.cddrc.gov.cn/zhuanti/detail.action?id=848157&classId=02071403
    Redis Key: waterfee
    API: /api/waterfee?amount=200

### 64 中心城区居民生活用气阶梯价格表 [ RedisHandler.py ]
    URL: http://www.cddrc.gov.cn/zhuanti/detail.action?id=848158&classId=02071403
    Redis Key: gasfee
    API: /api/gasfee?amount=200
    
### 65 殡仪服务机构 [ MySQLHandler.py ]
    URL: http://www.cdmzj.gov.cn/cdmz/mzhy/mzhy_byfwjg/index.html
    MySQL: service_cd.funeral_service_org
    API: /api/funeralserviceorg?name=长松寺

### 66 成都福利院 [ WelfareHouse.py ]
    URL: http://www.cdmzj.gov.cn/cdmz/mzhy/mzhy_fly/
    Redis Key: welfarehouse
    API: /api/welfarehouse

### 67 成都养老机构 [ MySQLHandler.py ]
    URL: http://www.cdmzj.gov.cn/cdmz/mzhy/mzhy_yljg/
    MySQL: service_cd.socialwelfarehouse
    API: /api/socialwelfarehouse

### 68 收养登记机关 [ MySQLHandler.py ]
    URL: http://www.cdmzj.gov.cn/cdmz/mzhy/mzhy_sydjjg/index.html
    MySQL: service_cd.adoption
    API: /api/adoption?name=天府新区
    
### 69 城乡社区日间照料中心 [ MySQLHandler.py ]
    URL: http://www.cdmzj.gov.cn/cdmz/mzhy/mzhy_rjzl/index.html
    MySQL: service_cd.carecenter
    API: /api/carecenter?name=颐康少城&addr=金河路

### 70 成都市民政局下属单位 [ SubordinateOrg.py ]
    URL: http://www.cdmzj.gov.cn/cdmz/mzhy/mzhy_qtxsdw/
    Redis Key: subordinateorg
    API: /api/subordinateorg

### 71 区县民政局 [ MySQLHandler.py ]
    URL: http://www.cdmzj.gov.cn/cdmz/mzhy/mzhy_qxmzj/
    MySQL: countycivilaffair
    API: /api/countycivilaffair?name=双流

### 72 法律援助机构 [ MySQLHandler.py ]
    URL: http://www.cdjustice.chengdu.gov.cn/cdssfj/flyzjgcx/cxfw.shtml
    MySQL: service_cd.legalaid
    API: /api/legalaid?name=大邑

### 73 中心城区生活垃圾处理费标准 [ RedisHandler.py ]
    URL: http://www.cddrc.gov.cn/detail.action?id=563865
    MySQL: service_cd.garbagefee
    API: /api/garbagefee?name=事业单位

### 74 成都体育公共场馆查询
    URL: http://ty.cd168.cn/
    MySQL: service_cd.publicstadium
    API: /api/publicstadium?area=武侯&type=羽毛球
    
### 75 成都体育彩票销售点查询
    URL: http://ty.cd168.cn/
    MySQL: service_cd.sportlottery
    API: /api/sportlottery?area=青羊

### 76 成都体质监测点查询
    URL: http://ty.cd168.cn/
    Redis Key: corporeitymoni
    API: /api/corporeitymoni
    
### 77 成都市健身路径查询
    URL: http://ty.cd168.cn/
    MySQL: service_cd.fitnesspath
    API: /api/fitnesspath?area=青羊&addr=一环路西二段&name=健身路径

### 78 成都市健身会所查询
    URL: http://ty.cd168.cn/
    MySQL: service_cd.fitnessclub
    API: /api/fitnessclub?area=武侯&type=器械
    
### 79 成都市学校场地查询
    URL: http://ty.cd168.cn/
    MySQL: service_cd.schoolsite
    API: /api/schoolsite?name=四川师范大学&area=青羊

### 80 成都市体育培训机构查询
    URL: http://ty.cd168.cn/
    MySQL: service_cd.sporttraining
    API: /api/sporttraining?area=青羊区&type=合气道
    
### 81 成都市体育用品销售查询    
    URL: http://ty.cd168.cn/
    MySQL: service_cd.sportgoods
    API: /api/sportgoods?name=劲浪&area=锦江区
    
### 82 成都图书馆查询
    URL: http://huigu.chengdu.gov.cn/special/template3.jsp?ClassID=02020615
    MySQL: service_cd.cdlibrary
    API: /api/cdlibrary?name=四川省图书

### 83 残疾证查询
    URL: http://www.cdpf.org.cn/2dzcx/
    API:
    验证码:/api/disabilitycertcaptcha
    调用接口: /api/disabilitycert?name=朱渐华&no=42032319790321173242&captcha=4644&JSESSIONID_INVOICE=xxxxxx

### 84 土地拍卖价格查询
    URL：http://www.cdggzy.com:8112/two/pmjg.html
    MySQL: service_cd.landauction
    API: /api/landauction?date=20151204&addr=三圣乡

### 85 成都初中查询
    URL: http://www.cdzsks.com/school/search
    MySQL: service_cd.juniorhighschool
    API: /api/juniorhighschool?name=树德&area=青羊&type=公办
    
### 86 成都小升初查询(2015)
    URL: http://www.cdzsks.com/partition/partitioninfo
    MySQL: service_cd.primary2junior
    API: /api/primary2junior?name=新华路小学
    
### 87 中小学教育费银行代收网点
    URL: http://bank.cdedu.com/page/wd.htm
    MySQL: service_cd.edufeebank
    API: /api/edufeebank?bank=中国工商银行&site=西较场支行&addr=锦里西路
    
