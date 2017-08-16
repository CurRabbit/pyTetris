import pygame
import Globals
from visual.Painter import Color

class Layer(object):

	def __init__(self, name = '', zorder = 0, 
		w = Globals.display_width, h = Globals.display_height, x = 0, y = 0):
		self.surface = None
		self.zorder = 0

		self.name = name
		self.x = 0
		self.y = 0
		self.width = w
		self.height = h
		self.visible = True
		self.surface = pygame.Surface((self.width, self.height))

	def get_pos(self):
		return self.x, self.y

	def reset(self, color = Color.WHITE):
		self.surface.fill(color)

	def centerlize(self):
		w, h = Globals.display_width, Globals.display_height
		self.x = int( (w - self.width)/ 2 )
		self.y = int( (h - self.height)/ 2 )

	def enable_alpha(self):
	 	self.surface.set_alpha()



class Display(object):

	def __init__(self):
		self.display = pygame.display.set_mode(
			(Globals.display_width, Globals.display_height)
		)
		self.layer_list = []

	def addLayer(self, layer):
		self.layer_list.append(layer)

	def removeLayerByName(self, layer_name):
		for layer in self.layer_list:
			if layer.name == layer_name:
				self.layer_list.remove(layer)

	def update(self):
		ordered_layer_list = sorted( self.layer_list, key = lambda x: x.zorder)
		for layer in ordered_layer_list:
			if layer.visible:
				self.display.blit(layer.surface, layer.get_pos())
		pygame.display.update()

	def create_new_layer(self, name, zorder = 0, 
		w = Globals.display_width, h = Globals.display_height, x = 0, y = 0):
		layer = Layer(name, zorder, w, h, x, y)
		self.addLayer(layer)
		return layer