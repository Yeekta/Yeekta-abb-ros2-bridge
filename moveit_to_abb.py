import rclpy
from rclpy.node import Node
from moveit_msgs.msg import DisplayTrajectory
from abb_robot_msgs.srv import SetRAPIDSymbol
from abb_robot_msgs.msg import RAPIDSymbolPath
import math

class MoveItToABB(Node):
    def __init__(self):
        super().__init__('moveit_to_abb')
        
        
        self.subscription = self.create_subscription(
            DisplayTrajectory,
            '/display_planned_path',
            self.listener_callback,
            10)
            
        
        self.client = self.create_client(SetRAPIDSymbol, '/rws/set_rapid_symbol')
        
        
        while not self.client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Waiting for /rws/set_rapid_symbol service...')

    def listener_callback(self, msg):
        if not msg.trajectory:
            return
            
        self.get_logger().info("New path received from MoveIt! Processing...")
        
        
        final_point = msg.trajectory[0].joint_trajectory.points[-1]
        joints_rad = final_point.positions
        
        
        j_deg = [math.degrees(j) for j in joints_rad]
        
        
        rapid_target = f"[[{j_deg[0]:.2f}, {j_deg[1]:.2f}, {j_deg[2]:.2f}, {j_deg[3]:.2f}, {j_deg[4]:.2f}, {j_deg[5]:.2f}], [9E9, 9E9, 9E9, 9E9, 9E9, 9E9]]"
        
        
        target_path = RAPIDSymbolPath(task="T_ROB1", module="ROS_Bridge", symbol="ros_target")
        flag_path = RAPIDSymbolPath(task="T_ROB1", module="ROS_Bridge", symbol="move_flag")

    
        def handle_response(future, variable_name):
            try:
                response = future.result()
                self.get_logger().info(f"Reply for '{variable_name}': Code={response.result_code}, Message='{response.message}'")
            except Exception as e:
                self.get_logger().error(f"Service call failed for '{variable_name}': {e}")

        
        req_joints = SetRAPIDSymbol.Request(path=target_path, value=rapid_target)
        future_joints = self.client.call_async(req_joints)
        future_joints.add_done_callback(lambda f: handle_response(f, "ros_target"))
        
       
        req_flag = SetRAPIDSymbol.Request(path=flag_path, value="TRUE")
        future_flag = self.client.call_async(req_flag)
        future_flag.add_done_callback(lambda f: handle_response(f, "move_flag"))
        
        self.get_logger().info(f"Command Sent! Target Degrees: {j_deg[0]:.1f}, {j_deg[1]:.1f}, {j_deg[2]:.1f}...")

def main():
    rclpy.init()
    node = MoveItToABB()
    print("Bridge Script with Error Logging Running. Waiting for MoveIt plans...")
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()
