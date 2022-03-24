# -*- coding:utf8 -*-
# rosbridge_websocket client

import time
import sys
from roslibpy import Message, Ros, Topic

def mainloop( host, port, topic_name ):
    # roscoreを実行しているサーバーへ接続
    ros_client = Ros( host, port )

    # right, up, left, down
    xy_command_list = [[0.5, 0], [0.0, 0.5], [-0.5, 0],  [0, -0.5] ]
    n_command = len(xy_command_list)
    repeat_times = 4 # repeat the same command to move farther

    # Publishするtopicを指定
    publisher = Topic(ros_client, topic_name, 'geometry_msgs/Twist')
    def start_sending():
        i = 0
        while True:
            if not ros_client.is_connected:
                break

            for j in range(repeat_times):
                # set command
                linear_x = xy_command_list[i][0]
                linear_y = xy_command_list[i][1]        

                # 送信するTwistメッセージの内容
                publisher.publish(Message({
                    'linear': {
                        'x': linear_x,
                        'y': linear_y,
                        'z': 0
                    },
                    'angular': {
                        'x': 0,
                        'y': 0,
                        'z': 0
                    }
                }))
                time.sleep(1) # 2 Hz ?

            i = (i+1) % n_command

        publisher.unadvertise()
    # Publish開始
    ros_client.on_ready(start_sending, run_in_thread=True)
    ros_client.run_forever()

if __name__ == '__main__':
    topic_name = sys.argv[1]

    #host = '192.168.100.40'
    host = '192.168.1.107'
    port = 9090

    mainloop( host, port, topic_name )
