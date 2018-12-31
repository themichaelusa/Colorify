### IMPORTS ###
import sys
from ColorFinder import ColorFinder
from PIL import Image 

### CONSTANTS ###
"""
default_stat_val = {
"count": 1, 
"rgb": None,
"nearest": None
}
"""

### FUNCTIONS ###

def get_new_default_stat_val():
	return {
	"count": 1, 
	"rgb": None,
	#"nearest": None
	}

def get_nearest_color_data(cf, hex_code):
	nearest = cf(hex_code)
	nearest.pop("luminance")
	return nearest

def build_stat_dict(image_path):
	cf = ColorFinder()
	im = Image.open(image_path)
	width, height = im.width, im.height
	pix = im.load()

	stat = {}
	for x in range(width):
		for y in range(height):
			rgb = pix[x,y][:3] # ignore alpha
			hex_code = cf.rgb_list_to_hex(rgb)
			stat_val = stat.get(hex_code, None)

			if stat_val is None:
				stat[hex_code] = get_new_default_stat_val()
				stat[hex_code]["rgb"] = rgb
				#nearest = get_nearest_color_data(cf, hex_code)
				#stat[hex_code]["nearest"] = nearest
			else:
				stat[hex_code]['count'] += 1

	return stat

def in_group(groups_dict, group_size):
	pass

def get_color_groups(group_size):
	pass

def get_weighted_average_group_color():
	pass

def get_all_weighted_average_group_colors():
	pass

def find_most_distant_group_color():
	pass

"""
def stat_dict_avg_count(stat_dict):
	all_keys = stat_dict.keys()
	master_count = 0

	for k in all_keys:
		master_count += stat_dict[k]['count']

	return master_count/len(all_keys)
"""

if __name__ == '__main__':
	image_path, group_size = sys.argv[1:3]
	print(build_stat_dict(sys.argv[1]))






