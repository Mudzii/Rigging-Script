# ====================================================================================== #
# ====================================================================================== #
from math import pow,sqrt
import pymel.core as pm
import maya.cmds as cmds
# ====================================================================================== #
# ====================================================================================== #


#  ================= Function to clear history/ freeze transform ======================= #
def CleanHist(obj):
    pm.delete(obj , ch = 1)
    pm.makeIdentity(obj, apply = True )
    
# =================== Function to measure distance between 2 objects =================== #
def Distance(objA, objB): 
    vecA = cmds.xform(str(objA), q=True, t=True, ws=True)
    vecB = cmds.xform(str(objB), q=True, t=True, ws=True)
	
    return sqrt(pow(vecA[0]-vecB[0],2)+pow(vecA[1]-vecB[1],2)+pow(vecA[2]-vecB[2],2))
    
# =================== Function to Recolour Object ====================================== #
def RecolourObj(obj, type):
    
    # enable color overrides 
    pm.setAttr(str(obj) + '.overrideEnabled', 1)
    pm.setAttr(str(obj) + '.overrideRGBColors', 1)
    
    # if IK/FK joint. IK joints = magenta. FK joints = green   
    if type is 'joint':
        if obj[-2] == 'I':
            pm.setAttr(str(obj) + '.overrideColorRGB', 0, 1, 0)   
        elif obj[-2] == 'F':
            pm.setAttr(str(obj) + '.overrideColorRGB', 1, 0, 1)       
    
    # if CTRL. Left side = red. Right side = blue. Middle = yellow
    elif type is 'nurbsCurve':
        if obj[0] == 'L':
            pm.setAttr(str(obj) + '.overrideColorRGB', 1, 0, 0)
      
        elif obj[0] == 'R':
            pm.setAttr(str(obj) + '.overrideColorRGB', 0, 0, 1)       

        else: 
            pm.setAttr(str(obj) + '.overrideColorRGB', 1, 1, 0) 
    
# =================== Function to reparent NURB shape ================================== #
def ReparentShape(nurbCTRL, parentCTRL):
  
    ctrlName = str(nurbCTRL[0])
    
    # get the shape node from ctrl
    shapes = pm.listRelatives(ctrlName)
    shape = shapes[0]
     
    # parent shape-node to 
    pm.parent(shape, parentCTRL[0], relative = True, shape= True)
    pm.delete(ctrlName)    
    
 
# =================== Function to create star-shape CTRL =============================== #
def CreateStarCTRL(CTRL_name, CTRL_list, rad, scle, norm):
    
    
    # create NURB circle
    nurbCTRL = cmds.circle( n = str(CTRL_name), nr =norm, c=(0, 0, 0), r= rad )
    
    # get CVs and scale
    curveCVs = cmds.ls('{0}.cv[:]'.format(CTRL_name), fl = True)
    selList = [curveCVs[0], curveCVs[2], curveCVs[4], curveCVs[6]]
    
    selection = pm.select(selList)
    pm.scale(selection, scle)
    
    CleanHist(nurbCTRL[0])
    
    # create offset GRP, parent CTRL to it and add CTRL to list
    offset_GRP = pm.group( em=True, name= str(CTRL_name) + '_offset_GRP' )
    pm.parent(nurbCTRL[0], offset_GRP)
    
    RecolourObj(CTRL_name, 'nurbsCurve')
    CTRL_list.append(offset_GRP)  

        
# =================== Function to create ball CTRL ===================================== #       
def CreateBallCTRL(CTRL_name, CTRL_list, rad):
    
    # create nurb circles & rotate
    nurbCTRL = pm.circle( n = str(CTRL_name), nr =(1,0,0), c=(0, 0, 0), r= rad )
    nurbCTRL1 = pm.circle( n = str('circle1'), nr =(0,0,1), c=(0, 0, 0), r= rad )
    nurbCTRL2 = pm.circle( n = str('circle2'), nr =(0,1,0), c=(0, 0, 0), r= rad )

    nurbCTRL3 = pm.circle( n = str('circle3'), nr =(1,0,0), c=(0, 0, 0), r= rad )
    pm.rotate(nurbCTRL3, [0,0,45])

    nurbCTRL4 = pm.circle( n = str('circle4'), nr =(1,0,0), c=(0, 0, 0), r= rad )
    pm.rotate(nurbCTRL4, [0,0,-45])

    # clean all history 
    CleanHist(nurbCTRL[0])
    CleanHist(nurbCTRL1[0])
    CleanHist(nurbCTRL2[0])
    CleanHist(nurbCTRL3[0])
    CleanHist(nurbCTRL4[0])

    # reparent shapes
    ReparentShape(nurbCTRL4, nurbCTRL)
    ReparentShape(nurbCTRL3, nurbCTRL)
    ReparentShape(nurbCTRL2, nurbCTRL)    
    ReparentShape(nurbCTRL1, nurbCTRL)    

    CleanHist(nurbCTRL[0])
    
    # create offset GRP, parent CTRL to it and add CTRL to list
    offset_GRP = pm.group( em=True, name= str(CTRL_name) + '_offset_GRP' )
    
    RecolourObj(CTRL_name, 'nurbsCurve') 
    CTRL_list.append(offset_GRP)   


    
# =================== Function to create simple circle CTRL ============================ #
def CreateCircleCTRL(CTRL_name, CTRL_list, prntJnt, norm, rad, offset):
    
    #create CTRL and offset grp
    CTRL = cmds.circle( n = str(CTRL_name), nr = norm, c=(0, 0, 0), r= rad )
    offset_GRP = pm.group( em=True, name= str(CTRL_name) + '_offset_GRP' )
    pm.parent(CTRL[0], offset_GRP) 
    
    # clear history for both objects
    CleanHist(CTRL[0])
    CleanHist(offset_GRP)
    
    # temp parentconstr GRP to move to pos (with rot)
    tempConst = pm.parentConstraint(prntJnt, str(offset_GRP), mo = False)
    pm.delete(tempConst)
    
    # rotate curve CVs
    curveCVs = cmds.ls('{0}.cv[:]'.format(CTRL[0]), fl = True)
    pm.rotate(curveCVs, offset)
    
    # parent const to joint
    pm.parentConstraint(str(CTRL_name), str(prntJnt), mo= False, w=1)
    
    # recolor CTRL and add to list 
    RecolourObj(CTRL_name, 'nurbsCurve')
    CTRL_list.append(offset_GRP)    
    
  
# =================== Function to create IK/FK CTRL ==================================== #    
def CreateIKFKSwitch(axis, Switch_CTRL, CTRL_list, visLine, wristJnt):
    
    clusterGRP = []
    
    #create IK/FK Switch ctrl ==========
    Switch_Offset_GRP = str(Switch_CTRL) + '_offset_GRP'
    CreateStarCTRL(Switch_CTRL, CTRL_list, 0.5, [0.3,0.3,0.3], (0,0,1))
    pm.addAttr(longName='IK_FK_Switch', at = 'double', defaultValue=0.0, minValue=0.0, maxValue=1)
    pm.setAttr(str(Switch_CTRL) + '.IK_FK_Switch', k = True) 
    
    # move offset GRP to wrist jnt, remove const
    tempConst = pm.parentConstraint(wristJnt, str(Switch_CTRL), mo = False, sr= ['x', 'y', 'z'])
    pm.delete(tempConst)
   
    pm.move(str(Switch_CTRL), (axis * 0.3,0.6, -1 ),  relative = True)
    CleanHist(Switch_CTRL)
    
    pm.xform(str(Switch_Offset_GRP), cp = True)   
    
    # IK FK switch line ================
    Switch_Line = pm.curve(n = visLine, d=1, p=[(0, 0, 0),(-1, 0, 0)], k=[0,1] )
    
    curvePoints = cmds.ls('{0}.cv[:]'.format(Switch_Line), fl = True)
    wristPos = cmds.xform(str(wristJnt), query=True, translation=True, worldSpace=True ) 
    CTRL_Pos = cmds.xform(str(Switch_CTRL), query=True, translation=True, worldSpace=True )
    
    pm.move( curvePoints[1], wristPos)
    pm.move( curvePoints[0], ((axis * 5.07), 0.09, -0.6))
    CleanHist(Switch_Line)
    
    pm.xform(str(Switch_Line), cp = True)
    
    # create clusters
    wristCluster = pm.cluster(curvePoints[1], n = (str(wristJnt) + '_IKFK_line_cluster'))
    CTRL_cluster = pm.cluster(curvePoints[0], n = (str(Switch_CTRL) + '_IKFK_line_cluster'))
    
    clusterGRP.extend([wristCluster, CTRL_cluster])
    
    tempClusterConst = pm.parentConstraint(str(wristJnt), str(wristCluster[1]), mo = False, w = 1) 
    tempCtrlConst = pm.parentConstraint(str(wristJnt), str(Switch_Offset_GRP), mo=True, w = 1)
    pm.parent(str(CTRL_cluster[1]), str(Switch_Offset_GRP))
    
    CTRL_list.append(Switch_Offset_GRP) 
    
    return clusterGRP
    
       
