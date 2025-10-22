import meshmagick.mmio as mmio
import os

def open_file(file_path):
    with open(file_path, 'r') as file:
        contents = file.read()
        return contents

def get_geom_contents(contents):
		splitcontents = contents.split('\n')
		points = splitcontents[0]
		panels = splitcontents[1]

		return points, panels

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

def edit_mesh_contents(contents, inputdata):
        splitcontents = contents.split('\n')
        splitcontents.pop()

        newcontent = ''
        for i, splits in enumerate(splitcontents):
             newcontent = newcontent + inputdata[i] + "\n"

        return newcontent

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
                    #We are in load cases to be solved
                    newcontent = newcontent + inputdata[3][headingcount] + "\t" + splite[1] + "\n"
                    headingcount += 1
               elif headingflag == 5:
                    #We are in post processing
                    newcontent = newcontent + inputdata[4][headingcount] + "\t" + splite[1] + "\n"
                    headingcount += 1
               elif headingflag == 6:  
                    #We are in QTF 
                    newcontent = newcontent + inputdata[5][headingcount] + "\t" + splite[1] + "\n"
                    headingcount += 1

     return newcontent

def write_file(file_path, content):
    with open(file_path, 'w') as file:
         file.write(content)

def get_directory_path():
    return os.path.dirname(os.path.abspath(__file__))

def list_files_in_directory(directory_path):
    return [f for f in os.listdir(directory_path) if os.path.isfile(os.path.join(directory_path, f))]

generic_file_path = get_directory_path() + "\\"
generic_folder_path = generic_file_path + "mesh"
names = list_files_in_directory(generic_folder_path)
name = names[0].replace(".obj", "")
mesh_geometry_file_path = generic_folder_path + "\\" + name
mesh_geom_file_path = generic_file_path + "\\" + name + "_Geom_File"

#Loads the mesh file
verts, faces = mmio.load_OBJ(mesh_geometry_file_path + ".obj")

#Writes the mesh files to .dat and the geom input format
mmio.write_MAR(mesh_geometry_file_path + ".Dat", verts, faces)
mmio.write_NEM(mesh_geom_file_path, verts, faces)

geom_content = open_file(mesh_geom_file_path)
points, panels = get_geom_contents(geom_content)
print(points)
print(panels)

# Replace with your file paths
input_solver_file_path = generic_file_path + 'input_solver.txt'
mesh_file_path = generic_file_path + 'Mesh.cal'
nemoh_file_path = generic_file_path + 'Nemoh.cal'

""" #Gauss quadrature (GQ) surface integration, N^2 GQ Nodes, specify N(1,4)
input1 = '2'
#eps_zmin for determine minimum z of flow and source points of panel, zmin=eps_zmin*body_diameter
input2 = '0.001'
#0 GAUSS ELIM.; 1 LU DECOMP.: 2 GMRES  !Linear system solver
input3 = '1'
#Restart parameter, Relative Tolerance, max iter -> additional input for GMRES
input4 = '10 1e-5 1000' """

input_solver_inputdata = ['2', '0.001', '1', '10 1e-5 1000']

""" #Name of the geomInput file.
input1 = 'Cube_Geom_File'
#1 for a symmetric (about xOz) body half-mesh, 0 otherwise.
input2 = '1'
#Translation about x and y axis (respectively)
input3 = '0 0'
#Coordinates of gravity centre
input4 = '0.000000 0.000000 0.000000'
#Target for the number of panels in refined mesh
input5 = '90'
#Minimum subdivision of a geometric panel
input6 = '2'
#Just a 0 always
input7 = '0'
#Scaling factor
input8 = '1'
#Water density kg/m^3
input9 = '1000.000000'
#Gravity acceleration m/s^2
input10 = '9.810000' """

mesh_inputdata = [name + '_Geom_File', '1', '0 0', '0.000000 0.000000 -9.740000', panels, '2', '0', '1', '1025.000000', '9.810000']

environmentdata = ['1025.0', '9.81', '0.', '0. 0.']
floatingdata = ['1']
bodydata = ["mesh\\" + name + ".dat", points + " " + panels, '6', '1 1. 0. 0. 0. 0. 0.', '1 0. 1. 0. 0. 0. 0.', '1 0. 0. 1. 0. 0. 0.', '2 1. 0. 0. 0. 0. -9.74', '2 0. 1. 0. 0. 0. --9.74', '2 0. 0. 1. 0. 0. -9.74', '6', '1 1. 0. 0. 0. 0. 0.', '1 0. 1. 0. 0. 0. 0.', '1 0. 0. 1. 0. 0. 0.', '2 1. 0. 0. 0. 0. -9.74', '2 0. 1. 0. 0. 0. -9.74', '2 0. 0. 1. 0. 0. -9.74', '0']
loadcasedata = ['1 50 0.1 6.0', '1 0. 0.']
postprocdata = ['1 0.1 10.', '1', '0 0. 180.', '0 10 100. 100.', '0', '1']
qtfdata = ['0']

nemoh_inputdata = [environmentdata, floatingdata, bodydata, loadcasedata, postprocdata, qtfdata]

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