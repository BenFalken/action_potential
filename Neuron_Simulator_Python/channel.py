from neuron_constants import *

class Channel:
	def __init__(self, ion_perm, start_x, is_voltage_gated, diam):
		self.ion_perm = ion_perm
		self.color = CHANNEL_COLORS[ion_perm]
		self.start_x = start_x
		self.diam = diam
		self.voltage_gated = is_voltage_gated
		if voltage_gated:
			self.setup_biophysics()

	def setup_biophysics():
		if self.ion_perm == 'Na':
			self.open_voltage = -55		# mV
			self.close_voltage = 50		# mV
			self.refractory = 1			# Seconds
		if self.ion_perm == 'K':
			self.open_voltage = 50		# mV
			self.close_voltage = -80	# mV
			self.refractory = 1			# Seconds