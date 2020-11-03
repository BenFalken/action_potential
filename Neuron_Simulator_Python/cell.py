from neuron_constants import *
from math import *
from random import randint, choice
import channel as channel_class

class Cell:
	def __init__(self):
		self.membrane_potential = 0
		self.ions = []
		self.channels = []
		self.ion_channel_nums = {}
		self.ion_population = {}
		self.dt = (MIN_DT+MAX_DT)/2
		self.make_ion_channels()

	def make_ion_channels(self):
		channel_list = []
		prev_start_x, prev_diam = 0, 0
		active_list = [True, False]
		for i in range(CHANNEL_NUM):
			start_x, diam = prev_start_x+prev_diam+randint(25, 50), randint(25, 50)
			is_voltage_gated = choice(active_list)
			ion_choice = choice(ION_CHOICES)
			channel_list.append({'ion_perm':ion_choice, 'start_x':start_x, 'is_voltage_gated':is_voltage_gated, 'diam':diam})
			prev_start_x, prev_diam = start_x, diam


		for channel in channel_list:
			start_x, diam = WIDTH*channel['start_x']/(prev_start_x+prev_diam), WIDTH*channel['diam']/(prev_start_x+prev_diam)
			is_voltage_gated = channel['is_voltage_gated']
			ion_perm = channel['ion_perm']

			try:
				self.channels.append(channel_class.Channel(ion_perm=ion_perm, start_x=start_x, is_voltage_gated=is_voltage_gated, diam=diam))
			except Exception as e:
				print(e)

		for channel in self.channels:
			if channel.ion_perm in list(self.ion_channel_nums.keys()):
				self.ion_channel_nums[channel.ion_perm] += 1
			else:
				self.ion_channel_nums[channel.ion_perm] = 1

	def get_membrane_potential(self):
		inside_ratio = 1
		outside_ratio = 1

		ion_channel_list = list(self.ion_channel_nums.values())
		ions_inside_list = self.get_ions_inside()

		try:
			max_ion_channels = max(ion_channel_list)

			for ion in ION_CHOICES:
				try:
					num_channels = self.ion_channel_nums[ion]
					ion_permeability = num_channels/max_ion_channels
					inside_ratio += ion_permeability*(ions_inside_list[ion])*ION_CHARGES[ion]
				except Exception as e:
					#print(e)
					continue
			for ion in ION_CHOICES:
				try:
					num_channels = self.ion_channel_nums[ion]
					ion_permeability = num_channels/max_ion_channels
					outside_ratio += ion_permeability*(self.ion_population[ion] - ions_inside_list[ion])*ION_CHARGES[ion]
				except Exception as e:
					#print(e)
					continue

			self.membrane_potential = self.nernst(inside_ratio, outside_ratio)
		except Exception as e:
			print(e)
			self.membrane_potential = 0

	def append_ion(self, ion):
		self.ions.append(ion)
		if ion.name in list(self.ion_population.keys()):
			self.ion_channel_nums[ion.name] += 1
			self.ion_population[ion.name] += 1
		else:
			self.ion_channel_nums[ion.name] = 1
			self.ion_population[ion.name] = 1

	def get_ions_inside(self):
		ions_inside = {}
		for ion in self.ions:
			if ion.name in list(ions_inside.keys()) and ion.y < MEMBRANE_START_Y:
				ions_inside[ion.name] += 1
			else:
				ions_inside[ion.name] = 1
		return ions_inside

	def nernst(self, inside_ratio, outside_ratio):
		try:
			return (R*T/(z*F))*log(inside_ratio/outside_ratio)
		except Exception as e:
			print(e)
			print(inside_ratio, outside_ratio)
			return 0
			#print(inside_ratio, outside_ratio)

	def process_click(self, event):
		index = event.key-49
		try:
			return ION_CHOICES[index]
		except:
			if event.key == 116:
				return CHANGE_DT
			elif event.key == 109:
				return GET_MEMBRANE_POT
			else:
				return 'Na'