import pygame				# 导入pygame模块
import sys					# 导入sys模块
import Bird					# 导入Bird模块
import BackGround 			# 导入BackGround模块
import Wall 				# 导入Wall模块

from pygame.locals import * # 导入pygame中的所有常量

pygame.init();				# 初始化pygame，为使用硬件做准备
pygame.mixer.init()			# 初始化混音器

# 背景音乐声音大小
mVolume = 0.1
# 音效声音大小
sVolume = 0.8
# 载入背景音乐及音效
pygame.mixer.music.load("sounds/background.ogg")
pygame.mixer.music.set_volume(mVolume)
pygame.mixer.music.play(-1)				# 循环播放背景音乐
wing = pygame.mixer.Sound("sounds/wing.ogg")
wing.set_volume(sVolume)
hit = pygame.mixer.Sound("sounds/hit.wav")
hit.set_volume(sVolume)
drop = pygame.mixer.Sound("sounds/drop.ogg")
drop.set_volume(sVolume)
bPass = pygame.mixer.Sound("sounds/pass.ogg")
bPass.set_volume(1)

# 窗口大小
screenSize = width, height = 288, 512
# 创建了一个窗口
screen = pygame.display.set_mode(screenSize)
# 设置敞口标题
pygame.display.set_caption("Flappy Bird")

# 得到背景对象
background = BackGround.BackGround(screenSize)
# 绘制背景
screen.blit(background.bgImages[0], background.rect[0])
screen.blit(background.ground, background.groundRect)

# 加载并绘制开始界面
gameReady = pygame.image.load("images/gameReady.png")
screen.blit(gameReady, (screenSize[0] / 2 - gameReady.get_rect().width / 2, 180))
# 绘制开始按钮
start = pygame.image.load("images/start.png")
# 开始按钮绘制位置
startPos = (int(screenSize[0] / 2 - start.get_rect().width / 2), 250)
screen.blit(start, startPos)
# 获取暂停/开始按钮
pauseom = pygame.image.load("images/pauseom.png")
play = pygame.image.load("images/play.png")
# 暂停/开始按钮绘制位置
playOrpausPos = (5, 5)
# 储存点击响应位置
clickPos = (playOrpausPos[0] + play.get_rect().width, playOrpausPos[1] + play.get_rect().height)

# 获取计分板
endPanel = pygame.image.load("images/end.png")
ok = pygame.image.load("images/ok.png")
endPos = (25, 193)
# ok按键在endPanel上的偏移位置
okPos = (endPos[0] + 79, endPos[1] + 78)
okRect = (okPos[0], okPos[1], 80, 28)
scorePos = (endPos[0] + 170, endPos[1] + 36)
bastPos = (endPos[0] + 180, endPos[1] + 76)

# 设置每搁多长设置一堵墙（注意，是两障碍物左边坐标之间的距离）
width = 200
# 根据障碍物之间的距离生成障碍物个数
walls = []
# 用于碰撞检测的障碍物精灵组
for i in range(0, int(screenSize[0] / width) + 1): 
	walls.append(Wall.Wall(screenSize, screenSize[0] + i * width))
# 障碍物数量
wallCount = len(walls)

# 得到player对象
player = Bird.Player(screenSize)
# 小鸟当前显示的图片的序号（用以实现飞翔效果）
birdFlyIndex = 0
# 点击屏幕时，小鸟飞起的时间（帧）
flyDelay = 10

# 分数
maxScore = 0
score = 0
# 字体大小
fontSize = 30
# 用以显示分数的字体
scoreFont = pygame.font.Font("fonts/font.ttf", fontSize)
endScoreFont = pygame.font.Font("fonts/BRADHITC.TTF", 20)

isFlying = 0
# 创建一个对象来帮助跟踪时间
clock = pygame.time.Clock()
# 用来设置延迟
delay = 80
# 表示当前为当前秒内的第多少帧
nowDelay = 1
# 是否停止障碍物的移动
stopMove = False
# 判断是否运行
running = False
# 是否暂停
isPause = False

def ReStart():
	background.Reset()
	player.Reset()
	for i in range(0, wallCount): 
		walls[i].SetPos(screenSize[0] + i * width)
	birdFlyIndex = 0
	score = 0
	nowDelay = 1
	stopMove = False
	running = False
	isPause = False

while not running: 
	for event in pygame.event.get():
		if event.type == QUIT: 
			pygame.quit()
			sys.exit()
		if event.type == MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]:
			x = pygame.mouse.get_pos()[0]
			y = pygame.mouse.get_pos()[1]
			if x > startPos[0] and x < startPos[0] + start.get_rect().width and y > startPos[1] and y < startPos[1] + start.get_rect().height: 
				running = True	
	# 更新屏幕内容
	pygame.display.flip()
	# 约束程序将永远不会超过每秒delay帧。
	clock.tick(delay)

# 游戏运行中
while running:
	for event in pygame.event.get():
		if event.type == QUIT: 
			pygame.quit()
			sys.exit()
		# 鼠标左键按下
		elif event.type == MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]:
			x = pygame.mouse.get_pos()[0]
			y = pygame.mouse.get_pos()[1]
			if x > playOrpausPos[0] and x < clickPos[0] and y > playOrpausPos[1] and y < clickPos[1]:
				isPause = not isPause
			elif player.active: 
				wing.play()
				player.Power()
				isFlying = flyDelay
			elif not player.active and \
			x > okRect[0] and x < okRect[0] + okRect[2] and y > okRect[1] and y < okRect[1] + okRect[3]:
				background.Reset()
				player.Reset()
				for i in range(0, wallCount): 
					walls[i].SetPos(screenSize[0] + i * width)
				birdFlyIndex = 0
				score = 0
				nowDelay = 1
				stopMove = False
				running = True
				isPause = False
		# 鼠标右键按下（测试切换背景图片）
		elif event.type == MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[2]:
			background.Change()
	# 游戏未暂停
	if not isPause: 
		# 绘制背景图片
		for i in range(0, background.bgCount):
			screen.blit(background.bgImages[i], background.rect[i])
		# 绘制背景地面
		screen.blit(background.ground, background.groundRect)
		# 绘制障碍物
		for wall in walls:
			for i in range(0, 2): 
				screen.blit(wall.images[i], wall.rect[i])
		# 绘制小鸟
			screen.blit(player.image, player.rect)

		if player.active: 
			# 移动背景
			if not stopMove:
				background.Move()
				# 移动障碍物
				for i in range(0, wallCount):
					walls[i].HorizontalMove()
					# 消失在视野内
					if walls[i].Disappear():
						# 播放音效
						bPass.play()
						if i == 0: 
							walls[i].SetPos(walls[wallCount - 1].rect[0].left + width)
						else: 
							walls[i].SetPos(walls[i - 1].rect[0].left + width)
						# 分数增加
						print(score)
						score += 1

			# 实现小鸟飞翔动画
			if not nowDelay % 5: 
				birdFlyIndex = (birdFlyIndex + 1) % 3
				player.image = player.flyImages[birdFlyIndex]
			# 飞行
			player.fly()
			if isFlying: 
				isFlying -= 1
				if not isFlying:
					player.Drop()

			# 绘制得分
			scoreText = scoreFont.render(str(score), True, (255, 255, 255))
			screen.blit(scoreText, (screenSize[0] / 2 - fontSize / 2, 60))

			# 是否撞到障碍物
			for wall in walls:
				if player.active and wall.IfCollider(player): 
					hit.play()
					drop.play()
					maxScore = score if(score > maxScore) else maxScore
					player.active = False
	
	if not player.active: 
		player.Died()
		screen.blit(endPanel, endPos)
		screen.blit(ok, okPos)
		scoreText = endScoreFont.render(str(score), False, (255, 255, 255))
		bastText = endScoreFont.render(str(maxScore), True, (255, 0, 0))
		screen.blit(scoreText, scorePos)
		screen.blit(bastText, bastPos)

	# 绘制开始/暂停按钮
	if isPause: 
		screen.blit(play, playOrpausPos)
	else: 
		screen.blit(pauseom, playOrpausPos)
	# 更新nowDelay
	nowDelay = (nowDelay + 1) % delay
	# 更新屏幕内容
	pygame.display.flip()
	# 约束程序将永远不会超过每秒delay帧。
	clock.tick(delay)
	