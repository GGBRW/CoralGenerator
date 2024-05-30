import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

def generate_l_system(num_iterations, axiom, rules):
    current_string = axiom
    for _ in range(num_iterations):
        new_string = ""
        for character in current_string:
            new_string += rules.get(character, character)
        current_string = new_string
    return current_string

def draw_l_system(instructions, angle, length):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    stack = []
    current_position = np.array([0.0, 0.0, 0.0])
    current_direction = np.array([0, 0, 1])
    directions = {
        '+': np.array([1, 0, 0]),
        '-': np.array([-1, 0, 0]),
        '&': np.array([0, 1, 0]),
        '^': np.array([0, -1, 0]),
        '\\': np.array([0, 0, 1]),
        '/': np.array([0, 0, -1]),
    }

    for cmd in instructions:
        if cmd in ['F', 'G']:  # Move forward
            next_position = current_position + current_direction * length
            ax.plot([current_position[0], next_position[0]],
                    [current_position[1], next_position[1]],
                    [current_position[2], next_position[2]], 'k-', lw=2)
            current_position = next_position
        elif cmd == '+':  # Turn right
            rotation_matrix = _rotation_matrix(directions['+'], angle)
            current_direction = np.dot(rotation_matrix, current_direction)
        elif cmd == '-':  # Turn left
            rotation_matrix = _rotation_matrix(directions['-'], angle)
            current_direction = np.dot(rotation_matrix, current_direction)
        elif cmd == '&':  # Pitch down
            rotation_matrix = _rotation_matrix(directions['&'], angle)
            current_direction = np.dot(rotation_matrix, current_direction)
        elif cmd == '^':  # Pitch up
            rotation_matrix = _rotation_matrix(directions['^'], angle)
            current_direction = np.dot(rotation_matrix, current_direction)
        elif cmd == '\\':  # Roll right
            rotation_matrix = _rotation_matrix(directions['\\'], angle)
            current_direction = np.dot(rotation_matrix, current_direction)
        elif cmd == '/':  # Roll left
            rotation_matrix = _rotation_matrix(directions['/'], angle)
            current_direction = np.dot(rotation_matrix, current_direction)
        elif cmd == '[':  # Save state
            stack.append((current_position.copy(), current_direction.copy()))
        elif cmd == ']':  # Restore state
            current_position, current_direction = stack.pop()

    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    plt.show()

def _rotation_matrix(axis, angle):
    angle = np.radians(angle)
    axis = axis / np.sqrt(np.dot(axis, axis))
    a = np.cos(angle / 2.0)
    b, c, d = -axis * np.sin(angle / 2.0)
    aa, bb, cc, dd = a*a, b*b, c*c, d*d
    bc, ad, ac, ab, bd, cd = b*c, a*d, a*c, a*b, b*d, c*d
    return np.array([[aa+bb-cc-dd, 2*(bc+ad), 2*(bd-ac)],
                     [2*(bc-ad), aa+cc-bb-dd, 2*(cd+ab)],
                     [2*(bd+ac), 2*(cd-ab), aa+dd-bb-cc]])

# Example usage
axiom = "F"
rules = {
    "F": "F[+F]F[-F]F"
}
angle = 25.7
length = 1.0

# Generate the L-system instructions
instructions = generate_l_system(4, axiom, rules)

# Draw the L-system
draw_l_system(instructions, angle, length)

