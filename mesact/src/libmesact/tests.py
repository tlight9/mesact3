
from functools import partial

from libmesact import dialogs
from libmesact import download

def connect(parent):
	parent.msg_open_abort_cancel_pb.clicked.connect(partial(test_dialogs, parent))
	parent.msg_open_cancel_pb.clicked.connect(partial(test_dialogs, parent))
	parent.msg_cancel_ok_pb.clicked.connect(partial(test_dialogs, parent))
	parent.msg_error_ok_pb.clicked.connect(partial(test_dialogs, parent))
	parent.msg_question_pb.clicked.connect(partial(test_dialogs, parent))
	parent.msg_yes_no_pb.clicked.connect(partial(test_dialogs, parent))
	parent.msg_yes_no_check_pb.clicked.connect(partial(test_dialogs, parent))
	parent.msg_ok_pb.clicked.connect(partial(test_dialogs, parent))

	parent.amd64_deb_pb.clicked.connect(partial(download.download_deb, 'amd64', parent))
	parent.armhf_deb_pb.clicked.connect(partial(download.download_deb, 'armhf', parent))
	parent.arm64_deb_pb.clicked.connect(partial(download.download_deb, 'arm64', parent))
	parent.bad_url_pb.clicked.connect(partial(download.download_deb, parent))
	parent.download_firmware_pb.clicked.connect(partial(download.download_firmware, parent))

def test_dialogs(parent):
	name = parent.sender().objectName()
	match name:
		case 'msg_open_abort_cancel_pb':
			result = dialogs.msg_open_abort_cancel(parent, 'Test', 'Title')
			print(result)
		case 'msg_open_cancel_pb':
			result = dialogs.msg_open_cancel(parent, 'Test', 'Title')
			print(result)
		case 'msg_cancel_ok_pb':
			result = dialogs.msg_cancel_ok(parent, 'Test', 'Title')
			print(result)
		case 'msg_error_ok_pb':
			result = dialogs.msg_error_ok(parent, 'Test', 'Title')
			print(result)
		case 'msg_question_pb':
			result = dialogs.msg_question(parent, 'Test', 'Title')
			print(result)
		case 'msg_yes_no_pb':
			result = dialogs.msg_yes_no(parent, 'Test', 'Title')
			print(result)
		case 'msg_yes_no_check_pb':
			result = dialogs.msg_yes_no_check(parent, 'Test', 'Title', 'Text')
			print(result)
		case 'msg_ok_pb':
			result = dialogs.msg_ok(parent, 'Test', 'Title')
			print(result)



