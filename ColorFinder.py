
# Michael Usachenko 2018, MIT License # 

### IMPORTS ###

import sys
import json
import numpy as np
from sklearn.neighbors import KDTree

### PRIVATE MODULE METHODS ###

# convert all_colors_api.json file to dictionary: hex -> data
def _colors_to_dict():
	hex_to_colors_dict = None
	with open('all_colors_api.json') as f:
		hex_to_colors_dict = json.load(f)
		hex_to_colors_dict = hex_to_colors_dict['colors']

	fmt_hex_to_colors = {}
	for color in hex_to_colors_dict:
		hex_code = color.pop('hex', None)[1:]
		fmt_hex_to_colors[hex_code] = color

	return fmt_hex_to_colors

def _colors_to_nparray(colors_dict):
	# all colors to array
	all_colors = colors_dict.values()
	all_colors_array = []

	for color in all_colors:
		rgb = color['rgb']
		split_arr = [rgb['r'], rgb['g'], rgb['b']]
		all_colors_array.append(split_arr)

	return np.asarray(all_colors_array)

class ColorFinder:
	def __init__(self):
		self.colors_dict = _colors_to_dict()
		self.colors_array = _colors_to_nparray(self.colors_dict)
		self.tree = KDTree(self.colors_array)

	# either pass as hex str, hex int, or rgb list 
	def __call__(self, code, nearest=True):
		return self.find_nearest(code)

	# example: [255, 255, 255] --> 'ffffff'
	def rgb_list_to_hex(self, rgb_list):
		as_hex = [str(hex(num))[2:] for num in rgb_list]
		return ''.join(as_hex[:3])

	# example: 'ffffff' --> [255, 255, 255]
	def hex_to_rgb_list(self, hex_code):
		r = int(hex_code[0:2], 16)
		g = int(hex_code[2:4], 16)
		b = int(hex_code[4:6], 16)
		return [r, g, b]

	# returns {name: "", rgb : [r, g, b]}
	def find_nearest(self, code):

		# set up nparray of [[r, g, b]]
		if isinstance(code, str):
			code = self.hex_to_rgb_list(code)
		rgb_arr = np.asarray([code])

		# query and return nearest color
		c_idx = self.tree.query(rgb_arr, return_distance=False)
		c_idx = c_idx[0][0] #unpack array nesting by KDTree

		rgb_list = self.colors_array[c_idx]
		hex_code = self.rgb_list_to_hex(rgb_list)
		return self.colors_dict[hex_code]

if __name__ == '__main__':
	cf = ColorFinder()
	print(cf([255, 29, 143]))

