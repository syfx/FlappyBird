import pygame				# 导入pygame模块
import sys					# 导入sys模块
import Bird					# 导入Bird模块
import BackGround 			# 导入BackGround模块

from pygame.locals import * # 导入pygame中的所有常量

pygame.init();				# 初始化pygame，为使用硬件做准备

# 窗口大小
screenSize = width, height = 288, 512
# 创建了一个窗口
screen = pygame.display.set_mode(screenSize)
# 设置敞口标题
pygame.display.set_caption("Flappy Bird")
# 获取背景图片
# background = pygame.image.load("images/bg_01.png").convert()
# 得到背景对象
background = BackGround.BackGround(screenSize)
# 得到player对象
player = Bird.Player(screenSize)
# 小鸟当前显示的图片的序号（用以实现飞翔效果）
birdFlyIndex = 0
# 点击屏幕时，小鸟飞起的时间（帧）
flyDelay = 15
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
			player.speed = player.upSpeed
			isFlying = flyDelay
		# 鼠标右键按下
		elif event.type == MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[2]:
			background.Change()
	# 绘制背景图片
	for i in range(0, background.bgCount):
		screen.blit(background.bgImages[i], background.rect[i])
	background.Move()
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
			player.speed = player.downSpeed
	
	# 更新nowDelay
	nowDelay = (nowDelay + 1) % delay
	# 更新屏幕内容
	pygame.display.flip()
	# 约束程序将永远不会超过每秒delay帧。
	clock.tick(delay)
	