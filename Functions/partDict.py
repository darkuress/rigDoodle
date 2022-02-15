armSet = [('shoulder', [5,10,2]), ('elbow', [8,10,0]), ('wrist', [11, 10, 2])]
handSet = ['palm']
fingerSet = ['thumb', 'index', 'middle', 'ring', 'pinky']

spineJoints = ['root', 'spine1', 'spine2', 'spine3', 'spine4', 'neckbase', 'head', 'jaw', 'jawend']
legJoints = ['root', 'pelvis', 'l_hip', 'l_knee', 'l_ankle', 'l_ball', 'l_toe']
legJointsR = ['r_hip', 'r_knee', 'r_ankle', 'r_ball', 'r_toe']
armJoints = ['spine4', 'l_clavicle', 'l_shoulder', 'l_elbow', 'l_wrist']
armJointsR = ['spine4','r_clavicle', 'r_shoulder', 'r_elbow', 'r_wrist']
handJoints = ['Palm']
fingerJoints = ['thumb', 'index', 'middle', 'ring', 'pinky']
tailJoints = ['tail0', 'tail1', 'tail2', 'tail3' 'tail4', 'tail5' 'tail6']


#####################################################
globalCtl = 'global_ctl'
localCtl = 'local_ctl'

lrPrefix     = ['l_', 'r_']
armElement   = ['clavicle', 'shoulder', 'elbow', 'wrist']
legElement   = ['hip', 'knee', 'ankle', 'ball', 'toe']
spineElement = ['spine1', 'spine2', 'spine3', 'spine4']
headElement  = ['neckbase', 'neck1', 'head', 'jaw', 'jawend']
rootElement  = ['root', 'pelvis']
handElement  = ['palm']
thumbElement = ['thumb1', 'thumb2', 'thumb3', 'thumb4']
indexElement = ['index1', 'index2', 'index3', 'index4', 'index5']
middleElement = ['middle1', 'middle2', 'middle3', 'middle4', 'middle5']
ringElement = ['ring1', 'ring2', 'ring3', 'ring4', 'ring5']
pinkyElement = ['pinky1', 'pinky2', 'pinky3', 'pinky4', 'pinky5']

#locator info, {'name' : ['translate', 'scale', 'lock attr info']}
rootPlaceLocs = { #root spine
              'root_adjust_ctl'        : [[0, 12, 0],    1,   'tx'],
              'pelvis_adjust_ctl'      : [[0, 12, 0]   , 1,   'tx']
                }
spinePlaceLocs = {#spine
              'spine1_adjust_ctl'      : [[0, 13, -0.5], 0.7, 'tx'],
              'spine2_adjust_ctl'      : [[0, 15, -0.7], 0.7, 'tx'],
              'spine3_adjust_ctl'      : [[0, 17, -0.7], 0.7, 'tx'],
              'spine4_adjust_ctl'      : [[0, 19, -0.3], 0.7, 'tx']
              }
headPlaceLocs = {#Neck, head, jaw
              'neckbase_adjust_ctl'    : [[0, 21, -0.4], 0.7, 'tx'],
              'neck1_adjust_ctl'    : [[0, 21.5, -0.4], 0.7, 'tx'],
              'head_adjust_ctl'        : [[0, 22, 0]   , 0.7, 'tx'],
              'jaw_adjust_ctl'         : [[0, 22, 2]   , 0.7, 'tx'],
              'jawend_adjust_ctl'      : [[0, 21, 3]   , 0.7, 'tx'],
                }
legPlaceLocs = {#Legs
              'l_hip_adjust_ctl'         : [[2, 12, -1]  , 1,   ''],
              'l_knee_adjust_ctl'      : [[2, 7, -0.2] , 1,   ''  ],
              'l_ankle_adjust_ctl'     : [[2, 2, -0.3] , 1,   ''  ],
              'l_ball_adjust_ctl'      : [[2, 0, 2]    , 1,   ''  ],
              'l_toe_adjust_ctl'       : [[2, 0, 3]    , 1,   ''  ]
                }
legPivotLocs = {
              'l_heel_PivotPosition'    : [[2, 0, -1]   , 0.7, ''  ],
              'l_sidein_PivotPosition'  : [[1.5, 0, 0]  , 0.7, ''  ],
              'l_sideout_PivotPosition' : [[2.5, 0, 0]  , 0.7, ''  ]
                }
armPlaceLocs = {#Arms
              'l_clavicle_adjust_ctl'   : [[2, 18, -1]  , 1,   ''  ],
              'l_shoulder_adjust_ctl'  : [[3, 20, -0.3], 1,   ''  ],
              'l_elbow_adjust_ctl'     : [[6, 20, -1.5], 1,   ''  ],
              'l_wrist_adjust_ctl'     : [[9, 20, -0.3], 1,   ''  ],
              #palm
              #'l_Palm_adjust_ctl'     : [[9.7, 20, -0.3],1,   ''  ]
            }

handPlaceLocs = {'l_palm_adjust_ctl'     : [[9.5, 20, -0.3], 1,   ''  ]}

#- fingers
thumbPlaceLocs = {'l_thumb1_adjust_ctl'      : [[10.5, 19.5, 1], 0.7, ''],
                  'l_thumb2_adjust_ctl'      : [[11.5, 19.3, 1.5], 0.7, ''],
                  'l_thumb3_adjust_ctl'      : [[12, 19.3, 1.5], 0.7, ''],
                  'l_thumb4_adjust_ctl'      : [[12.5, 19.3, 1.4], 0.7, '']  
                }

indexPlaceLocs = {'l_index1_adjust_ctl'      : [[10, 20.2, 0], 0.7, ''],
                  'l_index2_adjust_ctl'      : [[12, 20.2, 0], 0.7, ''],
                  'l_index3_adjust_ctl'      : [[13, 20.1, 0], 0.7, ''],
                  'l_index4_adjust_ctl'      : [[13.5, 20, 0], 0.7, ''],
                  'l_index5_adjust_ctl'      : [[14, 19.9, 0], 0.7, '']
                }

middlePlaceLocs = {'l_middle1_adjust_ctl'      : [[10, 20.2, -0.5], 0.7, ''],
                  'l_middle2_adjust_ctl'      : [[12, 20.2, -1], 0.7, ''],
                  'l_middle3_adjust_ctl'      : [[13, 20.1, -1], 0.7, ''],
                  'l_middle4_adjust_ctl'      : [[13.5, 20, -1], 0.7, ''],
                  'l_middle5_adjust_ctl'      : [[14, 19.9, -1], 0.7, '']
                }

ringPlaceLocs = {'l_ring1_adjust_ctl'      : [[10, 20.2, -1], 0.7, ''],
                  'l_ring2_adjust_ctl'      : [[12, 20.2, -1.5], 0.7, ''],
                  'l_ring3_adjust_ctl'      : [[13, 20.1, -1.5], 0.7, ''],
                  'l_ring4_adjust_ctl'      : [[13.5, 20, -1.5], 0.7, ''],
                  'l_ring5_adjust_ctl'      : [[14, 19.9, -1.5], 0.7, '']
                }

pinkyPlaceLocs = {'l_pinky1_adjust_ctl'      : [[10, 20.2, -1.5], 0.7, ''],
                  'l_pinky2_adjust_ctl'      : [[12, 20.2, -2], 0.7, ''],
                  'l_pinky3_adjust_ctl'      : [[13, 20.1, -2], 0.7, ''],
                  'l_pinky4_adjust_ctl'      : [[13.5, 20, -2], 0.7, ''],
                  'l_pinky5_adjust_ctl'      : [[14, 19.9, -2], 0.7, '']
                }