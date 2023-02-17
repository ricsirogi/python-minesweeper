import tkinter as tk
import random
import time
import json
import math

random.seed(time.time())
data_path = "GitHub\python-minesweeper\data.json"
class Window:
    def __init__(self):
        with open(data_path, "r") as i:
            self.data = json.load(i)
            custom = self.data.get("difficulties")
            
        self.last_difficulty = self.data.get("difficulty") # the difficulty selected when the game was last played
        self.last_custom_difficulty = self.data.get("custom_difficulty") # the custom difficulty selected when the game was last played
        self.win = tk.Tk()
        self.starting_frame = tk.Frame(self.win)
        self.game_frame = tk.Frame(self.win)
        self.custom_frame = tk.Frame(self.starting_frame)
        self.start = tk.Button(self.starting_frame, text="start", command=lambda: self.start_func())
        
        self.difficulty_button = tk.Button(self.starting_frame, text=f"difficulty: {self.last_difficulty}", command=lambda: self.difficulty_cycle())
        self.starting_frame.grid(row=0, column=0)
        self.start.grid(row=0, column=0)
        self.difficulty_button.grid(row=0, column=1)

        self.custom_mines_entry = tk.Entry(self.custom_frame)
        self.custom_row_entry = tk.Entry(self.custom_frame)
        self.custom_column_entry = tk.Entry(self.custom_frame)
        self.custom_mines_label = tk.Label(self.custom_frame, text="Mines: ")
        self.custom_row_label = tk.Label(self.custom_frame, text="Rows: ")
        self.custom_column_label = tk.Label(self.custom_frame, text="Columns: ")
        self.custom_mines_label.grid(row=0, column=2)
        self.custom_mines_entry.grid(row=0, column=3)
        self.custom_row_label.grid(row=0, column=4)
        self.custom_row_entry.grid(row=0, column=5)
        self.custom_column_label.grid(row=0, column=6)
        self.custom_column_entry.grid(row=0, column=7)
        self.custom_mines_entry.insert(0, custom["custom"][0])
        self.custom_row_entry.insert(0, custom["custom"][1])
        self.custom_column_entry.insert(0, custom["custom"][2])

        self.difficulty = self.data.get("difficulty")
        if self.difficulty == "custom":
            self.custom_frame.grid(row=0, column=2)

        self.reset_button = tk.Button(self.game_frame, text="😀", command=lambda:self.start_func())
        self.main_menu_button = tk.Button(self.game_frame, text="🏠", command=lambda:self.main_menu_func())
        self.mines_label = tk.Label(self.game_frame, text="000")
        self.time_label = tk.Label(self.game_frame, text="000")

        self.rows = -1
        self.columns = -1
        self.mines = -1
        self.tiles = []
        self.mine_index_list = []
        self.mine_list = []
        self.left_side_tile_index_list = []
        self.right_side_tile_index_list = []
        self.button_font_size = 6
        self.first_click = True
        self.discovered_tiles = 0
        self.game_end = False


    def difficulty_cycle(self):
        if self.difficulty == "begginer":
            self.difficulty = "intermediate"
            self.difficulty_button["text"] = "difficulty: intermediate"
        elif self.difficulty == "intermediate":
            self.difficulty = "expert"
            self.difficulty_button["text"] = "difficulty: expert"
        elif self.difficulty == "expert":
            self.difficulty = "custom"
            self.difficulty_button["text"] = "difficulty: custom"
            self.custom_frame.grid(row=0, column=2)
        elif self.difficulty == "custom":
            self.custom_frame.grid_forget()
            self.difficulty = "begginer"
            self.difficulty_button["text"] = "difficulty: begginer"

    def main_menu_func(self):
        self.game_frame.grid_forget()
        self.starting_frame.grid(row=0, column=0)

    def start_func(self):

        # assign the value of th rows, columns an mines
        if self.difficulty != "custom":
            self.mines = self.data.get("difficulties").get(self.difficulty)[0]
            self.rows = self.data.get("difficulties").get(self.difficulty)[1]
            self.columns = self.data.get("difficulties").get(self.difficulty)[2]
        else:
            if not self.custom_column_entry.get().isdigit() or not self.custom_row_entry.get().isdigit() or not self.custom_mines_entry.get().isdigit():
                return print("Error: Invalid custom column or custom row or custom mine")
            self.mines = int(self.custom_mines_entry.get())
            self.rows = int(self.custom_row_entry.get())
            self.columns = int(self.custom_column_entry.get())

        if self.columns < 7:
            self.columns = 7
            print("Warining: Columns didn't exceed the minimum requirement (7), defaulting to 7")
        if self.rows * self.columns-9 < self.mines:
            return print("Error: Too many mines!")

        self.first_click = True
        self.mine_index_list  = []
        self.mine_list = []
        for i in self.tiles:
            i.destroy()
        self.tiles = []
        self.left_side_tile_index_list =  []
        self.right_side_tile_index_list = []
        self.discovered_tiles = 0
        self.game_end = False
        self.reset_button.config(text="😀")

        temp = 0
        if self.mines < 10:
            temp = "00" + str(self.mines)
        elif self.mines < 100:
            temp = "0" + str(self.mines)
        else:
            temp = str(self.mines)
        
        self.mines_label["text"] = temp

        # update the latest difficulty in data.json
        temp = self.data
        temp["difficulty"] = self.difficulty
        with open(data_path, "w") as i:
            if self.difficulty == "custom":
                temp["difficulties"]["custom"] = [self.mines, self.rows, self.columns]
            json.dump(temp, i)

        self.starting_frame.grid_forget()
        self.game_frame.grid(row=0, column=0)

        # generate all the tiles
        a = 0
        for i in range(self.rows):
            self.left_side_tile_index_list.append(a)
            for j in range(self.columns):
                tile = tk.Label(self.game_frame, width=5, height=2, bg="#fffdb8", borderwidth=1, relief="solid", 
                                #font=("", self.button_font_size),
                                  text="")
                tile.grid(row=i + 1, column=j)
                self.tiles.append(tile)
                if j == self.columns - 1:
                    self.right_side_tile_index_list.append(a)
                self.tiles[a].bind("<Button-1>", lambda event, tile_type="blank", tile_index=a: self.tile_press(tile_type, tile_index))
                a += 1

        if self.columns % 2 == 1:
            self.reset_button.grid(row=0, column=int(math.floor(self.columns/2)))
        else:
            self.reset_button.grid(row=0, column=int(self.columns/2-1), columnspan=2)
        self.mines_label.grid(row=0, column=0, columnspan=2)
        self.time_label.grid(row=0, column=self.columns-2, columnspan=2)
        self.main_menu_button.grid(row=0, column=2)


    def generate_mines(self, tile_index):

        # get the position of the tiles surrounding the pressed tile
        positions = self.check_surrounding_tiles(tile_index)

        # generate the position of the mines
        while len(self.mine_index_list) < self.mines:
            num = random.randint(0, (self.rows * self.columns)-1)

            # make sure, that the generated mine positions is
            #    not already a mine position   | not the pressed tile | not around the pressed tile
            if num not in self.mine_index_list and num != tile_index and num not in positions:
                self.mine_index_list.append(num)

        # assign the function of each tile (a tile is either mine or blank)
        for i in range(self.rows * self.columns):
            if i in self.mine_index_list:
                self.tiles[i].bind("<Button-1>", lambda event, tile_type="mine", tile_index=i: self.tile_press(tile_type, tile_index))
            else:
                self.tiles[i].bind("<Button-1>", lambda event, tile_type="blank", tile_index=i: self.tile_press(tile_type, tile_index))
            
            # make each tile clickable with MB2 and MB3 to flag it
            self.tiles[i].bind("<Button-2>", lambda event, tile_type="flag", tile_index=i: self.tile_press(tile_type, tile_index))
            self.tiles[i].bind("<Button-3>", lambda event, tile_type="flag", tile_index=i: self.tile_press(tile_type, tile_index))
        for i in self.mine_index_list:
            self.mine_list.append(self.tiles[i])

    def check_surrounding_tiles(self, tile_index):
        positions = [] # the positions of the surrounding tiles

        # by default, every position is -1
        for i in range(8):
            positions.append(-1)

        for i in range(3):

                # if we're checking the left column, an the presse tile is on the left side, then continue
                if i == 0 and (tile_index in self.left_side_tile_index_list): 
                    continue
                # if we're checking the right column, an the presse tile is on the right side, then continue
                elif i == 2 and (tile_index in self.right_side_tile_index_list):
                    continue
                
                # get the position of the tile above, middle, and below of the currrently checked column 
                up = tile_index - self.columns - 1 + i 
                middle = tile_index - 1 + i
                down = tile_index + self.columns - 1 + i

                #! Above row check
                # if the clicked tile is on the top row, it doesn't need to check the row above it
                if tile_index >= self.columns:
                    if i == 0:
                        replace = 0
                        positions.pop(replace)
                        positions.insert(replace, up)
                    elif i == 1:
                        replace = 3
                        positions.pop(replace)
                        positions.insert(replace, up)
                    elif i == 2:
                        replace = 5
                        positions.pop(replace)
                        positions.insert(replace, up)

                #! Middle row check
                # if i == 1, that means that it tries to check itself, which is not neccessary
                if i != 1:
                    if i == 0:
                        replace = 1
                        positions.pop(replace)
                        positions.insert(replace, middle)
                    elif i == 1:
                        pass
                    elif i == 2:
                        replace = 6
                        positions.pop(replace)
                        positions.insert(replace, middle)
                
                #! Bottom row check
                # if the clicked tile is on the bottom row, it doesn't need to check the row below it
                if tile_index <= (self.columns * self.rows) - self.columns - 1:
                    if i == 0:
                        replace = 2
                        positions.pop(replace)
                        positions.insert(replace, down)
                    elif i == 1:
                        replace = 4
                        positions.pop(replace)
                        positions.insert(replace, down)
                    elif i == 2:
                        replace = 7
                        positions.pop(replace)
                        positions.insert(replace, down)

        return positions


    def tile_press(self, tile_type, tile_index):
        """
        positions:

        [0][3][5]
        [1][X][6] = [0][1][2][3][X][4][5][6][7]
        [2][4][7]
        """

        # on the first click of the game, generate the mines
        if self.first_click:
            self.generate_mines(tile_index)
            self.first_click = False

        if self.tiles[tile_index]["state"] == "disabled":
            
            # if the tile is pressed automatically, then return
            if tile_type == "auto_blank":
                return
            
            mines = 0
            flags = 0
            positions = self.check_surrounding_tiles(tile_index)

            for i in positions:
                if self.tiles[i] in self.mine_list:
                    mines += 1
                if self.tiles[i]["text"] == "⚑":
                    flags += 1

            if mines == flags:
                for i in positions:
                    if self.tiles[i]["text"] != "⚑":
                        if i in self.mine_index_list:
                            self.tile_press("mine", i)
                        else:
                            self.tile_press("auto_blank", i)

        if tile_type == "mine":
            self.game_end = True

            for i in self.tiles:
                i.config(state="disabled")
        
            self.reset_button.config(text="🙁")

            for i in self.mine_list:
                i.config(bg="red")
                if i["text"] != "⚑":
                    i.config(text="💣")

        # When the user clicks on a tile with MB2 or MB3
        elif tile_type == "flag":
            temp = int(self.mines_label["text"])
            if self.tiles[tile_index]["text"] == "⚑":
                self.tiles[tile_index]["text"] = ""
                temp += 1
                if temp < 10:
                    temp = "00" + str(temp)
                elif temp < 100:
                    temp = "0" + str(temp)
                else:
                    temp = str(temp)
            elif self.tiles[tile_index]["state"] != "disabled":
                self.tiles[tile_index].config(text="⚑")
                temp -= 1
                if temp < 10:
                    temp = "00" + str(temp)
                elif temp < 100:
                    temp = "0" + str(temp)
                else:
                    temp = str(temp)
            self.mines_label["text"] = temp

        elif tile_type == "blank" or tile_type == "auto_blank":
            
            # if the game has ended, then don't let the player press any more tiles
            if self.game_end:
                return
            
            mines = 0
            blank_tiles_index_list = [] # temporarily stores the index of the blank tiles around a clicked blank tile
            # search for mines around the pressed tile
            positions = self.check_surrounding_tiles(tile_index)

            for i in positions:
                if i == -1:
                    continue
                if self.tiles[i] in self.mine_list:
                    mines += 1
                else:
                    if i not in blank_tiles_index_list:
                        blank_tiles_index_list.append(i)

            self.color_tile(tile_index, mines)
            self.tiles[tile_index].config(text=f"{mines}", state="disabled", bg="#E9E9E9")

            self.discovered_tiles += 1
            if mines == 0:
                self.tiles[tile_index].config(text=f"", state="disabled")
                for i in blank_tiles_index_list:
                    self.tile_press("auto_blank", i)
            
        else:
            print("ERROR: Invalid tile type")


    def color_tile(self, tile_index, mines):
        if mines == 0:
            self.tiles[tile_index].config(disabledforeground="white")
        if mines == 1:
            self.tiles[tile_index].config(disabledforeground="blue")
        if mines == 2:
            self.tiles[tile_index].config(disabledforeground="green")
        if mines == 3:
            self.tiles[tile_index].config(disabledforeground="red")
        if mines == 4:
            self.tiles[tile_index].config(disabledforeground="purple")
        if mines == 5:
            self.tiles[tile_index].config(disabledforeground="black")
        if mines == 6:
            self.tiles[tile_index].config(disabledforeground="gray")
        if mines == 7:
            self.tiles[tile_index].config(disabledforeground="maroon")
        if mines == 8:
            self.tiles[tile_index].config(disabledforeground="turquoise")


if __name__ == '__main__':
    app = Window()
    app.win.mainloop()