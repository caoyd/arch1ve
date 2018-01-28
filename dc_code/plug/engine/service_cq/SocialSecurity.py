"""
URL - http://cqjy.cqhrss.gov.cn/cqwx/?cityid=500000
610326198006232014
030590

字段说明
name: 姓名
gender: 性别
nationality: 民族
birth_date: 出生日期
id: 身份证号
card_no: 社保卡号
personal_no: 个人编号
unit_no: 单位编号
unit_name: 单位名称
resident_type: 户口性质
work_type: 工种
insured_addr: 参保地
first_pay_date: 首次缴费时间/日期
first_insured_date: 首次参保日期
insured_status: 参保状态
account_status: 账户(卡)状态
retirement_date: 离退休时间
treatment_start_date: 待遇享受开始年月/领取失业金起始年月
insured_year: 社保年度/年度
total_month_of_year: 当年缴费月数
interest_of_year: 当年账户利息(元)
principal_of_year: 当年账户本金(元)
total_month: 累计缴费月数/缴费月数/失业前累计缴费月数/已缴费月数
total_unit_transfer: 累计单位划账存储额(元)
total_last_year: 上年末个人累计缴费本息(元)
payment_phase: 对应费款所属期/费用所属期/缴费年月
payment_base: 缴费基数/失业保险缴费基数/职工本人缴费基数
unit_payment: 单位缴纳金额(元)
personal_payment: 个人缴纳金额(元)
interest_over_year: 补缴个人跨年利息(元)
interest_this_year: 补缴个人本年利息(元)
payment_type: 缴费类型
payment_flag: 缴费标志
current_balance: 当前账户结余金额
total_account_payment: 当年账户累计支付金额
total_medical_fee: 本年医疗费累计
no_of_hospitalized: 本年住院次数
fee_item: 费款科目
unit_transfer_to_account: 单位缴费划账户金额
unit_transfer_to_plan: 单位缴费划统筹金额
medical_org_no: 医疗机构编号
medical_org_name: 医疗机构名称
medical_type: 医疗类别
large_payment: 大额支付
cash_payment: 现金支付
personal_account_payment: 个人账户支付
plan_payment: 统筹支付
other_amount: 其它补助金额
balance_date: 结算日期
injury_level: 伤残等级
certificate_no: 失业证书编号
month_remain: 失业保险金剩余月数
in_treatment: 是否享受待遇
month_of_treatment: 本次失业享受待遇月数
accounting_date: 到账日期
admin_org: 社保经办机构
unit_avg_wage: 单位上年度月平均工资
"""
import re
import json
import operator
import lxml.html
from urllib.parse import unquote_plus, urlencode, parse_qsl
from tornado.httpclient import HTTPRequest, HTTPError
from tornado.web import MissingArgumentError

from engine.common.Handlers import SpiderHandler
from engine.common.Utils import fake_useragent


class SSBase(object):
    def __init__(self, session):
        self.session = session

    def make_request(self, method, url, start=1, end=20):
        headers = {
            "User-Agent": fake_useragent(),
            "Cookie": self.session
        }
        data = {
            "startRow": start,
            "endRow": end
        }

        if method == "get":
            request = HTTPRequest(url, method=method.upper(), headers=headers)
        else:
            request = HTTPRequest(url, method=method.upper(), headers=headers, body=urlencode(data))

        return request


# Endowment insurance
class Pension(SSBase):
    def __init__(self, session):
        super().__init__(session)

    @staticmethod
    def parse_html(tp, raw):
        result = []

        if tp == "account":
            raw_json = json.loads(raw)
            for item in raw_json["pai"]["details"]:
                tmp = {
                    "name": item["xm"],
                    "personal_no": item["grbh"],
                    "id": item["sfzh"],
                    "unit_no": item["dwbh"],
                    "unit_name": item["dwmc"],
                    "insured_year": item["sbnd"],
                    "total_month_of_year": item["dnjfys"],
                    "interest_of_year": item["dnzhlx"],
                    "principal_of_year": item["dnzhbj"],
                    "total_month": item["ljjfys"],
                    "total_last_year": item["snmljgrjfbx"],
                }
                result.append(tmp)
            result.sort(key=operator.itemgetter("insured_year"), reverse=True)
        elif tp == "detail":
            raw_json = json.loads(raw)
            for item in raw_json["pci"]["details"]:
                tmp = {
                    "unit_no": item["dwbh"],
                    "unit_name": item["dwmc"],
                    "insured_addr": item["cbd"],
                    "name": item["xm"],
                    "personal_no": item["grbh"],
                    "payment_phase": item["dyfkssq"],
                    "payment_base": item["jfjs"],
                    "unit_payment": item["dwjfje"],
                    "personal_payment": item["grjfje"],
                    "interest_over_year": item["bjgrknlx"],
                    "interest_this_year": item["bjgrbnlx"],
                    "payment_type": item["jflx"],
                    "payment_flag": item["jfbz"],
                }
                result.append(tmp)
            result.sort(key=operator.itemgetter("payment_phase"), reverse=True)
        else:
            html = lxml.html.fromstring(raw)
            trs = html.xpath('//div[@class="content"]/table/tr')
            if len(trs):
                tmp = {
                    "name": trs[0].xpath(".//td")[1].text_content().strip(),
                    "personal_no": trs[1].xpath(".//td")[1].text_content().strip(),
                    "id": trs[2].xpath(".//td")[1].text_content().strip(),
                    "gender": trs[3].xpath(".//td")[1].text_content().strip(),
                    "nationality": trs[4].xpath(".//td")[1].text_content().strip(),
                    "unit_no": trs[5].xpath(".//td")[1].text_content().strip(),
                    "unit_name": trs[6].xpath(".//td")[1].text_content().strip(),
                    "insured_addr": trs[7].xpath(".//td")[1].text_content().strip(),
                    "first_pay_date": trs[8].xpath(".//td")[1].text_content().strip(),
                    "birth_date": trs[9].xpath(".//td")[1].text_content().strip(),
                    "resident_type": trs[10].xpath(".//td")[1].text_content().strip(),
                    "insured_status": trs[11].xpath(".//td")[1].text_content().strip(),
                    "retirement_date": trs[12].xpath(".//td")[1].text_content().strip(),
                    "treatment_start_date": trs[13].xpath(".//td")[1].text_content().strip(),
                }
                result.append(tmp)

        return result


# Medical Insurance
class Medical(SSBase):
    def __init__(self, session):
        super().__init__(session)

    @staticmethod
    def parse_html(tp, raw):
        result = []

        if tp == "account":
            raw_json = json.loads(raw)
            for item in raw_json["cbaai"]["details"]:
                tmp = {
                    "name": item["xm"],
                    "personal_no": item["grbh"],
                    "id": item["sfzh"],
                    "insured_year": item["nd"],
                    "current_balance": item["dqzhjyje"],
                    "total_account_payment": item["dnzhzfljje"],
                    "total_medical_fee": item["bnyllj"],
                    "no_of_hospitalized": item["bnzycs"],
                }
                result.append(tmp)
            result.sort(key=operator.itemgetter("insured_year"), reverse=True)

        elif tp == "detail":
            raw_json = json.loads(raw)
            for item in raw_json["cci"]["details"]:
                tmp = {
                    "unit_no": item["dwbh"],
                    "unit_name": item["dwmc"],
                    "insured_addr": item["cbd"],
                    "name": item["xm"],
                    "personal_no": item["grbh"],
                    "payment_phase": item["fkssq"],
                    "payment_base": item["jfjs"],
                    "unit_payment": item["dwjfje"],
                    "personal_payment": item["grjfje"],
                    "fee_item": item["fkkm"],
                    "unit_transfer_to_account": item["dwjfhzhje"],
                    "unit_transfer_to_plan": item["dwjfhtcje"],
                    "payment_type": item["jflx"],
                    "payment_flag": item["jfbz"],
                }
                result.append(tmp)
            result.sort(key=operator.itemgetter("payment_phase"), reverse=True)

        elif tp == "balance":
            raw_json = json.loads(raw)
            for item in raw_json["cfi"]["details"]:
                tmp = {
                    "name": item["xm"],
                    "id": item["sfzh"],
                    "personal_no": item["grbh"],
                    "card_no": item["ickh"],
                    "medical_org_no": item["yljgbh"],
                    "medical_org_name": item["yljgmc"],
                    "medical_type": item["yllb"],
                    "large_payment": item["defy"],
                    "cash_payment": item["xjzf"],
                    "personal_account_payment": item["grzhzf"],
                    "plan_payment": item["tczf"],
                    "other_amount": item["gwybzje"],
                    "balance_date": item["jsrq"]
                }
                result.append(tmp)
            result.sort(key=operator.itemgetter("balance_date"), reverse=True)

        # info
        else:
            raw_json = json.loads(raw)
            for item in raw_json["cbaai"]["details"]:
                tmp = {
                    "name": item["xm"],
                    "personal_no": item["grbh"],
                    "id": item["sfzh"],
                    "card_no": item["ickh"],
                    "gender": item["xb"],
                    "unit_no": item["dwbh"],
                    "unit_name": item["dwmc"],
                    "insured_addr": item["cbd"],
                    "first_pay_date": item["cbrq"],
                    "account_status": item["zhzt"],
                    "insured_year": item["nd"],
                    "total_month": item["sjjfys"]
                }
                result.append(tmp)
            result.sort(key=operator.itemgetter("insured_year"), reverse=True)

        return result


# Employment injury Insurance
class Injury(SSBase):
    def __init__(self, session):
        super().__init__(session)

    @staticmethod
    def parse_html(tp, raw):
        result = []

        if tp == "detail":
            raw_json = json.loads(raw)
            for item in raw_json["ici"]["details"]:
                tmp = {
                    "unit_no": item["dwbh"],
                    "unit_name": item["dwmc"],
                    "insured_addr": item["cbd"],
                    "name": item["xm"],
                    "personal_no": item["grbh"],
                    "payment_phase": item["jfny"],
                    "payment_base": item["jfjs"],
                    "unit_payment": item["dwjfje"],
                    "payment_type": item["jflx"],
                    "payment_flag": item["jfbj"],
                }
                result.append(tmp)
            result.sort(key=operator.itemgetter("payment_phase"), reverse=True)
        # info
        else:
            html = lxml.html.fromstring(raw)
            trs = html.xpath('//div[@class="content"]/table/tr')
            if len(trs):
                tmp = {
                    "name": trs[0].xpath(".//td")[1].text_content().strip(),
                    "personal_no": trs[1].xpath(".//td")[1].text_content().strip(),
                    "id": trs[2].xpath(".//td")[1].text_content().strip(),
                    "gender": trs[3].xpath(".//td")[1].text_content().strip(),
                    "unit_no": trs[4].xpath(".//td")[1].text_content().strip(),
                    "unit_name": trs[5].xpath(".//td")[1].text_content().strip(),
                    "insured_addr": trs[6].xpath(".//td")[1].text_content().strip(),
                    "first_pay_date": trs[7].xpath(".//td")[1].text_content().strip(),
                    "injury_level": trs[8].xpath(".//td")[1].text_content().strip(),
                    "insured_status": trs[9].xpath(".//td")[1].text_content().strip(),
                }
                result.append(tmp)

        return result


# Unemployment insurance
class Unemployment(SSBase):
    def __init__(self, session):
        super().__init__(session)

    @staticmethod
    def parse_html(tp, raw):
        result = []

        if tp == "detail":
            raw_json = json.loads(raw)
            for item in raw_json["uci"]["details"]:
                tmp = {
                    "unit_no": item["dwbh"],
                    "unit_name": item["dwmc"],
                    "insured_addr": item["cbd"],
                    "name": item["xm"],
                    "personal_no": item["grbh"],
                    "payment_phase": item["fkssq"],
                    "payment_base": item["jfjs"],
                    "unit_payment": item["dwjfje"],
                    "personal_payment": item["grjfje"],
                    "payment_type": item["jflx"],
                    "accounting_date": item["dzrq"] if item["dzrq"] else "",
                    "payment_flag": item["jfbj"],
                    "admin_org": item["jbjgmc"]
                }
                result.append(tmp)
            result.sort(key=operator.itemgetter("payment_phase"), reverse=True)
        # info
        else:
            html = lxml.html.fromstring(raw)
            trs = html.xpath('//div[@class="content"]/table/tr')
            if len(trs):
                tmp = {
                    "name": trs[0].xpath(".//td")[1].text_content().strip(),
                    "gender": trs[1].xpath(".//td")[1].text_content().strip(),
                    "id": trs[2].xpath(".//td")[1].text_content().strip(),
                    "resident_type": trs[3].xpath(".//td")[1].text_content().strip(),
                    "payment_base": trs[4].xpath(".//td")[1].text_content().strip(),
                    "total_month": trs[5].xpath(".//td")[1].text_content().strip(),
                    "treatment_start_date": trs[6].xpath(".//td")[1].text_content().strip(),
                    "certificate_no": trs[7].xpath(".//td")[1].text_content().strip(),
                    "month_of_treatment": trs[8].xpath(".//td")[1].text_content().strip(),
                    "month_remain": trs[9].xpath(".//td")[1].text_content().strip(),
                    "insured_status": trs[10].xpath(".//td")[1].text_content().strip(),
                    "is_treatment": trs[11].xpath(".//td")[1].text_content().strip(),
                    "insured_addr": trs[12].xpath(".//td")[1].text_content().strip(),
                }
                result.append(tmp)

        return result


# Maternity insurance
class Maternity(SSBase):
    def __init__(self, session):
        super().__init__(session)

    @staticmethod
    def parse_html(tp, raw):
        result = []

        if tp == "detail":
            raw_json = json.loads(raw)
            for item in raw_json["workerBirthPaymentDetailList"]:
                tmp = {
                    "unit_no": item["dwbh"],
                    "unit_name": item["dwmc"],
                    "insured_addr": item["cbd"],
                    "name": item["xm"],
                    "personal_no": item["grbh"],
                    "payment_phase": item["jfny"],
                    "payment_base": item["jfjs"],
                    "unit_payment": item["dwjfje"],
                    "payment_type": item["jflx"],
                    "accounting_date": item["dzrq"] if item["dzrq"] else "",
                    "payment_flag": item["jfbj"],
                }
                result.append(tmp)
            result.sort(key=operator.itemgetter("payment_phase"), reverse=True)
        # info
        else:
            html = lxml.html.fromstring(raw)
            trs = html.xpath('//div[@class="person_base_info"]/table/tr')
            if len(trs):
                tmp = {
                    "name": trs[0].xpath(".//td")[1].text_content().strip(),
                    "gender": trs[1].xpath(".//td")[1].text_content().strip(),
                    "id": trs[2].xpath(".//td")[1].text_content().strip(),
                    "personal_no": trs[3].xpath(".//td")[1].text_content().strip(),
                    "insured_addr": trs[4].xpath(".//td")[1].text_content().strip(),
                    "unit_no": trs[5].xpath(".//td")[1].text_content().strip(),
                    "unit_name": trs[6].xpath(".//td")[1].text_content().strip(),
                    "first_pay_date": trs[7].xpath(".//td")[1].text_content().strip(),
                    "insured_status": trs[8].xpath(".//td")[1].text_content().strip(),
                    "unit_avg_wage": trs[9].xpath(".//td")[1].text_content().strip(),
                    "payment_base": trs[10].xpath(".//td")[1].text_content().strip(),
                    "total_month": trs[11].xpath(".//td")[1].text_content().strip(),
                }
                result.append(tmp)

        return result


class SocialSecurity(SpiderHandler):
    def get_session(self):
        query_params = dict(parse_qsl(self.request.query, True))
        tmp_cookie = self.get_query_argument("JSESSIONID_INVOICE")
        session = "JSESSIONID=" + unquote_plus(tmp_cookie)
        return session

    async def do_process_logic(self, *args):
        action_str = args[0]

        # ============================
        # Login and return basic info
        # ============================
        if action_str.startswith("login"):
            uid = self.get_query_argument("id")
            password = self.get_query_argument("password")

            login_url = "http://cqjy.cqhrss.gov.cn/cqwx/wx/socialSecurity/directQuery.action"
            headers = {
                "Content-Type": "application/x-www-form-urlencoded",
                "User-Agent": fake_useragent(),
            }
            data = {
                "userVo.idNo": uid,
                "userVo.password": password
            }
            request = HTTPRequest(login_url, method="POST", headers=headers, body=urlencode(data))
            response = await self.browser.fetch(request)

            html = lxml.html.fromstring(response.body.decode("utf-8"))
            error = html.xpath('//input[@id="errorMessage"]')

            # Login error
            if len(error):
                error_msg = error[0].attrib["value"]
                self.send_json_response(error_msg, 0)
            else:
                # Get cookie from response header
                cookie = response.headers.get_list("Set-Cookie")[0]
                m = re.match('JSESSIONID=(.*?);\s', cookie)
                if m:
                    # Get cookie "JSESSIONID"
                    session = m.group(1)

                    # Request user info
                    info_url = "http://cqjy.cqhrss.gov.cn/cqwx/wx/socialSecurity/persionBasic.action"
                    headers = {
                        "User-Agent": fake_useragent(),
                        "Cookie": cookie
                    }
                    request = HTTPRequest(info_url, method="GET", headers=headers)
                    response = await self.browser.fetch(request)

                    if response.code == 200:
                        html = lxml.html.fromstring(response.body.decode("utf-8"))

                        trs = html.xpath('//div[@class="person_base_info"]/table/tr')
                        info = {
                            "name": trs[0].xpath(".//td")[1].text_content().strip(),
                            "personal_no": trs[1].xpath(".//td")[1].text_content().strip(),
                            "id": trs[2].xpath(".//td")[1].text_content().strip(),
                            "gender": trs[3].xpath(".//td")[1].text_content().strip(),
                            "nationality": trs[4].xpath(".//td")[1].text_content().strip(),
                            "birth_date": trs[5].xpath(".//td")[1].text_content().strip(),
                            "resident_type": trs[6].xpath(".//td")[1].text_content().strip(),
                            "work_type": trs[7].xpath(".//td")[1].text_content().strip(),
                            "first_insured_date": trs[8].xpath(".//td")[1].text_content().strip(),
                            "insured_status": trs[9].xpath(".//td")[1].text_content().strip(),
                        }

                        # Change cookie key name to JSESSIONID_INVOICE
                        self.set_cookie("JSESSIONID_INVOICE", session)
                        # self.set_header("Set-Cookie", cookie)
                        self.send_json_response([info])
                    else:
                        self.send_json_response([])

                else:
                    raise HTTPError(500, self.config["error"]["GET_COOKIE_ERR"])

        else:
            action = action_str.split('/')  # pension | medical | injury | unemployment | maternity
            opt = action[1] if len(action) > 1 else ""  # info | account | detail | balance

            query_params = dict(parse_qsl(self.request.query, True))
            if "JSESSIONID_INVOICE" not in query_params:
                raise MissingArgumentError("JSESSIONID_INVOICE")
            else:
                tmp_cookie = self.get_query_argument("JSESSIONID_INVOICE")

            session = "JSESSIONID=" + unquote_plus(tmp_cookie)

            p = query_params["page"] if "page" in query_params else ""
            ps = query_params["page_size"] if "page_size" in query_params else ""
            page, page_size = self.init_paging_param(p, ps)
            # Start row and end row
            start = page + 1
            end = page + page_size

            # ==============================
            # Endowment insurance (pension)
            # ==============================
            if action_str.startswith("pension"):
                url = {
                    "info": "http://cqjy.cqhrss.gov.cn/cqwx/wx/socialSecurity/pensionSecurity.action",
                    "account": "http://cqjy.cqhrss.gov.cn/cqwx/wx/socialSecurity/pAList.action",
                    "detail": "http://cqjy.cqhrss.gov.cn/cqwx/wx/socialSecurity/pCList.action"
                }
                method = "get" if opt == "info" else "post"

                pension = Pension(session)
                response = await self.browser.fetch(pension.make_request(method, url[opt], start, end))
                raw = response.body.decode("utf-8")
                result = pension.parse_html(opt, raw)
                self.send_json_response(result)
            # ==================
            # Medical insurance
            # ==================
            elif action_str.startswith("medical"):
                url = {
                    "info": "http://cqjy.cqhrss.gov.cn/cqwx/wx/socialSecurity/cBList.action",
                    "account": "http://cqjy.cqhrss.gov.cn/cqwx/wx/socialSecurity/cAList.action",
                    "detail": "http://cqjy.cqhrss.gov.cn/cqwx/wx/socialSecurity/cCList.action",
                    "balance": "http://cqjy.cqhrss.gov.cn/cqwx/wx/socialSecurity/cFList.action"
                }
                method = "get" if opt == "info" else "post"

                medical = Medical(session)
                response = await self.browser.fetch(medical.make_request(method, url[opt], start, end))
                raw = response.body.decode("utf-8")
                result = medical.parse_html(opt, raw)
                self.send_json_response(result)
            # ============================
            # Employment injury insurance
            # ============================
            elif action_str.startswith("injury"):
                url = {
                    "info": "http://cqjy.cqhrss.gov.cn/cqwx/wx/socialSecurity/iBInfo.action",
                    "detail": "http://cqjy.cqhrss.gov.cn/cqwx/wx/socialSecurity/iCList.action"
                }
                method = "get" if opt == "info" else "post"

                injury = Injury(session)
                response = await self.browser.fetch(injury.make_request(method, url[opt], start, end))
                raw = response.body.decode("utf-8")
                result = injury.parse_html(opt, raw)
                self.send_json_response(result)
            # =======================
            # Unemployment insurance
            # =======================
            elif action_str.startswith("unemployment"):
                url = {
                    "info": "http://cqjy.cqhrss.gov.cn/cqwx/wx/socialSecurity/uBInfo.action",
                    "detail": "http://cqjy.cqhrss.gov.cn/cqwx/wx/socialSecurity/uCList.action"
                }
                method = "get" if opt == "info" else "post"

                unemployment = Unemployment(session)
                response = await self.browser.fetch(unemployment.make_request(method, url[opt], start, end))
                raw = response.body.decode("utf-8")
                result = unemployment.parse_html(opt, raw)
                self.send_json_response(result)
            # ====================
            # Maternity insurance
            # ====================
            else:
                url = {
                    "info": "http://cqjy.cqhrss.gov.cn/cqwx/wx/socialSecurity/queryBirthInsuredInfo.action",
                    "detail": "http://cqjy.cqhrss.gov.cn/cqwx/wx/socialSecurity/queryBirthJfDetail.action?startRow=1&endRow=1200"
                }
                method = "get"

                maternity = Maternity(session)
                response = await self.browser.fetch(maternity.make_request(method, url[opt], start, end))
                raw = response.body.decode("utf-8")
                result = maternity.parse_html(opt, raw)
                self.send_json_response(result)
