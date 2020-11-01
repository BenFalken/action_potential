from neuron_constants import *
from random import randint, choice
import channel as channel_class

class Cell:
	def __init__(self):
		self.ions = []
		self.channels = []
		self.ion_channel_nums = {}
		self.ion_population = {}
		self.dt = (MIN_DT+MAX_DT)/2
		self.make_ion_channels()

	def make_ion_channels(self):
		prev_start_x = 0
		for i in range(CHANNEL_NUM):
			start_x, diam = randint(prev_start_x, WIDTH - ((CHANNEL_NUM - i)*50)), randint(25, 50)
			self.channels.append(channel_class.Channel(ion_perm=choice(ION_CHOICES), start_x=start_x, is_voltage_gated=False, diam=diam))
			prev_start_x, prev_diam = start_x, diam

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

		if len(ion_channel_list) > 0:
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

			return self.nernst(inside_ratio, outside_ratio)
		"""except Exception as e:
			print(e)
			return 0"""

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
		except:
			return 0
			#print(inside_ratio, outside_ratio)

	def process_click(self, event):
		index = event.key-49
		try:
			return ION_CHOICES[index]
		except:
			if event.key == 116:
				return None
			else:
				return 'Na'