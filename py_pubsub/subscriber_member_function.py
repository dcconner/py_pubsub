# Copyright 2016 Open Source Robotics Foundation, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import rclpy
from rclpy.node import Node
from rclpy.duration import Duration

from std_msgs.msg import String


class MinimalSubscriber(Node):

    def __init__(self):
        super().__init__('minimal_subscriber')
        self.subscription = self.create_subscription(
            String,
            'topic',
            self.listener_callback,
            10)
        self.subscription  # prevent unused variable warning

    def toggle_listening(self):
        if self.subscription is not None:
            self.get_logger().info(f" toggle listener : destroy existing subscription ...")
            self.destroy_subscription(self.subscription)
            self.subscription = None
        else:
            self.get_logger().info(f" toggle listener : renew subscription ...")
            self.subscription = self.create_subscription(
                String,
                'topic',
                self.listener_callback,
                10)

    def listener_callback(self, msg):
        self.get_logger().info('I heard: "%s"' % msg.data)
        #self.get_clock().sleep_for(Duration(seconds=0.5))
        #self.get_logger().info('       : "%s" after sleep' % msg.data)


def main(args=None):
    rclpy.init(args=args)

    minimal_subscriber = MinimalSubscriber()
    executor = rclpy.executors.MultiThreadedExecutor(num_threads=2)
    executor.add_node(minimal_subscriber)

    start = minimal_subscriber.get_clock().now()
    minimal_subscriber.get_logger().info(f" start time = {start}")
    while rclpy.ok():
        if minimal_subscriber.get_clock().now() - start > rclpy.duration.Duration(seconds=0.5):
            minimal_subscriber.toggle_listening()
            start = minimal_subscriber.get_clock().now()

        else:
            executor.spin_once(timeout_sec=0.01)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    minimal_subscriber.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
