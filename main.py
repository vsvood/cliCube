from enum import Enum
import random
import time

def hline(size: int):
    return (("+" + "-" * size) * 4 + "+")

class BasicDirections(Enum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3

class FaceEnum(Enum):
    U = 0
    L = 1
    F = 2
    R = 3
    B = 4
    D = 5

class Direction(Enum):
    CLOCKWISE = 0
    COUNTER_CLOCKWISE = 1

    def reversed(self):
        if self == Direction.CLOCKWISE:
            return Direction.COUNTER_CLOCKWISE
        return Direction.CLOCKWISE

class Slice:
    def __init__(self, size: int, left: list, bottom: list, right: list, up: list, face: list = None):
        self.size = size
        self.face = face
        self.ring = [left, bottom, right, up]

    def _rotate_face(self, direction: Direction):
        """
        Rotates the face of the slice in the specified direction.

        Args:
            direction (Direction): The direction to rotate the face. It can be
                                either Direction.CLOCKWISE or Direction.COUNTER_CLOCKWISE.

        The method first flips the face elements horizontally and then transposes
        the face matrix for a clockwise rotation. For a counter-clockwise rotation,
        it first flips the face elements vertically and then transposes the face matrix.
        """
        if direction == Direction.CLOCKWISE:
            for i in range(self.size):
                for j in range(self.size // 2):
                    self.face[j][i][0], self.face[self.size - 1 - j][i][0] = \
                        self.face[self.size - 1 - j][i][0], self.face[j][i][0]
            for i in range(self.size):
                for j in range(i + 1, self.size):
                    self.face[i][j][0], self.face[j][i][0] = self.face[j][i][0], self.face[i][j][0]
        elif direction == Direction.COUNTER_CLOCKWISE:
            for i in range(self.size):
                for j in range(self.size // 2):
                    self.face[i][j][0], self.face[i][self.size - 1 - j][0] = \
                        self.face[i][self.size - 1 - j][0], self.face[i][j][0]
            for i in range(self.size):
                for j in range(i + 1, self.size):
                    self.face[i][j][0], self.face[j][i][0] = self.face[j][i][0], self.face[i][j][0]

    def rotate(self, direction: Direction):
        """
        Rotate the slice in the specified direction.

        If the slice has a face, then it rotates the face of the slice in the
        specified direction. Then it rotates the ring of the slice in the same
        direction.

        Args:
            direction (Direction): The direction to rotate the slice. It can be
                                either Direction.CLOCKWISE or Direction.COUNTER_CLOCKWISE.
        """
        if direction == Direction.CLOCKWISE:
            if self.face:
                self._rotate_face(direction)
            for i in range(self.size):
                self.ring[0][i][0], self.ring[1][i][0], self.ring[2][i][0], self.ring[3][i][0] = \
                    self.ring[1][i][0], self.ring[2][i][0], self.ring[3][i][0], self.ring[0][i][0]
        elif direction == Direction.COUNTER_CLOCKWISE:
            if self.face:
                self._rotate_face(direction)
            for i in range(self.size):
                self.ring[0][i][0], self.ring[1][i][0], self.ring[2][i][0], self.ring[3][i][0] = \
                    self.ring[3][i][0], self.ring[0][i][0], self.ring[1][i][0], self.ring[2][i][0]


class Face:
    def __init__(self, size: int, face: list):
        self.size = size
        self.face = face

    def get_horizontal(self, idx: int, reverse: bool = False):
        if reverse:
            return [self.face[idx][self.size - 1 - i] for i in range(self.size)]
        return [self.face[idx][i] for i in range(self.size)]
    
    def get_vertical(self, idx: int, reverse: bool = False):
        if reverse:
            return [self.face[self.size - 1 - i][idx] for i in range(self.size)]
        return [self.face[i][idx] for i in range(self.size)]
    

class RotationType(Enum):
    HORIZONTAL = 0
    VERTICAL = 1
    FRONT = 2



class RubicCube:
    colors = ["\033[37mu\033[0m", "\033[32ml\033[0m", "\033[36mf\033[0m", "\033[34mr\033[0m", "\033[35mb\033[0m", "\033[33md\033[0m"]
    def __init__(self, size: int):
        self.size = size
        self.cube = []
        for color in RubicCube.colors:
            self.cube.append([])
            for _ in range(size):
                self.cube[-1].append([])
                for _ in range(size):
                    self.cube[-1][-1].append([color])

        left_face = Face(size, self.cube[1])
        right_face = Face(size, self.cube[3])
        front_face = Face(size, self.cube[2])
        back_face = Face(size, self.cube[4])
        up_face = Face(size, self.cube[0])
        down_face = Face(size, self.cube[5])

        self.front_slice = Slice(size,
                           left_face.get_vertical(-1, reverse=True),
                           down_face.get_horizontal(0, reverse=True),
                           right_face.get_vertical(0),
                           up_face.get_horizontal(-1),
                           self.cube[2])
        self.vectical_slices = []
        for i in range(size):
            if i < (self.size + 1) // 2:
                self.vectical_slices.append(
                    Slice(
                        size,
                        back_face.get_vertical(self.size - 1 - i, reverse=True),
                        down_face.get_vertical(i),
                        front_face.get_vertical(i),
                        up_face.get_vertical(i),
                    )
                )
            else:
                self.vectical_slices.append(
                    Slice(
                        size,
                        front_face.get_vertical(i),
                        down_face.get_vertical(i),
                        back_face.get_vertical(self.size - 1 - i, reverse=True),
                        up_face.get_vertical(i),
                    )
                )
        self.vectical_slices[0].face = self.cube[1]  # left face
        self.vectical_slices[-1].face = self.cube[3]  # right face

        self.horizontal_slices = []
        for i in range(size):
            if i < (self.size + 1) // 2:
                self.horizontal_slices.append(
                    Slice(
                        size,
                        left_face.get_horizontal(i),
                        front_face.get_horizontal(i),
                        right_face.get_horizontal(i),
                        back_face.get_horizontal(i),
                    )
                )
            else:
                self.horizontal_slices.append(
                    Slice(
                        size,
                        left_face.get_horizontal(i),
                        back_face.get_horizontal(i),
                        right_face.get_horizontal(i),
                        front_face.get_horizontal(i),
                    )
                )
        self.horizontal_slices[0].face = self.cube[0]  # up face
        self.horizontal_slices[-1].face = self.cube[5]  # down face


    def __str__(self):
        empty = ' ' * self.size
        result = hline(self.size) + '\n'
        for i in range(self.size):
            result += '|' + empty + \
                      '|' + ''.join(color[0] for color in self.cube[0][i]) + \
                      '|' + empty + \
                      '|' + empty + \
                      '|\n'
        result += hline(self.size) + '\n'
        for i in range(self.size):
            result += '|' + ''.join(color[0] for color in self.cube[1][i]) + \
                      '|' + ''.join(color[0] for color in self.cube[2][i]) + \
                      '|' + ''.join(color[0] for color in self.cube[3][i]) + \
                      '|' + ''.join(color[0] for color in self.cube[4][i]) + \
                      '|\n'
        result += hline(self.size) + '\n'
        for i in range(self.size):
            result += '|' + empty + \
                      '|' + ''.join(color[0] for color in self.cube[5][i]) + \
                      '|' + empty + \
                      '|' + empty + \
                      '|\n'
        result += hline(self.size) + '\n'
        return result
    
    def rotate(self, rotation_type: RotationType, direction: Direction, index = None):
        rotation_type = RotationType(rotation_type)
        direction = Direction(direction)
        if rotation_type == RotationType.HORIZONTAL:
            if index is None:
                for i in range(self.size):
                    if i < (self.size + 1) // 2:
                        self.horizontal_slices[i].rotate(direction)
                    else:
                        self.horizontal_slices[i].rotate(direction.reversed())
            else:
                self.horizontal_slices[index].rotate(direction)
        elif rotation_type == RotationType.VERTICAL:
            if index is None:
                for i in range(self.size):
                    if i < (self.size + 1) // 2:
                        self.vectical_slices[i].rotate(direction)
                    else:
                        self.vectical_slices[i].rotate(direction.reversed())
            else:
                self.vectical_slices[index].rotate(direction)
        elif rotation_type == RotationType.FRONT:
            self.front_slice.rotate(direction)

    def shuffle(self, iterations = 100):
        for _ in range(iterations):
            self.rotate(random.randint(0, 1), random.randint(0, 1), random.randint(0, self.size - 1))

    def is_solved(self):
        for i in range(6):
            for j in range(self.size):
                for k in range(self.size):
                    if self.cube[i][j][k][0] != self.cube[i][0][0][0]:
                        return False
        return True
    

def print_help_main_menu():
    help_message = """
You are in the main menu. What would you like to do?
Type 'exit' to quit
Type 'help' for this message
Type 'start' to start the game
More details are available in game help
"""
    print(help_message)

def print_help_game():
    help_message = """
You are in the game menu. What would you like to do?
Type 'exit' to quit
Type 'help' for this message
You will be asked to select the size of the cube
After that you will be asked about number of iterations to shuffle the cube
Provide this numbers and the game will start

In game you will use the following commands format:

rotate left, right, up, down, front respectively:
l, r, u, d, f
lowercase for clockwise, uppercase for counter clockwise

also you can use 8, 4, 2, 6 to rotate the whole cube
(it is convinient if you have keyboard with numpad)

for cubes with higher sizes you can use index of the slice to rotate

<rotation_type> <direction> <index>

 - rotation_type:
    0 for horizontal,
    1 for vertical,
    2 for front (only the front layer, dont take index)

 - direction:
    0 for clockwise,
    1 for counter clockwise

 - index: index of the slice to rotate, could be from 0 to size - 1
    index goes from left to right, top to bottom
    skip index if you want to rotate the whole cube
"""
    for line in help_message.splitlines():
        print(line)
        time.sleep(0.05)

def game():
    print("Lets play Rubik's Cube!")
    print()
    print_help_game()
    print()
    print("select the size of the cube")
    user_input = input()
    while True:
        while not user_input.isdigit():
            if user_input == 'exit':
                print("You will be returned to the main menu")
                return
            elif user_input == 'help':
                print_help_game()
            else:
                print("Invalid input")
            print("select the size of the cube")
            user_input = input()

        size = int(user_input)
        if size < 2:
            print ("Size must be at least 2, try again")
        else:
            break
        user_input = input()

    rubic = RubicCube(size)
    print("select the number of iterations to shuffle the cube")
    user_input = input()
    while True:
        while not user_input.isdigit():
            if user_input == 'exit':
                print("You will be returned to the main menu")
                return
            elif user_input == 'help':
                print_help_game()
            else:
                print("Invalid input")
            print("select the number of iterations to shuffle the cube")
            user_input = input()

        iterations = int(user_input)
        if iterations < 0:
            print ("Iterations must be at least 0, try again")
        else:
            break

    rubic.shuffle(iterations)

    print("Here is THE CUBE!!!")
    print()
    print(rubic)

    user_input = input()
    while user_input != 'exit':
        print(user_input)
        if user_input == 'help':
            print_help_game()
        elif user_input.lower() in ['u', 'l', 'f', 'r', 'd', '8', '4', '2', '6']:
            if user_input.islower():
                direction = Direction.CLOCKWISE
            else:
                direction = Direction.COUNTER_CLOCKWISE
            user_input = user_input.lower()
            if user_input == 'u':
                rubic.rotate(RotationType.HORIZONTAL, direction, 0)
            elif user_input == 'l':
                rubic.rotate(RotationType.VERTICAL, direction, 0)
            elif user_input == 'f':
                rubic.rotate(RotationType.FRONT, direction)
            elif user_input == 'r':
                rubic.rotate(RotationType.VERTICAL, direction, -1)
            elif user_input == 'd':
                rubic.rotate(RotationType.HORIZONTAL, direction, -1)
            elif user_input == '8':
                rubic.rotate(RotationType.VERTICAL, Direction.COUNTER_CLOCKWISE)
            elif user_input == '4':
                rubic.rotate(RotationType.HORIZONTAL, Direction.CLOCKWISE)
            elif user_input == '2':
                rubic.rotate(RotationType.VERTICAL, Direction.CLOCKWISE)
            elif user_input == '6':
                rubic.rotate(RotationType.HORIZONTAL, Direction.COUNTER_CLOCKWISE)
            print(rubic)

            if rubic.is_solved():
                print("You won!")
                break
        else:
            try:
                rubic.rotate(*map(int, user_input.split()))
                print(rubic)

                if rubic.is_solved():
                    print("You won!")
                    break
            except Exception:
                print("Invalid input")
        user_input = input()

    print("You will be returned to the main menu")
    

if __name__ == "__main__":
    greeting = """
   _.--""--._
 .'          '.
/   O      O   \\
|   \  ^^  /   |
\   '-----'   /
 '. _______ .'
   //_____\\\\
  (( ____ ))
   ''-----''

Welcome to CLI Rubik's Cube!  Get ready to solve it!
"""
    for line in greeting.splitlines():
        print(line)
        time.sleep(0.05) # Adds a slight pause for dramatic effect

    print("Type 'exit' to quit")
    print("Type 'help' for help")
    print("Type 'start' to start the game")

    user_input = input()
    while user_input != 'exit':
        if user_input == 'help':
            print_help_main_menu()
        elif user_input == 'start':
            game()
        else:
            print("Invalid command")
        user_input = input()