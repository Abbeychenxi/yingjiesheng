# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


import requests
import time
import sqlite3
import jieba
from scrapy import log

class Industry:
    def __init__(self):
        electronicBusiness = set([u'电商', u'电子商务'])
        filmAndTelevisionDrama = set([u'电影', u'戏剧'])
        education = set([u'教育', u'教师', u'校长', u'教学', u'老师', u'幼儿园', u'中学', u'实验学校', u'培训中心'])
        medicalCare = set([u'医生', u'医院', u'妇幼保健', u'社区卫生', u'中医医院', u'卫生局'])
        music = set([u'音乐'])
        software = set([u'软件', u'软件工程', u'运维', u'系统', u'erp', u'java', u'c++', u'android', u'算法', u'驱动', u'应用开发', u'ios', u'前端', u'测试', u'.net', u'it', u'手机', u'移动', u'c', u'研究所', u'计算机', u'flash', u'intern', u'程序开发', u'engineer', u'评测', u'信息技术', u'软件开发', u'基础架构'])
        biological = set([u'生物', u'细胞', u'血清', u'染色体', u'军事医学科学院', u'医学'])
        pharmacy = set([u'制药', u'医药', u'药剂'])
        civil = set([u'土木', u'建筑', u'给排水', u'暖通', u'地产', u'城乡规划', u'城乡建设', u'工程造价', u'万科', u'恒大'])
        machinery = set([u'机械', u'飞行器', u'航空', u'硬件', u'操作工', u'汽车', u'光学', u'电机', u'汽车部件', u'机械装备', u'纺织机械', u'电梯'])
        electric = set([u'电气', u'电磁', u'低频'])
        electronic = set([u'电子', u'射频', u'天线', u'电控', u'半导体', u'单片机'])
        chemicalIndustry = set([u'化工', u'工艺', u'工程控制', u'精细化工'])
        material = set([u'材料', u'装饰'])
        insurance = set([u'保险', u'财产保险', u'人寿'])
        securities = set([u'证券', u'金融', u'基金', u'期货', u'投资', u'资本'])
        bank = set([u'银行', u'民生银行', u'支行', u'分行', u'兴业银行', u'信用社'])
        exhibition = set([u'会展'])
        foreignTrade = set([u'外贸'])
        communication = set([u'通信'])
        executiveSecretary = set([u'行政', u'文秘', u'VP', u'助理', u'管理', u'前台', u'经理', u'经理助理', u'ae', u'项目管理', u'村官'])
        customerService = set([u'客服', u'客户服务'])
        sales = set([u'销售', u'客户代表', u'客户经理'])
        reporterEditor = set([u'记者', u'编辑', u'推广', u'策划', u'文案', u'翻译', u'频道'])
        investmentBank = set([u'投行', u'投资', u'风险投资', u'信用', u'信托', u'投行部'])
        legal = set([u'法律', u'律师', u'律师事务所', u'政务'])
        advisory = set([u'咨询', u'顾问'])
        logistics = set([u'物流', u'进出口'])
        artAndDesign = set([u'艺术', u'设计', u'平面设计师', u'卡通形象设计师', u'平面设计'])
        finance = set([u'财务', u'会计', u'信贷', u'审计', u'出纳', u'财务处'])
        humanResources = set([u'人力资源', u'猎头', u'人事', u'人力资源部', u'hr', u'人力'])
        marketing = set([u'营销', u'运营', u'市场', u'策略', u'众筹', u'营销策划', u'市场部'])
        others = set([u'网管', u'家禽', u'育种', u'楼面'])
        internet = set([u'互联网', u'php', u'web前端', u'产品经理', u'云计算', u'数据处理', u'机器学习', u'数据挖掘', u'自然语言处理', u'研发', u'反病毒', u'网购安全', u'搜索', u'网站', u'数据分析', u'产品leader', u'研发', u'项目经理', u'大数据', u'语言', u'网络', u'python', u'django', u'网页', u'web', u'数据', u'前端开发', u'网络科技', u'百度', u'腾讯', u'360', u'产品', u'j2ee'])

        industry = {
            u"电商": electronicBusiness,
            u"影视/戏剧": filmAndTelevisionDrama,
            u"教育": education,
            u"医疗": medicalCare,
            u"音乐": music,
            u"软件": software,
            u"生物": biological,
            u"制药": pharmacy,
            u"土木": civil,
            u"机械": machinery,
            u"电气": electric,
            u"电子": electronic,
            u"化工": chemicalIndustry,
            u"材料": material,
            u"保险": insurance,
            u"证券": securities,
            u"银行": bank,
            u"会展": exhibition,
            u"外贸": foreignTrade,
            u"通信": communication,
            u"行政/文秘": executiveSecretary,
            u"客服": customerService,
            u"销售": sales,
            u"记者/编辑": reporterEditor,
            u"投行": investmentBank,
            u"法律": legal,
            u"咨询": advisory,
            u"物流": logistics,
            u"艺术/设计": artAndDesign,
            u"财务/会计": finance,
            u"人力资源": humanResources,
            u"市场营销": marketing,
            u"其他": others,
            u"互联网": internet
        }
        self.reversedIndustry = {}
        for key in industry.iterkeys():
            for value in industry[key]:
                self.reversedIndustry[value] = key

    def handleInfo(self, info):
        keywords = jieba.cut(info)
        infoIndustry = set()
        for word in keywords:
            if word in self.reversedIndustry:
                infoIndustry.add(self.reversedIndustry[word])
        return infoIndustry


class XiaozhaoptPipeline(object):
    Link = 'http://cv.test.xiaomo.com/api/job/job'
    industryHandler = Industry()
    def process_item(self, item, spider):
        ensureItem = self._conditionalItem_(item)
        r = requests.post(self.Link, data=ensureItem)
        log.msg(r.status_code, level=log.DEBUG)
        # if r.status_code == requests.codes.ok:
        #     try:
        #         sql = 'insert into links values ("' + ensureItem['link'] + '")'
        #         spider.cu.execute(sql)
        #         spider.cx.commit()
        #     except sqlite3.IntegrityError:
        #         sql = 'delete from links where url ="' + ensureItem['link'] + '"'
        #         spider.cu.execute(sql)
        #         spider.cx.commit()
        return item

    def _conditionalItem_(self, item):
        ensureItem = {}
        for key in ('link', 'job', 'place', 'type', 'email', 'tag', 'description', 'releaseTime', 'industry'):
            if key == 'link':
                try:
                    if item['link']:
                        ensureItem[key] = self.dealInfo(item['link'])
                    else:
                        ensureItem[key] = u''
                except KeyError:
                    pass
            elif key == 'job':
                try:
                    if item['title']:
                        ensureItem[key] = self.dealInfo(item['title'])
                    else:
                        ensureItem[key] = u''
                except KeyError:
                    pass
            elif key == 'place':
                try:
                    if item['workPlace']:
                        ensureItem[key] = self.dealInfo(item['workPlace'])
                        ensureItem[key] = ensureItem[key][1:] if ensureItem[key][0] == u',' else ensureItem[key]
                    else:
                        ensureItem[key] = u''
                except KeyError:
                    pass
            elif key == 'type':
                try:
                    if item['positionType']:
                        ensureItem[key] = self.dealInfo(item['positionType']).split(':')[-1]
                        ensureItem[key] = ensureItem[key].split(u'：')[-1]
                    else:
                        ensureItem[key] = u''
                except KeyError:
                    pass
            elif key == 'email':
                try:
                    if item['email']:
                        ensureItem[key] = self.dealInfo(item['email'])
                    else:
                        ensureItem[key] = u''
                except KeyError:
                    pass
            elif key == 'tag':
                try:
                    if item['professionalLabel']:
                        ensureItem[key] = self.dealInfo(item['professionalLabel'])
                    else:
                        ensureItem[key] = u''
                except KeyError:
                    pass
            elif key == 'description':
                try:
                    if item['description']:
                        t = u''
                        for index in item['description']:
                            t += index
                        ensureItem[key] = t
                    else:
                        ensureItem[key] = u''
                except KeyError:
                    pass
            elif key == 'releaseTime':
                try:
                    if item['releaseTime']:
                        ensureItem[key] = self.dealInfo(item['releaseTime'])
                    else:
                        ensureItem[key] = u''
                except KeyError:
                    pass
            elif key == 'industry':
                try:
                    info = ensureItem['job'] + self.dealInfo(item['position'])
                except KeyError:
                    info = ensureItem['job']
                if info:
                    industry = self.industryInfo(info)
                else:
                    industry = u'None'
                ensureItem[key] = industry
        return ensureItem

    def dealInfo(self, temp):
        t = u','.join(temp)
        return t

    def industryInfo(self, info):
        setOfIndustry = self.industryHandler.handleInfo(info.lower())
        industry = u','.join(setOfIndustry)
        return industry