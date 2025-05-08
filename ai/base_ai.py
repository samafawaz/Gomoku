class BaseAI:
    def __init__(self, color):
        self.color = color

    def get_move(self, grid):
        """
        Should return (row, col)
        """
        raise NotImplementedError
