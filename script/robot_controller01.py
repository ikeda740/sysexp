#! /usr/bin/env python3

import rospy, sys
from geometry_msgs.msg import Twist

def mainloop( topic_name ):
    # object that publishes a topic
    twist_pub = rospy.Publisher(topic_name, Twist, queue_size=1000)

    # right, up, left, down 
    xy_command_list = [[0.5, 0], [0.0, 0.5], [-0.5, 0],  [0, -0.5] ]
    n_command = len(xy_command_list)

    # content of /cmd_vel
    twist = Twist()
    twist.linear.x = 0.0
    twist.linear.y = 0.0
    twist.linear.z = 0.0
    twist.angular.x = 0.0
    twist.angular.y = 0.0
    twist.angular.z = 0.0

    repeat_times = 6 # repeat the same command to move farther
    rate = rospy.Rate( 2 ) # 2 Hz
    i = 0
    while not rospy.is_shutdown():
        for j in range(repeat_times):
            # set command
            twist.linear.x = xy_command_list[i][0]
            twist.linear.y = xy_command_list[i][1]

            rospy.loginfo(twist)

            twist_pub.publish(twist)

            # sleep to keep 2 Hz
            rate.sleep()
        i = ( i + 1 ) % n_command

if __name__ == '__main__':
    topic_name = sys.argv[1]
    try:
        rospy.init_node('robot_controller', anonymous=True)
        mainloop( topic_name )
    except rospy.ROSInterruptException: pass
