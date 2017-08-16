from visual.Painter import Painter, Label, Color, Pen, Rectange


class PanelBase(object):

	def __init__(self, ui_layer = None):
		self.layer = ui_layer
		self.painter = Painter(self.layer)
		self.is_visible = True

	def on_loaded(self):
		pass

	def on_show(self):
		pass

	def on_hide(self):
		pass

	def on_destroy(self):
		pass

	def pen(self):
		_pen = Pen()
		_pen.border_width = 3
		_pen.border_color = Color.WHITE
		_pen.color = Color.BLACK
		return _pen

	def set_visible(self, is_visible):
		self.is_visible = is_visible
		self.layer.visible = is_visible


class PanelTitle(PanelBase):

	def __init__(self, ui_layer):
		super(PanelTitle, self).__init__(ui_layer)

	def on_loaded(self):
		self.layer.centerlize()

		root = Rectange(None, self.pen(), 180, 180,)
		label = Label(root, self.pen(), "Consolas", "Tetris Game" ,  24)
		label.set_bold(True)
		label.x, label.y = 5, 30

		hint_label = Label(root, self.pen(), 'Consolas', 'press "ENTER" to start', 14 )
		hint_label.set_italic(True)
		hint_label.x, hint_label.y = 5, 100

		self.painter.root_node = root
		self.painter.draw()



