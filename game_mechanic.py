#game_mechanic.py
#Jonathan Tang 85625237

import random

DEBUG = False

class Jewel:
    def __init__(self,color:chr,row:int,col:int,state:str):
        self.state = state
        self.color = color
        
        if self.state == "FROZEN":
            self.set_state_frozen()
        elif self.state == "IS_FALLER":
            self.set_state_is_faller()
        
        self.jewel_row = row
        self.jewel_col = col
        
    def get_color(self) -> chr:
        #Returns color of jewel as a character
        return self.color
    
    def set_state_frozen(self):
        self.state = "FROZEN"
        self.state_and_color =" "+ self.color+" "
        
    def set_state_is_faller(self):
        self.state = "IS_FALLER"
        self.state_and_color = "["+self.color+"]"

    def set_state_is_faller_not_frozen(self):
        self.state = "NOT_FROZEN_FALLER"
        self.state_and_color = "|"+self.color+"|"

    def set_state_is_match(self):
        self.state ="MATCH"
        self.state_and_color = "*"+self.color+"*"

    def get_state_and_color(self) ->str:
        return self.state_and_color

    def get_state(self) -> str:
        return self.state
    
    def set_col_pos(self,col:int):
        self.jewel_col = col
        
    def get_col_pos(self) -> int:
        #Returns column location of jewel
        return self.jewel_col

    def set_row_pos (self,row:int):
        self.jewel_row = row
        
    def get_row_pos(self) -> int:
        #Returns row location of jewel
        return self.jewel_row

    def get_col_pos_right(self) ->int:
        #Returns column position to the right
        return (self.jewel_col + 1)

    def get_col_pos_left(self) -> int:
        #Returns column position to the left
        return (self.jewel_col - 1)
    
    def get_row_pos_below(self) ->int:
        return (self.jewel_row + 1)

    def get_row_pos_above(self) ->int:
        return (self.jewel_row - 1)

class Faller:
    def __init__(self,top_color:chr,middle_color:chr,bottom_color:chr,col:int):
        #leftest column is 1
        self.col = col-1
        self.top_jewel = Jewel(top_color,-2,self.col,"IS_FALLER")
        self.middle_jewel = Jewel(middle_color,-1,self.col,"IS_FALLER")
        self.bottom_jewel = Jewel(bottom_color,0,self.col,"IS_FALLER")
        self.faller = [self.top_jewel,self.middle_jewel,self.bottom_jewel]
        self.faller_state = "IS_FALLER"
        
    def set_state_is_faller(self):
        #Sets all jewels in faller and faller itself as a faller state
        self.faller_state = "IS_FALLER"
        
        for jewel in self.faller:
            jewel.set_state_is_faller()
            
    def set_state_is_faller_not_frozen(self):
        #Sets all jewels in faller and faller itself as a faller but not frozen state
        self.faller_state = "NOT_FROZEN_FALLER"
                
        for jewel in self.faller:
            jewel.set_state_is_faller_not_frozen()

    def set_state_frozen(self):
        #Sets all jewels in faller and faller itself as a frozen state
        self.faller_state = "FROZEN"

        for jewel in self.faller:
            jewel.set_state_frozen()
                    
    def get_faller_state(self):
        #Returns the state of the faller
        return self.faller_state
    
    def get_lowest_row_pos(self):
        #Returns row position of lowest jewel in the Faller
        return self.faller[2].get_row_pos()
    
    def get_bottom_jewel(self):
        #Returns jewel that is on the bottom of faller
        return self.faller[2]

    def get_middle_jewel(self):
        #Returns jewel that is on the middle of faller
        return self.faller[1]
    
    def get_top_jewel(self):
        #Returns jewel that is on the top of faller
        return self.faller[0]
    
    def get_jewel_in_pos(self,pos:int):
        #Returns jewel in specified position of faller. 0 = top, 2 = bottom
        return self.faller[pos]
    
    def get_faller_list(self):
        #Returns list containing each jewel
        return self.faller
    
    def get_faller_height(self):
        #Returns height of the faller
        return len(self.faller)
    
    def get_faller_col(self):
        #Returns column position of column
        return self.col

    def get_col_pos_right(self):
        return self.get_bottom_jewel().get_col_pos_right()

    def get_col_pos_left(self):
        return self.get_bottom_jewel().get_col_pos_left()
    
    def set_column(self,col:int):
        #Moves postion property of faller to inputted column
        index = 0
        self.col = col
        for jewel in self.faller:
            self.faller[index].set_col_pos(col)
            index += 1
            
    def rotate(self):
        # moves bottom jewel to top and cascades rest down
        old_bottom_abs_row = self.get_bottom_jewel().get_row_pos()
        old_middle_abs_row = self.get_middle_jewel().get_row_pos()
        old_top_abs_row = self.get_top_jewel().get_row_pos()

        new_bottom_jewel = self.get_middle_jewel()
        new_middle_jewel = self.get_top_jewel()
        new_top_jewel = self.get_bottom_jewel()

        new_bottom_jewel.set_row_pos(old_bottom_abs_row)
        new_middle_jewel.set_row_pos(old_middle_abs_row)
        new_top_jewel.set_row_pos(old_top_abs_row)

        if DEBUG == True:
            print ("New Top Jewel is in row ",new_top_jewel.get_row_pos())
            print ("New Middle Jewel is in row ",new_middle_jewel.get_row_pos())
            print ("New Bottom Jewel is in row ",new_bottom_jewel.get_row_pos())

        self.faller = [new_top_jewel,new_middle_jewel,new_bottom_jewel]

class Field:
    def __init__(self,field_rows,field_cols):
        self._field_rows = field_rows
        self._field_cols= field_cols
        self._width = .8
        self._height = .9

    def top_left(self) -> (float,float):
        return (.5 - self._width/2, .5 - self._height/2)
                
    def width(self) -> float:
        return self._width

    def height(self) -> float:
        return self._height
    
    def grid_width(self) -> float:
        return self.width() / float(self._field_cols)

    def grid_height(self) -> float:
        return self.height()/ float(self._field_rows)

    
        

class GameState:
    def __init__(self,field_height,field_width):
        self.field_width = field_width
        self.field_height = field_height
        self._field = Field(field_height,field_width)
        
    def field_object(self) -> Field:
        return self._field
    
    def new_game_field(self) -> [[None]]:
        #Creates a list that has same number of sublists as height and number of elements in each list as width 
        self.field = []
        
        for row in range(self.field_height):
            self.field.append([])
            for col in range(self.field_width):
                self.field[-1].append(None)
    
    def get_field_width(self) ->int:
        #Returns width of the curent field
        return len(self.field[0])
    
    def get_field_height(self) ->int:
        # Returns height of the current field
        return len(self.field)

    def place_jewel_on_field(self,jewel):
        # Places a Jewel in the position stored in its attribute
        jewel_col = jewel.get_col_pos()
        jewel_row = jewel.get_row_pos()
        jewel_color = jewel.get_color()
        self.field[jewel_row][jewel_col] = jewel

    def is_empty(self,row:int,col:int)->bool:
        # Checks if location on field is Empty
        if self.field[row][col] == None:
            return True
        else:
            return False
        
    def update_faller_state(self, faller:Faller):
        # Updates the state of the faller depending on its current state and if the
        # space under it is empty
        bottom_jewel = faller.get_bottom_jewel()
        #If the space below lowest jewel in faller is empty, then don't do anything
        if self.below_Jewel_is_empty(bottom_jewel):
            pass
        #If the space below lowest jewel in faller is not empty, then update state of faller
        else:
            if faller.get_faller_state() == "IS_FALLER":
                faller.set_state_is_faller_not_frozen()
            elif faller.get_faller_state() == "NOT_FROZEN_FALLER":
                faller.set_state_frozen()

    def empty_below_faller (self,faller:Faller) ->bool:
        # Returns true if the space below faller is empty, false if not empty
            bottom_jewel = faller.get_bottom_jewel()
            return self.below_Jewel_is_empty(bottom_jewel)
    
    def below_Jewel_is_empty(self,jewel) -> bool:
        #Checks if position below Jewel is empty
        jewel_row_pos_below = jewel.get_row_pos_below()
        jewel_col = jewel.get_col_pos()

        try:
            if self.is_empty(jewel_row_pos_below,jewel_col):
                return True
            
            else:
                return False
            
        except IndexError:
            return False
    def right_Jewel_is_empty(self,jewel) -> bool:
        # Checks if position to right is empty. Returns true if it is. False if out of bounds
        jewel_row_pos= jewel.get_row_pos()
        jewel_col_right = jewel.get_col_pos_right()

        try:
            if self.is_empty(jewel_row_pos,jewel_col_right):
                return True
            else:
                return False
        except IndexError:
            return False

    def left_Jewel_is_empty(self,jewel) -> bool:
        # Checks if position to right is empty. Returns true if it is. False if out of ounds
        jewel_row_pos= jewel.get_row_pos()
        jewel_col_left = jewel.get_col_pos_left()

        try:
            if self.is_empty(jewel_row_pos,jewel_col_left):
                return True 
            else:
                return False
        except IndexError:
            return False

    def top_Jewel_is_empty(self,jewel) -> bool:
        # Checks if position to TOP is empty. Returns true if it is. False if out of bounds
        jewel_row_above= jewel.get_row_pos_above()
        jewel_col_pos = jewel.get_col_pos()

        try:
            if self.is_empty(jewel_row_above,jewel_col_pos):
                return True
            else:
                return False
        except IndexError:
            return False

    def below_Jewel_is_empty(self,jewel) -> bool:
        # Checks if position to BOTTOM is empty. Returns true if it is. False if out of bounds
        jewel_row_below= jewel.get_row_pos_below()
        jewel_col_pos = jewel.get_col_pos()
        try:
            if self.is_empty(jewel_row_below,jewel_col_pos):
                return True
            else:
                return False
        except IndexError:
            return False
        
    def top_left_Jewel_is_empty(self,jewel) -> bool:
        # Checks if position to TOP LEFT is empty. Returns true if it is. False if out of bounds
        jewel_row_above= jewel.get_row_pos_above()
        jewel_col_pos_left = jewel.get_col_pos_left()
        try:
            if self.is_empty(jewel_row_above,jewel_col_pos_left):
                return True
            else:
                return False
        except IndexError:
            return False
        
    def top_right_Jewel_is_empty(self,jewel) -> bool:
        # Checks if position to TOP RIGHT is empty. Returns true if it is. False if out of bounds
        jewel_row_above= jewel.get_row_pos_above()
        jewel_col_pos_right = jewel.get_col_pos_right()
        try:
            if self.is_empty(jewel_row_above,jewel_col_pos_right):
                return True
            else:
                return False
        except IndexError:
            return False

    def bottom_left_Jewel_is_empty(self,jewel) -> bool:
        # Checks if position to TOP LEFT is empty. Returns true if it is. False if out of bounds
        jewel_row_below= jewel.get_row_pos_below()
        jewel_col_pos_left = jewel.get_col_pos_left()
        try:
            if self.is_empty(jewel_row_below,jewel_col_pos_left):
                return True
            else:
                return False
        except IndexError:
            return False
        
    def bottom_right_Jewel_is_empty(self,jewel) -> bool:
        # Checks if position to TOP RIGHT is empty. Returns true if it is. False if out of bounds
        jewel_row_below= jewel.get_row_pos_below()
        jewel_col_pos_right = jewel.get_col_pos_right()
        try:
            if self.is_empty(jewel_row_below,jewel_col_pos_right):
                return True
            else:
                return False
        except IndexError:
            return False
        
    def add_row_jewels(self,row:int,row_of_jewels:str):
        #Add each jewel in row_of_jewels into passed in row
        col = 0
        for jewel_color in row_of_jewels:
            if jewel_color == ' ':
                pass
            else:
                new_jewel = Jewel(jewel_color,row,col,"FROZEN")
                self.place_jewel_on_field(new_jewel)
            col +=1
            
    def drop_jewel_one_down(self,jewel:Jewel):
        #Drops jewel one row down. Doesn't check if the jewel below is already occupied. Will overwrite.
        jewel_col = jewel.get_col_pos()
        jewel_row = jewel.get_row_pos()
        new_jewel_row = jewel.get_row_pos_below()
        jewel_row_above = jewel.get_row_pos_above()
        
        if DEBUG == True:
            print("The jewel_row is ",jewel_row, "and the new_jewel_row is ", new_jewel_row)
            
        # Only happens if jewel is not on the lowest row
        if new_jewel_row < self.get_field_height():
            #Only adds jewel to field if the position below it is in the field
            if new_jewel_row >= 0:
            #Copies current Jewel to spot below Jewel
                self.field[new_jewel_row][jewel_col] = jewel
            #Only erases its position if the jewel is already on the board
            if jewel_row >= 0:
                self.field[jewel_row][jewel_col] = None
                
        if DEBUG == True:
            print("Goes into the if statement. Below position of",jewel.get_state_and_color(),"is in field") 
            print("This is the iteration")
            self.display_field()
        jewel.set_row_pos(new_jewel_row)
            
    def drop_jewel (self,jewel:Jewel):
        #Continuously drops Jewel one position until position below isn't empty
        while self.below_Jewel_is_empty(jewel):
            self.drop_jewel_one_down(jewel)
            
    def place_faller_on_board(self,faller:Faller):
        #Places faller on field if its row_position value is on board
        faller_lowest_row = faller.get_lowest_row_pos()
        faller_col = faller.get_faller_col()
        jewel_rel_pos = faller.get_faller_height()-1
        
        #Iterates starting from lowest jewel in faller
        for jewel_abs_pos in range (faller_lowest_row,faller_lowest_row-3,-1):
            #if the position of the jewel in faller it not in field, skip
            if jewel_abs_pos <0:
                jewel_rel_pos -= 1
                continue
            #Goes into else if lowest row on faller isn't on lowest row on field.
            elif faller_lowest_row < self.get_field_height():
                if DEBUG == True:
                    print("the column being set is ",faller_col)
                self.field[jewel_abs_pos][faller_col] = faller.get_jewel_in_pos(jewel_rel_pos)
                if DEBUG == True:
                    print("The jewel in absolte row ", jewel_abs_pos,"and relative row ",jewel_rel_pos, "is ",faller.get_jewel_in_pos(jewel_rel_pos).get_state_and_color())
            #iterates to next lowest jewel position in respect to faller
            jewel_rel_pos -= 1
            
    def drop_faller_one_down(self,faller:Faller):
        #Drops each individual Jewel in Faller one space down
        for jewel in reversed(faller.get_faller_list()):
            if DEBUG == True:
                print("This is the state and color ",jewel.get_state_and_color())
                print("This is prev position ",jewel.get_row_pos())
            #Will only drop faller is lowest row on faller isn't on lowest row on field
            if faller.get_lowest_row_pos()<self.get_field_height():
                self.drop_jewel_one_down(jewel)
            else:
                break
            if DEBUG == True:
                print("This is new position ",jewel.get_row_pos())
        
    def drop_all_jewels(self):
        #Drops all the jewels on the field starting from bottom
        for row in range(self.field_height-1,-1,-1):
            for col in range(self.field_width):
                if self.is_empty(row,col):
                    pass
                else:
                    self.drop_jewel(self.field[row][col])
                    
    def rotate_faller(self,faller):
        # Rotates faller and adds it onto the board
        faller.rotate()
        self.place_faller_on_board(faller)
        
    def move_faller_right(self,faller:Faller):
        #Moves the faller to the right
        faller_right_col = faller.get_col_pos_right()
        if DEBUG == True:
            print("column to right of faller is ",faller_right_col)
        if self.faller_can_move_right(faller):
            faller.set_column(faller_right_col)
            self.erase_left_side(faller)

    def erase_left_side(self,faller:Faller):
        for jewel in faller.get_faller_list():
            if self.jewel_in_field(jewel):
                jewel_left_pos = jewel.get_col_pos_left()
                jewel_row = jewel.get_row_pos()
                self.field[jewel_row][jewel_left_pos] = None
            

    def faller_can_move_right(self,faller:Faller) ->bool:
        # Returns true if space to right of lowest faller is empty
        # or is not out of field
        
        #checks col position to right of lowest jewel
        
        jewel_right_pos = faller.get_bottom_jewel().get_col_pos_right()
        jewel_row_pos = faller.get_bottom_jewel().get_row_pos()

        # Goes into if if positon is not in righest position
        if jewel_right_pos < self.get_field_width():
            #Goes into if if position to right is empty
            if self.is_empty(jewel_row_pos,jewel_right_pos):    
                return True
        else:
            return False
        
    def move_faller_left(self,faller:Faller):
        #Moves the faller to the left
        faller_left_col = faller.get_col_pos_left()
        if DEBUG == True:
            print("column to left of faller is ",faller_left_col)
        if self.faller_can_move_left(faller):
            faller.set_column(faller_left_col)
            self.erase_right_side(faller)

    def erase_right_side(self,faller:Faller):
        for jewel in faller.get_faller_list():
            if self.jewel_in_field(jewel):
                jewel_right_pos = jewel.get_col_pos_right()
                jewel_row = jewel.get_row_pos()
                self.field[jewel_row][jewel_right_pos] = None
            

    def faller_can_move_left(self,faller:Faller) ->bool:
        # Returns true if space to left of lowest faller is empty
        # or is not out of field
        
        #checks col position to left of lowest jewel
        
        jewel_left_pos = faller.get_bottom_jewel().get_col_pos_left()
        jewel_row_pos = faller.get_bottom_jewel().get_row_pos()
        
        # Goes into if if positon is not in left position
        if jewel_left_pos >= 0:
            #Goes into if if position to right is empty
            if self.is_empty(jewel_row_pos,jewel_left_pos):
                return True
        else:
            return False
        
    def not_frozen_or_faller_in_field(self,faller:Faller)->bool:
        # Returns true if faller is in field or is not frozen
        faller_state = faller.get_faller_state()
        bool_value = True

            #Goes in if if faller is frozen
        if faller_state == "FROZEN":
            for jewel in faller.get_faller_list():
                # Goes in if if the jewel in the faller is above top row
                if jewel.get_row_pos() < 0 :
                    bool_value = False
                
        return bool_value   

    def move_faller_into_field(self,faller:Faller):
        # Moves Jewel until top jewel is in field or lowest part is above non-empty space
        # Starts checking from bottom jewel of faller
        for jewel in reversed(faller.get_faller_list()):
            #If the jewel is already on the board, skip it
            if jewel.get_row_pos() >= 0:
                continue
            # Move jewel until it is on screen aka the top row
            while jewel.get_row_pos() <0:
                self.drop_jewel_one_down(jewel)
                
            # Once jewel is on board, keep moving it down until it hits bottom
            jewel_col = jewel.get_col_pos()
            jewel_row_below = jewel.get_row_pos_below()
            if jewel_row_below < self.get_field_height():
                while self.is_empty(jewel.get_row_pos_below(),jewel_col):
                    self.drop_jewel_one_down(jewel)

                                    
    def check_horizontal_match(self)-> bool:
        # Returns False if there is no match. Marks center jewel of horizontal matches as match. Starts from top left and goes right
        match = False
        # For loop only iterates through values that aren't on the leftest or rightest col
        for row in range(self.field_height):
            for col in range(1,self.field_width-1):
                if DEBUG == True:
                    print ("ROW,COL: ",row, " ", col)
                if self.is_empty(row,col):
                    if DEBUG == True:
                        print("HORIZONTAL MATCH CHECK SPACE WAS EMPTY")
                    continue
                else:
                    if DEBUG == True:
                        print("HORIZONTAL MATCH CHECK SPACE WAS NOT EMPTY")
                    jewel = self.field[row][col]
                    jewel_state = jewel.get_state()
                    if jewel_state == "FROZEN" or jewel_state == "MATCH":
                        jewel_color = jewel.get_color()
                        jewel_left_col = col - 1
                        jewel_right_col = col + 1
                        if DEBUG == True:
                            print("HORIZONTAL MATCH JEWEL IS FROZEN")
                            print("Thing is right space of jewel is: ", self.field[row][jewel_right_col])
                        # Go into if is space to left and right of jewel are not empty
                        if ((self.right_Jewel_is_empty(jewel) != True) and (self.left_Jewel_is_empty(jewel) != True)):
                            if DEBUG == True:
                                print("Right space of jewel is: ", jewel.get_col_pos_right())
                                print("RIGHT SPACE IS EMPTY ",self.right_Jewel_is_empty(jewel))
                                print("LEFT SPACE IS EMPTY ",self.left_Jewel_is_empty(jewel))
                                print("SPACE TO RIGHT AND LEFT NOT EMPTY")
                                self.display_field()
                            jewel_left_color = self.field[row][jewel_left_col].get_color()
                            jewel_right_color = self.field[row][jewel_right_col].get_color()
                            if (jewel_left_color == jewel_color and jewel_right_color == jewel_color):
                                jewel.set_state_is_match()
                                self.field[row][jewel_left_col].set_state_is_match()
                                self.field[row][jewel_right_col].set_state_is_match()
                                match = True
                                if DEBUG == True:
                                    print("GOTTEM BOYS")
        return match
    
    def check_vertical_match(self)-> bool:
        # Returns False if there is no match. Marks center jewelof vartical matches as match. Starts from top left and goes right
        match = False
        # For loop only iterates through values that aren't on the top or bottom row
        for row in range(1,self.field_height-1):
            for col in range(self.field_width):
                if DEBUG == True:
                    print("ROW,COL: ",row, " ", col)
                if self.is_empty(row,col):
                    if DEBUG == True:
                        print("VERTICAL MATCH CHECK SPACE WAS EMPTY")
                    continue
                else:
                    if DEBUG == True:
                        print("VERTICAL MATCH CHECK SPACE WAS NOT EMPTY")
                    jewel = self.field[row][col]
                    jewel_state = jewel.get_state()
                    if jewel_state == "FROZEN" or jewel_state == "MATCH":
                        jewel_color = jewel.get_color()
                        jewel_top_row = row - 1
                        jewel_bottom_row = row + 1
                        if DEBUG == True:
                            print("VERTICAL MATCH JEWEL IS FROZEN")
                            print("Thing is top space of jewel is: ", self.field[jewel_top_row][col])
                        # Go into if is space to top and bottom of jewel are not empty
                        if ((self.top_Jewel_is_empty(jewel) != True) and (self.below_Jewel_is_empty(jewel) != True)):
                            if DEBUG == True:
                                print("Top space of jewel is: ", jewel.get_row_pos_above())
                                print("TOP SPACE IS EMPTY ",self.top_Jewel_is_empty(jewel))
                                print("BOTTOM SPACE IS EMPTY ",self.below_Jewel_is_empty(jewel))
                                print("SPACE TO TOP AND BOTTOM NOT EMPTY")
                                self.display_field()
                            jewel_top_color = self.field[jewel_top_row][col].get_color()
                            jewel_bottom_color = self.field[jewel_bottom_row][col].get_color()
                            if (jewel_top_color == jewel_color and jewel_bottom_color == jewel_color):
                                jewel.set_state_is_match()
                                self.field[jewel_bottom_row][col].set_state_is_match()
                                self.field[jewel_top_row][col].set_state_is_match()
                                match = True
                                if DEBUG == True:
                                    print("GOTTEM BOYS")
        return match
    
    def check_diaganol_match(self)-> bool:
        # Marks center jewel of match as match. Returns true if match occurs, else false
        match = False
        # For loop only iterates through values that aren't on the leftest or rightest col or top and bottom row
        for row in range(1,self.field_height-1):
            for col in range(1,self.field_width-1):
                if DEBUG == True:
                    print ("ROW,COL: ",row, " ", col)
                if self.is_empty(row,col):
                    if DEBUG == True:
                        print("DIAGONAL MATCH CHECK SPACE WAS EMPTY")
                    continue
                else:
                    if DEBUG == True:
                        print("DIAGONAL MATCH CHECK SPACE WAS NOT EMPTY")
                    jewel = self.field[row][col]
                    jewel_state = jewel.get_state()
                    if jewel_state == "FROZEN" or jewel_state == "MATCH":
                        jewel_color = jewel.get_color()
                        jewel_left_col = col - 1
                        jewel_right_col = col + 1
                        jewel_top_row = row - 1
                        jewel_bottom_row = row + 1
                        if DEBUG == True:
                            print("DIAGONAL MATCH JEWEL IS FROZEN")
                        # Go into if if space to TOP LEFT and BOTTOM RIGHT of jewel are not empty
                        if ((self.top_left_Jewel_is_empty(jewel) != True) and (self.bottom_right_Jewel_is_empty(jewel) != True)):
                            if DEBUG == True:
                                print("SPACE TOP LEFT AND BOTTOM RIGHT NOT EMPTY")
                                self.display_field()
                            jewel_top_left_color = self.field[jewel_top_row][jewel_left_col].get_color()
                            jewel_bottom_right_color = self.field[jewel_bottom_row][jewel_right_col].get_color()
                            if (jewel_top_left_color == jewel_color and jewel_bottom_right_color == jewel_color):
                                jewel.set_state_is_match()
                                self.field[jewel_top_row][jewel_left_col].set_state_is_match()
                                self.field[jewel_bottom_row][jewel_right_col].set_state_is_match()
                                match = True
                                if DEBUG == True:
                                    print("GOTTEM BOYS")
                        # Go into if if space to BOTTOM LEFT and TOP RIGHT of jewel are not empty
                        if ((self.bottom_left_Jewel_is_empty(jewel) != True) and (self.top_right_Jewel_is_empty(jewel) != True)):
                            if DEBUG == True:
                                print("SPACE BOTTOM LEFT AND TOP RIGHT NOT EMPTY")
                                self.display_field()
                            jewel_top_right_color = self.field[jewel_top_row][jewel_right_col].get_color()
                            jewel_bottom_left_color = self.field[jewel_bottom_row][jewel_left_col].get_color()
                            if (jewel_top_right_color == jewel_color and jewel_bottom_left_color == jewel_color):
                                jewel.set_state_is_match()
                                self.field[jewel_top_row][jewel_right_col].set_state_is_match()
                                self.field[jewel_bottom_row][jewel_left_col].set_state_is_match()
                                match = True
                                if DEBUG == True:
                                    print("GOTTEM 2 BOYS")
        return match
    
    def remove_matched_jewels(self):
        #Looks for jewels that are matched state and removes it
        for row in range(self.field_height):
            for col in range(self.field_width):
                if DEBUG == True:
                    print("Entered Remove_matched_Jewels")
                    print("Row, Col:", row, " ", col)
                    print(self.field[row][col].get_state())
                if self.is_empty(row,col):
                    continue
                elif self.field[row][col].get_state() == "MATCH":
                    self.field[row][col] = None
                    
    def jewel_in_pos(self,row:int,col:int) -> Jewel:
        return self.field[row][col]
    
    def jewel_in_field(self,jewel:Jewel) -> bool:
        # Returns true is the true is in field aka its row is >= 0
        return jewel.get_row_pos() >=0
        
    def display_field(self):
        #Prints out field saved in self.field in GameState
        for row in range(self.field_height):
            print("|",end="")
            for col in range(self.field_width):
                if self.is_empty(row,col):
                    print("   ",end="" )
                else:
                    print(self.field[row][col].get_state_and_color(),end="")
            print("|")

        print(" " +self.field_width*"---"+" ")

    def get_field(self):
        #Returns field stored in GameState
        return self.field
    
    def value_at (self,row:int,col:int) ->[[chr]]:
        #Returns color or None value in specified position
        if self.is_empty(row,col):
            return None
        else:
            return self.color_at(row,col)
        
    def check_match(self):
        # Returns True if there are matches, otherwise, returns false
        bool_value = False
        match1 = game_state.check_diaganol_match()
        match2 = game_state.check_vertical_match()
        match3 = game_state.check_horizontal_match()
        if (match1 == True or match2 == True or match3 == True):
            game_state.display_field()
            game_state.remove_matched_jewels()
            game_state.drop_all_jewels()
            bool_value = True
        return bool_value
    
    def color_at(self,row:int,col:int) -> [[chr]]:
        #Returns color that is in the field at the rol and col position
        return self.field[row][col].get_color()
