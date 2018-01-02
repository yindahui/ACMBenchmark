#!/usr/bin/env python
#-*- coding:utf-8 -*-

import urllib2
import re
import os.path
import sqlite3

#http://poj.org/
# 1. name ： ptt <div class="ptt" lang="en-US">*?</div>

class pkoj(object):
    def __init__(self, id):
        self.info = {}
        self.piclist = {}
        self.id = id
        self.url = "http://poj.org/"
        self.info['proid'] = str(id)

    def setID(self, id):
        self.id = id

    def check(self):
        url = '%sproblem?id=%d' % (self.url, self.id)
        response = urllib2.urlopen(url)
        content = response.read()
        p = '<div class="ptt" lang="en-US">(.*?)</div>'
        if re.search(p, content, re.S) != None:
            return True
        else:
            return False

    def getUrl(self):
        url = '%sproblem?id=%d' % (self.url, self.id)
        return url
    

    #获取网页源码
    def getHtmlResource(self, url):
        response = urllib2.urlopen(url)
        content = response.read()
        return content

    #从题目数据块中获取题目信息：
    def getProblemName(self, div):
        p = '<div class="ptt" lang="en-US">(.*?)</div>'
        self.info['name'] = re.search(p, div, re.S).group(1)
        return self.info

    #获取DescriptTion数据块
    def getDescription(self, source):
        p = r'<p class="pst">Description</p><div class="ptx" lang="en-US">(.*?)</div>'
        self.info['description'] = re.search(p, source, re.S).group(1)
        return self.info

    #获取Input数据块
    def getInput(self, source):
        p = r'<p class="pst">Input</p><div class="ptx" lang="en-US">(.*?)</div>'
        self.info['input'] = re.search(p, source, re.S).group(1)
        return self.info

    #获取Output数据块:
    def getOutput(self, source):
        p = r'<p class="pst">Output</p><div class="ptx" lang="en-US">(.*?)</div>'
        self.info['output'] = re.search(p, source, re.S).group(1)
        return self.info

    #获取Sample Input数据块:
    def getSampleInput(self, source):
        p = r'<p class="pst">Sample Input</p><pre class="sio">(.*?)</pre>'
        self.info['sampleinput'] = re.search(p, source, re.S).group(1)
        return self.info

    #获取Sample Output数据块:
    def getSampleOutput(self, source):
        p = r'<p class="pst">Sample Output</p><pre class="sio">(.*?)</pre>'
        self.info['sampleoutput'] = re.search(p, source, re.S).group(1)
        return self.info

    #获取图片信息并保存，并将超链接替换为图片名
    #piclist中存放的是图片链接。
    def getPicture(self):
        p = r'<img(.*?)src="(.*?)"'
        i = 1
        for key in self.info:
            content = self.info[key]
            #print content
            if re.search(p, content, re.IGNORECASE) != None:
                #content = '<img style="margin-left: 10px; margin-bottom: 10px;" src="images/3555_1.png" align="right"><img style="margin-left: 10px; margin-bottom: 10px;" src="images/3555_1.png" align="right">'
                imglist = re.findall(p, content, re.IGNORECASE)
                for img in imglist:
                    pic = img[1]
                    #print pic
                    picname = '%d_IMG_%d%s' % (self.id, i, os.path.splitext(pic)[1])
                    i=i+1
                    picurl = '%s%s' % (self.url, pic)
                    self.piclist[picname] = picurl
                    #替换字符串
                    self.info[key] = self.info[key].replace(pic, picname)

        #根据url下载图片信息。
        for key in self.piclist:
            print self.piclist[key]
            req = urllib2.urlopen(self.piclist[key])
            buf = req.read()
            self.piclist[key] = buf

        return self.piclist


    #获取一个题目所有信息
    def getAllInfo(self):
        url = '%sproblem?id=%d' % (self.url, self.id)
        #获取内容
        html = self.getHtmlResource(url)
        #获取题目
        self.getProblemName(html)
        self.getDescription(html)
        #获取Input
        self.getInput(html)
        self.getOutput(html)
        self.getSampleInput(html)
        self.getSampleOutput(html)

        self.getPicture()

        return (self.info, self.piclist)
        
        

    #打印所有信息：
    def printall(self):
        for key in self.info:
            print key+' : '+self.info[key]
        for key in self.piclist:
            print key+' : '+self.piclist[key]
    
    

#数据库存储类
'''
离线题库数据库文件为sqlite数据库，公包含两张表：
1. problem表
2. picure表
problem表：
-------------------------------------------------------
'''
class dbstorage():
    
    dbname = 'acm.db'

    def __init__(self):
        pass

    #建立连接数据库
    def getconn(self):
        self.conn = sqlite3.connect(self.dbname)
        self.conn.text_factory = str
        return self.conn

    #关闭数据库连接
    def closeconn(self):
        self.conn.close()

    #插入数据
    def insertData(self, infos, pictures):
        #创建游标对象
        c = self.conn.cursor()

        #插入题目信息
        #构造sql语句
        sql = 'insert into problem (proid, name, description, input, output, sampleinput, sampleoutput) values(?,?,?,?,?,?,?)'
        t = (infos['proid'], infos['name'], infos['description'], infos['input'], infos['output'], infos['sampleinput'], infos['sampleoutput'])
        c.execute(sql, t)
        self.conn.commit()

        #插入图片信息
        sql = 'insert into picture (name, image) values(?,?)'
        for key in pictures:
            t = (key, pictures[key])
            c.execute(sql, t)
            self.conn.commit()
            # 写到本地
            f = open('img/'+key, 'wb')
            f.write(pictures[key])
            f.close()

        
    

    
        


#response = urllib2.urlopen("http://poj.org/problem?id=1003")

#content = response.read()

#print getname(content)

def main():
    #url = 'http://poj.org/problem?id=1003'
    acm = pkoj(1000)
    db = dbstorage()
    db.getconn()
    
    for id in range(2853,4055):
        
        acm = pkoj(id)
        print '[+] Get %s ...' % acm.getUrl()
        if acm.check():
            (infos, pictures) = acm.getAllInfo()
            db.insertData(infos, pictures)
            print '  [-] Get %s successful!' % acm.getUrl()
        else:
            print '  [-] %s not found!' % acm.getUrl()

    db.closeconn()

def test():
    #url = 'http://poj.org/problem?id=1004'
    acm = pkoj(1004)
    db = dbstorage()
    db.getconn()
    (infos, pictures) = acm.getAllInfo()
    db.insertData(infos, pictures)

# main function
if __name__ == '__main__':
    main()
    




    
