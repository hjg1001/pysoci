import pygame,set,random,main,math
pygame.init()
width, height =set.mapwidth,set.mapheight
scrn = pygame.display.set_mode((set.screen_width,set.screen_height))#屏幕
back=pygame.Surface((width,height),pygame.SRCALPHA)#背景图层
human_img=pygame.Surface((width,height),pygame.SRCALPHA)#人类图层
text_img=pygame.Surface((width,height),pygame.SRCALPHA)#文字信息图层
info_img=pygame.Surface((set.screen_width,set.screen_height),pygame.SRCALPHA)#游戏信息图层
pygame.display.set_caption("PYSOCI")
font1=pygame.font.SysFont('VonwaonBitmap-16px.ttf',36)
font2=pygame.font.SysFont('Terminus.ttf',13)
font3=pygame.font.SysFont('Terminus.ttf',25)
#元素列表
grass1= pygame.image.load("grass1.png")#草
grass2= pygame.image.load("grass2.png")
grass3= pygame.image.load("grass3.png")
grass4= pygame.image.load("grass4.png")
humancd1=pygame.image.load('人类/小孩.png')#人类小孩
humanad1=pygame.image.load('人类/普通.png')#人类成年
humanop1=pygame.image.load('人类/老人.png')#人类老人
sleep=pygame.image.load('人类/睡觉.png')
hm=pygame.image.load('人类/锤子.png')
gz=pygame.image.load('人类/镐子.png')
tired=pygame.image.load('人类/汗.png')
low_hp=pygame.image.load('人类/低生命值.png')
hungry=pygame.image.load('人类/饥饿.png')
fm1=pygame.image.load('建筑/1.png')#食物工坊
hs1=pygame.image.load('建筑/0.png')#房子
r_1=pygame.image.load('建筑/2.png')#研究所
r4=pygame.image.load('r4.png')#资源(大-小)
r3=pygame.image.load('r3.png')
r2=pygame.image.load('r2.png')
r1=pygame.image.load('r1.png')
#元素列表
scale = 0.3#视野缩放级别
ho=0#画面横向偏移
ve=0#画面纵向偏移
#类列表
world_time=0
human_list=main.create()#人类列表
human_relation=main.relation_create(human_list)#人类关系列表
rl=main.cr_r()
resource_list=rl[0]#资源列表
fm_bd_list=[]#食物工坊列表
hs_bd_list=[]#房子列表
r_bd_list=[]#研究所
#调试用
def get():
	a=0
	print('关系列表',human_relation)
	for obj in resource_list:
		a+=1
		print('资源',a,'\n'.join(['%s:%s' % item for item in obj.__dict__.items()]))
#调试用
for x in range(0,width,10):#创建艹
		for y in range(0,height,10):
			grassobj= pygame.transform.scale(eval('grass'+str(random.randrange(1,4))),(10,10))
			back.blit(grassobj,(x,y))
#主循环
running = True
game_running=True
clock=pygame.time.Clock()
z_s,a_s,m_u,m_d,m_l,m_r=False,False,False,False,False,False
while running:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_z:
				z_s=True
			if event.key==pygame.K_a:
				a_s=True
			if event.key==pygame.K_UP:
				m_u=True
			if event.key==pygame.K_DOWN:
				m_d=True
			if event.key==pygame.K_LEFT:
				m_l=True
			if event.key==pygame.K_RIGHT:
				m_r=True
			if event.key==pygame.K_p and game_running:
				game_running=False
			elif event.key==pygame.K_p and game_running==False:
				game_running=True
		if event.type == pygame.KEYUP:
			if event.key==pygame.K_z:
				z_s=False
			if event.key==pygame.K_a:
				a_s=False
			if event.key==pygame.K_UP:
				m_u=False
			if event.key==pygame.K_DOWN:
				m_d=False
			if event.key==pygame.K_LEFT:
				m_l=False
			if event.key==pygame.K_RIGHT:
				m_r=False
	if z_s and scale>0.3:
		scale-=0.1
	if a_s and scale<3:
		scale+=0.1
	if m_u:
		ve+=50
	if m_d:
		ve-=50
	if m_l:
		ho+=50
	if m_r:
		ho-=50
	if game_running:
		#更新时间
		world_time+=1/50
		world_time=round(world_time,2)
	clock.tick(set.fps)
	scrn.fill((0,0,0,0))
	info_img.fill((0,0,0,0))
	text_img.fill((0,0,0,0))
	human_img.fill((0,0,0,0))
	#帧率获取
	fs=clock.get_fps()
	if fs!=0:fs=int(fs)
	fps_img=font1.render('FPS:'+str(fs),True,(255,255,255))
	time_img=font1.render('Years:'+str(world_time),True,(255,255,255))
	scale_img=font1.render('pause:'+str(not game_running),True,(255,255,255))
	for b in fm_bd_list:#更新食物工坊
		b_obj=pygame.transform.scale(fm1,(30,30))
		if b.jd<300:
			xy=(b.x+5,b.y+5)
			b_text=font3.render(f'{int((b.jd/300)*100)}%',False,(255,255,255),(230,0,0))
		else:
			xy=[b.x+15,b.y-15]
			b_text=font3.render(f'{b.id} c_num{b.c_num} pnum{b.num}',False,(74,80,160))
		text_img.blit(b_text,xy)
		back.blit(b_obj,(b.x,b.y))
	for b in hs_bd_list:#更新房子
		b_obj=pygame.transform.scale(hs1,(30,30))
		if b.jd<300:
			xy=(b.x+5,b.y+5)
			b_text=font3.render(f'{int((b.jd/300)*100)}%',False,(255,255,255),(230,0,0))
		else:
			xy=[b.x+15,b.y-15]
			b_text=font3.render(f'{b.id} pnum{b.num}',False,(74,80,160))
		text_img.blit(b_text,xy)
		back.blit(b_obj,(b.x,b.y))
	for b in r_bd_list:#更新研究所
		b_obj=pygame.transform.scale(r_1,(30,30))
		if b.jd<300:
			xy=(b.x+5,b.y+5)
			b_text=font3.render(f'{int((b.jd/300)*100)}%',False,(255,255,255),(230,0,0))
		else:
			xy=[b.x+15,b.y-15]
			b_text=font3.render(f'{b.id} pnum{b.num} T{b.tltn} B{b.btn}',False,(74,80,160))
		text_img.blit(b_text,xy)
		back.blit(b_obj,(b.x,b.y))
	for h in human_list:#更新人类
		if game_running:
			h.live_state=False
			h.b_action(fm_bd_list,hs_bd_list)
			h.work_state=False
			if resource_list!=[] and not h.live_state:h.work_action(fm_bd_list,hs_bd_list,r_bd_list,resource_list)
			if not h.live_state and not h.work_state:h.action(r_bd_list)
			dead=h.nc(human_list,human_relation)
			if not dead:
				x1=h.move(fm_bd_list,hs_bd_list,r_bd_list,resource_list,human_relation,human_list)
			h.y+=x1[1]
			h.x+=x1[0]
		h.debug=h.state_pick
		hid_img=font2.render(f'        {h.hid}',False,(238,238,0))
		age_1_img=font2.render(f'{h.state}',False,(230,0,0))
		x_img=font2.render(f'{int(h.age)} {int(h.hp)} / {int(h.maxhp)}              {h.debug}',False,(255,0,0))
		if h.kj==0:
			text_img.blit(hid_img,(h.x,h.y-15))
			text_img.blit(age_1_img,(h.x,h.y-10))
			text_img.blit(x_img,(h.x,h.y-3))
		scale_x=int(h.x*scale)
		scale_y=int(h.y*scale)
		obj2=[]
		if h.age<10:#小孩
			obj=humancd1
		elif h.age>18 and h.age<50:#成年(普通)
			obj=humanad1
		else:#老年
			obj=humanop1
		if h.state=='sleep_1':
			obj=sleep
		humanobj= pygame.transform.scale(obj,[int(45*scale*h.age_1),int(45*scale*h.age_1)])
		if h.kj==0:
			human_img.blit(humanobj, [scale_x+ho, scale_y+ve])
			if 'build' in str(h.state):
				obj2.append(hm)
			if h.state=='pick':
				obj2.append(gz)
			if h.hp<h.maxhp*0.45:
				obj2.append(low_hp)
			if h.bs<30:
				obj2.append(hungry)
			if h.jl<30 and 'sleep' not in str(h.state):
				obj2.append(tired)
			if obj2!=[]:
				for obj0 in obj2:
					obj1=pygame.transform.scale(obj0,[int(45*scale*h.age_1),int(45*scale*h.age_1)])
					human_img.blit(obj1,(scale_x+ho,scale_y+ve))
		if h.target!=[0,0] and h.kj==0:
			pygame.draw.line(human_img,(22,219,195),[scale_x+ho,scale_y+ve],[h.target[0]*scale+ho,h.target[1]*scale+ve])#绘制线段
	for k in resource_list:#更新资源
		r_o= pygame.transform.scale(eval(k.img),(10,10))
		if k.num>2000 and k.img!='r4':
			k.img='r4'
		if 2000>k.num>1000 and k.img!='r3':
			k.img='r3'
		if 500<k.num<1000 and k.img!='r2':
			k.img='r2'
		if 500>k.num and k.img!='r1':
			k.img='r1'
			r_o= pygame.transform.scale(eval(k.img),(10,10))
		if k.num<0.1:#资源消失
			k.die(resource_list)
			r_o= pygame.transform.scale(eval('grass'+str(random.randrange(1,4))),(10,10))
		back.blit(r_o,(k.x,k.y))
	new_back=pygame.transform.scale(back,(int(width*scale),int(height*scale)))
	scrn.blit(new_back,(ho,ve))#最低图层 背景
	info_img.blit(fps_img,(0,0))#游戏信息
	info_img.blit(time_img,(-4,20))#
	info_img.blit(scale_img,(-4,40))#
	scrn.blit(info_img,(0,0))#
	new_text_img=pygame.transform.scale(text_img,(int(round(width*scale,0)),int(round(height*scale,0))))##
	scrn.blit(human_img,(0,0))#人类图层
	scrn.blit(new_text_img,(ho,ve))##人类信息
	#更新屏幕
	pygame.display.flip()