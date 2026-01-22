import hou

def MlibSetColor():
    for n in hou.selectedItems():
        # set null shape and color
        #n.setUserData("nodeshape", "squared")
        col=(1,0,0);
        n.setColor(hou.Color(col));
        
def MlibCreateShotSetup():
    obj_level = hou.node("/obj")
    mlibshotsetup = obj_level.createNode("Mlib_ShotSetup")
        
def MlibCreateNullObjm():
    for n in hou.selectedItems():
        root = n.parent().path()
        if n.networkItemType() == hou.networkItemType.Node:
            if n.type().name() != "null":
                # create null 
                null = hou.node(root).createNode('null',"Out_" + "{0}".format(n.name()))
                
                # Setting node position
                selNodePos = n.position()
                null.setPosition(hou.Vector2(selNodePos[0], selNodePos[1]-1))
        
                # set null shape and color
                null.setUserData("nodeshape", "squared") 
                null.setColor(n.color())
                
                # set youtput / pin dot output
                for conn in n.outputConnections():
                    out_node = conn.outputNode()
                    out_item = conn.outputItem()
                    merge_input_index = conn.inputIndex()
                    if out_node:
                        #print(f"  - Output Node: {out_node.path()}")
                        out_node.setInput(merge_input_index, null)
                        
                    else:
                        if isinstance(out_item, hou.NetworkDot):
                            #print(f"  - Output Pin Dot: {out_item.path()}")
                            merge_input_index = conn.inputIndex()
                            out_item.setInput(merge_input_index, null)
                            
    
                # set input 
                null.setInput(0, n)
    
    
                # set selected
                n.setSelected(False)
                null.setSelected(True)
                
                # set display flag
                #n.setRenderFlag(True)
                #n.setRenderFlag(False)
                #null.setRenderFlag(True)
                #null.setDisplayFlag(True)

                #n.setDisplayFlag(False)
                
            else:            
                objm = hou.node(root).createNode('object_merge',"OBJM_" + "{0}".format(n.name()))
    
                # Setting node position
                selNodePos = n.position()
                objm.setPosition(hou.Vector2(selNodePos[0], selNodePos[1]-1))
                
                objm.parm("objpath1").set(n.path())
                objm.parm("xformtype").set(1)
                
                # set null shape and color
                shape = n.userData("nodeshape")
                if(shape == None):
                    shape = "rect"
                objm.setUserData("nodeshape", shape) 
                objm.setColor(n.color())
        
                # set selected
                n.setSelected(False)
                objm.setSelected(True)
                
    
                # set setDisplayFlag
                objm.setRenderFlag(True)
                objm.setDisplayFlag(True)
                #n.setRenderFlag(False)


        if n.networkItemType() == hou.networkItemType.NetworkDot:
            #print(f"选中的是 NetworkDot: {n.path()}")
            # create null 
            null = hou.node(root).createNode('null',"Out" + "{0}".format(n.name()))
        
            # Setting node position
            selNodePos = n.position()
            null.setPosition(hou.Vector2(selNodePos[0]-0.5, selNodePos[1]-1))
        
            # set input 
            null.setInput(0, n)
            
            # set output / pin dot output
            for conn in n.outputConnections():
                out_node = conn.outputNode()
                out_item = conn.outputItem()
                merge_input_index = conn.inputIndex()
                if out_node:
                    #print(f"  - Output Node: {out_node.path()}")
                    out_node.setInput(merge_input_index, null)
                    
                else:
                    if isinstance(out_item, hou.NetworkDot):
                        #print(f"  - Output Pin Dot: {out_item.path()}")
                        merge_input_index = conn.inputIndex()
                        out_item.setInput(merge_input_index, null)
                        

            # set input 
            null.setInput(0, n)


            # set selected
            n.setSelected(False)
            null.setSelected(True)
            
            # set display flag
            #null.setRenderFlag(True)
            #null.setDisplayFlag(True)
            #n.setDisplayFlag(False)
            #n.setRenderFlag(False)




def MlibExtractPath():
    # get path attribute name
    button_index,text= hou.ui.readInput("Attribute Name(primitive)", buttons=("OK", "Cancel"))
    # print(button_index)
    # print(text)


    # get current nodes
    currentNodes = hou.selectedNodes() 
    # print(currentNode)

    for i in currentNodes:

        # col = (0.5,0.5,0.5)
        # i.setColor(hou.Color(col))
        
        nodepath = i.path() # get path
        root = i.parent().path() # get root
        # print(root)
        nodepos = i.position() # get current node position
        # print(nodepos)
        
        pathAttcode = i.geometry().findPrimAttrib(text) # get path attribute
        pathAtt = []
        
        if pathAttcode :
            for path in pathAttcode.strings() :
                # print(path)
                pathAtt.append(path) # get all uniuqe attributes List
            # print(pathAtt)
            
        for ib in range(len(pathAtt)):
            # print(ib)
            # print(pathAtt[ib])
            
            name = pathAtt[ib].split("/") # get name
            # print(name[-1])
            name_fix = name[-1].replace(":", "_") 
            # fix name from ":" to "_", otherwise node name will be error
            
            # create blast
            blast = hou.node(root).createNode("blast","ExtraPath_" + name_fix)
            
            blast.setPosition(hou.Vector2(nodepos[0]+ib*3,nodepos[1]-1))
            blast.setInput(0, i)
            
            blast.parm("group").set("@" + text + "=" + pathAtt[ib])
            blast.parm("negate").set(1)
            
            # create null
            null = blast.createOutputNode("null","Out_ExtraPath_" + name_fix)
            
            null.setGenericFlag(hou.nodeFlag.DisplayComment,True)
            null.setComment(name[-1])
            
            
        

def MlibCreateGeo():
    #if tord==0:
    create=[]
        
    #choose nodes to run script
    for n in hou.selectedNodes():

        geos=hou.node('/obj').createNode('geo','{0}'.format(n.name()))
        
        objmerge=geos.createNode('object_merge','{0}'.format(n.name()))
        objmerge.parm('xformtype').set(1)
        objmerge.parm('objpath1').set(n.path())
       
        #create geo col
        col=(.5,0,1)
        geos.setColor(hou.Color(col))
        
        father=n.parent()
        pos=father.position()
        
        
        create.append(geos)
        
        # set position of each geo node
        for i in range(len(create)):
           geos.setPosition(hou.Vector2(pos[0]+i*3,pos[1]-4))
        
        # go back to obj level
        pane = hou.ui.paneTabOfType(hou.paneTabType.NetworkEditor)
        pane.setPwd(hou.node("/obj"))
        
        # select new node
        for i, n in enumerate(create):
            n.setSelected(True, clear_all_selected=(i == 0))
            
            
            
            
def MlibGeoToRs():

    # def find_cameras(node):
    #     cameras = []
    #     if node.type().name() == "cam":
    #         cameras.append(node.path())
    #     # 遍历子节点
    #     for child in node.children():
    #         cameras.extend(find_cameras(child))
    #     return cameras
    # # 获取 /obj 层级下的所有相机，包括子层级
    # obj_node = hou.node("/obj")
    # all_cameras = find_cameras(obj_node)
    # 输出所有相机路径
    # print(all_cameras)
    # print(len(all_cameras)!=0)
    create=[]
    #choose  nodes to render
    for n in hou.selectedNodes():
        # print(n)# 在选中节点下创建ROP网络（若不存在）
        # 在ROP网络中创建Redshift渲染节点
        rs_render = hou.node("/out").createNode("Redshift_ROP","rndr_" + "{0}".format(n.name()))
        # 设置基本渲染参数（示例）
        rs_render.parm("trange").set("on")
        # if(len(all_cameras)!=0):
            # rs_render.parm("RS_renderCamera").set(all_cameras[0])    # 指定渲染相机
        rs_render.parm("RS_outputFileNamePrefix").set("$HIP/render/v001/$OS/$OS.$F4.exr")  # image输出路径
        rs_render.parm("RS_archive_file").set("$HIP/rop/v001/$OS/$OS.$F4.rs")  # proxy输出路径
        #rs_render.parm("RS_archive_enable").set(True)
        rs_render.parm("RS_objects_candidate").set("")  # object
        rs_render.parm("RS_objects_force").set("{0}".format(n.name()))
        rs_render.parm("RS_lights_candidate").set("")  # light
        rs_render.setCurrent(True,True)
        create.append(rs_render)
        pos=(0,0,0)
        for i in range(len(create)):
            rs_render.setPosition(hou.Vector2(pos[0]+i*3,pos[1]-6))
    hou.ui.setStatusMessage(" Redshift node creation is complete and has been associated to the selected nodes ")
    # hou.ui.displayMessage("Redshift节点创建完成并已关联到: {}".format(n.name()))
    
    
    
def MlibExtractGroups():
    # 1. 获取当前选择的节点
    selected_nodes = hou.selectedNodes()
    
    if not selected_nodes:
        hou.ui.displayMessage("(Please select a node first).")
        return

    node = selected_nodes[0]
    parent = node.parent()
    geo = node.geometry()
    
    if not geo:
        hou.ui.displayMessage("(Selected node has no geometry).")
        return
        
    # --- 布局参数 ---
    base_pos = node.position()
    start_x = base_pos.x()
    start_y = base_pos.y()
    
    # 间距设置
    x_gap = 2.0  # 水平间距
    y_gap = 1.0  # 垂直间距 (Blast 在源节点下方多少)
    
    # 组计数器 (用来计算向右偏移的倍数)
    group_counter = 0
    
    # set color
    color_A = hou.Color((0.4, 0.5, 0.7))   # Point Group 颜色
    color_B = hou.Color((0.7, 0.5, 0.3)) # Primitive Group 颜色
    
    # 用于收集新创建的节点以便后续排版
    created_nodes = []

    # 定义一个内部函数来创建 Blast 和 Null
    def create_extract_setup(group_name, group_type_val, index, node_color):
        # 计算坐标
        # 第一个节点(index=0) X轴不变，后续每增加一个，X轴增加 x_gap
        current_x = start_x + (index * x_gap)
        
        blast_pos_y = start_y - y_gap
        null_pos_y = start_y - (y_gap * 2) # Null 再往下挪一个单位
        
        # group_type_val: 1 for Points, 2 for Primitives
        
        # 创建 Blast 节点
        blast = parent.createNode("blast", f"blast_{group_name}")
        blast.setInput(0, node)
        blast.parm("group").set(group_name)
        blast.parm("grouptype").set(group_type_val) # 设置组类型 (点或面)
        blast.parm("negate").set(1) # 勾选 Delete Non Selected (保留组)
        
        # 设置 Blast 位置
        # blast.setColor(node_color)
        blast.setPosition(hou.Vector2(current_x, blast_pos_y))
        
        
        # 创建 Null 节点
        null_node = parent.createNode("null", f"OUT_{group_name}")
        null_node.setInput(0, blast)
        
        # 设置 Null 节点的颜色 (例如黑色/深灰色，方便识别)
        null_node.setColor(node_color)
        null_node.setUserData("nodeshape", "squared") 
        
        # 设置 Null 位置 (X轴与Blast对齐，Y轴更靠下)
        null_node.setPosition(hou.Vector2(current_x, null_pos_y))
        
        # 
        created_nodes.append(blast)
        created_nodes.append(null_node)

    # 2. 遍历所有的 Primitive Groups (面组)
    for group in geo.primGroups():
        create_extract_setup(group.name(), 4, group_counter, color_B)
        group_counter += 1

    # 3. 遍历所有的 Point Groups (点组)
    for group in geo.pointGroups():
        create_extract_setup(group.name(), 3, group_counter, color_A)
        group_counter += 1
        

    # 4. print text
    if created_nodes:
        print(f"already extract {len(created_nodes)//2} groups")
    else:
        print("X(No groups found).")