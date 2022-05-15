import requests
import re 

#模拟浏览器行为
headers={'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36'}
#初始化列表，用于装入爬虫信息
info_lists=[] 

def judgment_sex(class_name):
	if class_name=='womenIcon':
		return '女'
	else:
		return '男'

def get_info(url):
	#获取网页数据
	res=requests.get(url,headers=headers)
	IDs=re.findall('正则表达式',res.text,re.S)
	levels=re.findall('正则表达式',res.text,re.S)
	sexs=re.findall('正则表达式',res.text,re.S)
	contents=re.findall('正则表达式',res.text,re.S)
	laughs=re.findall('正则表达式',res.text,re.S)
	comments=re.findall('正则表达式',res.text,re.S)

	for ID,level,sex,content,laugh,comment in zip(IDs,levels,sexs,contents,laughs,comments):
		info={'id':ID,
				'level':level,
				'sex':judgment_sex(sex),
				'content':content,
				'laugh':laugh,
				'comment':comment}
	info_lists.append(info)

if __name__=='__main__':
	#构造每一页的URL
	urls=['网页地址不变部分{‘网页地址变化部分’}.html'.format(str(i) for i in range(1,24))]
	for url in urls:
		get_info(url)

	#遍历列表，创建TXT文件
	for info_list in info_lists:
		f=open('文件路径/filename.txt','a+')
		#写入数据到TXT中
		try:
			f.write(info_list['ID']+'\n')
			f.write(info_list['level']+'\n')
			f.write(info_list['sex']+'\n')
			f.write(info_list['content']+'\n')
			f.write(info_list['laugh']+'\n')
			f.write(info_list['comment']+'\n')
			f.close()
		except UnicodeEncodeError:
			pass 

	


