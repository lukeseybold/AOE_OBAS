import meshmagick.mmio as mmio
import os
import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QPushButton, QLineEdit, QVBoxLayout, QHBoxLayout, QMainWindow, QDialog)
from PyQt5.QtCore import Qt

#Opens the file handed to it
def open_file(file_path):
    with open(file_path, 'r') as file:
        contents = file.read()
        return contents

#Gets the points and panels from the mesh file handed to it
def get_geom_contents(contents):
		splitcontents = contents.split('\n')
		points = splitcontents[0]
		panels = splitcontents[1]

		return points, panels

#Edits the contents of the numeric parameter input file
def edit_input_solver_contents(contents, inputdata):
        splitcontents = contents.split('\n', 3)
        number = [0, 0, 0, 0]
        rest = [0, 0, 0, 0]
        newcontent = ''
        for i, splits in enumerate(splitcontents):
            number[i] = splits.split('\t', 1)[0]
            rest[i] = '\t' + splits.split('\t', 1)[1]

        for i, rest in enumerate(rest):
            newcontent = newcontent + inputdata[i] + rest + '\n'
        
        return newcontent

#Edits the contents of the geom input file
def edit_mesh_contents(contents, inputdata):
        splitcontents = contents.split('\n')
        splitcontents.pop()

        newcontent = ''
        for i, splits in enumerate(splitcontents):
             newcontent = newcontent + inputdata[i] + "\n"

        return newcontent

#Edits the contents of the main input file
def edit_nemoh_contents(contents, inputdata):
     splits = contents.split('\n')
     splits.pop()

     headingflag = 0
     headingcount = 0
     newcontent = ''

     for split in splits:
          splite = split.split('\t', 1)

          if splite[0][0] == "-":
               headingflag += 1
               headingcount = 0
               newcontent = newcontent + splite[0] + "\n"
          else:
               if headingflag == 1:
                    #We are in the environment
                    newcontent = newcontent + inputdata[0][headingcount] + "\t" + splite[1] + "\n"
                    headingcount += 1
               elif headingflag == 2:
                    #we are in the description of floating bodies
                    newcontent = newcontent + inputdata[1][headingcount] + "\t" + splite[1] + "\n"
                    headingcount += 1
               elif headingflag == 3:
                    #We are in body 1
                    newcontent = newcontent + inputdata[2][headingcount] + "\t" + splite[1] + "\n"
                    headingcount += 1
               elif headingflag == 4:
                    #We are in body 2
                    newcontent = newcontent + inputdata[3][headingcount] + "\t" + splite[1] + "\n"
                    headingcount += 1
               elif headingflag == 5:
                    #We are in load cases to be solved
                    newcontent = newcontent + inputdata[4][headingcount] + "\t" + splite[1] + "\n"
                    headingcount += 1
               elif headingflag == 6: 
                    #We are in post processing 
                    newcontent = newcontent + inputdata[5][headingcount] + "\t" + splite[1] + "\n"
                    headingcount += 1
               elif headingflag == 7:  
                    #We are in QTF 
                    newcontent = newcontent + inputdata[6][headingcount] + "\t" + splite[1] + "\n"
                    headingcount += 1

     return newcontent

#Saves the file its handed
def write_file(file_path, content):
    with open(file_path, 'w') as file:
         file.write(content)

#Gets the path
def get_directory_path():
    return os.path.dirname(os.path.abspath(__file__))

#Lists files in a path
def list_files_in_directory(directory_path):
    return [f for f in os.listdir(directory_path) if os.path.isfile(os.path.join(directory_path, f))]

#This just gets the main file path determines the names of your mesh files and then makes more paths from them to use later
generic_file_path = get_directory_path() + "\\"
generic_folder_path = generic_file_path + "mesh"
names = list_files_in_directory(generic_folder_path)
name1 = names[0].replace(".obj", "")
name2 = names[1].replace(".obj", "") 
mesh_geometry_file_path1 = generic_folder_path + "\\" + name1
mesh_geometry_file_path2 = generic_folder_path + "\\" + name2
mesh_geom_file_path1 = generic_file_path + "\\" + name1 + "_Geom_File"
mesh_geom_file_path2 = generic_file_path + "\\" + name2 + "_Geom_File"

#Loads the mesh file
verts1, faces1 = mmio.load_OBJ(mesh_geometry_file_path1 + ".obj")
verts2, faces2 = mmio.load_OBJ(mesh_geometry_file_path2 + ".obj")

#Writes the mesh files to .dat and the geom input format
mmio.write_MAR(mesh_geometry_file_path1 + ".Dat", verts1, faces1)
mmio.write_NEM(mesh_geom_file_path1, verts1, faces1)

mmio.write_MAR(mesh_geometry_file_path2 + ".Dat", verts2, faces2)
mmio.write_NEM(mesh_geom_file_path2, verts2, faces2)

geom_content1 = open_file(mesh_geom_file_path1)
points1, panels1 = get_geom_contents(geom_content1)
print(points1)
print(panels1)

geom_content2 = open_file(mesh_geom_file_path2)
points2, panels2 = get_geom_contents(geom_content2)
print(points2)
print(panels2)

#Making more paths for the input files
input_solver_file_path = generic_file_path + 'input_solver.txt'
mesh_file_path = generic_file_path + 'Mesh.cal'
nemoh_file_path = generic_file_path + 'Nemoh.cal'

#Base input values for the numerical parameter input file
input_solver_inputdata = ['2', '0.001', '1', '10 1e-5 1000']

#Base input values for the geom input file
mesh_inputdata = [name2 + '_Geom_File', '1', '0 0', '0.000000 0.000000 -9.740000', panels2, '2', '0', '1', '1025.000000', '9.810000']

#Base input values for the main NEMOH input file
environmentdata = ['1025.0', '9.81', '0.', '0. 0.']
floatingdata = ['2']
bodydata1 = ["mesh\\" + name1 + ".dat", points1 + " " + panels1, '6', '1 1. 0. 0. 0. 0. 0.', '1 0. 1. 0. 0. 0. 0.', '1 0. 0. 1. 0. 0. 0.', '2 1. 0. 0. 0. 0. 0.803', '2 0. 1. 0. 0. 0. 0.803', '2 0. 0. 1. 0. 0. 0.803', '6', '1 1. 0. 0. 0. 0. 0.', '1 0. 1. 0. 0. 0. 0.', '1 0. 0. 1. 0. 0. 0.80', '2 1. 0. 0. 0. 0. 0.803', '2 0. 1. 0. 0. 0. 0.803', '2 0. 0. 1. 0. 0. 0.803', '0']
bodydata2 = ["mesh\\" + name2 + ".dat", points2 + " " + panels2, '6', '1 1. 0. 0. 0. 0. 0.', '1 0. 1. 0. 0. 0. 0.', '1 0. 0. 1. 0. 0. 0.', '2 1. 0. 0. 0. 0. -9.74', '2 0. 1. 0. 0. 0. -9.74', '2 0. 0. 1. 0. 0. -9.74', '6', '1 1. 0. 0. 0. 0. 0.', '1 0. 1. 0. 0. 0. 0.', '1 0. 0. 1. 0. 0. 0.', '2 1. 0. 0. 0. 0. -9.74', '2 0. 1. 0. 0. 0. -9.74', '2 0. 0. 1. 0. 0. -9.74', '0']
loadcasedata = ['1 50 0.1 6.0', '1 0. 0.']
postprocdata = ['1 0.1 10.', '1', '0 0. 180.', '0 10 100. 100.', '0', '1']
qtfdata = ['0']
nemoh_inputdata = [environmentdata, floatingdata, bodydata1, bodydata2, loadcasedata, postprocdata, qtfdata]

# Sample data: List of titles and their corresponding values
first_file_titles = [
    'Main Input File', 
    'Geometry Meshing Input File', 
    'Numerical Parameters Input File'
]

# List of subgroups for the main input file
main_input_subgroups = [
    'Environment',
    'Description of Floating Bodies', 
    'Body 1',
    'Body 2', 
    'Load Cases',
    'Post Processing',
    'QTF'
]

# Corresponding values for each subgroup
main_input_values = [
    environmentdata,
    floatingdata,               
    bodydata1,
    bodydata2,
    loadcasedata,
    postprocdata,
    qtfdata
]

#Base values for all of the input files
input_file_values = [
    #Main input file values
    main_input_values,
    #Geom Input file values
    mesh_inputdata,
    #Numerical parameter input file values
    input_solver_inputdata
]

# Titles for the main input file subgroups
main_input_titles = [
     #Envrionemnt Variables
    ["Fluid Density kg / m^3",
     "Gravitational Acceleration m/s^2",
     "Water depth m",
     "Wave measurment location Xeff Yeff"
     ],
     #Description of Floating Bodies
    [
     "Number of bodies (DONT EDIT)"
     ],
     #Body 1 Variables
    ["Name of mesh file (DONT EDIT)",
     "Number of nodes and number of panels in mesh (DONT EDIT)",
     "Number of degrees of freedom",
     "Surge",
     "Sway",
     "Heave",
     "Roll about a point",
     "Pitch about a point",
     "Yaw about a point",
     "Number of resulting generalised forces",
     "Force in x direction",
     "Force in y direction",
     "Force in z direction",
     "Moment force in x direction about a point",
     "Moment force in y direction about a point",
     "Moment force in z direction about a point",
     "Reserved (Don't Edit)"
     ],
    #Body 2 Variables
    ["Name of mesh file (DONT EDIT)",
     "Number of nodes and number of panels in mesh (DONT EDIT)",
     "Number of degrees of freedom",
     "Surge",
     "Sway",
     "Heave",
     "Roll about a point",
     "Pitch about a point",
     "Yaw about a point",
     "Number of resulting generalised forces",
     "Force in x direction",
     "Force in y direction",
     "Force in z direction",
     "Moment force in x direction about a point",
     "Moment force in y direction about a point",
     "Moment force in z direction about a point",
     "Reserved (Don't Edit)"
     ],
     #Load Cases
    ["Wave Frequency Range: unit (1 for rad/s, 2 for HZ, 3 for s), number of frequencys, min frequency, max frequency",
     "Wave direction range: number of waves, min wave direction, max wave direction (in degrees)"
     ],
     #Post Processing
    ["IRF (impulse response function) flag (0/1), time step, duration",
     "Pressure output flag (0/1)",
     "Kochin functions direction range: Number of Kochins, min angle, max angle (in degrees)",
     "Free surface elevation output: number of points in x direction (0 to deactivate) and y direction and (x,y) dimesniosn of domain",
     "RAO (response amplitude operator) flag (0/1)",
     "Output requency unit, 1 for rad/s, 2 for hz, 3 for s"
     ],
     #QTF
    ["QTF (quadratic Transfer Function) flag (0/1)"]
]

# Titles for the other input files
input_file_titles = [
    main_input_titles,
    #Titles for Geom Input File
    ["Name of the geomInput file",
     "1 for symmetric (about xOz) body half-mesh, 0 if else",
     "translation about x and y axis (respectively)",
     "Coordinates of gravity centre",
     "Target or the number of panels in refines mesh",
     "minimum subdivision of geometric panel",
     "Reseved Do Not Edit",
     "Scaling Factor",
     "Water Density kg/m^3",
     "Gravity acceleration m/s^2",
     ],
    #Titles for the numerical parameters input file
    ["Guass quadrature order N = [1,4] for surface integration, resulting in N^2 nodes",
     "eps_zmin for determining minimum z of flow and source point of panel",
     "Solver option: 0 for GAUSS ELIM., 1 for LU DECOMP., 2 for GMRES",
     "GMRES parameters: restart parameter, relative tolerance, max number of iterations",
     ]
]

#This is the UI which allows the user to edit any of the input values without needing to go into this python file
class EditSubgroupWindow(QDialog):
    def __init__(self, title, subgroups, main_window):
        super().__init__()
        self.setWindowTitle(title)
        self.main_window = main_window
        self.subgroups = subgroups
        self.initUI()

    def initUI(self):
        self.setGeometry(300, 100, 400, 200)
        layout = QVBoxLayout()
        layout.setSpacing(15)

        for index, subgroup in enumerate(self.subgroups):
            button = QPushButton(f"Edit {subgroup}", self)
            button.clicked.connect(lambda checked, index=index: self.open_value_window(index))
            layout.addWidget(button)

        close_button = QPushButton("Close", self)
        close_button.clicked.connect(self.close_window)
        layout.addWidget(close_button, alignment=Qt.AlignRight)

        self.setLayout(layout)

    def open_value_window(self, index):
        values = input_file_values[0][index]
        titles = main_input_titles[index]  # Get titles for the selected subgroup
        self.value_window = EditOptionsWindow(f"Edit {self.subgroups[index]}", values, titles, self.main_window, 0, index)
        self.hide()
        self.value_window.exec_()

    def close_window(self):
        self.main_window.show()
        self.close()

class EditOptionsWindow(QDialog):
    def __init__(self, title, values, titles, main_window, main_index, subgroup_index):
        super().__init__()
        self.setWindowTitle(title)  # Set the window title correctly
        self.main_window = main_window
        self.main_index = main_index
        self.subgroup_index = subgroup_index
        self.initUI(values, titles)

    def initUI(self, values, titles):
        self.setGeometry(300, 100, 500, 300)
        layout = QVBoxLayout()
        layout.setSpacing(15)

        self.line_edits = []

        for i, value in enumerate(values):
            h_layout = QHBoxLayout()
            label = QLabel(f"{titles[i]}:")  # Use the corresponding title for each value
            label.setMinimumWidth(300)
            label.setWordWrap(True)

            line_edit = QLineEdit(self)
            line_edit.setText(value)
            line_edit.setFixedWidth(150)
            self.line_edits.append(line_edit)

            h_layout.addWidget(label)
            h_layout.addWidget(line_edit)
            layout.addLayout(h_layout)

        close_button = QPushButton("Close", self)
        close_button.clicked.connect(self.close_window)
        layout.addWidget(close_button, alignment=Qt.AlignRight)

        self.setLayout(layout)

    def close_window(self):
        if self.main_index == 0:  # If editing the main input file
            for i, line_edit in enumerate(self.line_edits):
                input_file_values[self.main_index][self.subgroup_index][i] = line_edit.text()
        else:
            for i, line_edit in enumerate(self.line_edits):
                input_file_values[self.main_index][i] = line_edit.text()

        self.main_window.show()
        self.close()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Input Parameter Files')
        self.setGeometry(200, 100, 400, 250)
        self.initUI()

    def initUI(self):
        main_widget = QWidget(self)
        layout = QVBoxLayout(main_widget)
        layout.setSpacing(20)

        self.input_files = first_file_titles

        for index, input_file in enumerate(self.input_files):
            # Use the main title for the button label
            button = QPushButton(f"Edit {first_file_titles[index]}", self)
            button.setMinimumHeight(40)
            if index == 0:  # Main input file
                button.clicked.connect(lambda checked: self.open_subgroup_window())
            else:
                button.clicked.connect(lambda checked, index=index: self.open_edit_window(index))
            layout.addWidget(button)

        main_widget.setLayout(layout)
        self.setCentralWidget(main_widget)

    def open_subgroup_window(self):
        self.subgroup_window = EditSubgroupWindow("Edit Main Input File", main_input_subgroups, self)
        self.hide()
        self.subgroup_window.exec_()

    def open_edit_window(self, index):
        values = input_file_values[index]
        titles = input_file_titles[index]
        self.edit_window = EditOptionsWindow(f"Edit {input_file_titles[index][0][0]}", values, titles, self, index, None)
        self.hide()
        self.edit_window.exec_()

#After the user is done editing the code then applies all the changes
def on_app_close():
     #Opening All the Files
     input_solver_content = open_file(input_solver_file_path)
     mesh_content = open_file(mesh_file_path)
     nemoh_content = open_file(nemoh_file_path)

     #Editing All the Content
     new_input_solver_content = edit_input_solver_contents(input_solver_content, input_solver_inputdata)
     new_mesh_content = edit_mesh_contents(mesh_content, mesh_inputdata)
     new_nemoh_content = edit_nemoh_contents(nemoh_content, nemoh_inputdata)

     #Saving All the Files
     write_file(input_solver_file_path, new_input_solver_content)
     write_file(mesh_file_path, new_mesh_content)
     write_file(nemoh_file_path, new_nemoh_content)

# Initialize the application
app = QApplication(sys.argv)
app.aboutToQuit.connect(on_app_close)

window = MainWindow()
window.show()

sys.exit(app.exec_())
