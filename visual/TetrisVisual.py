# -*- coding: utf-8 -*-
import Globals
import pygame
from visual.Painter import Painter, Color, Pen, Rectange, UPDATE_FILL, Node, Label
from logic.TetrisLogic import TerisBlockConf, BLOCK_TYPE_UNDEFINED, BLOCK_TYPE_BOX
from visual.XMLReader import XMLReader


class TetrisVisualConfig(object):

	BORDER_WIDTH 	= 2
	BORDER_COLOR 	= Color.WHITE
	GRID_WIDTH 		= 30
	GRID_COLOR 		= Color.BLACK
	UI_STATE_WIDTH 	= 150


conf = TetrisVisualConfig

class VisualBase(object):

	def __init__(self, layer):
		self.layer = layer
		self.reader = XMLReader()


class TetrisVisual(VisualBase):


	XML = """
<Node name= "root" >
	<Node name= "box" >
	</Node>
	<Rectange name = "state_ui">
		<Rectange name = "msg_box" width = "110" height ="120"  x= "20" y = "10" >
			<Label name = "score_label" font= "Consolas" x = "10" y = "30"></Label>
			<Label name = "time_label" font= "Consolas" x = "10" y = "50"></Label>
			<Label name = "level_label" font= "Consolas" x = "10" y = "80"></Label>
		</Rectange>
		<Rectange name = "next_msg_box" width= "110" height="200" x= "20" y = "140">
			<Label name = "next_label"  font= "Consolas" x= "20" y = "10" >Next is</Label>
			<Rectange name = "hint_box" width="100" height= "100" x = "5" y = "50">
			</Rectange>
		</Rectange>
	</Rectange>
</Node>
"""


	def __init__(self, layer):
		super(TetrisVisual, self).__init__(layer)
		self.painter = None
		self.logic = None

		self.container = None
		self.score_label = None
		self.level_label = None
		self.time_label = None
		self.hint_box = None

		self.running_anim = False
		self.elimate_lines = []
		self.action = Globals.action_mgr.new_action('elimate')
		

	def grid_pen(self):
		grid_pen = Pen()
		grid_pen.border_width = conf.BORDER_WIDTH
		grid_pen.border_color = conf.BORDER_COLOR
		grid_pen.color = conf.GRID_COLOR
		return grid_pen

	def _init_canvas(self):
		self.painter = Painter(self.layer)

	def init(self, logic):
		self.logic = logic

		self._init_canvas()
		self.update(0, init_framework = True)

	def update(self, ts, init_framework = False):
		if init_framework:
			self._init_framework()
		if not self.running_anim:
			self._update_container_fill()
		self._update_label()

	def _update_container_fill(self):
		for i in xrange(self.logic.row):
			for j in xrange(self.logic.column):
				cell = self.logic.grids.grids[i][j]
				grid_name = 'g_%d_%d' % ( i, j )
				shape = self.container.getChildByName(grid_name)
				if cell.is_empty and shape:
					shape.pen.color = Color.BLACK
					shape.update(self.painter, UPDATE_FILL)
				elif not cell.is_empty and shape:
					shape.pen.color = cell.color
					shape.update(self.painter, UPDATE_FILL)

	def _update_label(self):
		self.level_label.setString("Level: %s" % self.logic.level)
		self.score_label.setString("Score: %s" % self.logic.score)
		self.time_label.setString("Time: %s" % self.logic.get_runing_time_str())

	def _init_framework(self):
		self.layer.reset(Color.BLACK)

		root = self.reader.parse_str(self.XML, self.grid_pen)
		container = root.getChildByName("box")
		w = conf.GRID_WIDTH
		width, height = w * self.logic.column , w * self.logic.row
		container.setContentSize(width, height)
		for i in xrange(self.logic.row):
			for j in xrange(self.logic.column):
				each_grid = Rectange(container, self.grid_pen(), w, w, j * w , i * w )
				grid_name = 'g_%d_%d' % ( i, j )
				each_grid.setName(grid_name)

		state_ui = root.getNodeByName('state_ui')
		state_ui.x, state_ui.y, state_ui.width, state_ui.height = width , 0, conf.UI_STATE_WIDTH, height
		state_ui.setContentSize(conf.UI_STATE_WIDTH, height)
		
		self.score_label = root.getNodeByName('score_label')
		self.score_label.text = "Score: %s" % self.logic.score 
		self.time_label = root.getNodeByName('time_label')
		self.time_label.text = "Time: %s" % self.logic.get_runing_time_str()
		self.level_label = root.getNodeByName('level_label')
		self.level_label.text = "Level: %s" % self.logic.level
		self.hint_box = root.getNodeByName('hint_box')
		self._update_hint_block()

		self.painter.root_node = root
		self.painter.centerlize()
		self.painter.draw()
		self.container = container


	def _update_hint_block(self):
		next_block_type = self.logic.next_block_type
		self.hint_box.removeAllChildren()
		if next_block_type != BLOCK_TYPE_UNDEFINED:
			hw, sx, sy = 20, 30, 30
			if next_block_type != BLOCK_TYPE_BOX:
				sy += 10
			_conf = TerisBlockConf.get(next_block_type)
			for p in _conf.get('init'):
				_x, _y = p[0] * hw + sx  + _conf.get('offset_x'), p[1] * hw + sy + _conf.get('offset_y', 0)
				_hint_rect = Rectange(self.hint_box, self.grid_pen(), hw, hw, _y, _x)
		self.hint_box.draw(self.painter)

	def on_create_new_block(self):
		self._update_hint_block()

	def on_elimate_start(self, lines):
		self.elimate_lines = lines
		self.action.start(5, 100, self._eliemate_anim_one_frame,
			self._elimate_anim_end)
		self.running_anim = True

	def _eliemate_anim_one_frame(self):
		for j in xrange(self.logic.column):
			for i in self.elimate_lines:
				grid_name = 'g_%d_%d' % ( i, j )
				shape = self.container.getChildByName(grid_name)
				shape.pen.color = Color.rand_color()
				shape.update(self.painter, UPDATE_FILL)

	def _elimate_anim_end(self):
		Globals.logic.on_emlimate_anim_end()
		self.running_anim = False


