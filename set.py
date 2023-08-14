#设置文件#
import random
#系统
mapwidth,mapheight=1600,1600#地图长宽,不要小于屏幕
screen_width,screen_height=720,1600#屏幕宽，屏幕长
#总游戏
human_num=65#初始人类数量
human_max=100#人类数量上限
resource=1.1#资源密度
resource_maxnum=2000#资源最大值
resource_minnum=100#资源最小值
build_m=800#建造范围(越大建筑建的越少)
build_gl=9.5#消极建造性(越大越不愿意造建筑)
move_f=430#人类会去往多少范围内的熟悉建筑物
min,max=-80,80#人类在定居地移动的范围
gl1=0.6#人类没事干 去熟悉建筑的概率,则去熟悉人类的概率为1-gl
eat_f=500#人类去蹭饭的最大范围
sleep_f=500#同上
sl_i1,sl_a1=0.02,0.1#在房子里睡多久(小-大) 值越小睡得越久
sl_i,sl_a=0.04,0.2#在外面睡 同上
hs=0#睡外面的概率 关系到人类是睡外面还是睡里面
food=5#食物工坊中最少有多少食物人类才去进食
tl=9#工作耗费的体力
#资源正常1000
fps=60#帧率
#人类设置,大部分数据上限为100
def seth():
	global sr,cv,jl,mj,pc,age,bs,maxhp,hp,tltn,wntn,btn,ts,sh,wg,md,jm,gl,zl
	sr=random.randrange(30,50)#身体素质
	cv=random.randrange(10,50)#智力
	jl=100#精力
	mj=random.randrange(300,550)#敏捷
	pc=random.randrange(1,100)#政治
	age=20#年龄
	bs=50#饱食度
	maxhp=random.randrange(100,150)#生命值上限
	hp=maxhp
	tltn=40#工具科技
	wntn=1#武器科技
	btn=2#建筑科技
	ts=0#财富
	sh=0#实力
	wg=age#顽固
	md=0#正负情绪(沮丧-高兴)0~50~100
	jm=0#激进情绪(平淡-愤怒)
	gl=50#个人利益
	zl=50#集体利益