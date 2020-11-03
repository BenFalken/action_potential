import gui, cell

if __name__ == "__main__":
	neuron = cell.Cell()
	GUI = gui.GUI(neuron)
	GUI.run_simulation(neuron)