import os
import shutil

def get_directory_path():
    return os.path.dirname(os.path.abspath(__file__))

def rename_folder(current_folder_path, new_folder_name):
    # Get the directory path where the current folder resides
    parent_dir = os.path.dirname(current_folder_path)

    # New folder path
    new_folder_path = os.path.join(parent_dir, new_folder_name)

    # Rename the folder
    os.rename(current_folder_path, new_folder_path)
    print(f"Folder renamed to: {new_folder_path}")

def move_files_to_new_folder(source_folder, new_folder_name):
	# Create a new folder inside the source folder
	new_folder_path = os.path.join(source_folder, new_folder_name)

	if not os.path.exists(new_folder_path):
		os.makedirs(new_folder_path)
		print(f"Created folder: {new_folder_path}")

	# Get all files in the source folder
	for item in os.listdir(source_folder):
		item_path = os.path.join(source_folder, item)

		# Skip the new folder itself
		if item_path != new_folder_path:
			if item == "HDDBConverter.exe":
				print('Did not move HDDB Converter')
			else:
				# Move the file to the new folder
				shutil.move(item_path, new_folder_path)
				print(f"Moved file: {item} to {new_folder_path}")

def ieditforcefiles(get_path, save_path):
	#Opens up the results file you want to edit
	with open(get_path, 'r') as file:
		lines = file.readlines()

	#This loops through the data in the file and puts it into 3 categorys, predata, garbagedata, and data to edit
	#The number in this loop need to be controled to be able to handle 3 body files as well
	i = 0
	predata = []
	garbagedata = []
	datatoedit = []
	for line in lines:
		if i < 7:
			predata.append(line)
		elif i < 13:
			garbagedata.append(line)
		elif i < 14:
			predata.append(line)
		else: 
			datatoedit.append(line)
		i += 1

	#This loop gets rid of the spaces in the data so we can edit them more easily (we are working in rows not columns how the data is organized)
	editeddata = []
	for data in datatoedit:
		newline = []
		splitdata = data.split(' ')
		for item in splitdata:
			if item != '':
				newline.append(item)
		editeddata.append(newline[:-12])

	#This reconstructs the data into the proper format 
	gooddata = []
	for things in editeddata:
		i = 0
		updatedline = []
		fullline = ''
		for thing in things:
			if i == 0:
				updatedline.append('  ' + thing)
			else: 
				if thing[0] == '-':
					updatedline.append(' ' + thing)
				else:
					updatedline.append('  ' + thing)
			i += 1
		for stuff in updatedline:
			fullline = fullline + stuff
		fullline = fullline + "\n"
		gooddata.append(fullline)

	#THis makes it into one big string to we can print it 
	filedata = ''
	for data in predata:
		filedata = filedata + data
	for data in gooddata:
		filedata = filedata + data

	#This saves the edited version
	with open(save_path, 'w') as file:
		file.writelines(filedata)

def editmydata(datatoedit):
	#This loop gets rid of the spaces in the data so we can edit them more easily (we are working in rows not columns how the data is organized)
	editeddata = []
	for data in datatoedit:
		newline = []
		splitdata = data.split(' ')
		for item in splitdata:
			if item != '':
				newline.append(item)
		editeddata.append(newline[:-12])
	return(editeddata)

def reconstructmydata(editeddata):
	#This reconstructs the data into the proper format 
	gooddata = []
	for things in editeddata:
		i = 0
		updatedline = []
		fullline = ''
		for thing in things:
			if i == 0:
				updatedline.append('  ' + thing)
			else: 
				if thing[0] == '-':
					updatedline.append(' ' + thing)
				else:
					updatedline.append('  ' + thing)
			i += 1
		for stuff in updatedline:
			fullline = fullline + stuff
		fullline = fullline + "\n"
		gooddata.append(fullline)
	return(gooddata)

def ieditradfiles(get_path, save_path):
	#Opens up the results file you want to edit
	with open(get_path, 'r') as file:
		lines = file.readlines()

	#This loops through the data in the file and puts it into 3 categorys, predata, garbagedata, and data to edit
	#The number in this loop need to be controled to be able to handle 3 body files as well
	i = 0
	predata = []
	garbagedata = []
	datatoedit1 = []
	gap1 = []
	datatoedit2 = []
	gap2 = []
	datatoedit3 = []
	gap3 = []
	datatoedit4 = []
	gap4 = []
	datatoedit5 = []
	gap5 = []
	datatoedit6 = []
	for line in lines:
		if i < 7:
			predata.append(line)
		elif i < 13:
			garbagedata.append(line)
		elif i < 14:
			predata.append(line)
		elif i < 89:
			datatoedit1.append(line)
		elif i < 90:
			gap1.append(line)
		elif i < 165:
			datatoedit2.append(line) 
		elif i < 166:
			gap2.append(line) 
		elif i < 241:
			datatoedit3.append(line) 
		elif i < 242:
			gap3.append(line) 
		elif i < 317:
			datatoedit4.append(line)
		elif i < 318:
			gap4.append(line)
		elif i < 393:
			datatoedit5.append(line)
		elif i < 394:
			gap5.append(line)
		elif i < 469:
			datatoedit6.append(line)
		i += 1

	#EDIT DATA HERE
	datatoedit1 = editmydata(datatoedit1)
	datatoedit2 = editmydata(datatoedit2)
	datatoedit3 = editmydata(datatoedit3)
	datatoedit4 = editmydata(datatoedit4)
	datatoedit5 = editmydata(datatoedit5)
	datatoedit6 = editmydata(datatoedit6)

	#RECOSTRUCT DATA HERE
	datatoedit1 = reconstructmydata(datatoedit1)
	datatoedit2 = reconstructmydata(datatoedit2)
	datatoedit3 = reconstructmydata(datatoedit3)
	datatoedit4 = reconstructmydata(datatoedit4)
	datatoedit5 = reconstructmydata(datatoedit5)
	datatoedit6 = reconstructmydata(datatoedit6)

	#THis makes it into one big string to we can print it 
	filedata = ''
	for data in predata:
		filedata = filedata + data
	for data in datatoedit1:
		filedata = filedata + data
	for data in gap1:
		filedata = filedata + data
	for data in datatoedit2:
		filedata = filedata + data
	for data in gap2:
		filedata = filedata + data
	for data in datatoedit3:
		filedata = filedata + data
	for data in gap3:
		filedata = filedata + data
	for data in datatoedit4:
		filedata = filedata + data
	for data in gap4:
		filedata = filedata + data
	for data in datatoedit5:
		filedata = filedata + data
	for data in gap5:
		filedata = filedata + data
	for data in datatoedit6:
		filedata = filedata + data

	#This saves the edited version
	with open(save_path, 'w') as file:
		file.writelines(filedata)

# Open and read a .tec file manually

mainpath = get_directory_path() + "\\"

diffractionpath = mainpath + 'results\\DiffractionForce.tec'
fkpath = mainpath + 'results\\FKForce.tec'
diffractionpath2 = mainpath + 'results\\DiffractionForce.tec'
fkpath2 = mainpath + 'results\\FKForce.tec'
radiationpath = mainpath + 'results\\RadiationCoefficients.tec'
radiationpath2 = mainpath + 'results\\RadiationCoefficients.tec'

#Adds new folder and places everything in it
new_folder_name = mainpath.rstrip('\\').rsplit('\\', 1)[-1]
meshpath = mainpath + new_folder_name + "\\" + 'mesh'
meshname = 'Mesh'
source_folder2  = mainpath + new_folder_name + "\\" + meshname

ieditforcefiles(diffractionpath, diffractionpath2)
ieditforcefiles(fkpath, fkpath2)
ieditradfiles(radiationpath, radiationpath2)

move_files_to_new_folder(mainpath, new_folder_name)
rename_folder(meshpath, meshname)
move_files_to_new_folder(source_folder2, new_folder_name)

print('\n')

print('Copy this code and enter it into the command terinal to run the HDDB Convertor')

print('\n')

commandstring = 'HDDBConverter.exe NEMOH 1 ' + new_folder_name + ' 0.0 .\\' + new_folder_name + ' 15 0.1 0 1'

print(commandstring)