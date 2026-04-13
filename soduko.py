#Definition of constants
NOT_FINISH = "NOT_FINISH"
FINISH_SUCCESS = "FINISH_SUCCESS"
FINISH_FAILURE = "FINISH_FAILURE"
FINISH_NOT_LEGIT="FINISH_NOT_LEGIT"
#Helper function 1
def options (sudoku_board:list, loc:tuple)->list or None:
    #Check if a filled cell was selected
    if sudoku_board[loc[0]][loc[1]]!=-1:
        return []
    option=[1,2,3,4,5,6,7,8,9]
    #Check rows and columns
    for i in range (9):
        if (sudoku_board[i][loc[1]]!=-1) and (sudoku_board[i][loc[1]] in option):
            option.remove(sudoku_board[i][loc[1]])
        if (sudoku_board[loc[0]][i]!=-1) and (sudoku_board[loc[0]][i] in option):
            option.remove(sudoku_board[loc[0]][i])
    #Check box
    for c in range (3):
        for r in range (3):
            col =((loc[0]//3)*3)+c
            row =((loc[1]//3)*3)+r
            if (sudoku_board[col][row]!=-1) and (sudoku_board[col][row] in option):
                option.remove((sudoku_board[col][row]))
    #If the array became completely empty, there are no suitable options, return NONE
    if len(option)==0:
        return None
    else:
        return option#Return the relevant options

#Helper function 2
def possible_digits(sudoku_board:list[list]):
    #Build matrix
    possible_list=[]
    for row in range(9):
        row_list = []
        for column in range(9):
            row_list.append(options(sudoku_board, (row, column)))   #Insert the values into the matrix
        possible_list.append(row_list)

    return possible_list

#Helper function 3
def one_stage (sudoku_board:list[list],possibilities:list[list[list]] or list[list[None]])-> tuple and str or str:
    global y_min, x_min
    for c in range (9):
        for r in range (9):
            #Check whether the initial board is solvable from the start
            if possibilities[c][r] is None:
                return FINISH_FAILURE
            # Check the validity of the given board
            for i in range (9):
                if (sudoku_board[c][r]==sudoku_board[c][i]!=-1) and (r!=i):
                    return FINISH_NOT_LEGIT
                if (sudoku_board[c][r]==sudoku_board[i][r]!=-1) and (c!=i):
                    return FINISH_NOT_LEGIT
            for i in range (3):
                for j in range (3):
                    row = ((r // 3) * 3) + i
                    col = ((c // 3) * 3) + j
                    if (-1!=sudoku_board[c][r]==sudoku_board[col][row]) and ((c!=col) or (r!=row)):
                        return FINISH_NOT_LEGIT

    #Perform the action until there are no arrays with only one option
    do_it_again=True
    while do_it_again:
        for r in range (9):
            for c in range (9):
                #Check whether the sudoku is unsolvable
                if possibilities[c][r] is None:
                    return FINISH_FAILURE
                #Remove cells with one matching value and update the matrices
                if len(possibilities[r][c])==1:
                    sudoku_board[r][c]=possibilities[r][c][0]
                    #Remove the number from the column and row
                    for i in range (9):
                        if (possibilities[r][c][0] in possibilities[r][i]) and (c!=i):
                            possibilities[r][i].remove(possibilities[r][c][0])
                        if (possibilities[r][c][0] in possibilities[i][c]) and (r!=i):
                            possibilities[i][c].remove(possibilities[r][c][0])
                    # Remove the number from the box
                    for i in range(3):
                        for j in range(3):
                            row = ((r // 3) * 3) + i
                            col = ((c // 3) * 3) + j
                            if (possibilities[r][c][0] in possibilities[row][col]) and (r != row or c != col):
                                possibilities[row][col].remove(possibilities[r][c][0])

                    possibilities[r][c]=[]
        #Check whether there are still cells with only one optional number
        counter = 0
        for i in range(9):
            for j in range(9):
                if len(possibilities[i][j]) == 1:
                    counter += 1
        if counter == 0:
            do_it_again = False
    # Find the minimum, without considering the empty cells
    minimum = 10
    for i in range(9):
        for j in range(9):
            if 0 < len(possibilities[i][j]) < minimum:
                x_min = i
                y_min = j
                minimum = len(possibilities[i][j])
    if minimum==10:
        return FINISH_SUCCESS
    else:
        return (x_min,y_min),NOT_FINISH
#Helper function 4
def fill_board(sudoku_board: list[list], possibilities: list[list]):
    while (one_stage(sudoku_board, possibilities) != FINISH_FAILURE) and (
            one_stage(sudoku_board, possibilities) != FINISH_SUCCESS) and (
            one_stage(sudoku_board, possibilities) != FINISH_NOT_LEGIT):

        row = int(one_stage(sudoku_board, possibilities)[0][0])
        column = int(one_stage(sudoku_board, possibilities)[0][1])
        print("Choose a number from the following options:")
        print(possibilities[row][column])

        num = input()  # Get input
        again = False

        # If the input is not a number
        if not num.isdigit():
            again = True
        else:
            num = int(num)  # Convert the input to an integer

        # Check whether the number is not among the options
        while num not in possibilities[row][column] or again:
            print("The number you chose is not in the options, please choose a number from the options:")
            print(possibilities[row][column])
            num = input()  # Additional input

            if num.isdigit():
                again = False
                num = int(num)

        # Insert into the board if the input is valid
        sudoku_board[row][column] = num
        possibilities = possible_digits(sudoku_board)

    return one_stage(sudoku_board, possibilities)


#Helper function 5
def create_random_board(sudoku_board:list[list]):
    import random
    # Randomize the number of cells to be filled at the start of the game
    N = random.randint(10, 20)
    # Create a list with all possible cell coordinates
    possible_coordinate_list = [(row, column) for row in range(9) for column in range(9)]
    # Calculate initial possibilities
    possibilities = possible_digits(sudoku_board)
    # Fill N random values into the board
    for i in range(N):
        # Randomize a number between 1 and the size of the remaining coordinates list
        K = random.randint(0,len(possible_coordinate_list)-1)
        row, column = possible_coordinate_list.pop(K)
        # Calculate the options for the current cell
        list_for_coordinate_options = possibilities[row][column]
        if list_for_coordinate_options:  # If there are legal options
            random_value = random.choice(list_for_coordinate_options)  # Choose a random value
            sudoku_board[row][column] = random_value  # Insert the value into the board
            # Update the board possibilities after inserting the value
            possibilities = possible_digits(sudoku_board)

#Helper function 5
def print_board(sudoku_board:list[list]):
    for row in range(9):
        print("----------------------------")
        print("|", end="")
        for column in range(9):
            print(sudoku_board[row][column], "|", end="")
        print()
    print("----------------------------")

#Helper function 6
def print_board_to_file(sudoku_board:list[list], file_name):
    #Writes the board to a file
    with open(file_name, 'a') as f:
        for row in range(9):
            f.write("-------------------\n")
            f.write("|")
            for column in range(9):
                f.write(str(sudoku_board[row][column]) + "|")
            f.write("\n")
        f.write("-------------------\n")
#Helper function 7
def print_result_to_file(file_name ,sudoku_board:list[list],status:str):
    if status == "FINISH_SUCCESS":
        with open(file_name, "a") as f:
            f.write("Here is the solved board\n")
        print_board_to_file(sudoku_board, file_name)
    if status == "FINISH_NOT_LEGIT":
        with open(file_name, "a") as f:
            f.write("Board is not legit!\n")
    if status == "FINISH_FAILURE":
        with open(file_name, "a") as f:
            f.write("Board is unsolvable\n")

example_board = [[5,3,-1,-1,7,-1,-1,-1,-1],
 [6,-1,-1,-1,-1,-1,1,-1,-1],
 [-1,-1,9,-1,-1,-1,-1,6,-1],
 [-1,-1,-1,-1,6,-1,-1,-1,3],
 [-1,-1,-1,8,-1,3,-1,-1,1],
 [-1,-1,-1,-1,-1,-1,-1,-1,-1],
 [-1,6,-1,-1,-1,-1,-1,-1,-1],
 [-1,-1,-1,-1,1,-1,-1,-1,-1],
 [-1,-1,-1,-1,8,-1,-1,-1,9]]
perfect_board = [[5,3,4,6,7,8,9,1,2],
 [6,7,2,1,9,5,3,4,8],
 [1,9,8,3,4,2,5,6,7],
 [8,5,9,7,6,1,4,2,3],
 [4,2,6,8,5,3,7,9,1],
 [7,1,3,9,2,4,8,5,6],
 [9,6,1,5,3,7,2,8,4],
 [2,8,7,4,1,9,6,3,5],
 [3,4,5,2,8,6,1,7,9]]
impossible_board = [[5,1,6,8,4,9,7,3,2],
 [3,-1,7,6,-1,5,-1,-1,-1],
 [8,-1,9,7,-1,-1,-1,6,5],
 [1,3,5,-1,6,-1,9,-1,7],
 [4,7,2,5,9,1,-1,-1,6],
 [9,6,8,3,7,-1,-1,5,-1],
 [2,5,3,1,8,6,-1,7,4],
 [6,8,4,2,-1,7,5,-1,-1],
 [7,9,1,-1,5,-1,6,-1,8]]
bug_board = [[5,3,4,6,7,8,9,1,2],
 [6,7,2,1,9,5,3,4,9],
 [1,9,8,3,4,2,5,6,7],
 [8,5,9,7,6,1,4,2,3],
 [4,2,6,8,5,3,7,9,1],
 [7,1,3,9,2,4,8,5,6],
 [9,6,1,5,3,7,2,8,4],
 [2,8,7,4,1,9,6,3,5],
 [3,4,5,2,8,6,1,7,9]]
# This board has two solutions - one for 2 and one for 4
interesting_board = [[5,3,4,6,7,8,9,1,2],
 [6,7,2,1,9,5,3,4,8],
 [1,9,8,3,4,2,5,6,7],
 [-1,-1,-1,7,6,1,4,2,3],
 [-1,-1,-1,8,5,3,7,9,1],
 [-1,-1,-1,9,2,4,8,5,6],
 [-1,-1,-1,-1,3,7,2,8,4],
 [-1,-1,-1,-1,1,9,6,3,5],
 [-1,-1,-1,-1,8,6,1,7,9]]
board2 = [[-1,6,-1,4,3,-1,-1,-1,1],
 [5,-1,-1,-1,7,-1,-1,-1,-1],
 [-1,1,-1,9,-1,-1,8,-1,-1],
 [-1,-1,-1,-1,-1,2,3,-1,9],
 [-1,8,-1,-1,-1,-1,-1,6,-1],
 [-1,-1,-1,-1,-1,-1,-1,-1,-1],
 [-1,-1,-1,-1,-1,-1,-1,-1,-1],
 [9,-1,2,3,-1,-1,-1,-1,4],
 [-1,-1,4,7,2,-1,-1,-1,8]]
board1 = [[5,-1, 4,-1, 7,-1,-1, 1,-1],
 [6,-1, 2, 1,-1,-1, 3,-1,-1],
 [1,-1, 8,-1, 4,-1,-1, 6,-1],
 [-1, 5,-1,-1, 6,-1,-1, 2,-1],
 [-1, 2,-1, 8,-1, 3,-1,-1,-1],
 [-1,-1,-1,-1,-1, 4,-1, 5, 6],
 [-1, 6, 1, 5, 3, 7, 2, 8, 4],
 [-1, 8, 7,-1, 1, 9,-1, 3,-1],
 [-1,-1,-1, 2, 8,-1,-1,-1, 9]]



random_board = [[-1 for _ in range(9)] for _ in range(9)]
create_random_board(random_board)
output_file = "sudoku_solved.txt"
with open(output_file,"w") as f:
    f.write("the results are as follow:\n\n")
board= example_board
pos=possible_digits(board)
solved_board= fill_board(board, pos)
print_result_to_file(output_file,board,solved_board)
print("finish board 1")
#Run number 1
board= perfect_board
pos=possible_digits(board)
solved_board= fill_board(board, pos)
print_result_to_file(output_file,board,solved_board)
print("finish board 2")
#Run number 2
board= impossible_board
pos=possible_digits(board)
solved_board= fill_board(board, pos)
print_result_to_file(output_file,board,solved_board)
print("finish board 3")
#Run number 3
board= bug_board
pos=possible_digits(board)
solved_board= fill_board(board, pos)
print_result_to_file(output_file,board,solved_board)
print("finish board 4")
#Run number 4
board= interesting_board
pos=possible_digits(board)
solved_board= fill_board(board, pos)
print_result_to_file(output_file,board,solved_board)
print("finish board 5")
#Run number 5
board= random_board
pos=possible_digits(board)
solved_board= fill_board(board, pos)
print_result_to_file(output_file,board,solved_board)
print("finish board 6")
#Run number 6