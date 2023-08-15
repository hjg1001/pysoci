import math,numpy as np
import set,random
class Mt:#计算类
	def move_coordinate(self,ar1,ar2,max_speed):
		#print('输进来的值',ar1,ar2,max_speed)
		distance_x = ar2[0]-ar1[0]
		distance_y = ar2[1] - ar1[1]
		distance = ((distance_x ** 2) + (distance_y ** 2)) ** 0.5
		direction_x = distance_x / distance
		direction_y = distance_y / distance
		jx=direction_x
		jy=direction_y
		dd=1
		if distance > max_speed:
			jx= direction_x * max_speed
			jy=direction_y * max_speed
			distance -= max_speed
		else:
			dd=0
		return [jx*5,jy*5,dd]
mt=Mt()
human_relation,human_list={},[]
class fm_bd:#民用工坊类,有科技前提下300资源升级一次
	def __init__(self,x,y,jd,id,lv):
		self.bd='fm'
		self.id=id
		self.x,self.y=x,y
		self.level=lv
		self.jd=jd#建造进度
		self.maxnum=1+lv#最大容量
		self.num=0#工坊内人数
		self.c_jd=0#生产产品的进度
		self.c_num=0#产品量
class hs_bd:#住所 300
	def __init__(self,x,y,jd,id,lv):
		self.bd='hs'
		self.id=id
		self.x,self.y=x,y
		self.level=lv
		self.jd=jd
		self.maxnum,self.num=2+lv,0
class r_bd:#研究所
	def __init__(self,x,y,jd,id,lv):
		self.bd='r'
		self.id,self.x,self.y,self.level,self.jd=id,x,y,lv,jd
		self.maxnum,self.num=2+lv,0
		self.tltn=0#工具科技
		self.wntn=0#武器
		self.btn=0#建筑
class Human:#人类类
	def __init__(self,x,y,hid):
		self.buid_a=0#建筑倾向
		self.debug=0#调试
		self.hid=hid
		self.id=0
		set.seth()
		self.x=x
		self.y=y
		self.sr=set.sr
		self.cv=set.cv
		self.jl=set.jl
		self.mj=set.mj
		self.pc=set.pc
		self.age=set.age
		self.bs=set.bs
		self.hp=set.hp
		self.maxhp=set.maxhp
		self.tltn=set.tltn
		self.wntn=set.wntn
		self.btn=set.btn
		self.ts=set.ts
		self.sh=set.sh
		self.sh_1=0#实力修正(同伙实力)
		self.wg=set.wg
		self.md=set.md
		self.jm=set.jm
		self.gl=set.gl
		self.zl=set.zl
		self.age_1=1#生长值(0-1)
		self.state=None
		self.target=[0,0]
		self.speed=1
		self.w_q=50#工作倾向
		self.w_q1=0#工作倾向修正
		self.b_q=50#建造倾向
		self.kj=0#所处空间 0室外 1室内
		self.bd_food=0#食物需求
		self.bd_fight=0#武力需求
		self.bd_house=0#住所需求
		self.bd_research=0#研究需求
		self.r=0#携带资源
		self.resource_obj=0#采集资源对象
		self.c_obj=0#两个多余的,不敢动(继续建造(升级)对象 工作对象)
		self.w_obj=0#
		self.bd_obj=0#进行建筑行为时的建筑对象
		self.work_bdid={}#更倾向于在哪些建筑工作/升级/建造(id)
		self.work_bd={}#id对应的对象
		self.state_pick=0#采集资源的目的
		self.live_bdid={}#更倾向于在哪些建筑居住(id)
		self.live_bd={}#id对应对象
		self.work_state=False#是否在工作状态
		self.live_state=False#是否在干一些必须做的事(进食等)
		self.pd=False#通用的判断变量
		self.pd2=False
		self.re_tool=0.3#研究工具加成
		self.re_build=0.3#研究建筑加成
		self.re_wp=0.3#研究武器加成
		self.l=0#学习计时器
	def die(self,human_list,human_relation):#死亡
		if self.kj==1:
			if self.w_obj!=0:
				if abs(self.x-self.w_obj.x)<10 and abs(self.y-self.w_obj.y)<10:
					self.w_obj.num-=1
			if self.bd_obj!=0:
				if abs(self.x-self.bd_obj.x)<10 and abs(self.y-self.bd_obj.y)<10:
					self.bd_obj.num-=1
		del human_relation[str(self.id)]
		human_list.remove(self)
		del self
	def nc(self,list2,list3):#基础值自然演变
		dead=False
		self.sh=self.sr*0.5+self.maxhp*0.2+self.hp*0.3+self.mj*0.1+self.cv*0.1+self.pc*0.1+self.sh_1
		#需求变化
		self.w_q=self.bd_food*100+self.w_q1+self.bd_research*1.3+100#注意修改
		if self.r<0:self.r=0
		if self.r>self.sr*0.2+self.tltn*0.1:self.r=self.sr*0.2+self.tltn*0.1
		self.bd_food=(self.jm*0.1+8)/(self.bs+self.md*0.1+0.1)
		self.bd_house=(self.jm*0.1+8)/(self.jl+self.md*0.1+0.1)
		self.bd_research=((self.cv*1.1+self.md*0.1)*0.03+0.2)/(self.jm*0.09+2.1)
		self.speed=((self.mj*0.5+self.sr*0.5+self.jl*0.4+self.md*0.1+self.jm*0.2)*self.age_1)/50#最大速度
		if self.hp>self.maxhp:self.hp=self.maxhp
		self.wg=self.age#顽固=年龄
		self.bs-=self.sr*0.001+random.random()*0.5#饱食度下降
		self.age+=1/50#年龄增长
		if self.age<=5:#五岁以下
			self.age_1,self.hp,self.maxhp,self.hp_1=0.01,10,10,0
		if self.age>5 and self.age<40 and self.age_1<1:#生长
			self.age_1+=self.bs*0.00009
		if self.age>=51:#五十岁以上
			self.age_1=(self.sr*0.9/((self.age-50)*0.5))*0.05
		if self.age_1<0:self.age_1=0.01
		if self.age_1>1:self.age_1=1
		if self.hp <=self.maxhp and self.bs>1:#生命值恢复
			self.hp+=(self.bs*0.03+self.sr*0.02+self.jl*0.009+self.md*0.008)*0.05*self.age_1
		if self.bs<1:
			self.bs=0.01
			self.hp-=random.random()/(self.sr*0.03*self.age_1)
		if self.hp<=0:
			self.die(list2,list3)
			dead=True
		return dead
	def pick(self,r_list):#采集(寻找资源并准备采集)
			k,b={},{}
			for i,r in enumerate(r_list):
				dis=((r.x-self.x)**2+(r.y-self.y)**2)**0.5
				k[str(i)]=dis
				b[str(i)]=r
			h=sorted(k,key=k.get)
			self.target=[b[h[0]].x,b[h[0]].y]
			self.state='pick'
			self.resource_obj=b[h[0]]
	def move(self,fm_bd_list,hs_bd_list,r_bd_list,r_list,human_relation,human_list):#闲置时的移动,通用移动
		#难绷写的我都看不懂
		new_xy=[0,0]
		if self.state==None:#如果状态为闲置
			if self.target==[0,0]:#如果没目标,设目标
					#抽取关系好的人或建筑并向其靠近
					gl=random.random()
					if self.jl<0:self.jl=0.1
					if gl>1-set.gl1:#靠近住房或工房
						gl2=random.random()
						if gl2>0.1 and self.work_bd!={}:#靠近工房
							r1=[]
							for r in (fm_bd_list):
								dis=((r.x-self.x)**2+(r.y-self.y)**2)**0.5
								if r in self.work_bd.values() and r.jd>300 and dis<set.move_f:
									r1.append(r)
							if r1!=[]:#如果有熟悉的建筑物
								k,b={},{}
								obj,T=False,False
								for i,r in enumerate(self.work_bdid):#i序列 r键名(id)
									k[str(i)]=self.work_bdid[r]#数值字典
									b[str(i)]=r#对象字典
								if not T:
									if len(self.work_bd)>4:
										obj=random.randrange(0,4)
									elif len(self.work_bd)==1:
										obj=True
									else:
										obj=random.randrange(0,len(self.work_bd)-1)
									h=sorted(k,key=k.get)
									if obj!=True:
										self.target=[self.work_bd[b[h[obj]]].x+random.randrange(set.min,set.max),self.work_bd[b[h[obj]]].y+random.randrange(set.min,set.max)]
									else:
										self.target=[self.work_bd[b[h[0]]].x+random.randrange(set.min,set.max),self.work_bd[b[h[0]]].y+random.randrange(set.min,set.max)]
									self.state='moving'
						elif self.live_bd!={}:#靠近住房
							r1=[]
							for r in (hs_bd_list):
								dis=((r.x-self.x)**2+(r.y-self.y)**2)**0.5
								if r in self.live_bd.values() and r.jd>300 and dis<set.move_f:
									r1.append(r)
							if r1!=[]:#如果有熟悉的建筑物
								k,b={},{}
								obj,T=False,False
								for i,r in enumerate(self.live_bdid):#i序列 r键名(id)
									k[str(i)]=self.live_bdid[r]#数值字典
									b[str(i)]=r#对象字典
								if not T:
									if len(self.live_bd)>4:
										obj=random.randrange(0,4)
									elif len(self.live_bd)==1:
										obj=True
									else:
										obj=random.randrange(0,len(self.live_bd)-1)
									h=sorted(k,key=k.get)
									if obj!=True:
										self.target=[self.live_bd[b[h[obj]]].x+random.randrange(set.min,set.max),self.live_bd[b[h[obj]]].y+random.randrange(set.min,set.max)]
									else:
										self.target=[self.live_bd[b[h[0]]].x+random.randrange(set.min,set.max),self.live_bd[b[h[0]]].y+random.randrange(set.min,set.max)]
									self.state='moving'
					elif human_relation[str(self.id)]!={}:#靠近人
						pass
					else:#啥都没有 目标随机
						if random.random() >0.7 and self.target==[0,0]:
							target1=[self.x+random.randrange(-200,200),self.y+random.randrange(-200,200)]
							#print('随机增长',target1[0]-self.x)
							self.target=[target1[0],target1[1]]
							self.state='moving'
		xg=0
		#如果目标超出地图
		if self.target[0]<0:
			#print('超左')
			self.target[0]+=random.randrange(int(-(self.target[0])),int(-(self.target[0]))+120)#右移
			xg=1
		if self.target[0]>set.mapwidth:
			xg=1
			#print('超右')
			self.target[0]-=random.randrange(int(self.target[0]-set.mapwidth),int(self.target[0]-set.mapwidth+120))#左移
		if self.target[1]<0:
			xg=1
			#print('超上')
			self.target[1]+=random.randrange(int(-(self.target[1])),int(-(self.target[1]))+120)#下移
		if self.target[1]>set.mapheight:
			self.target[1]-=random.randrange(int(self.target[1]-set.mapheight),int(self.target[1]-set.mapheight)+120)#上移
			#print('超下')
			xg=1
		if self.target!=[0,0] and xg!=1:
			arry=[abs(self.target[0]-self.x)<self.speed+10,abs(self.target[1]-self.y)<self.speed+10]
#-此处添加行为效果-
			if all(arry) and self.state=='moving':#继续瞎晃
				self.target=[0,0]
				self.state=None
			if all(arry) and self.state=='pick':#采集资源
				if self.resource_obj in r_list and self.r<self.sr*0.2+self.tltn*0.1:#资源没被挖完且有空间
					nm=(self.sr*0.009+self.md*0.01+self.tltn*0.4+self.jl*0.1)*0.1
					(self.resource_obj).num-=nm
					self.r+=nm
					self.work_state=True
					#精力减少
					mm=(nm*set.tl)/self.tltn+random.random()-random.random()
					if mm<0:mm=abs(mm)
					self.jl-=mm
					if self.jl<0:self.jl=0.1
					elif self.jl>100:self.jl=100
			if all(arry)and self.state=='build_fm':#建造新的食物工坊
				if self.r>0.01:
					fm=fm_bd(self.target[0],self.target[1],0,len(fm_bd_list),self.btn)
					fm_bd_list.append(fm)
					self.state='c_build'
					self.c_obj=fm
					self.work_state=True
			if all(arry)and self.state=='up':
				self.c_obj.level+=1
				self.c_obj.maxnum+=1
				self.c_obj.jd=0
				self.state=None
				self.target=[0,0]
			if all(arry)and self.state=='build_r':#建造新的研究所
				if self.r>0.01:
					fm=r_bd(self.target[0],self.target[1],0,len(r_bd_list),self.btn)
					r_bd_list.append(fm)
					self.state='c_build'
					self.c_obj=fm
					self.work_state=True
			if all(arry)and self.state=='build_hs':#建造新的食物工坊
				if self.r>0.01:
					fm=hs_bd(self.target[0],self.target[1],0,len(hs_bd_list),self.btn)
					hs_bd_list.append(fm)
					self.state='c_build'
					self.c_obj=fm
					self.work_state=True
			if self.state=='c_build':#强制修bug
				if self.c_obj.jd>300:
					self.state=None
					self.target=[0,0]
					self.state_pick=0
			if all(arry)and self.state=='c_build':#继续建造建筑物
				if self.r>0.01 and self.c_obj.jd<300:
					nm=(self.sr*0.009+self.md*0.01+self.tltn*0.4+self.jl*0.1)*0.4
					self.r-=nm
					(self.c_obj).jd+=nm
					mm=(nm*set.tl)/self.tltn+random.random()-random.random()
					if mm<0:mm=abs(mm)
					self.jl-=mm
					if self.jl<0:self.jl=0.1
					elif self.jl>100:self.jl=100
					if self.c_obj not in self.work_bd.values() or self.work_bd=={}:
						if self.c_obj.bd!='hs':
							self.work_bdid[str(self.c_obj.id)]=random.random()
							self.work_bd[str(self.c_obj.id)]=self.c_obj
					if self.c_obj not in self.live_bd.values() or self.live_bd=={}:
						if self.c_obj.bd=='hs':
							self.live_bdid[str(self.c_obj.id)]=random.random()
							self.live_bd[str(self.c_obj.id)]=self.c_obj
					else:#继续建造建筑时增加对它的熟悉度
							if self.c_obj.bd!='hs':
								obj=[key for key, value in self.work_bd.items()if value==self.c_obj]
								self.work_bdid[obj[0]]+=random.random()
							if self.c_obj.bd=='hs':
								obj=[key for key, value in self.live_bd.items()if value==self.c_obj]
								self.live_bdid[obj[0]]+=random.random()
					self.work_state=True
				elif self.c_obj.jd<300:
					self.pick(r_list)
					self.state_pick='c_build'
			if self.w_obj!=0 and (self.w_obj.num>self.w_obj.maxnum or self.w_obj.num<0):
				self.w_obj.num=0
			if self.state=='work' and (self.w_obj).num>=(self.w_obj).maxnum and self.kj ==0:
				self.state=None
				self.target=[0,0]
				self.state_pick=0
			if self.state=='work' and self.w_obj.bd=='hs':
				obj=[key for key, value in self.work_bd.items()if value==self.w_obj]
				del self.work_bdid[obj[0]]
				del self.work_bd[obj[0]]
			if self.state=='eat':#迷知途返 没吃的就不去
				self.live_state=True
				if self.bd_obj.c_num<set.food:
					self.state=None
					self.target=[0,0]
			if self.state=='sleep':
				self.live_state=True
				if self.bd_obj.num>=self.bd_obj.maxnum and self.kj==0:
					self.state=None
					self.target=[0,0]
			if self.state=='pick':
				if self.resource_obj not in r_list:
					self.state=None
					self.target=[0,0]
			if all(arry) and self.state=='work':
				self.work_state=True
				#食物工坊工作
				if self.r>0.1 and self.w_obj.bd=='fm':
					if self.kj==0:
						self.w_obj.num+=1
						self.pd=True
					self.kj=1
					nm=(self.sr*0.009+self.md*0.01+self.tltn*0.4+self.jl*0.1)*0.4
					self.w_obj.c_jd+=nm
					self.r-=nm
					self.w_q1+=random.random()
					obj=[key for key, value in self.work_bd.items()if value==self.w_obj]
					self.work_bdid[obj[0]]+=random.random()
					mm=(nm*set.tl)/self.tltn+random.random()-random.random()
					if mm<0:mm=abs(mm)
					self.jl-=mm
					if self.jl<0:self.jl=0.1
					elif self.jl>100:self.jl=100
					if self.w_obj.c_jd>20:
						self.w_obj.c_num+=1
						self.w_obj.c_jd-=20
					if self.w_obj.c_jd<0:
						self.w_obj.c_jd=0
				elif self.w_obj.bd=='fm':
					if self.pd:
						self.w_obj.num-=1
						self.pd=False
					self.kj=0
					self.state=None
					self.target=[0,0]
				#研究所工作
				if self.r>0.01 and self.w_obj.bd=='r':
					if self.kj==0:self.w_obj.num+=1
					self.kj=1
					nm=(self.cv*0.02+self.md*0.01+self.tltn*0.03+self.jl*0.1)*0.01
					mm=(nm*set.tl)/self.tltn+random.random()-random.random()
					if mm<0:mm=0.1
					#决定研究什么
					re=0
					o=self.re_tool+self.re_build+self.re_wp
					if o==0:
						u=['tool','build']
						re=u[random.randrange(0,1)]
					else:
						if self.re_tool/o>random.random():
							re='tool'
						elif self.re_build/o>random.random():
							re='build'
					if re=='tool':
						if self.w_obj.tltn<self.tltn:#提高研究所的科技水平
							self.w_obj.tltn+=nm*5+self.re_tool
							self.jl-=mm
							self.r-=nm*2
						else:#提高自己水平
							self.tltn+=nm
							self.jl-=mm
							self.r-=nm
							self.re_tool+=random.random()*0.01
					if re=='build':
						if self.w_obj.btn<self.btn:
							self.w_obj.btn+=nm*5+self.re_build
							self.jl-=mm
							self.r-=nm*2
						else:
							self.btn+=nm
							self.r-=nm
							self.jl-=mm
							self.re_build+=random.random()*0.01
				elif self.w_obj.bd=='r':
					if self.kj==1:self.w_obj.num-=1
					self.kj=0
					self.state=None
					self.target=[0,0]
			elif all(arry) and self.state=='eat':
				if self.bd_obj.c_num>0 and self.bd_food>random.uniform(0.2,0.3):
					num=(100-self.bs)/10+random.randrange(-1,1)#该人类顺走的食物数量
					if num<0:num=1
					if num>self.bd_obj.c_num:num=self.bd_obj.c_num
					self.bd_obj.c_num-=num
					self.bs+=10*num
					self.kj=1
				else:
					self.kj=0
					self.state=None
					self.target=[0,0]
			if self.state=='sleep':
				if self.bd_obj.num<0:
					self.bd_obj.num=0
			if self.state=='teach':
				for i in human_list:
					if ((i.x-self.x)**2+(i.y-self.y)**2)**0.5<100:
						nm=(self.cv*0.02+self.md*0.01+self.pc*0.03+self.jl*0.1)*0.01
						if i.tltn<self.tltn:
							i.tltn+=nm*4
						elif i.btn<self.btn:
							i.btn+=nm*4
						elif i.wntn<self.wntn:
							i.wtn+=nm*4
				self.state=None
				self.target=[0,0]
			if self.state=='learn':
				for i in r_bd_list:
					if ((i.x-self.x)**2+(i.y-self.y)**2)**0.5<100 and self.l>random.randrange(3,6) and self.tltn<i.tltn:
						self.tltn+=0.01
						self.l+=0.1
					else:
						self.state=None
						self.target=[0,0]
			if all(arry) and self.state=='sleep':#睡室内
				if self.bd_house>random.uniform(set.sl_i1,set.sl_a1):
					self.jl+=random.random()*random.uniform(2,4)
					if self.kj==0:self.bd_obj.num+=1
					self.kj=1
					self.live_state=True
					self.live_bdid[str(self.bd_obj.id)]=random.random()
					self.live_bd[str(self.bd_obj.id)]=self.bd_obj
				elif self.bd_house<random.uniform(set.sl_i1,set.sl_a1):#睡饱了
					self.kj=0
					self.state=None
					self.target=[0,0]
					self.bd_obj.num-=1
			if all(arry) and self.state=='sleep_1':#睡外面
				if self.bd_house>random.uniform(set.sl_i,set.sl_a):#数值越大睡得越少
					self.jl+=random.random()*random.uniform(1,2)
				else:
					self.state=None
					self.target=[0,0]
		if self.target!=[0,0] and self.state!='sleep_1':#如果有目标，继续移动
			#print('原始',[self.x,self.y])
			#print('目标',self.target)
			#print('速度',self.speed)
			new_xy=mt.move_coordinate([self.x,self.y],[self.target[0],self.target[1]],self.speed)
			if new_xy[2]==0: self.target=[self.x,self.y]
			#print('增长值',new_xy,'\n')
		return new_xy
#-此处定义行为-
	def build_fm(self,fm_bd_list,r_list):
			if 0.01+self.bd_food+random.uniform(0,0.5)>random.uniform(0.2,10):#初始0.1%概率建造
				#建造食物工坊(自动检测)
				if self.r>0.01:#创建一个新工坊
					cg=0
					if fm_bd_list=={}:
						self.target=[self.x*0.8,self.y*0.8]
					else:
						x1=self.x+random.randrange(-100,100)
						y1=self.y+random.randrange(-100,100)
					for k in fm_bd_list:
						if abs(k.x)+30==abs(x1)+30 and abs(k.y)+30==abs(y1)+30:
							cg=1
					if cg==0 and fm_bd_list!={}:
						self.target=[x1,y1]
					self.state='build_fm'
				elif r_list !=[]:
					self.pick(r_list)
					self.state_pick='build_fm'
	def build_hs(self,fm_bd_list,r_list):
			if 0.01+self.bd_house+random.uniform(0,0.5)>random.uniform(0.2,10):
				#建造房子(自动检测)
				if self.r>0.01:
					cg=0
					if fm_bd_list=={}:
						self.target=[self.x*0.8,self.y*0.8]
						self.state='build_hs'
					else:
						x1=self.x+random.randrange(-100,100)
						y1=self.y+random.randrange(-100,100)
						for k in fm_bd_list:
							if abs(k.x)+30==abs(x1)+30 and abs(k.y)+30==abs(y1)+30:
								cg=1
								break
					if cg==0 and fm_bd_list!={}:
						self.target=[x1,y1]
						self.state='build_hs'
				elif r_list !=[]:
					self.pick(r_list)
					self.state_pick='build_hs'
	def build_r(self,fm_bd_list,r_list):
		if 0.01+self.bd_research+random.uniform(0,0.5)>random.uniform(0.2,10):
			#建造研究所(自动检测)
			if self.r>0.01:
				cg=0
				if fm_bd_list=={}:
					self.target=[self.x*0.8,self.y*0.8]
					self.state='build_r'
				else:
					x1=self.x+random.randrange(-100,100)
					y1=self.y+random.randrange(-100,100)
					for k in fm_bd_list:
						if abs(k.x)+30==abs(x1)+30 and abs(k.y)+30==abs(y1)+30:
							cg=1
							break
				if cg==0 and fm_bd_list!={}:
					self.target=[x1,y1]
					self.state='build_r'
			elif r_list !=[]:
				self.pick(r_list)
				self.state_pick='build_r'
	def upgrade(self,fm_bd_list,hs_bd_list,r_bd_list,r_list):
		r1,r2,w=[],[],False
		k={}
		#决定升级哪种类型的建筑
		bd=None
		#优先级低-高
		if 0.01+self.bd_research+random.uniform(0,0.5)>random.uniform(0.2,10) and r_bd_list!=[] and 0.99>random.random():
			bd='r'
		if 0.01+self.bd_house+random.uniform(0,0.5)>random.uniform(0.2,10) and hs_bd_list!=[] and 0.99>random.random() and not self.pd2:
			bd='house'
		if 0.01+self.bd_food+random.uniform(0,0.5)>random.uniform(0.2,10) and fm_bd_list!=[] and 0.99>random.random() and not self.pd:
			bd='food'
		self.pd,self.pd2=False,False
		if bd=='food':
			for r3,r in enumerate(fm_bd_list):#升级食物工坊
				dis=((r.x-self.x)**2+(r.y-self.y)**2)**0.5
				if dis<set.build_m and r.jd>=300 and r.level<int(self.btn):#在建筑范围内 帮
					r2.append(r)#其他不认识的建筑
				if r in self.work_bd.values() and r.jd>300 and r.level<int(self.btn):#是自己熟悉的建筑 帮
					r1.append(r)#熟悉的建筑
					w=True
		elif bd=='r':
			for r3,r in enumerate(r_bd_list):#继续造研究所
				dis=((r.x-self.x)**2+(r.y-self.y)**2)**0.5
				if dis<set.build_m and r.jd>=300 and r.level<int(self.btn):#在建筑范围内 帮
					r2.append(r)#其他不认识的建筑
				if r in self.work_bd.values() and r.jd>300 and r.level<int(self.btn):#是自己熟悉的建筑 帮
					r1.append(r)#熟悉的建筑
					w=True
		elif bd=='house':
			for r3,r in enumerate(hs_bd_list):
				dis=((r.x-self.x)**2+(r.y-self.y)**2)**0.5
				if dis<set.build_m and r.jd>=300 and r.level<int(self.btn):#在建筑范围内 帮
					r2.append(r)#其他不认识的建筑
				if r in self.work_bd.values() and r.jd>300 and r.level<int(self.btn):#是自己熟悉的建筑 帮
					r1.append(r)#熟悉的建筑
					w=True
		#决定升级(工作用建筑)
		if self.r>0 and r1!=[] and self.work_bd!={} and w and bd!='house':#如果有熟悉的建筑物
			k,b={},{}
			obj,T=False,False
			for i,r in enumerate(self.work_bdid):#i序列 r键名(id)
				k[str(i)]=self.work_bdid[r]#数值字典
				b[str(i)]=r#对象字典
			if not T:
				if len(self.work_bd)>4:
					obj=random.randrange(0,4)
				elif len(self.work_bd)==1:
					obj=True
				else:
					obj=random.randrange(0,len(self.work_bd)-1)
				h=sorted(k,key=k.get)
				if obj!=True:
					self.target=[self.work_bd[b[h[obj]]].x,self.work_bd[b[h[obj]]].y]
					self.c_obj=self.work_bd[b[h[obj]]]
				else:
					self.target=[self.work_bd[b[h[0]]].x,self.work_bd[b[h[0]]].y]
					self.c_obj=self.work_bd[b[h[0]]]
				self.state='up'
		elif r2 != [] and self.r<0.1 and bd!='house':#资源不足 去挖
				self.pick(r_list)
				self.state_pick='up'
		elif r1!= []and self.r<0.1 and bd=='house':#资源不足 去挖
				self.pick(r_list)
				self.state_pick='up'
		elif r2!=[] and self.work_bd=={} and bd!='house':#没有自己熟悉的建筑物 没造过建筑物 随便挑一个去继续建造
			if len(r1)<2:vs=0
			else:vs=random.randrange(0,len(r2)-1)
			self.work_bdid[str(len(self.work_bd))]=random.random()
			self.work_bd[str(len(self.work_bd))]=r2[vs]
		elif r2!=[] and bd!='house':#熟悉的建筑都已经完工 去建范围内其他建筑
				self.state='up'
				self.target=[r2[0].x,r2[0].y]
				self.c_obj=r2[0]
		elif r1==[] and r2==[] and bd=='food':
			self.pd=True
		#继续升级(房子)
		if self.r>0 and r1!=[] and self.live_bd!={} and w and bd=='house':#如果有熟悉的建筑物
			k,b={},{}
			obj,T=False,False
			for i,r in enumerate(self.live_bdid):#i序列 r键名(id)
				k[str(i)]=self.live_bdid[r]#数值字典
				b[str(i)]=r#对象字典
			if not T:
				if len(self.live_bd)>4:
					obj=random.randrange(0,4)
				elif len(self.live_bd)==1:
					obj=True
				else:
					obj=random.randrange(0,len(self.live_bd)-1)
				h=sorted(k,key=k.get)
				if obj!=True:
					self.target=[self.live_bd[b[h[obj]]].x,self.live_bd[b[h[obj]]].y]
					self.c_obj=self.live_bd[b[h[obj]]]
				else:
					self.target=[self.live_bd[b[h[0]]].x,self.live_bd[b[h[0]]].y]
					self.c_obj=self.live_bd[b[h[0]]]
				self.state='up'
		elif r2!= []and self.r<0.1 and bd=='house':
				self.pick(r_list)
				self.state_pick='up'
		elif r1!= []and self.r<0.1 and bd=='house':
				self.pick(r_list)
				self.state_pick='up'
		elif r2!=[] and self.live_bd=={} and bd=='house':
			if len(r1)<2:vs=0
			else:vs=random.randrange(0,len(r2)-1)
			self.live_bdid[str(len(self.live_bd))]=random.random()
			self.live_bd[str(len(self.live_bd))]=r2[vs]
		elif r2!=[] and bd=='house':
				self.state='up'
				self.target=[r2[0].x,r2[0].y]
				self.c_obj=r2[0]
		elif r1==[] and r2==[] and bd=='house':
			self.pd2=True
		if k=={}:
			self.state_pick=0
	def c_build(self,fm_bd_list,hs_bd_list,r_bd_list,r_list):#继续建造建筑(自动检测)
		r1,r2,w=[],[],False
		k={}
		#决定建造哪种类型的建筑
		bd=None
		#优先继续建造级低-高
		if 0.01+self.bd_research+random.uniform(0,0.5)>random.uniform(0.2,10) and r_bd_list!=[] and 0.99>random.random():
			bd='r'
		if 0.01+self.bd_house+random.uniform(0,0.5)>random.uniform(0.2,10) and hs_bd_list!=[] and 0.99>random.random() and not self.pd2:
			bd='house'
		if 0.01+self.bd_food+random.uniform(0,0.5)>random.uniform(0.2,10) and fm_bd_list!=[] and 0.99>random.random() and not self.pd:
			bd='food'
		self.pd,self.pd2=False,False
		if bd=='food':
			for r3,r in enumerate(fm_bd_list):#继续造食物工坊
				dis=((r.x-self.x)**2+(r.y-self.y)**2)**0.5
				if dis<set.build_m and r.jd<300:#在建筑范围内 帮
					r2.append(r)#其他不认识的建筑
				if r in self.work_bd.values() and r.jd<300:#是自己熟悉的建筑 帮
					r1.append(r)#熟悉的建筑
					w=True
		elif bd=='r':
			for r3,r in enumerate(r_bd_list):#继续造研究所
				dis=((r.x-self.x)**2+(r.y-self.y)**2)**0.5
				if dis<set.build_m and r.jd<300:#在建筑范围内 帮
					r2.append(r)#其他不认识的建筑
				if r in self.work_bd.values() and r.jd<300:#是自己熟悉的建筑 帮
					r1.append(r)#熟悉的建筑
					w=True
		elif bd=='house':
			for r3,r in enumerate(hs_bd_list):
				dis=((r.x-self.x)**2+(r.y-self.y)**2)**0.5
				if dis<set.build_m and r.jd<300:#在建筑范围内 帮
					r2.append(r)#其他不认识的建筑
				if r in self.live_bd.values() and r.jd<300:#是自己熟悉的建筑 帮
					r1.append(r)#熟悉的建筑
					w=True
		#决定继续建造(工作用建筑)
		if self.r>0 and r1!=[] and self.work_bd!={} and w and bd!='house':#如果有熟悉的建筑物
			k,b={},{}
			obj,T=False,False
			for i,r in enumerate(self.work_bdid):#i序列 r键名(id)
				k[str(i)]=self.work_bdid[r]#数值字典
				b[str(i)]=r#对象字典
			if not T:
				if len(self.work_bd)>4:
					obj=random.randrange(0,4)
				elif len(self.work_bd)==1:
					obj=True
				else:
					obj=random.randrange(0,len(self.work_bd)-1)
				h=sorted(k,key=k.get)
				if obj!=True:
					self.target=[self.work_bd[b[h[obj]]].x,self.work_bd[b[h[obj]]].y]
					self.c_obj=self.work_bd[b[h[obj]]]
				else:
					self.target=[self.work_bd[b[h[0]]].x,self.work_bd[b[h[0]]].y]
					self.c_obj=self.work_bd[b[h[0]]]
				self.state='c_build'
		elif r2 != [] and self.r<0.1 and bd!='house':#资源不足 去挖
				self.pick(r_list)
				self.state_pick='c_build'
		elif r1!= []and self.r<0.1 and bd=='house':#资源不足 去挖
				self.pick(r_list)
				self.state_pick='c_build'
		elif r2!=[] and self.work_bd=={} and bd!='house':#没有自己熟悉的建筑物 没造过建筑物 随便挑一个去继续建造
			if len(r1)<2:vs=0
			else:vs=random.randrange(0,len(r2)-1)
			self.work_bdid[str(len(self.work_bd))]=random.random()
			self.work_bd[str(len(self.work_bd))]=r2[vs]
		elif r2!=[] and bd!='house':#熟悉的建筑都已经完工 去建范围内其他建筑
				self.state='c_build'
				self.target=[r2[0].x,r2[0].y]
				self.c_obj=r2[0]
		elif r1==[] and r2==[] and bd=='food':
			self.pd=True
		#继续建造(房子)
		if self.r>0 and r1!=[] and self.live_bd!={} and w and bd=='house':#如果有熟悉的建筑物
			k,b={},{}
			obj,T=False,False
			for i,r in enumerate(self.live_bdid):#i序列 r键名(id)
				k[str(i)]=self.live_bdid[r]#数值字典
				b[str(i)]=r#对象字典
			if not T:
				if len(self.live_bd)>4:
					obj=random.randrange(0,4)
				elif len(self.live_bd)==1:
					obj=True
				else:
					obj=random.randrange(0,len(self.live_bd)-1)
				h=sorted(k,key=k.get)
				if obj!=True:
					self.target=[self.live_bd[b[h[obj]]].x,self.live_bd[b[h[obj]]].y]
					self.c_obj=self.live_bd[b[h[obj]]]
				else:
					self.target=[self.live_bd[b[h[0]]].x,self.live_bd[b[h[0]]].y]
					self.c_obj=self.live_bd[b[h[0]]]
				self.state='c_build'
		elif r2!= []and self.r<0.1 and bd=='house':#资源不足 去挖
				self.pick(r_list)
				self.state_pick='c_build'
		elif r1!= []and self.r<0.1 and bd=='house':#资源不足 去挖
				self.pick(r_list)
				self.state_pick='c_build'
		elif r2!=[] and self.live_bd=={} and bd=='house':#没有自己熟悉的建筑物 没造过建筑物 随便挑一个去继续建造
			if len(r1)<2:vs=0
			else:vs=random.randrange(0,len(r2)-1)
			self.live_bdid[str(len(self.live_bd))]=random.random()
			self.live_bd[str(len(self.live_bd))]=r2[vs]
		elif r2!=[] and bd=='house':#熟悉的建筑都已经完工 去建范围内其他建筑
				self.state='c_build'
				self.target=[r2[0].x,r2[0].y]
				self.c_obj=r2[0]
		elif r1==[] and r2==[] and bd=='house':
			self.pd2=True
		if k=={}:
			self.state_pick=0
	def work(self,fm_bd_list,r_list):#工作行为
		k,b,a={},{},False
		if self.work_bd!={}:#有熟悉的建筑 去最熟悉的建筑工作
			for i,r in enumerate(self.work_bd):#在食物工坊工作
				if self.work_bd[r].num<self.work_bd[r].maxnum and self.work_bd[r].jd>=300:
					k[str(i)]=self.work_bdid[r]
					b[str(i)]=self.work_bd[r]
			if k!={}:
				h=sorted(k,key=k.get)
				self.target=[b[h[0]].x,b[h[0]].y]
				self.state='work'
				self.w_obj=b[h[0]]
			elif fm_bd_list!=[]:#最熟悉的建筑满了 随便找一个继续干
				k,b={},{}
				for i,r in enumerate(fm_bd_list):
					dis=((r.x-self.x)**2+(r.y-self.y)**2)**0.5
					if dis<set.move_f and r.jd>300:
						k[str(i)]=dis
						b[str(i)]=r
				if k!={}:
					h=sorted(k,key=k.get)
					self.w_obj=b[h[0]]
					self.work_bdid[str(self.w_obj.id)]=random.random()
					self.work_bd[str(self.w_obj.id)]=self.w_obj
		elif fm_bd_list!=[]:#没有熟悉建筑 加一个离的最近的建筑物为熟悉建筑
			k,b={},{}
			for i,r in enumerate(fm_bd_list):
				dis=((r.x-self.x)**2+(r.y-self.y)**2)**0.5
				if dis<set.move_f and r.jd>300:
					k[str(i)]=dis
					b[str(i)]=r
			if k!={}:
				h=sorted(k,key=k.get)
				self.w_obj=b[h[0]]
				self.work_bdid[str(self.w_obj.id)]=random.random()
				self.work_bd[str(self.w_obj.id)]=self.w_obj
		if k!={} and self.r<0.01:
			self.pick(r_list)
			self.state_pick='work'
	def eat(self,fm_bd_list):#吃
		k,b={},{}
		for i,r in enumerate(fm_bd_list):
			dis=((r.x-self.x)**2+(r.y-self.y)**2)**0.5
			if r.c_num>set.food and dis<set.eat_f:
				k[str(i)]=dis
				b[str(i)]=r
		if k!={}:
			self.live_state=True
			h=sorted(k,key=k.get)
			self.target=[b[h[0]].x,b[h[0]].y]
			self.state='eat'
			self.bd_obj=b[h[0]]
	def sleep(self,hs_bd_list):#睡
		if self.live_bd!={}:#有熟悉的房子
			k,b={},{}
			for i,r in enumerate(self.live_bdid):
				dis=((self.live_bd[r].x-self.x)**2+(self.live_bd[r].y-self.y)**2)**0.5
				if self.live_bd[r].num<self.live_bd[r].maxnum and dis<set.sleep_f and self.live_bd[r].jd>=300:
					k[str(i)]=self.live_bdid[r]
					b[str(i)]=self.live_bd[r]
			if k!={}:#最熟悉的房子没住满
				self.live_state=True
				h=sorted(k,key=k.get)
				self.target=[b[h[0]].x,b[h[0]].y]
				self.state='sleep'
				self.bd_obj=b[h[0]]
			else:#满了
				k,b={},{}
				for i,r in enumerate(hs_bd_list):
					dis=((r.x-self.x)**2+(r.y-self.y)**2)**0.5
					if dis<set.sleep_f and r.jd>300:
						k[str(i)]=dis
						b[str(i)]=r
					if k!={}:
						self.live_state=True
						h=sorted(k,key=k.get)
						self.bd_obj=b[h[0]]
						self.live_bdid[str(self.bd_obj.id)]=random.random()
						self.live_bd[str(self.bd_obj.id)]=self.bd_obj
					elif set.hs>random.random():#周围没房子 睡地上
						self.state='sleep_1'
						self.live_state=True
						self.target=[self.x+3,self.y+3]
		else:#没有熟悉房子
			k,b={},{}
			for i,r in enumerate(hs_bd_list):
				dis=((r.x-self.x)**2+(r.y-self.y)**2)**0.5
				if dis<set.sleep_f and r.jd>300:
					k[str(i)]=dis
					b[str(i)]=r
			if k!={}:
				h=sorted(k,key=k.get)
				self.live_state=True
				self.bd_obj=b[h[0]]
				self.live_bdid[str(self.bd_obj.id)]=random.random()
				self.live_bd[str(self.bd_obj.id)]=self.bd_obj
			elif set.hs>random.random():
				self.state='sleep_1'
				self.live_state=True
				self.target=[self.x+3,self.y+3]
#-此处触发行为-
	#1.劳动行为(建造与劳作) 依靠资源的行为
	def work_action(self,fm_bd_list,hs_bd_list,r_bd_list,r_list):
		gl,dis,s=0,0,0
		if self.state=='pick' and self.r>=self.sr*0.2+self.tltn*0.1:
			if self.state_pick=='c_build':s='c_build'
			if self.state_pick=='work':s='work'
			if self.state_pick=='build_fm':s='build_fm'
			if self.state_pick=='build_hs':s='build_hs'
			if self.state_pick=='build_r':s='build_r'
			if self.state_pick=='up':s='up'
			if s==0:
				self.state=None
				self.target=[0,0]
		if (self.state==None and self.jl>2)or(s=='work'):#工作
			if self.w_q>15:
				self.work(fm_bd_list,r_list)
			elif s=='work':
				self.state=None
				self.target=[0,0]
		if (self.state==None or s=='up')and (fm_bd_list!=[] or hs_bd_list!=[]or r_bd_list!=[]) and 0.1>random.random():
			self.upgrade(fm_bd_list,hs_bd_list,r_bd_list,r_list)
		if (self.state==None or s=='c_build') and (fm_bd_list!=[] or hs_bd_list!=[] or r_bd_list!=[]):
			self.c_build(fm_bd_list,hs_bd_list,r_bd_list,r_list)#继续建造
		if self.state==None or s=='build_fm':#建造食物工坊
			for r in fm_bd_list:
				dis=(((r.x-self.x)**2)+((r.y-self.y)**2))**0.5
				if dis<set.build_m and r.num<r.maxnum:
					gl=set.build_gl
					break
				else:
					gl=0
			if 9.5-gl>random.uniform(8,14):#有建筑且未满员情况下难以建造
				self.build_fm(fm_bd_list,r_list)
				self.work_state=True
			elif s=='build_fm':
				self.state_pick=0
		if self.state==None or s=='build_hs':#建造房子
			gl=0
			for r in hs_bd_list:
				dis=(((r.x-self.x)**2)+((r.y-self.y)**2))**0.5
				if dis<set.build_m and r.num<r.maxnum:
					gl=set.build_gl
					break
				else:
					gl=0
			if 9.5-gl>random.uniform(8,14):
				self.build_hs(hs_bd_list,r_list)
				self.work_state=True
			elif s=='build_hs':
				self.state_pick=0
		if self.state==None or s=='build_r':#研究所
			gl=0
			for r in r_bd_list:
				dis=(((r.x-self.x)**2)+((r.y-self.y)**2))**0.5
				if dis<set.build_m and r.num<r.maxnum:
					gl=set.build_gl
					break
				else:
					gl=0
			if 9.5-gl>random.uniform(8,14):
				self.build_r(r_bd_list,r_list)
				self.work_state=True
			elif s=='build_r':
				self.state_pick=0
		return self.work_state
	#2.自然行为(转悠和社交,攻击等) 不耗资源的行为
	def action(self,r_bd_list):
		if not self.work_state:#没工作和劳动,触发自然行为
			if self.state==None and self.bd_research>random.uniform(0.2,19) and 0.1>random.random():
				self.state='teach'
			if self.state==None and self.bd_research>random.uniform(0.5,19)and 0.1>random.random()and r_bd_list!=[]:
				self.state='learn'
			if self.state==None:#随机移动(若无其他自然行为，最终手段)
				self.target=[0,0]
	#3.基础行为 不干可能会死的行为
	def b_action(self,fm_bd_list,hs_bd_list):
		if self.bd_food>random.uniform(0.2,0.3) and not self.work_state and self.state==None:#吃
			self.eat(fm_bd_list)
		if self.bd_house>random.uniform(0.2,0.3) and not self.work_state and self.state==None:#睡
			self.sleep(hs_bd_list)
class resource:
	def __init__(self,x,y):
		self.num=random.randrange(set.resource_minnum,set.resource_maxnum)#资源值
		self.x=x
		self.y=y
		self.img='r1'
	def die(self,r_list):#资源的消失
		r_list.remove(self)
		del self
def cr_r():#布置资源
	r_list=[]
	c_x=random.randrange(1000,set.mapwidth)
	c_y=random.randrange(1000,set.mapheight)#随机中心点
	for x in range(0,set.mapwidth,10):
		for y in range(0,set.mapheight,10):
			dis=abs(x-c_x)+abs(y-c_y)
			if random.random()<set.resource/(dis+1):
				k=resource(x,y)
				r_list.append(k)
	return r_list,c_x,c_y
def create():#布置人类
	u=0
	human_list=[]
	xy=np.random.rand(set.human_num, 2) * np.array([set.mapwidth, set.mapheight])
	for i in xy:
		human=Human(xy[u][0],xy[u][1],u)
		human_list.append(human)
		human=dict()
		u+=1
	return human_list
def relation_create(listname):
	po=0
	for i in listname:
		po=1
		z_id=random.randrange(2,100000)
		if i.id==z_id:
			z_id+=random.randrange(2,60000)
		human_relation[str(z_id)]={}
		i.id=z_id#创建关系树
		if po==0:#创建第一个关系树
			i.id=1
			human_relation[str(i.id)]={}
	return human_relation