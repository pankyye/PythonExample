import pygame
from pygame.sprite import Group 
from settings import Settings
from ship import Ship 
from alien import Alien 
import game_functions as gf 


def run_game():
	pygame.init() #初始化游戏
	ai_settings=Settings()
	screen=pygame.display.set_mode((ai_settings.screen_width,ai_settings.screen_height)) #创建一个屏幕对象,尺寸为元祖数据
	pygame.display.set_caption('Alien Invasion')
	
	ship=Ship(ai_settings,screen)
	aliens=Group()
	bullets=Group()
	gf.create_fleet(ai_settings,screen,ship,aliens)

	while True:
		gf.check_events(ai_settings,screen,ship,bullets)
		ship.update()
		gf.update_bullets(bullets)
		gf.update_screen(ai_settings,screen,ship,aliens,bullets)


run_game()