# Rubik's Cube CLI Simulator

## Description

This is a Python command-line interface (CLI) Rubik's Cube simulator that allows you to simulate and solve Rubik's Cubes of any size. The cube is represented in the console as an unfolded cube, and you can interact with it using simple commands.

## Features

- **Customizable Cube Size**: Simulate a Rubik's Cube of any size (e.g., 2x2x2, 3x3x3, 4x4x4, etc.).
- **Random Shuffle**: Specify the number of iterations to shuffle the cube for a varied challenge.
- **Interactive Controls**: Rotate individual faces or the entire cube using intuitive commands.
- **Console Visualization**: View the cube's unfolded representation directly in the console.

## Installation

### Prerequisites

- Python 3.x installed on your system.

### Steps

1. **Clone the Repository**

      git clone https://github.com/yourusername/your-repo-name.git
   

2. **Navigate to the Project Directory**

      cd your-repo-name
   

3. **Run the Simulator**

      python main.py
   

## Usage

### Main Menu

Upon running the simulator, you'll be greeted with the main menu:


You are in the main menu. What would you like to do?
Type 'exit' to quit
Type 'help' for this message
Type 'start' to start the game
More details are available in game help


- **Type start** to begin a new game.
- **Type help** to view the help message.
- **Type exit** to quit the simulator.

### Starting a New Game

After selecting start, you'll proceed to the game setup:

1. **Select Cube Size**

   You'll be prompted to enter the size of the cube (e.g., 3 for a standard 3x3x3 cube).

2. **Set Shuffle Iterations**

   Next, specify the number of iterations to shuffle the cube. A higher number increases the scramble complexity.

### Game Controls

Control the cube using simple commands:

#### Face Rotation Commands

- **Rotate Left Face**

  - Clockwise: Type l
  - Counter-clockwise: Type L

- **Rotate Right Face**

  - Clockwise: Type r
  - Counter-clockwise: Type R

- **Rotate Up Face**

  - Clockwise: Type u
  - Counter-clockwise: Type U

- **Rotate Down Face**

  - Clockwise: Type d
  - Counter-clockwise: Type D

- **Rotate Front Face**

  - Clockwise: Type f
  - Counter-clockwise: Type F

#### Whole Cube Rotation Commands

- **Using Numpad Keys** (if available):

  - Rotate Up: Press 8
  - Rotate Left: Press 4
  - Rotate Down: Press 2
  - Rotate Right: Press 6

#### Advanced Rotation (For Larger Cubes)

For cubes larger than 3x3x3, you can rotate specific slices using the following command format:


<rotation_type> <direction> <index>


- **rotation_type**:

  - 0 for horizontal rotation
  - 1 for vertical rotation
  - 2 for front rotation (only affects the front layer; index is not needed)

- **direction**:

  - 0 for clockwise rotation
  - 1 for counter-clockwise rotation

- **index**:

  - The index of the slice to rotate (from 0 to size - 1)
  - Indices go from left to right and top to bottom

**Examples:**

- Rotate the second horizontal slice clockwise:

  
  0 0 1
  

- Rotate the first vertical slice counter-clockwise:

  
  1 1 0
  

- Rotate the front layer clockwise:

  
  2 0
  

### Exiting the Game

- **Type exit** at any prompt to quit the game and return to the main menu.

## Contributing

Contributions are welcome! If you have suggestions or improvements, feel free to open an issue or submit a pull request.

### Steps to Contribute

1. **Fork the Repository**

2. **Create a New Branch**

   bash
   git checkout -b feature/YourFeature
   

3. **Commit Your Changes**

   bash
   git commit -m "Add your message here"
   

4. **Push to Your Branch**

   bash
   git push origin feature/YourFeature
   `

5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contact

For questions or feedback, please contact your-email@example.com.

---

Enjoy solving the Rubik's Cube from your console!

Context: [ p:410 c:2660 t:3070 ]

© GPT-o1-preview