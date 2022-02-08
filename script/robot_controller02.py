# rosbridge_tcp json client
import socket
import json
import sys, time

def make_message(twist, topic_name):
    return json.dumps(dict(op='publish',
                        topic=topic_name,
                        msg=twist))

def make_twist(x_lin, y_lin, z_lin, x_ang, y_ang, z_ang):
    return dict(linear=dict(x=x_lin, y=y_lin, z=z_lin),
                angular=dict(x=x_ang, y=y_ang, z=z_ang))

def mainloop( topic_name ):
    # right, up, left, down 
    xy_command_list = [[0.5, 0], [0.0, 0.5], [-0.5, 0],  [0, -0.5] ]
    n_command = len(xy_command_list)

    repeat_times = 6 # repeat the same command to move farther
    i = 0
    while True:
        for j in range(repeat_times):
            # set command
            linear_x = xy_command_list[i][0]
            linear_y = xy_command_list[i][1]

            twist = make_twist(linear_x, linear_y, 0.0, 0.0, 0.0, 0.0)            
            message = make_message(twist, topic_name)

            sock.send(message.encode('utf-8'))
            time.sleep(0.5) # 2 Hz ?

        i = ( i + 1 ) % n_command
    
    # stop robot
    twist = make_twist(0.0, 0.0, 0.0, 0.0, 0.0, 0.0)
    message = make_message(twist, topic_name)
    sock.send(message)
    
    sock.close()

if __name__ == '__main__':
    topic_name = sys.argv[1]

    host = '192.168.1.107'  # IP address (Jetson)
    port = 9090

    sock = socket.socket()
    sock.connect((host, port))

    mainloop( topic_name )
