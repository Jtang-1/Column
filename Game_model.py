# Game_model
# Jonathan Tang 85625237

from game_mechanic import Jewel,Faller,GameState
import random

TEST = False
AUTO_FALLER = True

def run_user_interface():
    
    if TEST == True:
    #    field_height = ask_field_height()
    #    field_width = ask_field_width()
        game_state =GameState(5,5)
        create_empty_field(game_state)
        
        new_jewel = Jewel('A',1,4,"FROZEN")
        new_jewel2 = Jewel('B',2,5,"FALLING")

    ##    game_state.place_jewel_on_field(new_jewel)
    ##    game_state.drop_jewel(new_jewel)
    ##    game_state.display_field()
    ##    print("")

        game_state = GameState(5,5)
        game_state.place_jewel_on_field(new_jewel2)

        game_state.add_row_jewels(0,'YXY X')
        game_state.add_row_jewels(1,'YYY Y')
        game_state.add_row_jewels(2,'BYY Y')
        game_state.add_row_jewels(3,'BBB Y')
        game_state.add_row_jewels(4,'BYB Y')
        game_state.drop_all_jewels()
        game_state.display_field()
        
    ##    new_jewel2 = Jewel('B',0,2,"FROZEN")
    ##    game_state.display_field()
    ##    
    ##    game_state.place_jewel_on_field(new_jewel2)
    ##    game_state.display_field()
    ##    
    ##    game_state.drop_jewel_one_down(new_jewel2)
    ##    game_state.display_field()
    ##    
    ##    game_state.drop_jewel_one_down(new_jewel2)
    ##    game_state.display_field()
        


        new_faller = Faller('J','Y','J',4)
        game_state.place_faller_on_board(new_faller)
        game_state.update_faller_state(new_faller)
        game_state.display_field()
        while game_state.empty_below_faller(new_faller):
            game_state.drop_faller_one_down(new_faller)
            game_state.update_faller_state(new_faller)
            game_state.display_field()
        game_state.update_faller_state(new_faller)
        game_state.display_field()
        

        game_state.check_diaganol_match()
        game_state.check_vertical_match()
        game_state.check_horizontal_match()
        game_state.display_field()
        game_state.remove_matched_jewels()
        game_state.display_field()

        game_state.drop_all_jewels()
        game_state.display_field()  
    else:
        
        field_height = int(ask_field_height())
        field_width = int(ask_field_width())
        game_state = GameState (field_height,field_width)
        create_field(game_state)

        while check_match(game_state):
            pass
        game_state.display_field()

        running = True
        while running:
            if AUTO_FALLER == False:
                faller_init = ask_input()   #Want input of F  
                if faller_init == "Q":
                    break
                    running = False
                if faller_init == None:
                    continue
                elif faller_init[0] == "F":
                    faller_col = int(faller_init[2])
                    faller_top_color = faller_init[4]
                    faller_middle_color = faller_init[6]
                    faller_bottom_color = faller_init[8]
                    new_faller = Faller(faller_top_color,faller_middle_color,faller_bottom_color,faller_col)
                else:
                    continue

            if AUTO_FALLER == True:
                new_faller = Faller("A","B","C",1)
        
            
            while (new_faller.get_faller_state() != "FROZEN" and running == True):
                game_state.place_faller_on_board(new_faller)
                game_state.display_field()
                faller_command = ask_input() #print("Put in > < or R")

                if faller_command == "Q":
                    running = False
                    break
                elif faller_command == ">":
                    game_state.move_faller_right(new_faller)
                elif faller_command == "<":
                    game_state.move_faller_left(new_faller)
                elif faller_command == "R":
                    game_state.rotate_faller(new_faller)
                elif game_state.empty_below_faller(new_faller) and faller_command == "":
                    game_state.drop_faller_one_down(new_faller)
                    game_state.update_faller_state(new_faller)
                elif faller_command == "":
                    game_state.update_faller_state(new_faller)
                
                
            while check_match(game_state):
                pass
            game_state.move_faller_into_field(new_faller)
            while check_match(game_state):
                pass
            game_state.display_field()

            
            if game_state.not_frozen_or_faller_in_field(new_faller) != True:
               print("GAME OVER")
               running = False


def create_field(game_state:GameState) -> None:
    #Creates a correctly sized GameState and creates
    start_input = input () # EMPTY or CONTENTS "
    if start_input == "EMPTY":
        create_empty_field(game_state)
    elif start_input == "CONTENTS":
        create_filled_field(game_state)

def create_empty_field(game_state:GameState) -> None:
    game_state.new_game_field()
    
def create_filled_field(game_state:GameState) -> None:
    game_state.new_game_field()
    
    for i in range (game_state.get_field_height()):
        row_of_jewels = input("Row_of_Jewel "+ str(game_state.get_field_width())+" ")
        game_state.add_row_jewels(i,row_of_jewels)
        
    if check_match(game_state) != True:
        game_state.drop_all_jewels()

def check_match(game_state:GameState):
    # Returns True if there are matches, otherwise, returns false
    bool_value = False
    match1 = game_state.check_diaganol_match()
    match2 = game_state.check_vertical_match()
    match3 = game_state.check_horizontal_match()
    if (match1 == True or match2 == True or match3 == True):
        game_state.remove_matched_jewels()
        game_state.drop_all_jewels()
        bool_value = True
    return bool_value
        
def update_faller(game_state: GameState, faller:Faller ):
    game_state.place_faller_on_board(faller)
    game_state.update_faller_state(faller)
    
def ask_input() ->str:
    user_input = input()
    if user_input == "":
        return user_input
    else:
        return handle_input(user_input[0],user_input)

def random_faller(game_state:GameState) -> Faller:
    jewel_colors = ['A','B','C','D','E','F','G']
    field_columns = range(1,game_state.get_field_width() + 1)
    
    top_color = random.choice(jewel_colors)
    middle_color = random.choice(jewel_colors)
    bottom_color = random.choice(jewel_colors)
    random_col = random.choice(field_columns)

    return Faller(top_color,middle_color,bottom_color,random_col)

def handle_input(user_command,user_input) -> str:
    if user_command == "F":
        return user_input
    if user_command == "Q":
        return user_input
    if user_command == ">":
        return user_input
    if user_command == "<":
        return user_input
    if user_command == "R":
        return user_input
    else:
        return None
    
def ask_field_height() -> int:
    #Returns input height of the field
    field_height = input() #"Field Height?"
    return field_height

def ask_field_width() -> int:
    #Returns input width of the field
    field_width = input() #"Field Width?"
    return field_width

if __name__ == "__main__":
    run_user_interface()
