# -*- coding: utf-8 -*-
import pygame
import Globals
import random

##################### Color ##################

class Color(object):
	"""颜色"""

	RED 	= (255, 0, 0)
	GREEN 	= (0, 255, 0)
	BLUE	= (0, 0, 255)
	BLACK 	= (0, 0, 0)
	WHITE	= (255, 255, 255)
	YELLOW	= (255, 255, 0)
	ORANGE	= (255, 97, 0)
	BROWN 	= (127, 42, 42)
	PURPLE	= (160, 32, 240)
	PINK	= (255, 192, 203)
	GREY 	= (192, 192, 192)

	@staticmethod
	def rand_color():
		return random.choice([ 
			Color.RED, Color.GREEN, Color.BLUE, Color.BLACK, Color.WHITE,
			Color.YELLOW, Color.ORANGE, Color.BROWN, Color.PURPLE,
			Color.PINK, Color.GREY
			])


################### Shape ####################

class NodeFactory(object):

	NODE_FACTORY = {
	}

	@staticmethod
	def create_node(node_type_name):
		return NodeFactory.NODE_FACTORY.get(node_type_name)

def register_node():
	def wapper(cls):
		NodeFactory.NODE_FACTORY[cls.__name__] = cls
		return cls
	return wapper

UPDATE_BORDER 	= 1
UPDATE_FILL 	= 2
UPDATE_ALL 		= 3

@register_node()
class Node(object):
	"""结点"""

	ATTRS = {
		'x': int,
		'y': int,
		'width': int,
		'height': int,
		'name': str
	}

	def __init__(self, parent = None, x = 0, y = 0):
		self.x = x
		self.y = y
		self.parent = parent
		self.children_list = []
		self.name = ''
		self.local_z_order = 0 

		self.scale = 1.0
		self.width = 0
		self.height = 0
		if parent:
			parent.addChild(self)

	def setattribute(self, attr_name, val):
		if attr_name not in self.ATTRS:
			return 
		val_type = self.ATTRS[attr_name]
		if val_type != str:
			val = val_type(val)
		setattr(self, attr_name, val)

	def _visit_children(self, painter, op = 0, *args):
		if self.children_list != 0:
			ordered_child_list = sorted( self.children_list, key = lambda x: x.getLocalZOrder() )
			for child in ordered_child_list:
				if op == 0:
					child.draw(painter, *args)
				elif op == 1:
					child.update(painter, *args)

	def draw(self, painter):
		self._visit_children(painter)

	def update(self, painter, update_type = UPDATE_ALL):
		self._visit_children(painter, 1, update_type)

	def getName(self):
		return self.name

	def setName(self, node_name):
		self.name = node_name

	def getLocalZOrder(self):
		return self.local_z_order

	def setLocalZOrder(self, zorder):
		self.local_z_order = zorder

	def getParent(self):
		return self.parent

	def removeFromParent(self):
		self.parent = None
		self.parent.removeChild(self)

	def getChildren(self):
		return self.children_list

	def getChildByName(self, child_name):
		for child in self.children_list:
			if child.getName() == child_name:
				return child
		return None

	def removeAllChildren(self):
		self.children_list = []

	def removeChild(self, node):
		if node in self.children_list:
			self.children_list.remove(node)
			node.parent = None

	def removeChildByName(self, child_name):
		find_node = self.getChildByName(child_name)
		if find_node:
			self.removeChild(find_node)

	def addChild(self, node):
		self.children_list.append(node)
		node.parent = self

	def getContentSize(self):
		return self.width, self.height

	def setContentSize(self, w, h):
		self.width = w
		self.height = h

	def getPosition(self):
		return self.x, self.y

	def _getRealScale(self):
		real_scale = self.scale
		p = self.parent
		while p:
			real_scale *= p.scale
			p = p.parent
		return real_scale

	def getVirutualContentSize(self):
		max_x, max_y = 0, 0
		for child in self.children_list:
			pos = child.x, child.y
			size = child.getContentSize()
			x = pos[0] + size[0]
			if  x > max_x:
				max_x = x
			y = pos[1] + size[1]
			if y > max_y:
				max_y = y
		return max_x, max_y

	def getNodeByName(self, name):
		for child in self.children_list:
			find_node = child.getNodeByName(name)
			if find_node:
				return find_node
			if child.name == name:
				return child
		return None

@register_node()
class Rectange(Node):

	ATTRS = Node.ATTRS 

	def __init__(self, parent = None, pen = None, w = 0, h = 0, x= 0 , y = 0):
		super(Rectange, self).__init__(parent, x, y)
		self.pen = pen
		self.width = w
		self.height = h
		

	def draw(self, painter):
		self._update_part(painter, UPDATE_ALL)
		super(Rectange, self).draw(painter)

	def _update_part(self, painter, update_type):
		scale = self._getRealScale()
		real_width, real_height = int(scale * self.width) , int(scale * self.height) 
		if real_height <= 0 or real_height <= 0:
			return

		pos_x, pos_y = painter.convertToWorldPos(self)
		pen = self.pen
		bw = int(scale * pen.border_width)

		if update_type & UPDATE_FILL:
			# fill the block
			_rect = pygame.Rect(pos_x + bw, pos_y + bw, real_width - bw, real_height - bw)
			pygame.draw.rect(painter.layer.surface, pen.color, _rect)

		# draw the border 
		if update_type & UPDATE_BORDER:
			if bw <= 0:
				return
			pygame.draw.lines(painter.layer.surface, pen.border_color, True, 
				[ [pos_x, pos_y + real_height] , [pos_x, pos_y], [pos_x + real_width , pos_y],
				  [pos_x + real_width , pos_y + real_height] ], 
				bw)

	def update(self, painter, update_type = UPDATE_ALL):
		self._update_part(painter, update_type)
		super(Rectange, self).update(painter, update_type)

@register_node()
class Label(Node):

	ATTRS = dict( Node.ATTRS  ,** {
			'font': str,
			'size': int,
			'text': str,
			'bold': bool,
			'italic': bool
		})

	def __init__(self, parent = None, pen = None, font = "Consolas", text= "", size =16, antialias = False,
			 x = 0, y = 0):
		super(Label, self).__init__(parent, x, y)
		self.pen = pen
		self.font = font
		self.size = size
		self.text = text
		self.antialias = antialias
		self.painter = None

		self.bold = False
		self.italic = False


	def draw(self, painter):
		self.painter = painter
		self._render(painter)
		super(Label, self).draw(painter)

	def update(self, painter, update_type = UPDATE_ALL):
		self._render(painter)
		super(Label, self).update(painter, update_type)

	def _render(self, painter):
		pen = self.pen
		scale = self._getRealScale()
		font_size = int(self.size * scale)
		if font_size <= 0 :
			return
		py_font = pygame.font.SysFont(self.font, font_size)
		if self.bold:
			py_font.set_bold(True)
		if self.italic:
			py_font.set_italic(True)
		text_surface = py_font.render(self.text, self.antialias, pen.border_color, pen.color)
		pos_x, pos_y = painter.convertToWorldPos(self)

		surface = painter.layer.surface
		surface.blit(text_surface, (pos_x, pos_y))

	def setString(self, text):
		if self.painter is None:
			return
		self.text = text
		self.draw(self.painter)

	def set_bold(self, is_bold):
		self.bold = is_bold

	def set_italic(self, is_italic):
		self.italic = is_italic
	

################## Pen #################


class Pen(object):
	"""画笔"""

	def __init__(self):
		self.border_color = Color.BLACK
		self.border_width = 0
		self.color = Color.WHITE


################# Painter ##############


class Painter(object):
	# 2D painter

	def __init__(self, layer, node = None):
		self.layer = layer
		self.x = 0
		self.y = 0
		self.root_node = node

	def draw(self):
		if self.root_node:
			self.root_node.draw(self)

	def convertToWorldPos(self, node):
		pos_x, pos_y = node.x, node.y
		p = node.parent
		while p:
			pos_x += p.x
			pos_y += p.y
			p = p.parent
		return pos_x + self.x , pos_y + self.y

	def centerlize(self):
		if self.root_node is None:
			return
		w, h = self.layer.width, self.layer.height
		size = self.root_node.getVirutualContentSize()
		offset_x = int( (w - size[0]) / 2 )
		offset_y = int( (h - size[1]) / 2 )
		self.root_node.x = offset_x
		self.root_node.y = offset_y


