import pygame
import Globals
from logic.TetrisLogic import TetrisControllerBlock

def _deco_pack(inner_dict, v):
	def _deco(func):
		def _func(*args, **kwargs):
			return func(*args, **kwargs)
		if type(v) in (list, tuple):
			for _v in v:
				inner_dict[_v] = _func
		else:
			inner_dict[v] = _func
	return _deco

KEY_DOWN_EVENT = {}
def key_down(v):
	return _deco_pack(KEY_DOWN_EVENT, v)


class Input(object):

	def __init__(self):
		pygame.key.set_repeat(50, 80)

	def tick(self):
		for event in pygame.event.get():
			if event.type == pygame.KEYDOWN:
				if event.key in KEY_DOWN_EVENT:
					KEY_DOWN_EVENT[event.key](self)
			if event.type == pygame.QUIT:
				Globals.G.game_over()
				
	@key_down(pygame.K_x)
	def game_exit(self):
		Globals.G.game_over()

	@key_down((pygame.K_a, pygame.K_LEFT))
	def move_left(self):
		Globals.logic.input(TetrisControllerBlock.ACTION_MOVE_LEFT)

	@key_down((pygame.K_d, pygame.K_RIGHT))
	def move_right(self):
		Globals.logic.input(TetrisControllerBlock.ACTION_MOVE_RIGHT)

	@key_down((pygame.K_w, pygame.K_UP))
	def rotate(self):
		Globals.logic.input(TetrisControllerBlock.ACTION_ROTATE)

	@key_down((pygame.K_s, pygame.K_DOWN))
	def move_down(self):
		Globals.logic.input(TetrisControllerBlock.ACTION_MOVE_DOWN)

	@key_down((pygame.K_h, pygame.K_RETURN))
	def game_start(self):
		Globals.logic.game_start()
