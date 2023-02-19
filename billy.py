import math
from PIL import Image, ImageDraw, ImageFont
import sys

class Playground():
    def __init__(self, n = 1):
        self.n = n
        self.grid = [["NO MOVE"] * n for _ in range(n)]
        self.START = [(1, 1), (n, n)]
        self.debug = False

    def __repr__(self):
        board = []
        for x in range(self.n):
            row = []
            for y in range(self.n):
                row.append(self.grid[y][x])
            board.append(row)
        board = board[::-1]
        k = {
            "LEFT": "<",
            "RIGHT": ">",
            "UP": "⌃",
            "DOWN": "v",
            "NO MOVE": "*",
            "BILLY": "B"
        }
        s = '\n'.join([' | '.join(k[c] for c in row) for row in board])
        return f"{s}\n{' | '.join([str(i) for i in range(1, self.n + 1)])}"

    def fetch(self, x, y):
        if x == 0 and y == 1:
            return "RIGHT"
        elif x > self.n or y > self.n or x < 1 or y < 1:
            return "NO MOVE"
        else:
            return self.grid[x - 1][y - 1]

    def set(self, x, y, move):
        move = move.upper()
        if move in ["LEFT", "RIGHT", "UP", "DOWN", "NO MOVE", "BILLY"]:
            self.grid[x - 1][y - 1] = move
        else:
            raise ValueError("Invalid move. Must be one of: LEFT, RIGHT, UP, DOWN, NO MOVE, BILLY")

    @staticmethod
    def from_file(file="billy.txt"):
        with open(file, "r") as f:
            lines = f.readlines()
            n = len(lines[0].split())
            if n != len(lines):
                raise ValueError("Invalid board. Must be square.")
            p = Playground(n)
            k = {
                "<": "LEFT",
                ">": "RIGHT",
                "^": "UP",
                "v": "DOWN",
                "*": "NO MOVE",
                "B": "BILLY"
            }
            for y, line in enumerate(lines[::-1]):
                for x, move in enumerate(line.split()):
                    p.set(x + 1, y + 1, k[move])
            return p

    def to_image(self, file="billy_answer.jpg"):
        # Create new image
        img = Image.new('RGB', (self.n * 100, self.n * 100), color = 'white')
        d = ImageDraw.Draw(img)
        # Draw grid
        for x in range(0, self.n * 100, 100):
            d.line((x, 0, x, self.n * 100), fill=(0, 0, 0), width=2)
        for y in range(0, self.n * 100, 100):
            d.line((0, y, self.n * 100, y), fill=(0, 0, 0), width=2)

        # Draw moves
        for y in range(self.n):
            for x in range(self.n):
                move = self.grid[x][self.n - y - 1]
                if move == "LEFT":
                    d.text((x * 100 +40, y * 100 +35), "←", fill=(0, 0, 0), font=ImageFont.truetype("SF-Pro-Display-Regular.otf", 25))
                elif move == "RIGHT":
                    d.text((x * 100 +40, y * 100 +35), "→", fill=(0, 0, 0), font=ImageFont.truetype("SF-Pro-Display-Regular.otf", 25))
                elif move == "UP":
                    d.text((x * 100 +40, y * 100 +35), u"↑", fill=(0, 0, 0), font=ImageFont.truetype("SF-Pro-Display-Regular.otf", 25))
                elif move == "DOWN":
                    d.text((x * 100 +40, y * 100 +35), "↓", fill=(0, 0, 0), font=ImageFont.truetype("SF-Pro-Display-Regular.otf", 25))
                elif move == "NO MOVE":
                    d.rectangle((x * 100 + 2, y * 100 + 2, x * 100 +99, y * 100 +99), fill=(100, 100, 100))
                elif move == "BILLY":
                    d.text((x * 100 +40, y * 100 +35), "B", fill=(0, 0, 0), font=ImageFont.truetype("SF-Pro-Display-Regular.otf", 25))

        # Save image
        img.save(file)


    def set_debug(self, debug):
        self.debug = debug

    def subdivide(self, n, coordinates, shrinkage = 2):
        n_prime = math.ceil(n * (1/shrinkage))
        divisions = []

        y_span = coordinates[0][1]
        for _ in range(shrinkage):
            x_span = coordinates[0][0]
            for _ in range(shrinkage):
                x_coord = (
                    x_span,
                    x_span + n_prime - 1
                ) if x_span + n_prime - 1 <= coordinates[1][0] else (coordinates[1][0] - n_prime + 1, coordinates[1][0])
                y_coord = (
                    y_span,
                    y_span + n_prime - 1
                ) if y_span + n_prime - 1 <= coordinates[1][1] else (coordinates[1][1] - n_prime + 1, coordinates[1][1])
                divisions.append(((x_coord[0], y_coord[0]), (x_coord[1], y_coord[1])))
                x_span = x_span + n_prime + 1
            y_span = y_span + n_prime + 1
        return (divisions, n_prime)

    def get_bounding_box(self, n, coordinates):
        boundary_cells = []
        coordinates = list(coordinates)
        if coordinates[0] == (1,1):
            boundary_cells.append((0, 1))
        if self.debug:
            print(f"Coordinates: {coordinates}")
        boundary_box_coordinates = (
            (coordinates[0][0] - 1, coordinates[0][1] - 1),
            (coordinates[1][0] + 1, coordinates[1][1] + 1)
        )
        boundary_box_size = n + 2
        if self.debug:
            print(f"Boundary box size: {boundary_box_size} => {boundary_box_coordinates}")
        for x in range(boundary_box_coordinates[0][0], boundary_box_coordinates[1][0] + 1):
            if (x <= 0 or x > self.n):
                continue
            for y in range(boundary_box_coordinates[0][1], boundary_box_coordinates[1][1] + 1):
                if y <= 0 or y > self.n:
                    continue
                if (x < coordinates[0][0] or x > coordinates[1][0]) or (y < coordinates[0][1] or y > coordinates[1][1]):
                    boundary_cells.append((x, y))
        return boundary_cells

    class Visits():
        def __init__(self):
            self.ins = 0
            self.outs = 0

        def __repr__(self):
            return "ins: {}, outs: {}".format(self.ins, self.outs)

        def is_here(self):
            return self.ins > self.outs

    def has_left(self, x, y, quad_coords):
        m = self.fetch(x, y)
        if m == "LEFT" and (x == quad_coords[0][0]):
            return 1
        elif m == "RIGHT" and (x == quad_coords[1][0]):
            return 1
        elif m == "UP" and (y == quad_coords[1][1]):
            return 1
        elif m == "DOWN" and (y == quad_coords[0][1]):
            return 1
        return 0

    def has_entered(self, x, y, quad_coords):
        m = self.fetch(x, y)
        xp, yp = x + 1 if m == "RIGHT" else x - 1 if m == "LEFT" else x, y + 1 if m == "UP" else y - 1 if m == "DOWN" else y
        if xp >= quad_coords[0][0] and xp <= quad_coords[1][0] and yp >= quad_coords[0][1] and yp <= quad_coords[1][1]:
            return 1
        return 0


    def count_visits(self, quad_coords, boundary_cells):
        visits = self.Visits()
        checked = set()
        # count entries
        for x, y in boundary_cells:
            visits.ins += self.has_entered(x, y, quad_coords)
        # count exits
        for x in range(quad_coords[0][0], quad_coords[1][0] + 1):
            for y in [quad_coords[0][1], quad_coords[1][1]]:
                if (x, y) not in checked:
                    k = visits.outs
                    checked.add((x, y))
                    if self.debug:
                        print(f"Checking ({x}, {y}), move is {self.fetch(x, y)}")
                    visits.outs += self.has_left(x, y, quad_coords)
                    if self.debug and k != visits.outs:
                        print(f"({x}, {y}) has left")
        for y in range(quad_coords[0][1], quad_coords[1][1] + 1):
            for x in [quad_coords[0][0], quad_coords[1][0]]:
                if (x, y) not in checked:
                    checked.add((x, y))
                    k = visits.outs
                    if self.debug:
                        print(f"Checking ({x}, {y}), move is {self.fetch(x, y)}")
                    visits.outs += self.has_left(x, y, quad_coords)
                    if self.debug and k != visits.outs:
                        print(f"({x}, {y}) has left")
        return visits

    def find_billy(self):
        return self.__find_billy(self.n, self.START)

    def xf(self, n, coordinates):
        return self.__find_billy(n, coordinates)

    def __find_billy(self, n, coordinates):
        # base case n < 4
        if n <= 2:
            if self.debug:
                print(f"Checking {coordinates} for Billy at n={n}")
            # return coordinate of billy
            for x in range(coordinates[0][0], coordinates[1][0] + 1):
                for y in range(coordinates[0][1], coordinates[1][1] + 1):
                    if self.fetch(x, y) == "BILLY":
                        return f"Billy is at ({x}, {y})"
            return False

        # Inductive Step
        quads, n_prime = self.subdivide(n, coordinates)
        for quad in quads:
            if self.debug:
                print(f"Checking {quad} for Billy at n={n} (n'={n_prime})")
            boundary_cells = self.get_bounding_box(n_prime, quad)
            v = self.count_visits(quad, boundary_cells)
            if self.debug:
                print(f"Boundary cells: {boundary_cells}")
                print(f"Visits: {v}")
            if v.ins - v.outs < 0:
                raise Exception("Invalid state: more exits than entries")
            if v.is_here():
                if self.debug:
                    print(f"Found Billy at {quad} at n={n} (n'={n_prime})")
                    print("-----------------------------------------------------")
                return self.__find_billy(n_prime, quad)
            if self.debug:
                print(f"Did not find Billy at {quad} at n={n} (n'={n_prime})")
                print("-----------------------------------------------------")
        return False

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 billy.py <input_file>")
        sys.exit(1)

    pg = Playground.from_file(sys.argv[1])
    print(pg)
    print(pg.find_billy())
    pg.to_image(sys.argv[1].split(".")[0] + ".png")

if __name__ == "__main__":
    main()