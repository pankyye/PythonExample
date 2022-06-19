import pygame
from pygame.sprite import Sprite 

class Alien(Sprite):

	def __init__(self,ai_settings,screen):
		super(Alien,self).__init__()
		self.screen=screen
		self.ai_settings=ai_settings
		#加载外星人图像，并设置其rect属性
		self.image=pygame.image.load('images/alien.png')
		self.rect=self.image.get_rect()
		self.rect.x=self.rect.width
		self.rect.y=self.rect.height
		self.x=float(self.rect.x)

	def blitme(self):
		#在指定位置绘制外星人
		self.screen.blit(self.image,self.rect)