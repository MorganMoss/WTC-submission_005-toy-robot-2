import math

class ToyRobot:
    """
    An instance of this class is a robot that can be 
    controlled via commands and sends messages to the console.
        * Only robot_... methods should be called outside the class
    """
    def robot_say_message(self, message:str, name:str = "", end:str = "\n"):
        """
        Robot Sends message to console.

        Args:
            message (str): The text the robot sends to the console.
            name (str, optional): show robot name before message. 
            Defaults to empty string.
            end (str, optional): string appended after the last value. 
            Defaults to newline.
        """
        print(f"{name}: {message}" if name != "" else f"{message}" , end=end) 


    def robot_report_position(self):
        """
        Makes robot send a message displaying its current position.
        """
        self.robot_say_message(
            f" > {self.name} " +
            f"now at position {str(self.position).replace(' ', '')}.")


    def valid_move(self, steps:int): 
        """
        Checks if the move ends in a valid area.

        Args:
            steps (int): The distance the robot moves.

        Returns:
            bool: False if invalid move.
            tuple: The new position if valid move.
        """
        new_position = (
                (self.position[0] \
                + steps*round(math.sin(math.radians(self.rotation)))),
                (self.position[1] \
                + steps*round(math.cos(math.radians(self.rotation)))))
        if (self.bounds[0][0] <= new_position[0] <= self.bounds[0][1]) \
        and (self.bounds[1][0] <= new_position[1] <= self.bounds[1][1]):
            return new_position
        self.robot_say_message(
            "Sorry, I cannot go outside my safe zone.",
            self.name)
        return False


    def robot_move(self, steps:int):
        """
        Moves the robot and then the robot sends a message saying it has done so.

        Args:
            steps (int): The distance the robot moves.
                * Positive int moves forward.
                * Negative int moves back.

        Returns:
            bool: True if move was successful.
        """
        new_position = self.valid_move(steps)

        if new_position:
            self.position = new_position
            direction = "forward" if steps >= 0 else "back"
            self.robot_say_message(
                f" > {self.name} moved {direction} by {abs(steps)} steps.")
            return True
        return False
            

    def robot_get_name(self):
        """
        Sets robots name to a given input.
        """
        self.robot_say_message("What do you want to name your robot? ", end="")
        self.name = input()


    def command_valid(self, command:list):
        """
        Checks if the input is valid and has the correct arguments.
            * If the input has more than the required arguments,
            the remainder is ignored.

            * Converts the command list into desired types in 
            the process of checking.

            * Robot sends appropriate error messages.

        Args:
            command (list): contains a command then arguments as strings.

        Returns:
            list: contains a valid uppercase command 
            and the necessary arguments in their correct types
            if the input was valid.
            bool: False when the command or arguments are invalid
        """
        if command[0].upper() not in self.command_dict:
            self.robot_say_message(
                f"Sorry, I did not understand '{' '.join(command)}'.", self.name)
            return False
        command[0] = command[0].upper()
        command_reqs = self.command_dict[command[0]][2]
        if command_reqs != [None]:
            #if it needs more arguments
            if len(command) != len(command_reqs) + 1:
                self.robot_say_message(" ".join([
                        f"Sorry, '{command[0]}'",
                        f"needs {len(command_reqs)}",
                        "arguments"]),
                        self.name)
                return False
            for index, arg_type in enumerate(command_reqs):
                try:
                    command[index +1] = arg_type(command[index+1])
                except:
                    self.robot_say_message(" ".join([
                        f"Sorry, '{command[index+1]}'",
                        f"needs to be of type '{arg_type().__class__.__name__}\
                        '"]),
                        self.name)
                    return False
        return command


    def robot_get_command(self):
        """
        Continuosly asks for a valid command until one is given.

        Returns:
            list: contains a valid uppercase command 
            and the necessary arguments in their correct types.
        """
        self.robot_say_message("What must I do next? ", self.name, end="")
        command = self.command_valid(input().split(" "))
        if not command:
            return self.robot_get_command()
        return [command[0].upper(), *command[1:]] \
                if len(command) > 1 else command


    def command_forward(self, steps:int):
        """
        Moves robot forward and displays appropriate messages.

        Args:
            steps (int): The distance the robot moves.
        """
        self.robot_move(abs(steps))
        self.robot_report_position()
        

    def command_back(self, steps:int):
        """
        Moves robot back and displays appropriate messages.

        Args:
            steps (int): The distance the robot moves.
        """
        self.robot_move(-abs(steps))
        self.robot_report_position()


    def command_turn_right(self, degrees:int = 90):
        """
        Rotates robot 90° to the right
        and displays appropriate messages.

        Args:
            degrees (int): The amount the robot turns in degrees. 
            Defaults to 90.
        """
        self.rotation += degrees
        while self.rotation >= 360:  
            self.rotation -= 360

        self.robot_say_message(
            f" > {self.name} turned right.")
        self.robot_report_position()


    def command_turn_left(self, degrees:int = 90):
        """
        Rotates robot 90° to the left
        and displays appropriate messages.

        Args:
            degrees (int): The amount the robot turns in degrees. 
            Defaults to 90.
        """
        self.rotation -= degrees
        while self.rotation < 0:  
            self.rotation += 360

        self.robot_say_message(
            f" > {self.name} turned left.")
        self.robot_report_position()


    def command_sprint(self, steps:int):
        """
        Recursively moves the robot.

        Args:
            steps (int): The ditance the robot moves.
        """
        if steps != 0 and self.robot_move(steps):
            self.command_sprint(steps + (-1 if steps > 0 else 1))
        else:
            self.robot_report_position()


    def command_off(self):
        """
        Exits and displays appropriate message.
        """
        self.robot_say_message("Shutting down..", self.name)
        raise SystemExit
        

    def command_help(self):
        """
        Robot displays a detailed list of all the commands available.
        """
        self.robot_say_message("I can understand these commands:")
        for key, value in self.command_dict.items():
            #test_main is stupid
            spaces = "  " if key == "OFF" else " " if key == "HELP" else "\t"
            self.robot_say_message(f"{key}{spaces}- {value[0]}")


    def robot_execute_command(self, command:list):
        """
        Executes a specific command available to the robot

        Args:
            command (list): contains a valid uppercase command 
            and the necessary arguments in their correct types.
        """
        self.command_dict[command[0]][1](
            *command[1:] if self.command_dict[command[0]][1] != [None] else None)
            
    
    def __init__(self, name:str = "", position:tuple = (0,0),
                 rotation:int = 0) -> None:
        """
        Constructor that sets the default values for the robot
        when a new instance of it is created.

        Args:
            name (str, optional): Robot's name. Defaults to "".
            position (tuple, optional): Starting position. Defaults to (0,0).
            rotation (int, optional): Starting direction. Defaults to 0.
        """
        self.bounds = ((-100, 100), (-200, 200))
        self.position = position
        self.rotation = rotation
        self.name = name
        self.command_dict = {
        "OFF"       : ("Shut down robot",
                        self.command_off ,
                        [None]),
        "HELP"      : ("provide information about commands", 
                        self.command_help, 
                        [None]),
        "FORWARD"   : ("Move robot foward by [number] steps", 
                        self.command_forward, 
                        [int]),
        "BACK"      : ("Move robot back by [number] steps", 
                        self.command_back, 
                        [int]),
        "RIGHT"      : ("Rotate robot right", 
                        self.command_turn_right, 
                        [None]),    
        "LEFT"      : ("Rotate robot left", 
                        self.command_turn_left, 
                        [None]),
        "SPRINT"   : ("Move robot foward by [number] steps", 
                        self.command_sprint, 
                        [int]),               
        }


def robot_start():
    """This is the entry function, do not change"""
    robot = ToyRobot()
    robot.robot_get_name()
    robot.robot_say_message("Hello kiddo!", robot.name)
    command = [""]
    while True: 
        command = robot.robot_get_command()
        try:
            robot.robot_execute_command(command)
        except SystemExit:
            break


if __name__ == "__main__":
    robot_start()
