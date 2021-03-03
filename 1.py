
import numpy as np
import math


def get_input():
    print('\nFollowing transformations can be performed:')
    print('1. Rotation about x-axis')
    print('2. Rotation about y-axis')
    print('3. Rotation about z-axis')
    print('4. Translation about x-axis')
    print('5. Translation about y-axis')
    print('6. Translation about z-axis')

    rot_x = int(input('\nEnter angle to rotate x-axis (in degrees): '))
    rot_x = math.pi/180*rot_x
    rot_y = int(input('Enter angle to rotate y-axis (in degrees): '))
    rot_y = math.pi/180*rot_y
    rot_z = int(input('Enter angle to rotate z-axis (in degrees): '))
    rot_z = math.pi/180*rot_z

    trans_x = int(input('Enter translation from x-axis: '))
    trans_y = int(input('Enter translation from y-axis: '))
    trans_z = int(input('Enter translation from z-axis: '))

    frame_known = ''
    while frame_known != 'a' and frame_known != 'b':
        frame_known = input('Point is known in frame? (A/B): ').lower()
        if frame_known != 'a' and frame_known != 'b':
            print('Two frames are \'A\' or \'B\'')

    initial_coordinates = np.array(list(
        map(int, input('\nEnter position of the point in the frame: ').split())))

    return initial_coordinates, calc(rot_x, rot_y, rot_z, trans_x, trans_y, trans_z, frame_known)


def calc(rot_x, rot_y, rot_z, trans_x, trans_y, trans_z, frame_known):
    rx = np.array([[1, 0, 0],
                   [0, math.cos(rot_x), -math.sin(rot_x)],
                   [0, math.sin(rot_x), math.cos(rot_x)]])

    ry = np.array([[math.cos(rot_y), 0, math.sin(rot_y)],
                   [0, 1, 0],
                   [-math.sin(rot_y), 0, math.cos(rot_y)]])

    rz = np.array([[math.cos(rot_z), -math.sin(rot_z), 0],
                   [math.sin(rot_z), math.cos(rot_z), 0],
                   [0, 0, 1]])

    r = rz @ ry @ rx

    if frame_known == 'a':
        d = np.array([[trans_x], [trans_y], [trans_z]])
        temp = -r.T@d
        temp = np.vstack((temp, [1]))

        prod = np.hstack(
            (np.vstack((r.T, np.array([0, 0, 0]))), temp))

        return prod

    elif frame_known == 'b':
        d = np.array([[trans_x], [trans_y], [trans_z], [1]])

        prod = np.hstack(
            (np.vstack((r, np.array([0, 0, 0]))), d))

        return prod


def transform(initial_coordinates, prod):
    initial_coordinates = np.hstack((initial_coordinates, 1))
    final_coordinates = prod@initial_coordinates

    return final_coordinates[:3]


def print_final_answer(final_coordinates):
    print('\nPosition of the point in other frame is: ({}, {}, {})'.format(
          final_coordinates[0], final_coordinates[1], final_coordinates[2]))


if __name__ == '__main__':
    initial_coordinates, prod = get_input()
    final_coordinates = transform(initial_coordinates, prod)
    print_final_answer(final_coordinates)