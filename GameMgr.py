# -*- coding: utf-8 -*-
import pygame


class GameMgr(object):

	FPS = 30

	def __init__(self):
		self.is_game_over = False
		self.main_clock = pygame.time.Clock()
		self.logic = None
		self.render = None
		self.init = None
		pygame.init()

	def __del__(self):
		pygame.quit()

	def start(self):
		self.is_game_over = False
		if self.init:
			self.init()
		self._start_loop()

	def _start_loop(self):
		while not self.is_game_over:
			if self.logic:
				ts = self.main_clock.get_time()
				self.logic(ts)
			if self.render:
				self.render(ts)
			self.main_clock.tick(GameMgr.FPS)
			

	def game_over(self):
		self.is_game_over = True

	def destroy(self):
		self.is_game_over = True
		self.main_clock = None
