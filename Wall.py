import pygame
import random

class Wall(pygame.sprite.Sprite):
	#设置障碍物位置
	def SetPos(self, leftPos):
		# 障碍物处置位置随机
		iRan = random.randint(self.safeSpace if(self.safeSpace > 192) else 192, self.sHeight - 192 + self.safeSpace)
		self.rect[0].left, self.rect[0].top = leftPos, iRan - self.safeSpace - self.rect[0].height
		self.rect[1].left, self.rect[1].top = leftPos, iRan

	# 构造函数
	def __init__(self, screenSize, leftPos):
		pygame.sprite.Sprite.__init__(self)
		# 加载障碍物图片
		self.images = []
		self.images.extend([ \
			pygame.image.load("images/upWall.png").convert_alpha(), \
			pygame.image.load("images/downWall.png").convert_alpha() \
			])
		# 获取上边和下边障碍物的矩形区域
		self.rect = []
		self.rect.extend([self.images[0].get_rect(), self.images[1].get_rect()])
		# 移动速度,与背景速度保持一致
		self.speed = 1
		# 两障碍物之间的宽度
		self.safeSpace = 100
		# 保存游戏窗口大小
		self.sWidth, self.sHeight = screenSize[0], screenSize[1]
		# 设置初始位置
		self.SetPos(leftPos)

	# 水平移动
	def HorizontalMove(self):
		for i in range(0, 2):
			self.rect[i].left -= self.speed

	# 判断当前障碍物是否消失在视野之内
	def Disappear(self):
		if self.rect[0].left <= 0 - self.rect[0].width: 
			return True
		else: 
			return False