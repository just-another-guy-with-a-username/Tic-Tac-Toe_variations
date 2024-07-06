class Move():
    def __init__(self, i, j, type, num):
        self.cell_one = [i, j]
        self.cell_two = []
        self.type = type
        self.num = num
        self.final_state = None

    def get_cell_two(self, i, j):
        self.cell_two = [i, j]

    def final_statef(self, decider):
        if decider:
            self.final_state = self.cell_one
        else:
            self.final_state = self.cell_two
        self.cell_one = None
        self.cell_two = None
