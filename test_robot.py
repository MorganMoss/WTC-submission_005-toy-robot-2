import math
import unittest
import robot
from io import StringIO
from test_base import captured_io

class TestRobot(unittest.TestCase):


    robby = robot.ToyRobot()


    def test_create_robot(self):
        self.assertEqual(self.robby.name, "")
        self.assertEqual(self.robby.position, (0,0))
        self.assertEqual(self.robby.rotation, 0)


    def test_robot_get_name(self):
        with captured_io(StringIO('ROBBY\n')) as (out, err):
            self.robby.robot_get_name()
        output = out.getvalue().strip()
        self.assertEqual("What do you want to name your robot?", output)
        self.assertEqual(self.robby.name, "ROBBY")
    

    def test_get_command_and_valid_command(self):
        for key, command in self.robby.command_dict.items():
            input_string = "Fail\n"
            input_string += f"{key} 1\n"
            input_string += f"{key.lower()} 1\n"
            input_string += f"{key[0]}{key[1:len(key)-1].lower()}{key[-1]} 1\n"
            input_string += f"{key[0].lower()}{key[1:len(key)-1]}{key[-1].lower()} 1\n"

            with captured_io(StringIO(input_string)) as (out, err):
                for _ in range(4):
                    if command[2] != [None]:
                        result = self.robby.robot_get_command()
                        self.assertEqual(result[0], key)
                        for i, arg in enumerate(command[2]):
                            self.assertIsInstance(result[i+1], arg)
                    else:
                        self.assertEqual(self.robby.robot_get_command()[0], key)


    def test_command_help(self):
        with captured_io(StringIO()) as (out, err):
            self.robby.robot_execute_command(["HELP"])
        output = out.getvalue().strip()

        self.assertIn(
"""I can understand these commands:
OFF  - Shut down robot
HELP - provide information about commands
FORWARD\t- Move robot foward by [number] steps
BACK\t- Move robot back by [number] steps
RIGHT\t- Rotate robot right
LEFT\t- Rotate robot left
SPRINT\t- Move robot foward by [number] steps""", output)
    

    def test_move(self):
        for angle in range(0, 271, 90):
            self.robby.rotation = angle
            angle = math.radians(angle)
            self.robby.robot_move(5)
            self.assertEqual(self.robby.position, 
                            (round(5*math.sin(angle)),round(5*math.cos(angle))))
            self.robby.position = (0,0)


    def test_turn(self):
        self.robby.rotation = 0
        self.robby.robot_execute_command(["LEFT"])
        self.assertEqual(self.robby.rotation, 270)
        self.robby.rotation = 0
        self.robby.robot_execute_command(["RIGHT"])
        self.assertEqual(self.robby.rotation, 90)

        for _ in range(3):
            self.robby.robot_execute_command(["RIGHT"])
        self.assertEqual(self.robby.rotation, 0)


    def test_command_off(self):
        with captured_io(StringIO()) as (out, err):
            try:
                self.robby.robot_execute_command(["OFF"])
            except SystemExit:
                ...
        output = out.getvalue().strip()
        self.assertEqual("Shutting down..", output)
    

        

