from neuron_constants import *

class Channel:
	def __init__(self, ion_perm, start_x, is_voltage_gated, diam):
		self.ion_perm = ion_perm
		self.color = CHANNEL_COLORS[ion_perm]
		self.start_x = start_x
		self.diam = diam
		self.voltage_gated = is_voltage_gated
		self.sinceLastClosed = 0
		self.isOpen = True
		if is_voltage_gated:
			self.color = VOLTAGE_CHANNEL_COLORS[ion_perm]
			self.isOpen = False
			self.setup_biophysics()

	def setup_biophysics(self):
		if self.ion_perm == 'Na':
			self.open_voltage = -50*(10**(-3))	# mV
			self.close_voltage = 30*(10**(-3))	# mV
			self.refractory = 100				# Seconds
		if self.ion_perm == 'K':
			self.open_voltage = 50*(10**(-3))	# mV
			self.close_voltage = -80*(10**(-3))	# mV
			self.refractory = 100				# Seconds

	def check_state(self, cell):
		voltage, dt = cell.membrane_potential, cell.dt
		if self.voltage_gated:
			self.sinceLastClosed += dt
			if self.ion_perm == 'Na' and voltage > self.close_voltage:
				self.inactivate_channel()
			elif self.ion_perm == 'K' and voltage < self.close_voltage:
				self.inactivate_channel()
			elif self.ion_perm == 'Na' and voltage > self.open_voltage and self.sinceLastClosed > self.refractory:
				self.activate_channel()
			elif self.ion_perm == 'K' and voltage > self.close_voltage and self.sinceLastClosed > self.refractory:
				self.activate_channel()

	def inactivate_channel(self):
		self.isOpen = False
		self.sinceLastClosed = 0
		self.color = BLACK

	def activate_channel(self):
		self.isOpen = True
		self.color = VOLTAGE_CHANNEL_COLORS[self.ion_perm]