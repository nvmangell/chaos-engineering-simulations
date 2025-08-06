import json
import random
import time
from fake_useragent import UserAgent
from selenium import webdriver
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver import ActionChains
from selenium.webdriver.support import expected_conditions as ECimport 
from selenium.webdriver.support import expected_conditions as EC
import pdb
from utils.constants import Login, Time

def get_random_move():
    return "a2a4"

def make_move(driver, move: str):
    start_move = move[0:2]
    end_move = move[2:]
    source_move = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, f"square-{start_move}")))
    target_move = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, f"square-{end_move}")))
    actions = ActionChains(driver)
    actions.drag_and_drop(source_move,target_move).perform()

    return


columns = "abcdefgh"
rows = "12345678"

def calculate_knight_moves(current_square):
    col, row = current_square[0], int(current_square[1])
    col_index = columns.index(col)

    possible_moves = [
        (2, 1), (2, -1), (-2, 1), (-2, -1),
        (1, 2), (1, -2), (-1, 2), (-1, -2),
    ]

    valid_moves = []
    for move in possible_moves:
        new_col_index = col_index + move[0]
        new_row = row + move[1]

        if 0 <= new_col_index < 8 and 1 <= new_row <= 8:
            new_square = f"{columns[new_col_index]}{new_row}"
            valid_moves.append(new_square)

    return valid_moves

def calculate_rook_moves(current_square):
    col, row = current_square[0], int(current_square[1])
    valid_moves = []

    for c in columns:
        if c != col: 
            valid_moves.append(f"{c}{row}")

    for r in rows:
        if int(r) != row:
            valid_moves.append(f"{col}{r}")

    return valid_moves

def calculate_bishop_moves(current_square):
    col, row = current_square[0], int(current_square[1])
    col_index = columns.index(col)
    valid_moves = []

    for i in range(1, 8):
        if col_index + i < 8 and row + i <= 8:
            valid_moves.append(f"{columns[col_index + i]}{row + i}")
        if col_index - i >= 0 and row + i <= 8:
            valid_moves.append(f"{columns[col_index - i]}{row + i}")
        if col_index + i < 8 and row - i >= 1:
            valid_moves.append(f"{columns[col_index + i]}{row - i}")
        if col_index - i >= 0 and row - i >= 1:
            valid_moves.append(f"{columns[col_index - i]}{row - i}")

    return valid_moves

def calculate_queen_moves(current_square):
    return calculate_rook_moves(current_square) + calculate_bishop_moves(current_square)

def calculate_king_moves(current_square):
    col, row = current_square[0], int(current_square[1])
    col_index = columns.index(col)
    valid_moves = []

    possible_moves = [
        (1, 0), (-1, 0), (0, 1), (0, -1),
        (1, 1), (1, -1), (-1, 1), (-1, -1),
    ]

    for move in possible_moves:
        new_col_index = col_index + move[0]
        new_row = row + move[1]

        if 0 <= new_col_index < 8 and 1 <= new_row <= 8:
            valid_moves.append(f"{columns[new_col_index]}{new_row}")

    return valid_moves

def calculate_pawn_moves(current_square, is_black=True):
    col, row = current_square[0], int(current_square[1])
    valid_moves = []

    if is_black:
        if row > 1:
            valid_moves.append(f"{col}{row - 1}")
        if row == 7:
            valid_moves.append(f"{col}{row - 2}")
    else:
        if row < 8:
            valid_moves.append(f"{col}{row + 1}")
        if row == 2:
            valid_moves.append(f"{col}{row + 2}")

    return valid_moves


def get_piece_moves_function(data_piece):
    # Map data_piece to corresponding move calculation functions
    if data_piece in ["bN", "wN"]:  # Knight
        return calculate_knight_moves
    elif data_piece in ["bR", "wR"]:  # Rook
        return calculate_rook_moves
    elif data_piece in ["bB", "wB"]:  # Bishop
        return calculate_bishop_moves
    elif data_piece in ["bQ", "wQ"]:  # Queen
        return calculate_queen_moves
    elif data_piece in ["bK", "wK"]:  # King
        return calculate_king_moves
    elif data_piece in ["bP", "wP"]:  # Pawn
        return calculate_pawn_moves
    else:
        return None

def find_first_move(driver):
    pieces = driver.find_elements(By.CLASS_NAME, "piece-417db")
    for piece in pieces:
        ActionChains(driver).move_to_element(piece).perform()
        time.sleep(0.5) 

        data_piece = piece.get_attribute("data-piece")
        data_square = piece.find_element(By.XPATH, "..").get_attribute("data-square")

        move_function = get_piece_moves_function(data_piece)

        if move_function:
            if data_piece in ["bP", "wP"]:
                is_black = data_piece.startswith("b")
                valid_moves = move_function(data_square, is_black=is_black)
            else:
                valid_moves = move_function(data_square)
            
            print(f"Found {data_piece} at {data_square}")
            print(f"Valid moves: {valid_moves}")

            # Try dragging the piece to its valid moves
            for move in valid_moves:
                try:
                    # Find the target square
                    target_square = driver.find_element(By.XPATH, f"//div[@data-square='{move}']")
                    ActionChains(driver).drag_and_drop(piece, target_square).perform()
                    print(f"Moved {data_piece} from {data_square} to {move}")
                    return piece, target_square
                except Exception as e:
                    print(f"Could not move {data_piece} to {move}: {e}")    
    return None, None


def find_first_move(driver):
    pieces = driver.find_elements(By.CLASS_NAME, "piece-417db")
    for piece in pieces:
        ActionChains(driver).move_to_element(piece).perform()
        time.sleep(0.5)  # Allow hover effect to appear

        # Get piece attributes
        data_piece = piece.get_attribute("data-piece")
        data_square = piece.find_element(By.XPATH, "..").get_attribute("data-square")

        # Handle knight movement (bN for black knight)
        if data_piece == "bN":
            print(f"Found black knight at {data_square}")
            valid_moves = calculate_knight_moves(data_square)
            print(f"Valid moves for knight: {valid_moves}")

            # Try dragging the knight to its valid moves
            for move in valid_moves:
                try:
                    # Find the target square
                    target_square = driver.find_element(By.XPATH, f"//div[@data-square='{move}']")
                    ActionChains(driver).drag_and_drop(piece, target_square).perform()
                    print(f"Moved knight from {data_square} to {move}")
                    return piece, target_square
                except Exception as e:
                    print(f"Could not move to {move}: {e}")
    
    return None, None
def find_first_move(driver):
    pieces = driver.find_elements(By.CLASS_NAME, "piece-417db")
    for piece in pieces:
        # Hover over the piece
        ActionChains(driver).move_to_element(piece).perform()
        time.sleep(0.5)  # Allow some time for hover effect

        # Get the piece type (e.g., bN for black knight)
        data_piece = piece.get_attribute("data-piece")
        current_square = piece.find_element(By.XPATH, "..").get_attribute("data-square")
        print(f"Checking piece {data_piece} at {current_square}")

        # Calculate possible moves based on the piece type
        valid_moves = []
        if data_piece == "bN":  # Black Knight
            valid_moves = calculate_knight_moves(current_square)

        # Highlighted squares on the board
        highlighted_squares = []
        squares = driver.find_elements(By.XPATH, "//div[contains(@class, 'square')]")
        for square in squares:
            background_color = driver.execute_script(
                "return window.getComputedStyle(arguments[0]).getPropertyValue('background-color');", square
            )
            if background_color == 'rgb(105, 105, 105)':  # Adjust based on your hover highlight color
                square_data = square.get_attribute("data-square")
                if square_data and square_data != current_square:
                    highlighted_squares.append(square)

        # Filter highlighted squares to match valid moves
        valid_targets = [square for square in highlighted_squares if square.get_attribute("data-square") in valid_moves]
        print(f"Valid targets for {data_piece} at {current_square}: {[sq.get_attribute('data-square') for sq in valid_targets]}")

        if valid_targets:
            # Randomly select a target square
            target_square = random.choice(valid_targets)
            print(f"Moving {data_piece} from {current_square} to {target_square.get_attribute('data-square')}")

            # Drag and drop the piece to the selected target square
            ActionChains(driver).drag_and_drop(piece, target_square).perform()
            time.sleep(1)
            return piece, target_square

    return None, None