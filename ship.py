class Ship:
    def make_occup_list(self):
        count = 0
        while True:
            if self.orientation != 'v':
                self.occup.append((self.row_idx, self.col_idx + count))
            else:
                self.occup.append((self.row_idx + count, self.col_idx))
            count += 1
            print(self.occup)
            if len(self.occup) == self.size:
                break

    def __init__(self, **kwargs):
        self.orientation = None
        self.col_idx = None
        self.row_idx = None
        self.occup = []
        for key, value in kwargs.items():
            setattr(self, key, value)
