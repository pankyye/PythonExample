import sys
import pygame
from bullet import Bullet 
from alien import Alien 

def check_events(ai_settings,screen,ship,bullets):
	"""相应按键和鼠标事件"""

	for event in pygame.event.get():
		if event.type==pygame.QUIT:
			sys.exit()
		elif event.type==pygame.KEYDOWN:
			check_keydown_events(event,ai_settings,screen,ship,bullets)
		elif event.type==pygame.KEYUP:
			check_keyup_events(event,ship) 

def check_keydown_events(event,ai_settings,screen,ship,bullets):
	if event.key==pygame.K_RIGHT:
		ship.moving_right=True
	elif event.key==pygame.K_LEFT:
		ship.moving_left=True
	elif event.key==pygame.K_SPACE:
		fire_bullet(ai_settings,screen,ship,bullets)
	elif event.key==pygame.K_q:
		sys.exit()
		

def fire_bullet(ai_settings,screen,ship,bullets):
	if len(bullets)<ai_settings.bullets_allowed:
		new_bullet=Bullet(ai_settings,screen,ship)
		bullets.add(new_bullet)

def check_keyup_events(event,ship):
	if event.key==pygame.K_RIGHT:
		ship.moving_right=False 
	elif event.key==pygame.K_LEFT:
		ship.moving_left=False 


def update_screen(ai_settings,screen,ship,aliens,bullets):
	"""更新屏幕上的图像，并切换到新屏幕"""
	#每次循环时都重新绘制屏幕
	screen.fill(ai_settings.bg_color)
	for bullet in bullets:
		bullet.draw_bullet()
	ship.blitme()
	aliens.draw(screen)
	#让最近绘制的屏幕可见
	pygame.display.flip()

def update_bullets(bullets):
	"""
	更新子弹位置，并删除已消失的子弹
	"""
	bullets.update() #更新子弹位置

	#删除已消失的子弹
	for bullet in bullets.copy():
		if bullet.rect.bottom<=0:
			bullets.remove(bullet)

def create_fleet(ai_settings,screen,ship,aliens):
	"""
	创建外星人群
	"""
	alien=Alien(ai_settings,screen)
	number_aliens_x=get_number_aliens_x(ai_settings,alien.rect.width)
	number_rows=get_number_rows(ai_settings,ship.rect.height,alien.rect.height)
	
	for row_number in range(number_rows):
		for alien_number in range(number_aliens_x):
			create_alien(ai_settings,screen,aliens,alien_number,row_number)

def get_number_aliens_x(ai_settings,alien_width):
	"""
	计算每行可容纳多少个外星人
	"""
	available_space_x=ai_settings.screen_width-2*alien_width
	number_aliens_x=int(available_space_x/(2*alien_width))
	return number_aliens_x

def create_alien(ai_settings,screen,aliens,alien_number,row_number):
	"""
	创建一个外星人并将其放在当前行
	"""
	alien=Alien(ai_settings,screen)
	alien_width=alien.rect.width
	alien.x=alien_width+2*alien_width*alien_number
	alien.rect.x=alien.x
	alien.rect.y=alien.rect.height+2*alien.rect.height*row_number
	aliens.add(alien)

def get_number_rows(ai_settings,ship_height,alien_height):
	"""
	计算屏幕可容纳多少行外星人
	"""
	available_space_y=(ai_settings.screen_height-(3*alien_height)-ship_height)
	number_rows=int(available_space_y/(2*alien_height))
	return number_rows






















