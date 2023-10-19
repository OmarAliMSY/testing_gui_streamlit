#POS_LASTSETPOINT = 2706
#POS_CURRENTANGLE=2830
#POS_DELTAPHI=2954
#POS_DAYMAXANGLE=3078
#POS_DAYMINANGLE=3202
#POS_MAXLASTMOTORCURRENT=3330
#POS_MAXLASTMOTORTORQUE=3454

layout_db110="""
                82          STW1                USINT
                83          STW2                USINT
                84        set_on              BOOL
                86          SetFrequ            REAL
                90          ActFrequ            REAL
                98          Speed               REAL
                102         Current             REAL
                106         Torque              REAL
                114       local               BOOL
                124         nSoftOM             USINT
                134         phi1                REAL
                138         phi2                REAL
                142         twist_angle	        REAL"""

layout_db504_tr="""
                0           wz_adress_1          USINT
                1           tr_adress_1          USINT
                2           errorcode_1          USINT
                4           timestamp_1          DTL
                16          windvalue_1          REAL
                20          trackervalue_1       REAL
                24          wz_adress_2          USINT
                25          tr_adress_2          USINT
                26          errorcode_2          USINT
                28          timestamp_2          DTL
                40          windvalue_2          REAL
                44          trackervalue_2       REAL
                48          wz_adress_3          USINT
                49          tr_adress_3          USINT
                50          errorcode_3          USINT
                52          timestamp_3          DTL
                64          windvalue_3          REAL
                68          trackervalue_3       REAL"""

layout_db504_f="""
                0           wz_adress_1          USINT
                1           tr_adress_1          USINT
                2           timestamp_1          DTL
                14          errorcode_1          INT
                16          wz_adress_2          USINT
                17          tr_adress_2          USINT
                18          timestamp_2          DTL
                30          errorcode_2          INT
                32          wz_adress_3          USINT
                33          tr_adress_3          USINT
                34          timestamp_3          DTL
                46          errorcode_3          INT"""

layout_db511="""
                0           tr_adress            USINT
                2           errorcode            INT
                4           timestamp            DTL"""

layout_db300 = """
4 Motor_current_offset1   USINT
20  Motor_current_offset2   USINT
36  Motor_current_offset3   USINT
"""

layout_db4 = """
                4          current_position_offset1    REAL
                8          current_position_offset2    REAL
                12         current_position_offset3    REAL
"""

layout_db103 = """
                82            actualFrequency_t1         REAL
                86            current_t1                 REAL
                90            torque_t1                  REAL
                94            maxLastMotorTorque_t1      REAL
                98            statusNumber_t1            USINT
                100.0           EmergencyStop           BOOL     
                100.1           moveWithHandHeldDevice1 BOOL  
                100.2           activeHandHeldDevice    BOOL    
                100.3           moveWithHandHeldDevice2 BOOL  
                100.4           fault                   BOOL
                102           errorCode_t1               INT
                104           northSensorAngle_t1        REAL
                108           southSensorAngle_t1        REAL
                112           twistAngle_t1              REAL
                116           sensor1Offset_t1           REAL
                120           sensor2Offset_t1           REAL
                124           setAngle_t1                REAL
                128           actualeDeltaPhi             REAL
                134           actualFrequency_t2         REAL
                138           current_t2                 REAL
                142           torque_t2                  REAL
                146           maxLastMotorTorque_t2      REAL
                150           statusNumber_t2            USINT 
                152.0         EmergencyStop              BOOL
                152.1           moveWithHandHeldDevice1 BOOL   
                152.2           activeHandHeldDevice  BOOL     
                152.3           moveWithHandHeldDevice2 BOOL   
                152.4           fault                BOOL 
                154           errorCode_t2               INT   
                156           northSensorAngle_t2        REAL
                160           southSensorAngle_t2        REAL
                164           twistAngle_t2              REAL
                168           sensor1Offset_t2           REAL
                172           sensor2Offset_t2           REAL
                176           setAngle_t2                REAL
                180           actualeDeltaPhi_t2         REAL
"""


layout_db105 = """
                2              torque_abs                    REAL
                6              torque_percentage             REAL
"""


