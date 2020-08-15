from gameController import *
import sys
import getopt


def read_txt(path):
    f = open(path)

    line1 = f.readline().rstrip("\n")
    list1 = line1.split(" ")
    n, m = int(list1[0]), int(list1[1])
    main_matrix = np.zeros((n, m))

    for i in range(n):
        line = f.readline().rstrip("\n")
        list = line.split(" ")
        for j in range(m):
            main_matrix[i, j] = int(list[j])

    list2 = (f.readline().rstrip("\n")).split(" ")

    pacman_coordinate = ((int(list2[0]), int(list2[1])))
    return n, m, main_matrix, pacman_coordinate


def main(argv):
    input_file = ''
    output_file = ''
    flag = [0, 0]
    level = 1
    try:
        opts, args = getopt.getopt(
            argv, "hi:o:l:", ["ifile=", "ofile=", "level="])
    except getopt.GetoptError:
        print('pacman.py -i <input_file> -o <output_file>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('pacman.py -i <input_file> -o <output_file>')
            sys.exit()
        elif opt in ("-i", "--ifile"):
            input_file = arg
            flag[0] = 1
        elif opt in ("-o", "--ofile"):
            output_file = arg
            flag[1] = 1
        elif opt in ("-l", "--level"):
            level = arg

    import os
    THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
    path = "../random_map/Maze-15_3.txt"
    if flag[0]:
        input_file = os.path.join(THIS_FOLDER, input_file)
        path = input_file
    if flag[1]:
        out_file = os.path.join(THIS_FOLDER, output_file)
    n, m, main_matrix, pacman_coordinate = read_txt(path)
    game = GameController(main_matrix, pacman_coordinate)
    game.StartGame(int(level))


if __name__ == "__main__":
    main(sys.argv[1:])
