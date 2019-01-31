#! python3
# -*- coding: utf-8 -*-
'''
Created on 2018年11月25日

@author: danny
'''
import os
import threading
import time

from bs4 import BeautifulSoup
import requests



#the below should fill up
#header
headers = {'user-agent': 'you should write your user-agent here',
           'Cookie' : 'you should write your cookie here'
           }
#path
path = 'you should write your path here'

#get soup of website
def webin(url, headers = ''):
    #request
    if(headers == ''):
        text = requests.get(url)
    else:
        text = requests.get(url, headers = headers)
    
    #html
    if(text.text != ''):
        html = BeautifulSoup(text.text, 'html.parser')
    else:
        html = ''
        
    return  html
    
    
#download picture    
def download(src, count, headers):    
    fail = 0
    time.sleep(10)
    while(True):
        try:
            picture = requests.get(src, headers = headers)
            #try to get picture src
            if picture.status_code == 200:
                open(path + str(count) + '.jpg', 'wb').write(picture.content)
                break
            else:
                raise
        #fail to download, retry
        except:
            #fail too much time
            if fail >= 5:
                print('Picture ' + str(count) + 'Download fail')
                break
            
            print('Download Fail!!!  retry')
            fail += 1
            
#get each picture url            
def GetPicture(url, headers):
    #loop variable
    href = ''
    count = 0
    fail = 0
    DownloadList = list()
    
    #loop for picture url
    while(url != href and count < 40):
        #init
        href = url
        #time.sleep(random.uniform(0.5,1))
        print(url)
        
        #try to get picture src
        try:
            #soup
            soup = webin(url, headers)  
            soup = soup.find('div', id = 'i3')
            
            #get picture url
            src = soup.find('img').get('src')
            
            #download picture
            count += 1
            num = int(url[url.find('-', 20) + 1 :])
            DownloadList.append(threading.Thread(target = download, args = (src, num, headers, )))
            DownloadList[count - 1].start()
            
            #next picture url
            url = soup.find('a').get('href')  
            
            fail = 0
            
        except:
            if fail >= 5:
                print('Get Picture URL Error!!')
                break
            
            print('Get Picture URL Fail!!!  retry')
            fail += 1        
            href = str(fail)
            time.sleep(10)
    
#url
url = input('輸入網址: ')

#soup
soup = webin(url, headers)

#folder name
name = soup.find('h1', id = 'gj').get_text()
if name == '':
    name = soup.find('h1', id = 'gn').get_text()
print(name)

#make a new folder
try:
    os.mkdir(path + name + '/')
except:
    name = input('檔名或路徑不合法，請輸入檔名: ')
    os.mkdir(path + name + '/')
    
path += name + '/'
print(path)

#loop variable
p = 0
fail = 1
PageList = list()

#loop for all page
while(True):
    try:
        #get first picture url in page
        pic = soup.find('div', class_ = 'gdtm').find('a')
        href = pic.get('href')
        print(href)
        
        #start to find picture url
        PageList.append(threading.Thread(target = GetPicture, args = (href, headers,)))
        PageList[p].start()
        p += 1
        
        #check for last  page
        page = soup.find_all('td', onclick = "document.location=this.firstChild.href")
        print(page[len(page) - 1].get_text())
        if(page[len(page) - 1].get_text() != '>'): break
        
        #next page
        print(url + '?p=' + str(p))
        soup = webin(url + '?p=' + str(p), headers)
        
    except:
        if fail >= 5:
            print('Main Loop Error!!')
            break
        
        print('Main Loop Fail!!!  retry')
        fail += 1   
        time.sleep(10)
        
print('finish')
