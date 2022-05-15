import requests
from bs4 import BeautifulSoup
import time 

#模拟浏览器行为
headers={'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36'}

def get_info(url):
	#获取网页数据
	wb_data=requests.get(url,headers=headers)
	#解析网页数据
	soup=BeautifulSoup(wb_data.text,'lxml')
	#获取歌曲排名数据
	ranks=soup.select('span.pc_temp_num')
	#获取title数据（包含歌手和歌名）
	titles=soup.select('div.pc_temp_songlist > ul > li > a')
	#获取歌曲时间数据
	times=soup.select('span.pc_temp_tips_r > span')

	for rank,title,time in zip(ranks,titles,times):
		data={'rank':rank.get_text().strip(),
				'singer':title.get_text().split('-')[1].strip(),
				'song':title.get_text().split('-')[0].strip(),
				'time':time.get_text().strip()}
	print(data)

if __name__=='__main__':
	#构造每一页的URL
	urls=['https://www.kugou.com/yy/rank/home/{}-8888.html'.format(str(i) for i in range(1,24))]
	for url in urls:
		get_info(url)

	#每隔一秒钟获取爬取一次
	time.sleep(1)


	


