import xml.dom.minidom
from Painter import NodeFactory

class XMLReader(object):

	def __init__(self):
		self.dom = None

	def parse_str(self, document, pen_creator):
		self.dom = xml.dom.minidom.parseString(document)
		cur = self.dom.documentElement
		parent = None
		return self._add_create_node(cur, parent, pen_creator)

	def _add_create_node(self, dom_node, parent, pen_creator):
		node = self._generate_node(dom_node, parent, pen_creator)
		for child in dom_node.childNodes:
			if child.nodeType == child.ELEMENT_NODE:
				self._add_create_node(child, node, pen_creator)
		return node

	def _generate_node(self, current, parent, pen_creator):
		node_name = current.nodeName
		attributes = current.attributes
		attribute_maps = {}
		if attributes :
			for i in xrange(attributes.length):
				attr = attributes.item(i)
				name = attr.name 
				attribute_maps[name] = current.getAttribute(name)
		if current.firstChild and current.firstChild.data:
			attribute_maps['text'] = current.firstChild.data
		
		return self._create_node(node_name, attribute_maps, parent, pen_creator)

	def _create_node(self, node_name, attributes_map, parent, pen_creator):
		cls = NodeFactory.create_node(node_name)
		_node = cls(parent)
		for attr, val in attributes_map.iteritems():
			_node.setattribute(attr, val)
		if pen_creator:
			_node.pen = pen_creator()
		return _node

