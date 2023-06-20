def precompute_cumulative_sum(matrix):
    rows = len(matrix)
    cols = len(matrix[0])

    # Create a cumulative sum matrix with an extra row and column of zeros
    cumulative_sum = [[0] * (cols + 1) for _ in range(rows + 1)]

    # Compute cumulative sums
    for i in range(1, rows + 1):
        for j in range(1, cols + 1):
            # Calculate the cumulative sum using the formula:
            # sum = top + left - diagonal + current_value
            cumulative_sum[i][j] = (
                cumulative_sum[i - 1][j] + cumulative_sum[i][j - 1] - cumulative_sum[i - 1][j - 1] + matrix[i - 1][j - 1]
            )

    return cumulative_sum


def calc_sum(row_index1, row_index2, column_index1, column_index2, cumulative_sum):
    # Calculate the sum of the submatrix using the precomputed cumulative sum matrix
    # Formula: sum_submatrix = SAT[r+1][s+1] - SAT[p][s+1] - SAT[r+1][q] + SAT[p][q]
    return (
        cumulative_sum[row_index2 + 1][column_index2 + 1]
        - cumulative_sum[row_index2 + 1][column_index1]
        - cumulative_sum[row_index1][column_index2 + 1]
        + cumulative_sum[row_index1][column_index1]
    )


matrix = [
    [0, 2, 5, 4, 1],
    [4, 8, 2, 3, 7],
    [6, 3, 4, 6, 2],
    [7, 3, 1, 8, 3],
    [1, 5, 7, 9, 4],
]
p, q = 1, 1
r, s = 3, 3

# Check if p, q, r, s are valid indices
if p < 0 or p >= len(matrix) or q < 0 or q >= len(matrix[0]) or r < 0 or r >= len(matrix) or s < 0 or s >= len(matrix[0]):
    print("Invalid submatrix coordinates!")
else:
    # Precompute the cumulative sum matrix
    cumulative_sum = precompute_cumulative_sum(matrix)

    # Calculate the sum of the submatrix using the cumulative sum matrix
    submatrix_sum = calc_sum(p, r, q, s, cumulative_sum)

    # Print the result
    print(submatrix_sum)