POS_LASTSETPOINT = 2706
POS_CURRENTANGLE=2830
POS_DELTAPHI=2954
POS_DAYMAXANGLE=3078
POS_DAYMINANGLE=3202
POS_MAXLASTMOTORCURRENT=3330
POS_MAXLASTMOTORTORQUE=3454

layout_db110="""
                82          STW1                USINT
                83          STW2                USINT
                84.0        set_on              BOOL
                86          SetFrequ            REAL
                90          ActFrequ            REAL
                98          Speed               REAL
                102         Current             REAL
                106         Torque              REAL
                114.0       local               BOOL
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
                98              statusNumber                USINT
                102             errorCode                   INT
                104             northSensorAngle            REAL
                108             southSensorAngle            REAL
                112             TiltTwistAngle              REAL
                124             TiltSetAngle                REAL
"""
