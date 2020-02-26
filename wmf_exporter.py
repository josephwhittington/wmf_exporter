#script.py

import maya.cmds as cmds
import pymel.core as pm
import unicodedata

def export(path, material_name):
    print path
    print "materialnameexport:"
    print material_name
    result = cmds.ls( orderedSelection=True )

    shapesInSel = cmds.ls(dag=1,o=1,s=1,sl=1)
    shadingGrps = cmds.listConnections(shapesInSel,type='shadingEngine')
    shaders = cmds.ls(cmds.listConnections(shadingGrps),materials=1)

    tex_color_map = "`"
    tex_metallic_map = "`"
    tex_roughness_map = "`"
    tex_normal_map = "`"
    tex_ao_map = "`"

    # AO Map
    fileNode = cmds.listConnections('%s.TEX_ao_map' % (shaders[0]), type='file')
    if fileNode != None:
        tex_ao_map = cmds.getAttr("%s.fileTextureName" % fileNode[0])
    # Diffuse
    fileNode = cmds.listConnections('%s.TEX_color_map' % (shaders[0]), type='file')
    tex_color_map = cmds.getAttr("%s.fileTextureName" % fileNode[0])
    # Metallic map
    fileNode = cmds.listConnections('%s.TEX_metallic_map' % (shaders[0]), type='file')
    tex_metallic_map = cmds.getAttr("%s.fileTextureName" % fileNode[0])
    # Roughness map
    fileNode = cmds.listConnections('%s.TEX_roughness_map' % (shaders[0]), type='file')
    tex_roughness_map = cmds.getAttr("%s.fileTextureName" % fileNode[0])
    # Normal map
    fileNode = cmds.listConnections('%s.TEX_normal_map' % (shaders[0]), type='file')
    tex_normal_map = cmds.getAttr("%s.fileTextureName" % fileNode[0])

    ## File renames
    tex_color_map = tex_color_map[tex_color_map.rfind('/')+1::]
    tex_color_map = tex_color_map[0: tex_color_map.rfind('.')] + ".dds"

    tex_metallic_map = tex_metallic_map[tex_metallic_map.rfind('/')+1::]
    tex_metallic_map = tex_metallic_map[0: tex_metallic_map.rfind('.')] + ".dds"

    tex_roughness_map = tex_roughness_map[tex_roughness_map.rfind('/')+1::]
    tex_roughness_map = tex_roughness_map[0: tex_roughness_map.rfind('.')] + ".dds"

    tex_normal_map = tex_normal_map[tex_normal_map.rfind('/')+1::]
    tex_normal_map = tex_normal_map[0: tex_normal_map.rfind('.')] + ".dds"

    tex_ao_map = tex_ao_map[tex_ao_map.rfind('/')+1::]
    tex_ao_map = tex_ao_map[0: tex_ao_map.rfind('.')] + ".dds"

    ## Todo: add error checking to not add file extensions if texture is missing

    ## Smaple output
    print tex_color_map
    print tex_metallic_map
    print tex_roughness_map
    print tex_normal_map
    print tex_ao_map

    # Write to the file
    path = path + "/" + material_name + ".wmf"
    print path
    thing = open(path, "w")
    thing.write("# Whittington Material File \n# Version Rc0.1\n\n")
    thing.write("#BEGIN\n")
    thing.write("#diffuse\n")
    thing.write(tex_color_map)
    thing.write("\n#metallic\n")
    thing.write(tex_metallic_map)
    thing.write("\n#roughness\n")
    thing.write(tex_roughness_map)
    thing.write("\n#normal\n")
    thing.write(tex_normal_map)
    thing.write("\n#ao\n")
    thing.write(tex_ao_map)
    thing.write("\n#END\n")
    thing.close()

material_name = "material"

def change(*args):
    global material_name
    print args[0]
    material_name = args[0]
    material_name = unicodedata.normalize('NFKD', material_name).encode('ascii','ignore')
    print "CHANGE::"
    print material_name

nameWindow = cmds.window("001__WMF_EXPORT_WINDOW", t="WMF Export", w=300, h=300)
cmds.columnLayout(adj = True)
cmds.text("WHITTINGTON MATERIAL FILE (WMF 1.0) EXPORTER", height=30)
cmds.separator(height=10)
cmds.text("Material Name")
cmds.text("",height=5)
cmds.textField(height=30, changeCommand=change)
cmds.separator(height=15)
cmds.button(l="Export", command=grabDirectoryName)
cmds.showWindow(nameWindow)
    
def grabDirectoryName(*args):
    global material_name
    thing = pm.fileDialog2(fileMode=3, dialogStyle=2)[0]
    thing = unicodedata.normalize('NFKD', thing).encode('ascii','ignore')
    print "material name: "
    print material_name
    export(thing, material_name)
    cmds.deleteUI(nameWindow)