# -*- coding: utf-8 -*-
import threading,Queue,hashlib
import json,os
import socket,ssl,httplib,urllib2

supercms=''
textbuff=1
ssl._create_default_https_context = ssl._create_unverified_context

def WebCMS(url):
    
    mulocal = threading.Lock()
    queue = Queue.Queue()
    http = 'http://'
    IsThread=[]

    r = open("data.json")
    f = json.load(r, encoding='utf-8')
    for x in f:
        queue.put(x)
    def miniwebcms(url):
        global supercms
        global textbuff
        while textbuff == 1:
            
            mulocal.acquire()
            x = queue.get()
            mulocal.release()
            zurl =http + url + x["url"]

            print zurl
            erbai = 0
            try:
                reurlopen = urllib2.urlopen(zurl,timeout=20)
                erbai = reurlopen.code
                xreurlopen = reurlopen.read()
                reurlopen.close()
            except urllib2.URLError as e:
                if hasattr(e, 'code'):
                    erbai = e.code
                elif hasattr(e, 'reason'):
                    continue
            except socket.timeout as e:
                continue
            except httplib.BadStatusLine as e:
                continue
            except socket.error as e:
                continue

            if erbai == 200:
                if x["md5"] == '':
                    urlbool = x["re"]
                    urlbool = str(urlbool)
                    if urlbool in xreurlopen:
                        recmsnameurl = 'http://'+url+x["url"] + ':' + x["name"]
                        supercms = recmsnameurl
                        textbuff = 0

                else:
                    m = hashlib.md5()
                    m.update(xreurlopen)
                    md5 = m.hexdigest()
                    if md5 == x["md5"]:
                        cmsnameurl = x["url"] + ':' + x["name"]
                        textbuff = 0
                        supercms = cmsnameurl

                    else:
                        pass
            if queue.empty():
                supercms = 'NULL'
                textbuff = 0
    for i in xrange(100):
        t = threading.Thread(target = miniwebcms,args=(url,))
        t.start()
        IsThread.append(t)

    for t in IsThread:
        t.join()
    return supercms

print WebCMS('www.baidu.com')