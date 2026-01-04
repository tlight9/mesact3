import subprocess
from subprocess import Popen, PIPE

from PyQt6.QtWidgets import QApplication, QInputDialog, QLineEdit
from PyQt6.QtWidgets import QDialogButtonBox

from libmesact import dialogs
from libmesact import utilities


def getPassword(parent):
	dialog = 'You need root privileges\nfor this operation.\nEnter your Password:'
	password, okPressed = QInputDialog.getText(parent, 'Password Required', dialog, QLineEdit.Password, "")
	if okPressed and password != '':
		return password

def get_results(parent, prompt, result, viewport, task=None):
	output = prompt[0].lstrip()
	if result == 0:
		outcome = 'Success'
	else:
		outcome = 'Failed'
	getattr(parent, viewport).clear()
	getattr(parent, viewport).appendPlainText(f'{task}')
	getattr(parent, viewport).appendPlainText(f'Returned: {outcome}')
	getattr(parent, viewport).appendPlainText(f'{output}\n')

def check_ip(parent):
	if not parent.address_cb.currentData():
		dialogs.errorMsgOk('An IP address must be selected', 'Error!')
		parent.main_tw.setCurrentIndex(0)
		parent.address_cb.setFocus()
		return False
	return True

def firmware_changed(parent):
	if parent.firmware_cb.currentData():
		parent.flash_pb.setEnabled(True)
		parent.reload_pb.setEnabled(True)
		parent.verify_pb.setEnabled(True)
	else:
		parent.flash_pb.setEnabled(False)
		parent.reload_pb.setEnabled(False)
		parent.verify_pb.setEnabled(False)

def find_ip_board(parent):
	if utilities.check_emc():
		dialogs.errorMsgOk(f'LinuxCNC must NOT be running\n to search for a board', 'Error')
		return
	addresses = ['10.10.10.10', '192.168.1.121']
	parent.verify_pte.setPlainText('Looking for IP boards')
	QApplication.processEvents()
	for address in addresses:
		parent.verify_pte.appendPlainText(f'Checking {address}')
		QApplication.processEvents()
		cmd = ['ping', '-c', '1', address]
		output = subprocess.run(cmd, capture_output=True, text=True)
		if output.returncode == 0:
			cmd = ['mesaflash', '--device', 'ether', '--addr', address]
			output = subprocess.run(cmd, capture_output=True, text=True)
			parent.verify_pte.clear()
			msg = (f'Find IP Board Results:{output.stdout}')
			parent.verify_pte.setPlainText(msg)
			break
		elif output.returncode != 0:
			parent.verify_pte.appendPlainText(f'No Board found at {address}')

def verify_ip_board(parent): # make me toss up the error message and return False
	board_name = parent.board_cb.currentText()
	if utilities.check_emc():
		dialogs.errorMsgOk(f'LinuxCNC must NOT be running\n to read the {board_name}', 'Error')
		return
	if check_ip(parent):
		address = parent.address_cb.currentText()
		cmd = ['ping', '-c', '1', address]
		output = subprocess.run(cmd, capture_output=True, text=True)
		if output.returncode != 0:
			msg = (f'No Board found at {address}')
			dialogs.errorMsgOk(msg, 'Error')
			return
		cmd = ['mesaflash', '--device', 'ether', '--addr', address]
		output = subprocess.run(cmd, capture_output=True, text=True)
		selected_board = parent.board_cb.currentText().upper()
		if output.stdout.split()[0] == 'ETH':
			connected_board = output.stdout.split()[2]
		else:
			msg = (f'Device found at {address}\nis not a Mesa Board')
			dialogs.errorMsgOk(msg, 'Error')
			return
		if selected_board == connected_board:
			return True
		else:
			msg = (f'The selected {selected_board} board\n'
			f'does not match the\nconnected {connected_board} board')
			dialogs.errorMsgOk(msg, 'Error')
			return False

def verify_board(parent): # needs to use Popen for password
	board_name = parent.board_cb.currentText()
	cmd = []
	prompt = None
	if utilities.check_emc():
		dialogs.errorMsgOk(f'LinuxCNC must NOT be running\n to read the {board_name}', 'Error')
		return
	if parent.board_interface == 'eth':
		if verify_ip_board(parent):
			ipAddress = parent.address_cb.currentText()
			parent.verify_pte.setPlainText(f'Looking for {board_name} at {ipAddress}')
			cmd = ['mesaflash', '--device', parent.mesaflash_name, '--addr', ipAddress]
			p = Popen(cmd, stdin=PIPE, stderr=PIPE, stdout=PIPE, text=True)
			prompt = p.communicate()
		else:
			return

	elif parent.board_interface == 'spi':
		# mesaflash --device spi --addr 
		msg = ('The Verify Board Function\n'
		'has not been programed yet for SPI\n'
		'JT might need your help\n'
		'getting this done')
		dialogs.msg_ok(msg, 'title')

	elif parent.board_interface == 'pci':
		if not parent.password:
			password = getPassword(parent)
			parent.password = password
		if parent.password != None:
			cmd = ['sudo', '-S', 'mesaflash', '--device', parent.mesaflash_name]
			p = Popen(cmd, stdin=PIPE, stderr=PIPE, stdout=PIPE, text=True)
			prompt = p.communicate(parent.password + '\n')
	if prompt:
		get_results(parent, prompt, p.returncode, 'verify_pte', 'Verify Board')








