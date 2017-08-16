# -*- coding: utf-8 -*-
import pygame
import Globals
from GameMgr import GameMgr
from Input import Input
from ui.Panel import PanelTitle
from Display import Display
from visual.Action import ActionMgr


def game_init():
	Globals.display = Display()
	game_layer = Globals.display.create_new_layer(
			'game_layer', 0)
	ui_layer = Globals.display.create_new_layer(
		'ui_layer', 1, 190, 190 )
	ui_layer.enable_alpha()

	Globals.action_mgr = ActionMgr()
	from visual.TetrisVisual import TetrisVisual
	Globals.visual = TetrisVisual(game_layer)
	from logic.TetrisLogic import TetrisLogic
	Globals.logic = TetrisLogic(10, 12)
	Globals.visual.init(Globals.logic)
	Globals.game_input = Input()
	Globals.ui = PanelTitle(ui_layer)
	Globals.ui.on_loaded()

def game_render(ts):
	Globals.visual.update(ts)
	Globals.action_mgr.tick(ts)
	Globals.display.update()

def game_logic(ts):
	Globals.game_input.tick()
	Globals.logic.tick(ts)

_G = GameMgr()
Globals.G = _G
_G.init   = game_init
_G.render = game_render
_G.logic  = game_logic

_G.start()
del Globals.G
Globals.G = None

quit()