def is_winner(grid, size, row, col):
    color = grid[row][col]
    if color is None:
        return False

    directions = [
        (1, 0),  # vertical
        (0, 1),  # horizontal
        (1, 1),  # diagonal down-right
        (1, -1)  # diagonal down-left
    ]

    for dr, dc in directions:
        count = 1
        r, c = row + dr, col + dc
        while 0 <= r < size and 0 <= c < size and grid[r][c] == color:
            count += 1
            r += dr
            c += dc

        r, c = row - dr, col - dc
        while 0 <= r < size and 0 <= c < size and grid[r][c] == color:
            count += 1
            r -= dr
            c -= dc

        if count >= 5:
            return True

    return False


def is_draw(grid):
    for row in grid:
        if None in row:
            return False
    return True
