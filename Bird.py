import pygame

class Player(pygame.sprite.Sprite): 
	# 构造函数
	#screenSize: 游戏窗口尺寸
	def __init__(self, screenSize): 
		pygame.sprite.Sprite.__init__(self)
		# 飞动时的动画
		self.flyImages = []
		# 添加图片
		self.flyImages.extend([ \
			# 得到一个Surface对象
			pygame.image.load("images/bird1.png").convert_alpha(), \
			pygame.image.load("images/bird2.png").convert_alpha(), \
			pygame.image.load("images/bird3.png").convert_alpha() \
			])
		# 当前组成帧动画的图片的数量
		self.imageCount = len(self.flyImages)
		# 当前帧显示的图片
		self.image = self.flyImages[0]
		# 储屏幕尺寸
		self.sWidth, self.sHeight = screenSize[0], screenSize[1]
		# 得到当前Surface对象的矩形区域
		self.rect = self.image.get_rect()
		# 当前的速度，规定向上为正，向下为负
		self.speed = 3
		# 下落速度(向下为正)
		self.downSpeed = 3
		# 上升速度（向下为负）
		self.upSpeed = -6
		# 旋转速度（顺时针为负，逆时针为正）
		self.rotateSpeed = 2
		# 初始化位置
		self.rect.left, self.rect.top = 5, 1

	def fly(self): 
		# 约束自傲鸟不超过游戏窗口
		if self.speed < 0 and self.rect.top > 0 \
		  	or self.speed > 0 and self.rect.top < self.sHeight - self.rect.height - 30: 
			self.rect.top += self.speed;
			# print(self.rotateSpeed)
		pygame.transform.rotate(self.image, self.rotateSpeed)
		self.rotateSpeed -= 1

	# 努力向上飞起
	def Power(self):
		self.speed = self.upSpeed
		self.rotateSpeed += 2

	# 向下坠落
	def Drop(self):
		self.speed = self.downSpeed