from neuron_constants import *
from math import *

class Ion:
	def __init__(self, name, x, y):
		self.name = name
		self.charge = ION_CHARGES[name]
		self.color = ION_COLORS[name]
		self.mass = 1
		self.x = x
		self.y = y

	def update(self, cell):
		ions, channels, membrane_potential, dt = cell.ions, cell.channels, cell.membrane_potential, cell.dt
		grad_x, grad_y = self.get_gradient(ions)
		delta_x, delta_y = self.return_delta(grad_x, grad_y, dt)

		if not self.notInMembrane(delta_x, delta_y) and self.inChannel(delta_x, delta_y, channels):
			self.x = self.testChannels(delta_x, channels)
			self.y = clamp(self.y + delta_y, 0, HEIGHT)
		if (self.notInMembrane(delta_x, delta_y) and self.willNotPassMembrane(delta_x, delta_y)) or self.inChannel(delta_x, delta_y, channels):
			self.x = clamp(self.x + delta_x, 0, WIDTH)
			self.y = clamp(self.y + delta_y, 0, HEIGHT)
		elif self.y > MEMBRANE_END_Y and self.notInMembrane(delta_x, delta_y):
			self.x = clamp(self.x + delta_x, 0, WIDTH)
			self.y = MEMBRANE_END_Y + 1
		elif self.notInMembrane(delta_x, delta_y):
			self.x = clamp(self.x + delta_x, 0, WIDTH)
			self.y = MEMBRANE_START_Y - 1
		else:
			self.x = self.testChannels(delta_x, channels)
			self.y = clamp(self.y + delta_y, 0, HEIGHT)

	def get_gradient(self, ions):
		x_force, y_force = 0, 0	# Newtons (N)
		for ion in ions:
			try:
				diff_x, diff_y = self.x - ion.x, self.y - ion.y
			except:
				print(self.x, self.y)
				print(ion.x, ion.y)
			dist_mag = (diff_x**2) + (diff_y**2)

			try:
				theta = atan(abs(diff_y/diff_x))
			except:
				theta = pi/2

			mult_y, mult_x = -1, -1

			if diff_y > 0:
				mult_y = 1
			if diff_x > 0:
				mult_x = 1

			if dist_mag != 0:
				x_force += (mult_x*abs(cos(theta))*self.charge*ion.charge/dist_mag) #+((e**(self.charge*ion.charge))/dist_mag)
				y_force += (mult_y*abs(sin(theta))*self.charge*ion.charge/dist_mag) #+((e**(self.charge*ion.charge))/dist_mag)
			else:
				continue
		x_force, y_force = x_force/self.mass, y_force/self.mass
		return x_force, y_force

	def return_delta(self, grad_x, grad_y, dt):
		return 0.5*grad_x*(dt**2), 0.5*grad_y*(dt**2)

	def notInMembrane(self, delta_x, delta_y):
		return (self.y < MEMBRANE_START_Y or self.y > MEMBRANE_END_Y)

	def willNotPassMembrane(self, delta_x, delta_y):
		return ((self.y < MEMBRANE_START_Y and self.y + delta_y < MEMBRANE_START_Y) or (self.y > MEMBRANE_END_Y and self.y + delta_y > MEMBRANE_END_Y))

	def inChannel(self, delta_x, delta_y, channels):
		x, y = self.x + delta_x, self.y + delta_y
		anyChannelOpen = False
		for channel in channels:
			if channel.isOpen and channel.ion_perm == self.name and (abs(x-channel.start_x) <= channel.diam/2): #or abs(y - ((MEMBRANE_END_Y+MEMBRANE_START_Y)/2)) > ((MEMBRANE_END_Y-MEMBRANE_START_Y)/2)-1)
				anyChannelOpen = True
		return anyChannelOpen

	def testChannels(self, delta_x, channels):
		for channel in channels:
			if channel.isOpen and channel.ion_perm == self.name and (abs(self.x-channel.start_x) <= channel.diam/2) and (abs((self.x+delta_x)-channel.start_x) > channel.diam/2):
				return clamp(self.x + delta_x, channel.start_x-(channel.diam/2)+1, channel.start_x+(channel.diam/2)-1)
		return clamp(self.x + delta_x, 0, WIDTH)