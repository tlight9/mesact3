import os, shutil
from datetime import datetime

def build(parent):
	# if Axis is the GUI add the shutup file
	if parent.gui_cb.currentData() == 'axis':
		if parent.axis_nag_cb.isChecked():
			shutup_file = os.path.expanduser('~/.axisrc')
			if not os.path.isfile(shutup_file):
				with open(shutup_file, 'w') as f:
					f.writelines(['root_window.tk.call("wm","protocol",".","WM_DELETE_WINDOW","destroy .")'])
					parent.info_pte.appendPlainText(f'Building {shutup_file}')

	if parent.custom_hal_cb.isChecked():
		custom_file = os.path.join(parent.config_path, 'custom.hal')
		if not os.path.isfile(custom_file):
			contents = ['# This file was created with the Mesa Configuration Tool on ']
			contents.append(datetime.now().strftime('%b %d %Y %H:%M:%S') + '\n')
			contents.append('# Add HAL commands to this file that need to be executed BEFORE the GUI loads\n')
			contents.append('# This file will not be modified by the Configuration tool if it exists\n')
			with open(custom_file, 'w') as f:
				f.writelines(contents)
				parent.info_pte.appendPlainText(f'Building {custom_file}')

	if parent.postgui_hal_cb.isChecked():
		# create the postgui.hal file if not there
		postgui_file = os.path.join(parent.config_path, 'postgui.hal')
		if not os.path.isfile(postgui_file):
			contents = ['# This file was created with the Mesa Configuration Tool on ']
			contents.append(datetime.now().strftime('%b %d %Y %H:%M:%S') + '\n')
			contents.append('# Add HAL commands to this file that need to be executed AFTER the GUI loads\n')
			contents.append('# This file will not be modified by the Configuration tool if it exists\n')
			with open(postgui_file, 'w') as f:
				f.writelines(contents)
				parent.info_pte.appendPlainText(f'Building {postgui_file}')

	if parent.shutdown_hal_cb.isChecked():
		# create the shutdown.hal file if not there
		shutdown_file = os.path.join(parent.config_path, 'shutdown.hal')
		if not os.path.isfile(shutdown_file):
			contents = ['# This file was created with the Mesa Configuration Tool on ']
			contents.append(datetime.now().strftime('%b %d %Y %H:%M:%S') + '\n')
			contents.append('# Add HAL commands to this file that need to be executed AFTER the GUI shuts down\n')
			contents.append('# This file will not be modified by the Configuration tool if it exists\n')
			with open(shutdown_file, 'w') as f:
				f.writelines(contents)
				parent.info_pte.appendPlainText(f'Building {shutdown_file}')

	# create the readme file if text in readme_pte
	if parent.readme_pte.toPlainText():
		readme_file = os.path.join(parent.config_path, 'README')
		with open(readme_file, 'w') as f:
			f.writelines(parent.readme_pte.toPlainText())

	# create the linuxcnc/subroutines directory if requested and not there
	if parent.subroutine_cb.isChecked():
		sub_path = os.path.expanduser('~/linuxcnc/subroutines')
		if not os.path.isdir(sub_path):
			os.mkdir(os.path.expanduser('~/linuxcnc/subroutines'))
			parent.info_pte.appendPlainText(f'The directory {sub_path} was created')

	# create the var file if not there
	var_file = os.path.join(parent.config_path, 'parameters.var')
	if not os.path.isfile(var_file):
		open(var_file, 'a').close()
		parent.info_pte.appendPlainText(f'The parameters file {var_file} was created')

	# create the tool file if not there
	tool_file = os.path.join(parent.config_path, 'tool.tbl')
	if not os.path.isfile(tool_file):
		with open(tool_file, 'w') as f:
			f.write(';\n')
			f.write('T1  P1  ;sample tool')
		parent.info_pte.appendPlainText(f'The tool table file {tool_file} was created')

	# create the pyvcp panel if checked and not there
	if parent.pyvcp_cb.isChecked():
		pyvcp_file = os.path.join(parent.config_path, 'pyvcp.xml')
		if not os.path.isfile(pyvcp_file):
			contents = ["<?xml version='1.0' encoding='UTF-8'?>\n"]
			contents.append('<pyvcp>\n')
			contents.append('<!--\n')
			contents.append('Build your PyVCP panel between the <pyvcp></pyvcp> tags.\n')
			contents.append('Make sure your outside the comment tags.\n')
			contents.append('The contents of this file will not be overwritten\n')
			contents.append('when you run the configuration tool again.\n')
			contents.append('-->\n')
			contents.append('	<label>\n')
			contents.append('		<text>"This is a Sample Label:"</text>\n')
			contents.append('		<font>("Helvetica",10)</font>\n')
			contents.append('	</label>\n')
			contents.append('</pyvcp>\n')
			with open(pyvcp_file, 'w') as f:
				f.writelines(contents)
				parent.info_pte.appendPlainText(f'Building {pyvcp_file}')

	if parent.ladder_gb.isChecked():
		ladder_file = os.path.join(parent.config_path, 'ladder.clp')
		if not os.path.isfile(ladder_file):
			source = os.path.join(parent.lib_path, 'ladder.clp')
			if os.path.isfile(source):
				shutil.copy(source, ladder_file)








