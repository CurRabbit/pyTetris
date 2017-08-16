# -*- coding: utf-8 -*-
import random
from visual.Painter import Color
import datetime
import Globals

BLOCK_TYPE_UNDEFINED= 0
BLOCK_TYPE_BOX 		= 1
BLOCK_TYPE_STRIP 	= 2
BLOCK_TYPE_L_WORD	= 3
BLOCK_TYPE_R_WORD 	= 4
BLOCK_TYPE_L_L		= 5
BLOCK_TYPE_R_L		= 6
BLOCK_TYPE_T  		= 7

def rand_block_type():
	return random.choice([
		BLOCK_TYPE_BOX, BLOCK_TYPE_STRIP, BLOCK_TYPE_L_WORD,
		BLOCK_TYPE_R_WORD, BLOCK_TYPE_L_L, BLOCK_TYPE_R_L, BLOCK_TYPE_T ])

class TetrisRule(object):

	CREATE_NEW_SCORE = 10
	CLEAR_LINE_SCORE = 50
	LEVEL_SCORE_MAP  = {
		2:	500,
		3:	1000,
		4:	2000,
		5:	4000,
		6:	7000,
		7:	11000	
	}
	INIT_SPEED = 1000

TerisBlockConf = {
	BLOCK_TYPE_BOX : {
		'init': [(0,0), (1,0), (1,1), (0,1)],
		'rotatable':False,
		'color': Color.GREEN,
		'offset_x': 0
	},
	BLOCK_TYPE_STRIP: {
		'init': [(-1,0), (0,0), (1,0), (2,0)],
		'rotatable':True,
		'color': Color.YELLOW,
		'offset_x': 0
	},
	BLOCK_TYPE_L_WORD: {
		'init': [(0,-1), (0,0), (1,0), (1,1)],
		'rotatable':True,
		'color': Color.RED,
		'offset_x': 0
	},
	BLOCK_TYPE_R_WORD: {
		'init': [(1,-1), (1, 0), (0,0), (0,1)],
		'rotatable':True,
		'color': Color.ORANGE,
		'offset_x': 0
	},
	BLOCK_TYPE_L_L: {	
		'init': [(0,-1), (0,0), (-1,0), (-2,0)],
		'rotatable':True,
		'color': Color.PURPLE,
		'offset_x': 30,
		'offset_y': 10
	},
	BLOCK_TYPE_R_L: {
		'init': [(-1, -1), (-1,0), (0,0), (1,0)],
		'rotatable':True,
		'color': Color.PINK,
		'offset_x': 10,
		'offset_y': 10
	},
	BLOCK_TYPE_T: {
		'init': [(0,-1), (0,0), (1,0), (0,1)],
		'rotatable':True,
		'color': Color.BLUE,
		'offset_x': 0
	}
}

class TetrisControllerBlock(object):

	ACTION_MOVE_LEFT 	= 1
	ACTION_MOVE_RIGHT 	= 2
	ACTION_MOVE_DOWN	= 3
	ACTION_ROTATE 		= 4

	def __init__(self, block_type, grids):
		self.block_type = block_type
		self.pos = (-3, int(grids.column / 2),  )
		conf = TerisBlockConf.get(block_type)
		self.point_list = conf.get('init')
		self.rotatable = conf.get('rotatable', False)
		self.color = conf.get('color', (255, 255, 255))
		self.grids = grids

	def _rotate(self):
		# rotate in local axis
		changed_points = []
		if self.rotatable is False:
			changed_points = self.point_list
		else:
			for point in self.point_list:
				changed_points.append((-point[1], point[0]))
		if self.grids.accept(changed_points, self.pos):
			self.point_list = changed_points
			self.grids.fill(self)

	def _move(self, act):
		changed_pos = [self.pos[0], self.pos[1]]
		if act == TetrisControllerBlock.ACTION_MOVE_LEFT:
			changed_pos[1] -= 1
		elif act == TetrisControllerBlock.ACTION_MOVE_RIGHT:
			changed_pos[1] += 1
		elif act == TetrisControllerBlock.ACTION_MOVE_DOWN:
			changed_pos[0] += 1
		if self.grids.accept(self.point_list, changed_pos):
			self.pos = changed_pos
			self.grids.fill(self)
		else:
			if act == TetrisControllerBlock.ACTION_MOVE_DOWN:
				self.grids.fix_block(self)

	def action(self, act, is_auto = False):
		if act == TetrisControllerBlock.ACTION_ROTATE:
			self._rotate()
		else:
			self._move(act)


class TetrisGrid(object):

	def __init__(self):
		self.is_empty = True
		self.color = -1
		self.is_fixed = False

	def clear_dynamic(self):
		if not self.is_empty and not self.is_fixed:
			self.is_empty = True
			self.color = -1

	def accept(self):
		return not self.is_fixed

	def fill(self, control_blcok):
		self.color = control_blcok.color
		self.is_empty = False
		self.is_fixed = False

	def fix(self):
		self.is_fixed = True

	def clear(self):
		self.is_empty = True
		self.color = -1
		self.is_fixed = False


class TetrisGrids(object):

	def __init__(self, column, row, logic):
		self.column = column
		self.row = row
		self.grids = None
		self.logic = logic
		self.reset()

	def reset(self):
		self.grids = []
		for i in xrange(self.row):
			self.grids.append([])
			for j in xrange(self.column):
				self.grids[i].append(TetrisGrid())

	def accept(self, changed_points, pos):
		for p in changed_points:
			g_pos = ( pos[0] + p[0], pos[1] + p[1] )
			if not self._check_pos_valid(g_pos):
				return False
			if self._need_not_collide_check_or_fill(g_pos):
				continue
			if not self._check_collide(g_pos):
				return False
		return True

	def _check_pos_valid(self, pos):
		return (pos[0] >= -4 and pos[0] < self.row) and\
			(pos[1] >= 0 and pos[1] < self.column)

	def _need_not_collide_check_or_fill(self, pos):
		return pos[0] >= -4 and pos[0] < 0

	def _check_collide(self, pos):
		return self.grids[pos[0]][pos[1]].accept()

	def fill(self, control_block):
		self._clear_dynamic()
		pos = control_block.pos
		for p in control_block.point_list:
			g_pos = ( pos[0] + p[0], pos[1] + p[1] )
			if self._need_not_collide_check_or_fill(g_pos):
				continue
			self.grids[g_pos[0]][g_pos[1]].fill(control_block)

	def _clear_dynamic(self):
		for i in xrange(self.row):
			for j in xrange(self.column):
				self.grids[i][j].clear_dynamic()

	def fix_block(self, control_block):
		pos = control_block.pos
		for p in control_block.point_list:
			g_pos = ( pos[0] + p[0], pos[1] + p[1] )
			if self._need_not_collide_check_or_fill(g_pos):
				self.logic.game_over()
				return
			else:
				self.grids[g_pos[0]][g_pos[1]].fix()
		self.logic.create_new_block()
		self._try_elimate_lines()


	def _try_elimate_lines(self):
		clear_lines = []
		for i in xrange(self.row):
			line_empty = False
			for j in xrange(self.column):
				if self.grids[i][j].accept():
					line_empty = True
					continue
			if not line_empty:
				clear_lines.append(i)
		if len(clear_lines) > 0 :
			self.logic.elimate_lines(clear_lines)
			for i in reversed(clear_lines):
				self.grids.pop(i)
		
			for x in clear_lines:
				self.grids.insert(0, [])
				for j in xrange(self.column):
					self.grids[0].append(TetrisGrid())


class TetrisLogic(object):
	# ----------- column ------------
	# |
	# row
	# |

	def __init__(self, column, row):
		self.grids = TetrisGrids(column, row, self)
		self.column = column
		self.row = row
		self.control_block = None
		self.lock = False
		self.is_running = False

		self.score = 0
		self.level = 1
		self.next_block_type = BLOCK_TYPE_UNDEFINED
		self.time_counter = 0
		self.ms_counter = 0

	def reset(self):
		self.score = 0
		self.level = 1
		self.is_running = False
		self.lock = False
		self.control_block = None
		self.time_counter = 0
		self.grids.reset()
	
	def game_over(self):
		Globals.ui.set_visible(True)
		print '########### game over ##############'
		self.is_running = False

	def game_start(self):
		if self.is_running:
			return
		self.reset()
		self.is_running = True
		Globals.ui.set_visible(False)
		print '######### game start #############'

		self.control_block = TetrisControllerBlock(rand_block_type(), self.grids)
		self.next_block_type = rand_block_type()
		Globals.visual.on_create_new_block()

	def elimate_lines(self, clear_lines):
		self.score += len(clear_lines) * TetrisRule.CLEAR_LINE_SCORE
		self._try_level_up()
		self.lock = True
		Globals.visual.on_elimate_start(clear_lines)

	def on_emlimate_anim_end(self):
		self.lock = False

	def tick(self, ms):

		if self.is_running:
			self.time_counter += ms
		if not self.is_running or self.lock:
			return 
		self.ms_counter += ms
		if self.ms_counter  >= int(TetrisRule.INIT_SPEED /self.level):
			self.control_block.action(TetrisControllerBlock.ACTION_MOVE_DOWN, 
				is_auto = True)
			self.ms_counter = 0

	def create_new_block(self):
		self.control_block = TetrisControllerBlock(self.next_block_type, self.grids)
		self.next_block_type = rand_block_type()
		self.score += TetrisRule.CREATE_NEW_SCORE
		self._try_level_up()
		Globals.visual.on_create_new_block()

	def _try_level_up(self):
		level_up_score = TetrisRule.LEVEL_SCORE_MAP.get(self.level + 1, 0)
		if level_up_score <= self.score:
			self.level += 1

	def get_runing_time_str(self):
		second = int(self.time_counter / 1000)
		if second >= 3600:
			second = 0
			self.time_counter = 0
		minute = int(second / 60)
		second = second % 60
		t = datetime.datetime.strptime('%s:%s' % (minute,second), '%M:%S')
		return t.strftime('%M:%S')

	def input(self, act):
		if not self.is_running or self.lock:
			return
		self.control_block.action(act)
	