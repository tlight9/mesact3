import os, traceback
from datetime import datetime

def build(parent):

	hal_path = os.path.join(parent.config_path, 'main' + '.hal')
	parent.info_pte.appendPlainText(f'Building {hal_path}')

	contents = []
	contents = ['# This file was created with the Mesa Configuration Tool on ']
	contents.append(datetime.now().strftime('%b %d %Y %H:%M:%S') + '\n')
	contents.append('# If you make changes to this file DO NOT run the configuration tool again!\n')
	contents.append('# This file will be replaced with a new file if you do!\n')

	# build the standard header
	contents.append('\n# kinematics\n')
	contents.append('loadrt [KINS](KINEMATICS)\n')

	contents.append('\n# motion controller\n')
	contents.append('loadrt [EMCMOT](EMCMOT) ')
	contents.append('servo_period_nsec=[EMCMOT](SERVO_PERIOD) ')
	contents.append('num_joints=[KINS](JOINTS)\n')

	contents.append('\n# hostmot2 driver\n')
	contents.append('loadrt hostmot2\n')

	contents.append('loadrt ')
	if parent.board_interface == 'eth':
		contents.append('hm2_eth ')
	elif parent.board_interface == 'pci':
		contents.append('hm2_pci ')
	elif parent.board_interface == 'spi':
		contents.append('hm2_spix ')

	if parent.board_interface == 'eth':
		contents.append(f'board_ip="{parent.address_cb.currentText()}" config="sserial_port_0=00000000"\n')

	contents.append(f'\nsetp hm2_{parent.hal_name}.0.watchdog.timeout_ns {parent.servo_period_sb.value() * 5}\n')

	# PID
	pid_count = 0
	pid_string = ''
	for axis in parent.coordinates_lb.text():
		if parent.coordinates_lb.text().count(axis) == 1:
			pid_string += f'pid.{axis.lower()},'
		elif parent.coordinates_lb.text().count(axis) > 1:
			pid_string += f'pid.{axis.lower()}{pid_count},'
			pid_count += 1
	if parent.spindle_rpm_le.text():
		pid_string += f'pid.s,'
	contents.append(f'\nloadrt pid names={pid_string[:-1]}\n')

	if parent.board_type == 'stepper':
		contents.append('\n# Why Mesa Stepper Boards need a PID controller\n')
		contents.append('# Mesa hardware step generators at every servo thread invocation, the step\n')
		contents.append('# generator hardware is given a new velocity. Without feedback from the PID\n')
		contents.append('# controller the hardware position would slowly drift because of clock speed and\n')
		contents.append('# timing differences between LinuxCNC and the step generator hardware.\n')
		contents.append('# The PID controller gets feedback from the actual (fractional) step position and\n')
		contents.append('# corrects for these small differences.\n')

		contents.append('\n# DPLL TIMER\n')
		contents.append(f'setp hm2_{parent.hal_name}.0.dpll.01.timer-us -200\n')
		contents.append(f'setp hm2_{parent.hal_name}.0.stepgen.timer-number 1\n')

	contents.append('\n# THREADS\n')
	contents.append(f'addf hm2_{parent.hal_name}.0.read servo-thread\n')
	contents.append('addf motion-command-handler servo-thread\n')
	contents.append('addf motion-controller servo-thread\n')

	pid_list = pid_string[:-1].split(',')
	for pid in pid_list:
		contents.append(f'addf {pid}.do-pid-calcs servo-thread\n')
	contents.append(f'addf hm2_{parent.hal_name}.0.write servo-thread\n')

	contents.append('\n# amp enable\n')
	contents.append(f'net motion-enable <= motion.motion-enabled\n')

	# Joints
	# 7i96s has a pwmgen enable for something
	drive_enables = {'7i76': 'stepgen', '7i76E': 'stepgen', '7i76EU': 'stepgen',
	'7i77': 'pwmgen',
	'7i95': 'stepgen', '7i95T': 'stepgen', '7i96': 'stepgen', '7i96S': 'stepgen',
	'7i97': 'pwmgen', '7i97T': 'pwmgen'}

	joint = 0
	for i in range(3):
		# need the board type
		board = getattr(parent, f'c{i}_board_tw').tabText(0)
		if board:
			print(board)
			for j in range(6):
				axis = getattr(parent, f'c{i}_axis_{j}').currentData()
				if axis:
					contents.append(f'\n# Axis: {axis} Joint: {joint} Output: {j}\n')
					contents.append(f'# PID Setup\n')
					contents.append(f'setp {pid_list[joint]}.Pgain [JOINT_{joint}](P)\n')
					contents.append(f'setp {pid_list[joint]}.Igain [JOINT_{joint}](I)\n')
					contents.append(f'setp {pid_list[joint]}.Dgain [JOINT_{joint}](D)\n')
					contents.append(f'setp {pid_list[joint]}.bias [JOINT_{joint}](BIAS)\n')
					contents.append(f'setp {pid_list[joint]}.FF0 [JOINT_{joint}](FF0)\n')
					contents.append(f'setp {pid_list[joint]}.FF1 [JOINT_{joint}](FF1)\n')
					contents.append(f'setp {pid_list[joint]}.FF2 [JOINT_{joint}](FF2)\n')
					contents.append(f'setp {pid_list[joint]}.deadband [JOINT_{joint}](DEADBAND)\n')
					contents.append(f'setp {pid_list[joint]}.maxoutput [JOINT_{joint}](MAX_OUTPUT)\n')
					contents.append(f'setp {pid_list[joint]}.error-previous-target True\n')

					# Enables
					contents.append('\n# Joint Enables\n')
					contents.append(f'net {axis}-enable => pid.{axis}.enable\n')
					contents.append(f'net {axis}-enable <= joint.{joint}.amp-enable-out\n')
					# FIXME this needs to be sorted out for all boards
					contents.append(f'net {axis}-enable <= hm2_{parent.hal_name}.0.{drive_enables[board]}.00.enable\n')

					joint += 1

	# contents.append(f'{}\n')
	# E Stop
	external_estop = False
	for i in range(3): # test for an external e stop input
		for j in range(16):
			key = getattr(parent, f'c{i}_input_{j}').text()
			if key[0:6] == 'E Stop':
				external_estop = True
	if not external_estop:
		contents.append('\n# Standard I/O Block - EStop, Etc\n')
		contents.append('# create a signal for the estop loopback\n')
		contents.append('net estop-loopback iocontrol.0.emc-enable-in <= iocontrol.0.user-enable-out\n')


	try:
		with open(hal_path, 'w') as f:
			f.writelines(contents)
			parent.info_pte.appendPlainText(f'Finished Building the {hal_path} file')

	except OSError:
		parent.info_pte.appendPlainText(f'OS error\n {traceback.print_exc()}')
