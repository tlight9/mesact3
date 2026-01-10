import os, traceback
from datetime import datetime

from libmesact import io

def build(parent):
	file_path = os.path.join(parent.config_path, 'sserial.hal')
	parent.info_pte.appendPlainText(f'Building {file_path}')
	ss_board = parent.ss_card_cb.currentData()
	if ss_board:
		contents = []
		contents = ['# This file was created with the Mesa Configuration Tool on ']
		contents.append(datetime.now().strftime('%b %d %Y %H:%M:%S') + '\n')
		contents.append('# If you make changes to this file DO NOT use the Configuration Tool\n')

		match ss_board:
			case '7i64':
				contents.append(build_inputs(parent, ss_board, 24))
			case '7i70':
				contents.append(build_inputs(parent, ss_board, 48))


def build_inputs(parent, ss_board, count):
	inputs = []
	for i in range(count):
		if getattr(parent, f'ss{ss_board}in_' + str(i)).text() != 'Select':
			key = getattr(parent, f'ss{ss_board}in_' + str(i)).text()
			inputs.append(f'{io.inputs[key]} hm2_{mb}.0.{ss_board}.0.0.input-{i:02}\n')
	return inputs

def build_outputs(parent, count):
	pass




def build_file(parent, file_path, contents):
	try:
		with open(file_path, 'w') as f:
			f.writelines(contents)
	except OSError:
		parent.info_pte.appendPlainText(f'OS error\n {traceback.print_exc()}')

