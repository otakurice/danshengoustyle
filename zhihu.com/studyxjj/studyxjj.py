#!/usr/bin/python3

import requests,json,re,time,os,jieba
import matplotlib.pyplot as plt
from scipy.misc import imread
from wordcloud import WordCloud,ImageColorGenerator
from collections import Counter

def txtcreat(filename,filelist):
	txt = open('%s/%s的%s.txt' % (user_name,user_name,filename),'w')
	for f in filelist:
		txt.write(f[0] + '\n')
		txt.write(f[1] + '\n\n')
	txt.close()

def sex(gender):
	if gender == 1:
		ta = '他'
	elif gender == 0:
		ta = '她'
	else:
		ta = 'ta'
	return ta

def wordfre(filename,filelist):
    if len(filelist):
        wordlist = []
        wordlist_new = []
        isCN = 1
        back_coloring = imread("bg.jpg")
        stopwords = {}.fromkeys([line.rstrip() for line in open('stopwords.txt')]) # 停用词词表
        cloud = WordCloud(font_path='font.ttf', # 若是有中文的话，这句代码必须添加，不然会出现方框，不出现汉字
                background_color="white",  # 背景颜色
                max_words=2000,  # 词云显示的最大词数
                mask=back_coloring,  # 设置背景图片
                max_font_size=100,  # 字体最大值
                random_state=42,
                width=1000, height=860, margin=2,# 设置图片默认的大小,但是如果使用背景图片的话,那么保存的图片大小将会按照其大小保存,margin为词语边缘距离
                )
        for fi in filelist:
            if type(fi) is list:
                for li in fi:
                    wordlist += jieba.cut(li,cut_all = False)
            else:
                wordlist += jieba.cut(fi,cut_all = False)
        for w in wordlist:
        	if w not in stopwords:
        		wordlist_new.append(w)
        wordstr = (',').join(wordlist_new)
        wc = cloud.generate(wordstr)
        image_colors = ImageColorGenerator(back_coloring)
        plt.figure("wordc")
        plt.imshow(wc.recolor(color_func=image_colors))
        wc.to_file('%s/%s的%s词云.png' % (user_name,user_name,filename))
        worddict = Counter(wordlist_new)
        print('%s%s的词频：\n%s' % (user_name,filename,worddict.most_common(20)))

user_id = 'wang-dong-ci'
url = 'https://www.zhihu.com/api/v4/members/' + user_id + '/activities?limit=10&desktop=True'
headers = {
    'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
    'authorization': 'oauth c3cef7c66a1843f8b3a9e6a1e3160e20'
}
answer_list = [] #回答列表
article_list = [] #发表文章列表
vote_list = [] #赞同回答+赞同文章列表
column_follow = [] #关注专栏列表
question_list = [] #创建问题列表
question_list_number = 0
question_follow = [] #关注问题列表
question_follow_number = 0
topic_follow = [] #关注话题列表
topic_follow_number = 0
collect_follow = [] #关注收藏夹列表
collect_follow_number = 0
livejoin_list = [] #参加的live列表
i=1
while True:
	req = requests.get(url,headers=headers)
	req.encoding = 'utf-8'
	result = json.loads(req.text)
	user_name = result['data'][0]['actor']['name']
	gender = result['data'][0]['actor']['gender']
	print('正在获取第' + str(i) + '页动态…')
	i+=1
	for d in result['data']:
		print(d['verb'])
		if d['verb'] == 'ANSWER_CREATE':
			content = re.sub('<.*?>','',d['target']['content'])
			# print(content)
			answer_list.append([d['target']['question']['title'],content])
		elif d['verb'] == 'MEMBER_CREATE_ARTICLE':
			content = re.sub('<.*?>','',d['target']['content'])
			# print(content)
			article_list.append([d['target']['title'],content])
		elif d['verb'] == 'QUESTION_CREATE':
			print(d['target']['title'])
			question_list.append(d['target']['title'])
			question_list_number+=1
		elif d['verb'] == 'ANSWER_VOTE_UP':
			content = re.sub('<.*?>','',d['target']['content'])
			print(d['target']['question']['title'])
			# print(content)
			vote_list.append([d['target']['question']['title'],content])
		elif d['verb'] == 'QUESTION_FOLLOW':
			print(d['target']['title'])
			question_follow.append(d['target']['title'])
			question_follow_number+=1
		elif d['verb'] == 'TOPIC_FOLLOW':
			print(d['target']['name'])
			topic_follow.append(d['target']['name'])
			topic_follow_number+=1
		elif d['verb'] == 'MEMBER_VOTEUP_ARTICLE':
			content = re.sub('<.*?>','',d['target']['content'])
			print(d['target']['title'])
			# print(content)
			vote_list.append([d['target']['title'],content])
		elif d['verb'] == 'MEMBER_FOLLOW_COLUMN':
			print(d['target']['title'])
			column_follow.append(d['target']['title'])
		elif d['verb'] == 'MEMBER_FOLLOW_COLLECTION':
			print(d['target']['title'])
			collect_follow.append(d['target']['title'])
			collect_follow_number+=1
		elif d['verb'] == 'LIVE_JOIN':
			print(d['target']['subject'])
			livejoin_list.append(d['target']['subject'])
	if result['paging']['is_end'] is False:
		url = result['paging']['next']
		# print(url)
	else:
		break
	time.sleep(5)

if os.path.exists(user_name) is False:
	os.mkdir(user_name)
text = open('%s/%s的研究报告.txt' % (user_name,user_name),'w')
text.write('%s关注了%s个话题，%s个收藏夹，%s向知友们提出了%s个问题，对%s个问题很感兴趣。\n' % (user_name,topic_follow_number,collect_follow_number,sex(gender),question_list_number,question_follow_number))
text.write('%s关注的话题有：\n' % user_name)
for t in topic_follow:
	text.write('  %s' % t)
text.write('\n%s关注的收藏夹有：\n' % sex(gender))
for c in collect_follow:
	text.write('  %s\n' % c)
text.write('\n%s提出的问题有：\n' % sex(gender))
for q in question_list:
	text.write('  %s\n' % q)
text.write('\n%s很感兴趣的问题有：\n' % sex(gender))
for q in question_follow:
	text.write('  %s\n' % q)
text.close()
txtcreat('赞同合辑',vote_list)
txtcreat('回答合辑',answer_list)
txtcreat('文章合辑',article_list)
wordfre('关注问题',question_follow)
wordfre('赞同回答+文章',vote_list)
wordfre('回答问题',answer_list)
wordfre('发表文章',article_list)