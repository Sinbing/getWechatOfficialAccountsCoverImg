#*#* --- Coding By: UTF-8 --- *#*#
from func_timeout import FunctionTimedOut, func_timeout
import requests
from lxml import etree
import pyperclip
import time
import sys
import os


# ===== 静态文本变量 ==== #
outputText ='''----------------
该封面图片链接为：
'''



def resolveURL(html):
    global outputURL
    try:                                                                    # 尝试解析用户输入内容，过滤非文章URL内容
        htmlSouce:str = requests.get(html)
        etree_html:str = etree.HTML(htmlSouce.text)
        content:list = etree_html.xpath('/html/body/script[16]/text()')        # list 2 str |2
        script_txt:str = ''.join(content)
        script_var1:str = script_txt[script_txt.index('msg_cdn_url = \"'):]    # getImgURL |3
        script_var:str = script_var1[:script_var1.index('var cdn_url')]
        script_var2:str = script_var[:script_var1.index('\";')]
        outputURL = script_var2[15:]
    except:                                                                 # 无法处理输入URL时，给出报错
        print('无法解析到图片链接，请检查输入内容是否为公众号文章URL')
        shutdown(3)
    if outputURL != '':
        pyperclip.copy(outputURL)
        print (outputText + outputURL + '\n#=  封面URL已复制至剪贴板中  =#\n----------------\n')
    else:
        print ('无法解析到有效URL。')
        shutdown(5)


def downloadImg(URL):
    try:
        req = requests.get(URL)
        filename:str = ('封面.jpg')
        fileCount:int = 1
        while os.path.isfile(filename) == True:                                 # 查找软件根目录下是否已有下载后文件，若有-> 文件名= 封面n.jpg
            fileCountStr:str = str(fileCount)
            filename:str = '封面' + fileCountStr + '.jpg'
            fileCount = fileCount + 1
        with open(filename, 'wb') as f:
            f.write(req.content)
            print('下载成功\n')
            pyperclip.copy(inputHtml)                                                 # 更替剪贴板URL为原文章URL
            print(' -----剪贴板内容已更替为原微信公众号文章URL----- \n')
    except FunctionTimedOut:                                                        # 等待用户输入超时后退出
        sys.exit(0)


def cauFlag(flagValue:str):                                             # 解析 Flag 当Flag == y -> Value = 1 | Flag == n -> Value = 0 | Falg = ilegal -> shudown(5)
    global cauFlagValue
    cauFlagValue = 0
    if flagValue == 'y':
        cauFlagValue = 1
    elif flagValue == 'n':
        cauFlagValue = 0
    else:
        print('未检测到(y\\n)\n')                                   # 对于用户是否下载输入的非法判定
        shutdown(3)


def shutdown(stime):
    strtime = str(stime)
    print ('程序将在 ' + strtime + 's 后自动关闭。')
    time.sleep(stime)
    sys.exit(0)


if __name__ == '__main__':
    endProgame:str = 0
    while endProgame == 0:                                                          # 当用户确认关闭后方关闭程序。
        inputHtml:str = input('\n请输入需要获取封面的微信公众号文章URL: \n')             # UserInput -> inputHtml
        resolveURL(inputHtml)
        try:
            print('\n如需自动下载请在10s内输入 y ，超时后程序将自动关闭')
            downloadFlag = func_timeout(10, lambda: input('是否需要下载封面图片(y/n)\n'))    # 等待用户输入，输入y -> 下载 | 超时10s
            cauFlag(downloadFlag)
            if cauFlagValue == 1:
                downloadImg(outputURL)
            else:
                shutdown(3)
        except FunctionTimedOut:
            shutdown(0)
        try:
            print('\n如需继续下载文章图片请在10s内输入 y ，超时后程序将自动关闭')
            endProgameFlag = func_timeout(10,lambda: input('是否需要继续下载文章封面图片？ (y/n)\n')) # 等待用户输入，y -> 循环执行 n -> 退出
            cauFlag(endProgameFlag)
            if cauFlagValue == 0:
                endProgame = 1
        except FunctionTimedOut:
            shutdown(0)
    shutdown(3)