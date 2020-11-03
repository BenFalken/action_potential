from math import *
from neuron_constants import *
import pygame, cell, channel
import ion as ion_class

class GUI:
	def __init__(self, cell):
		self.circle_x = 10*cell.dt
		self.SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))

	def welcome(self):
		print('** Welcome!')
		print('** For each command, click the following:')
		print('* Add sodium ion (1)')
		print('* Add potassium ion (2)')
		print('* Add chloride ion (2)')
		print('* Move green slider to speed up/slow down (t)')
		print('* Get membrane potential (m)')
		print('** Have fun!')

	def setup(self):
		pygame.init()
		self.SCREEN.fill(WHITE)

	def process_click(self, event, cell):
		name = cell.process_click(event)
		x, y = pygame.mouse.get_pos()
		if name == GET_MEMBRANE_POT:
			print('Membrane potential is: ', cell.membrane_potential)
		elif name == CHANGE_DT:
			circle_x = clamp(x, SCROLL_BAR_START_X, SCROLL_BAR_START_X+SCROLL_BAR_WIDTH)
			cell.dt = (circle_x-SCROLL_BAR_START_X)/10
			print('Simulation speed up by: ', cell.dt, 'x')
		else:
			new_ion = ion_class.Ion(name=name, x=x, y=y)
			if new_ion.notInMembrane(delta_x=0, delta_y=0):
				cell.append_ion(new_ion)

	def draw_membrane(self):
		pygame.draw.rect(self.SCREEN, BLUE, (0, MEMBRANE_START_Y, WIDTH, MEMBRANE_END_Y-MEMBRANE_START_Y))

	def draw_slider(self):
		pygame.draw.rect(self.SCREEN, SCROLL_BAR_COLOR, (SCROLL_BAR_START_X, SCROLL_BAR_START_Y, SCROLL_BAR_WIDTH, SCROLL_BAR_HEIGHT))
		pygame.draw.ellipse(self.SCREEN, SCROLL_CIRCLE_COLOR, (circle_x - (SCROLL_CIRCLE_RAD/2), SCROLL_BAR_START_Y, SCROLL_CIRCLE_RAD, SCROLL_CIRCLE_RAD))

	def draw_channels(self, cell):
		for channel in cell.channels:
			pygame.draw.rect(self.SCREEN, channel.color, (channel.start_x - (channel.diam/2), MEMBRANE_START_Y, channel.diam, MEMBRANE_END_Y-MEMBRANE_START_Y))
			channel.check_state(cell)

	def draw_ions(self, cell):
		for ion in cell.ions:
			pygame.draw.ellipse(self.SCREEN, ion.color, (ion.x - (ION_WIDTH/2), ion.y - (ION_WIDTH/2), ION_WIDTH, ION_WIDTH))
			ion.update(cell)

	def perform_checks(self, cell):
		pygame.display.update()
		cell.get_membrane_potential()

	def run_simulation(self, cell):
		self.setup()
		self.welcome()
		while True:
			for event in pygame.event.get():
				self.SCREEN.fill(WHITE)
				if event.type == pygame.KEYDOWN:
					self.process_click(event, cell)
				self.draw_membrane()
				self.draw_channels(cell)
				self.draw_ions(cell)
				self.perform_checks(cell)