import pygame

class BackGround(pygame.sprite.Sprite): 
	def __init__(self, screenSize):
		pygame.sprite.Sprite.__init__(self)
		# 获取屏幕的高度和宽度
		self.sWidth, self.sHeight = screenSize[0], screenSize[1]
		# 地面背景图片
		self.ground = pygame.image.load("images/ground.png").convert_alpha()
		# 得到地面的矩形区域
		self.groundRect = self.ground.get_rect()
		# 设置地面背景初始位置
		self.groundRect.left, self.groundRect.top = 0, self.sHeight - 30
		# 储存背景图片的数组
		self.images = []
		self.images.extend([ \
			pygame.image.load("images/bg_01.png").convert_alpha(), \
			pygame.image.load("images/bg_02.png").convert_alpha() \
			])
		# 图片数量
		self.imageCount = len(self.images)
		# 当前背景图片子imge中的小标
		self.sub = 0
		# 当前的背景图片
		self.image = self.images[self.sub]
		# 用来绘制背景的图片
		self.bgImages = []
		# 使用两张图片来实现背景循环
		self.bgImages.extend([self.image, self.image])
		# 用以绘制背景的图片的数量
		self.bgCount = len(self.bgImages)
		# 获取背景的矩形区域
		self.rect = []
		self.rect.extend([ \
			self.bgImages[0].get_rect(), \
			self.bgImages[1].get_rect() \
			])
		# 背景移动速度
		self.speed = 2
		# 设置背景初始时的位置
		self.rect[0].left, self.rect[0].top = 0, 0
		self.rect[1].left, self.rect[1].top = self.sWidth, 0

	#实现背景移动
	def Move(self):
		for rect in self.rect:
			rect.left -= self.speed
		# 实现背景循环
		if self.rect[0].left <= (0 - self.sWidth): 
			self.rect[0].left = self.rect[1].left + self.sWidth
			self.bgImages[0] = self.image
		if self.rect[1].left <= (0 - self.sWidth): 
			self.rect[1].left = self.rect[0].left + self.sWidth	
			self.bgImages[1] = self.image

	# 改变背景
	def Change(self):
		self.sub = (self.sub + 1) % self.imageCount
		self.image = self.images[self.sub]

	# 重置背景位置
	def Reset(self):
		self.rect[0].left, self.rect[0].top = 0, 0
		self.rect[1].left, self.rect[1].top = self.sWidth, 0