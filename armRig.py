# ================================ #
# ================================ #
import pymel.core as pm
import maya.cmds as cmds
import createControllers
import createJoints
# ================================ #
# ================================ #


#  ================= Function to create Arm ============================================ #
#def CreateArm(WS_LOC, spaceGrps, rigging_GRP, ctrl_GRP, skeleton_GRP, vis_aid_GRP, jntList, IKJntList, FKJntList, CTRLs, prefix, jntRadius):

def CreateArm(WS_LOC, space_Grps, rigging_GRPs, CTRLs_GRP, prefix, jntList, IKJntList, FKJntList, jntRadius):
    
    side = 1
    if prefix == 'R_':
        side = -1
