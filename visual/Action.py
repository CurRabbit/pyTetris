

class Action(object):

	def __init__(self, name):
		self.name = name
		self.frame_index = 0
		self.max_frame = 0
		self.frame_callback = None
		self.anim_end_callback = None
		self.delay_ts = 0
		self.anim_ts = 0

		self.is_running = False
		self.args = None

	def start(self, max_frame, delay, frame_cb, end_cb):
		self.max_frame = max_frame
		self.delay_ts = delay
		self.frame_callback = frame_cb
		self.anim_end_callback = end_cb

		self.is_running = True
		self.frame_index = 0 

	def _each_frame_start(self):
		if self.frame_callback:
			self.frame_callback()
		self.anim_ts = 0
		self.frame_index += 1
		if self.frame_index >= self.max_frame:
			self.is_running = False
			if self.anim_end_callback:
				self.anim_end_callback()

	def tick(self, ts):
		self.anim_ts += ts
		if self.anim_ts >= self.delay_ts:
			self._each_frame_start()

class ActionMgr(object):

	def __init__(self):
		self.action_list = []

	def new_action(self, name):
		action = Action(name)
		self.addAction(action)
		return action

	def addAction(self, action):
		self.action_list.append(action)

	def removeActionByName(self, name):
		action_to_remove = []
		for action in self.action_list:
			if action.name == name:
				action_to_remove.append(action)
		for a in action_to_remove:
			self.action_list.remove(a)

	def tick(self, ts):
		for action in self.action_list:
			if action.is_running:
				action.tick(ts)




