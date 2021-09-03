class c_packet_type:
    PACKET_HEARTBEAT=0
    PACKET_ROTATION=1
    PACKET_GYRO=2
    PACKET_HANDSHAKE=3
    PACKET_ACCEL=4
    PACKET_MAG=5
    PACKET_RAW_CALIBRATION_DATA=6
    PACKET_CALIBRATION_FINISHED=7
    PACKET_CONFIG=8
    PACKET_RAW_MAGENTOMETER=9
    PACKET_PING_PONG=10
    PACKET_SERIAL=11
    PACKET_BATTERY_LEVEL=12
    PACKET_TAP=13
    PACKET_RESET_REASON=14
    PACKET_SENSOR_INFO=15
    PACKET_ROTATION_2=16
    PACKET_ROTATION_DATA=17
    PACKET_MAGENTOMETER_ACCURACY=18
    
    PACKET_RECIEVE_HEARTBEAT=1
    PACKET_RECIEVE_VIBRATE=2
    PACKET_RECIEVE_HANDSHAKE=3
    PACKET_RECIEVE_COMMAND=4

    COMMAND_CALLIBRATE=1
    COMMAND_SEND_CONFIG=2
    COMMAND_BLINK=3
class c_packets:
    eight_zero=bytearray([0]*8)
class c_misc:
    target_port=6969
class sensor:
    DATA_TYPE_CORRECTION=2
    DATA_TYPE_NORMAL=1