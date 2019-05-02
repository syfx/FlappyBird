import pygame				# 导入pygame模块
import sys					# 导入sys模块
import Bird					# 导入Bird模块
import BackGround 			# 导入BackGround模块
import Wall 				# 导入Wall模块

from pygame.locals import * # 导入pygame中的所有常量

pygame.init();				# 初始化pygame，为使用硬件做准备

# 窗口大小
screenSize = width, height = 288, 512
# 创建了一个窗口
screen = pygame.display.set_mode(screenSize)
# 设置敞口标题
pygame.display.set_caption("Flappy Bird")
# 得到背景对象
background = BackGround.BackGround(screenSize)
# 设置每搁多长设置一堵墙（注意，是两障碍物左边坐标之间的距离）
width = 400
# 根据障碍物之间的距离生成障碍物个数
walls = []
wallLeftPos = []
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
isFlying = 0
# 创建一个对象来帮助跟踪时间
clock = pygame.time.Clock()
# 用来设置延迟
delay = 80
# 表示当前为当前秒内的第多少帧
nowDelay = 1
# 判断是否运行
running = True

while running:
	for event in pygame.event.get():
		if event.type == QUIT: 
			pygame.quit()
			sys.exit()
		# 鼠标左键按下
		elif event.type == MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]:
			player.Power()
			isFlying = flyDelay
		# 鼠标右键按下
		elif event.type == MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[2]:
			background.Change()
	# 绘制背景图片
	for i in range(0, background.bgCount):
		screen.blit(background.bgImages[i], background.rect[i])
	# 绘制背景地面
	screen.blit(background.ground, background.groundRect)
	# 移动背景
	background.Move()
	# 绘制障碍物
	for wall in walls:
		for i in range(0, 2): 
			screen.blit(wall.images[i], wall.rect[i])
	# 移动障碍物
	for i in range(0, wallCount):
		walls[i].HorizontalMove()
		# 消失在视野内
		if walls[i].Disappear():
			if i == 0: 
				walls[i].SetPos(walls[wallCount - 1].rect[0].left + width)
			else: 
				walls[i].SetPos(walls[i - 1].rect[0].left + width)
	# 绘制小鸟
	screen.blit(player.image, player.rect)
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
	# 更新nowDelay
	nowDelay = (nowDelay + 1) % delay
	# 更新屏幕内容
	pygame.display.flip()
	# 约束程序将永远不会超过每秒delay帧。
	clock.tick(delay)
	