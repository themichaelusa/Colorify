### IMPORTS ###
import sys
import math
from ColorFinder import ColorFinder
from PIL import Image 

### CONSTANTS ###
cf = ColorFinder()
GROUP_SIZE = 0
BW_GROUP_SIZE = 32
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

### FUNCTIONS ###

def get_new_default_stat_val():
	return {
	"count": 1, 
	"rgb": None,
	#"nearest": None
	}

def normal_round(n):
    if n - math.floor(n) < 0.5:
        return math.floor(n)
    return math.ceil(n)

def get_nearest_color_data(cf, hex_code):
	nearest = cf(hex_code)
	nearest.pop("luminance")
	return nearest

def build_stat_dict(image_path):
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

def add_new_group(groups, center_hex_code):
	groups.append({center_hex_code: {'codes': [], 'size': 0}})

def in_group(groups, groups_idx, hex_code):
	center_val = list(groups[groups_idx].keys())[0]
	center_rgb = cf.hex_to_rgb_list(center_val)
	hex_code_rgb = cf.hex_to_rgb_list(hex_code)

	diff_count = 0
	for center_chan, code_chan in zip(center_rgb, hex_code_rgb):
		diff_count += abs(center_chan-code_chan)

	return diff_count <= GROUP_SIZE 

def add_to_group(groups, groups_idx, color_stats):
	group_ref = groups[groups_idx]
	ref_key = list(groups[groups_idx].keys())[0]
	group_ref[ref_key]['codes'].append(color_stats)
	group_ref[ref_key]['size'] += color_stats['count']

def get_color_groups(stat_dict):
	groups, hex_codes = [], list(stat_dict.keys())
	add_new_group(groups, hex_codes[0])
	hex_codes_len = len(hex_codes)
	codes_progess_count = 0

	for code in hex_codes[1:]:
		focus_idx = 0

		# if in any existing group, add to group
		# else add new groups
		while focus_idx < len(groups):
			if in_group(groups, focus_idx, code):
				stat_val = stat_dict[code]
				add_to_group(groups, focus_idx, stat_val)
				break
			focus_idx += 1
		else:
			add_new_group(groups, code)

	# remove empty groups
	fmt_groups = []	
	for group in groups:
		center = list(group.keys())[0]
		if group[center]['size'] > 0:
			fmt_groups.append(group)
	
	# get avg size
	avg_size = 0
	for group in fmt_groups:
		group_key = list(group.keys())[0]
		group_size = group[group_key]['size']
		avg_size += group_size
	avg_size /= len(fmt_groups)


	final_groups = []
	for group in fmt_groups:
		group_key = list(group.keys())[0]
		group_size = group[group_key]['size']
		if group_size >= avg_size:
			final_groups.append(group)

	return final_groups

def get_weighted_average_group_color(group):

	group_size, tr, tg, tb = group['size'], 0, 0, 0
	for color_dict in group['codes']:
		weight = color_dict['count']/group_size
		r, g, b = color_dict['rgb']
		#print("weight:", weight)
		tr += weight*r
		tg += weight*g
		tb += weight*b

	# todo: remove white-ish or black-ish 
	return {'rgb': (normal_round(tr), normal_round(tg), normal_round(tb)), 'size':group_size}


def get_all_weighted_average_group_colors(groups):

	# weight all groups
	all_weighted_groups = []
	for group in groups:
		group_body = list(group.values())[0]
		all_weighted_groups.append(
			get_weighted_average_group_color(group_body))

	#total_pixel_count = get_total_size(groups)

	# remove all grey-ish groups if they are proportionally > 60% of image 

	return all_weighted_groups

def find_most_distant_group_color(wa_groups):
	pass


# if picture is more than 98% black or white, use opposite color that is most distant 
# else remove color groups that are black-ish or white-ish (within 32)

def get_total_size(groups):
	size = 0
	for group in groups:
		print(group) 
		size += group['size']
	return size

def is_bw_picture(groups, total_size):
	total_pct_bw = 0
	for group in groups:
		r, g, b = group['rgb']
		print(group)

		# dist from black 
		black_dist = r+g+b
		if black_dist <= BW_GROUP_SIZE:
			total_pct_bw += group['size']/total_size
			continue
		
		# dist from white
		w_r, w_g, w_b = abs(r-255), abs(g-255), abs(b-255)
		white_dist = w_r+w_g+w_b
		if white_dist <= BW_GROUP_SIZE:
			total_pct_bw += group['size']/total_size
			continue 

	print("total pct bw:", total_pct_bw)
	return total_pct_bw >= .98


"""
def stat_dict_avg_count(stat_dict):
	all_keys = stat_dict.keys()
	master_count = 0

	for k in all_keys:
		master_count += stat_dict[k]['count']

	return master_count/len(all_keys)
"""

if __name__ == '__main__':
	image_path = sys.argv[1]
	GROUP_SIZE = int(sys.argv[2])
	sd = build_stat_dict(image_path)
	groups = get_color_groups(sd)
	print(groups)
	groups_avg = get_all_weighted_average_group_colors(groups)
	#total_size = get_total_size(groups)
	is_bw_picture(groups, total_size)
