# NESTED LISTS

basic_grid = [[0 for _ in range(5)] for _ in range(5)]
grid = [[0,0,3,0],  # Each purple bracket on a new line is a row
        [0,1,1,0],  # Each number in a purple bracket is a column index
        [1,1,0,0],
        [0,2,0,0],]

for row in grid:
    strrow = [str(x) for x in row]
    print("|".join(strrow))
    print("-------")


def sum_cols_rows(grid):
    row_sums = [0,0,0,0]
    col_sums = [0,0,0,0]
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            col_sums[j] += grid[i][j]
            row_sums[i] += grid[i][j]
    return row_sums, col_sums

row_sums, col_sums = sum_cols_rows(grid)

print("rowsums", row_sums)
print("colsums", col_sums)

grid[1][3] = "X"
print(grid)