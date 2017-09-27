# -*- coding: utf-8 -*

from pyquery import PyQuery as pq
import chardet
import urllib2
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import as_completed
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

pool = ThreadPoolExecutor(max_workers=5)
futures = []

sql = '''INSERT INTO wp_posts (post_author, post_content, post_title, post_status) 
SELECT '1', 
'%s', 
'%s',
'draft' FROM DUAL
 WHERE NOT EXISTS(SELECT post_title FROM wp_posts WHERE post_title = '%s');
INSERT INTO wp_term_relationships (object_id, term_taxonomy_id) 
SELECT 
	(SELECT LAST_INSERT_ID()), 
	(SELECT term_id FROM wp_terms WHERE name = '%s') FROM DUAL
 WHERE NOT EXISTS(SELECT object_id FROM wp_posts a
LEFT JOIN wp_term_relationships b
ON a.ID = b.object_id
 WHERE post_title = '%s' AND object_id IS NOT NULL);
'''

def foreachhtml(url, proxy = None, referer = None):
	print 'down:', url
	host = '/'.join(url.split('/')[0:3])

	# set http proxy  
	if proxy:  
		handlers = [urllib2.ProxyHandler({'http': 'http://%s/' % proxy, 'https': 'http://%s/' % proxy})]  
		opener =  urllib2.build_opener(*handlers)  
	else:  
		opener   =  urllib2.build_opener()  

	method   =  urllib2.Request(url)  
	# set HTTP Referer  
	if referer:  
		method.add_header('Referer', referer)  

	# add user agent  
	method.add_header('User-Agent', 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36')  
	method.add_header('Accept-Language', 'en-US,en;q=0.5')  
 
	result   =  opener.open(method, timeout=100)  

	TestData = result.read()
	encodingName = chardet.detect(TestData)['encoding']
	html = TestData
	if encodingName.startswith('GB'):
		html =  unicode(TestData, 'gbk')
		# html = html.encode('utf-8')
	return host, pq(html)


def queryhtml(url, callback, next_page):
	host, doc = foreachhtml(url)
	if callable(next_page):
		next_url = next_page(host, url, doc)
		if next_url != '':
			querystart(next_url, callback, next_page)
	if callable(callback):
		callback(host, url, doc)

def querystart(url, callback, next_page):
	print len(futures)
	futures.append(pool.submit(queryhtml, url, callback, next_page))

def downfile(url, filename):
	TestData = urllib.urlopen(url).read()
	imgf = open(filename, 'wb')
	imgf.write(TestData)
	imgf.close()

def returnURL(host, url):
	if url[0:7] == 'http://':
		return url
	else:
		return host+url

def down_next_page(host, url, doc):
	# if n <= -1 and doc('.next-page').html() is None:
	# 	down(url, n+1)
	# 	return
	b = True
	for i in doc('.nolink'):
		if pq(i).text().encode('utf-8') == '下一页':
			b = False
	if b:
		next_url = returnURL(host, pq(doc('.page a')[-2]).attr('href'))
		print pq(doc('.page a')[-2]).text().encode('utf-8'), next_url
		return next_url
		# down('/'.join(url.split('/')[0:-1])+'/'+doc('.next-page a').attr('href'));
	return ''


def down(host, url, doc):

	div = doc('.newslist ul li table tr')
	for i in div:
		i = pq(i)
		data = pq(i('td')[0]).text().encode('utf-8')
		icon = pq(i('td')[1]).text().encode('utf-8')
		title = pq(i('td')[2]).text().encode('utf-8')
		nurl = returnURL(host, pq(i('td')[2])('a').attr('href'))
		print data, icon, title, nurl
		_, text = foreachhtml(nurl)
		text = text('#text')
		pq(text('table tr')[-1]).remove()
		pq(text('table td')[-1]).remove()
		text('script').remove()
		# pq(text('table tr')[-1]).remove()
		text = text.html().encode('utf-8')
		text = text.replace('<img ', '<img class="alignnone size-medium wp-image-24" ')
		text = text.replace('MP4吧|WWW.MP4Pa.COM', 'WWW.YUNDAPIAN.COM')
		# icon = i('header .label-important').text()
		# title = i('header h2 a').text()
		# headimg = i('.thumb-span img').attr('src')
		# text = downbody(host, i('header h2 a').attr('href'))
		# if len(headimg.split('http')) <= 1: headimg = host + headimg
		# # s = ', '.join([icon, title, headimg])
		# # f.write(s+'\n')
		f.write(sql % (text, title, title, icon, title))


def downbody(host, url):
	try:
		if host == '':
			host = '/'.join(url.split('/')[0:3])
			url = '/'+'/'.join(url.split('/')[4:])
		_, doc = foreachhtml(host+url)

		# for i in doc('.article-content img'):
		# 	print pq(i).attr('src')
		# 	downfile(host+pq(i).attr('src'), 'img/'+pq(i).attr('src').split('/')[-1])
		text = doc('.article-content').html()
		text = text.replace('<img ', '<img class="alignnone size-medium wp-image-24" ')
		text = text.replace('"/uploads/', '"'+host+'/uploads/')
		if doc('.next-page').html():
			try:
				text += downbody('', host+'/'+'/'.join((url).split('/')[0:-1])+'/'+doc('.next-page a').attr('href'))
			except e:
				print e
		
		# print text
		return text
	except Exception, e2:
		print e2
	return ''


# f = open('down.txt', 'wb+')
# # down('http://zhainanshe.xyz/youguowang/')
# # querystart('http://zhainanshe.xyz/xiurenwang/', down, down_next_page)
# count = 0
# host, Adoc = foreachhtml("http://www.mp4pa.com")
# for i in Adoc('body')('.newmenu1 ul li a'):
# 	if count >= 1:
# 		iurl = returnURL(host, pq(i).attr('href').encode('utf-8'))
# 		iname = pq(i).html().encode('utf-8')
# 		print iname, iurl
# 		querystart(iurl, down, down_next_page)
# 	count += 1

# def isDone():
# 	for i in futures:
# 		if i.done() == False:
# 			for future in as_completed(futures):
# 				future.result()
# 			isDone()
# 			return
# isDone()

# f.close()

src = 'https://www.javbus3.com/'
srcName = 'AP-'

start = 31
end = 32 #399

for i in xrange(start, end):
	url = "%s%s%03d" % (src, srcName, i)
	host, Adoc = foreachhtml(url, "127.0.0.1:8787")
	print host