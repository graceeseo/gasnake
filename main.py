# Welcome to
# __________         __    __  .__                               __
# \______   \_____ _/  |__/  |_|  |   ____   ______ ____ _____  |  | __ ____
#  |    |  _/\__  \\   __\   __\  | _/ __ \ /  ___//    \\__  \ |  |/ // __ \
#  |    |   \ / __ \|  |  |  | |  |_\  ___/ \___ \|   |  \/ __ \|    <\  ___/
#  |________/(______/__|  |__| |____/\_____>______>___|__(______/__|__\\_____>
#
# This file can be a nice home for your Battlesnake logic and helper functions.
#
# To get you started we've included code to prevent your Battlesnake from moving backwards.
# For more info see docs.battlesnake.com

###==============================###
### RULES ###
###==============================###

## Criteria to win
#- Avoid walls (it must stay within the boundary)
#- Avoid running into your own body or other battlesnakes
#- Eat food to stay healthy. Battlesnakes lose 1 health on every turn.
#Eliminated if health reaches zero. Food = 1
# - Head-to-head collision - the longer battlesnake will survive. If both are the same length, they are both eliminated.

#- Size = 11 x 11
#- operate in coorinates based.
# left bottom = 0, top left = 11
# right bottom = 11

# Watch video: https://youtu.be/yAA2HpMKiaA

## Battlesnake HTTP API
#- GET /
#    - testing latency and defining how your battlesnake looks
#- POST /move
#    - analyze the game board and return your next move
# - POST /start & POST /end
#     - allocate & deallocate any game specific resources
#     - Optional

## Other Technical Notes
#- Battlesnakes must respond with HTTP 200 OK
#- Battlesnakes have 500 ms to respond (includes roundtrip latency)
#- Any error will move your battlesnake forward
#- The game engine runs in GCP US-WEST1

###==============================###
###==============================###

import random
import typing


# info is called when you create your Battlesnake on play.battlesnake.com
# and controls your Battlesnake's appearance
# TIP: If you open your Battlesnake URL in a browser you should see this data
def info() -> typing.Dict:
  print("INFO")

  return {
      "apiversion": "1",
      "author": "",  # TODO: Your Battlesnake Username
      "color": "#888888",  # TODO: Choose color
      "head": "default",  # TODO: Choose head
      "tail": "default",  # TODO: Choose tail
  }


# start is called when your Battlesnake begins a game
def start(game_state: typing.Dict):
  print("GAME START")


# end is called when your Battlesnake finishes a game
def end(game_state: typing.Dict):
  print("GAME OVER\n")


# move is called on every turn and returns your next move
# Valid moves are "up", "down", "left", or "right"
# See https://docs.battlesnake.com/api/example-move for available data
def move(game_state: typing.Dict) -> typing.Dict:

  is_move_safe = {"up": True, "down": True, "left": True, "right": True}

  my_head = game_state["you"]["body"][0]  # Coordinates of your head
  my_neck = game_state["you"]["body"][1]  # Coordinates of your "neck"

  # Prevent your Battlesnake from moving backwards
  if my_neck["x"] < my_head["x"]:  # Neck is left of head, don't move left
    is_move_safe["left"] = False

  elif my_neck["x"] > my_head["x"]:  # Neck is right of head, don't move right
    is_move_safe["right"] = False

  elif my_neck["y"] < my_head["y"]:  # Neck is below head, don't move down
    is_move_safe["down"] = False

  elif my_neck["y"] > my_head["y"]:  # Neck is above head, don't move up
    is_move_safe["up"] = False

  # TODO: Step 1 - Prevent your Battlesnake from moving out of bounds
  board_width = game_state['board']['width']
  board_height = game_state['board']['height']

  # if x is at the right edge of the board, don't move right
  if my_head["x"] == board_width - 1:
    is_move_safe["right"] = False

  # if x is at the left edge of the board, don't move left
  if my_head["x"] == 0:
    is_move_safe["left"] = False

  # if x is at the top edge of the board, don't move up
  if my_head["y"] == board_height - 1:
    is_move_safe["up"] = False

  # if x is at the bottom edge of the board, don't move down
  if my_head["y"] == 0:
    is_move_safe["down"] = False

  # TODO: Step 2 - Prevent your Battlesnake from colliding with itself
  my_body = game_state['you']['body']

  # Check if right of head is my body
  block = {"x": my_head["x"] + 1, "y": my_head["y"]}
  if block in my_body:
    is_move_safe["right"] = False

  # Check if left of head is my body
  block = {"x": my_head["x"] - 1, "y": my_head["y"]}
  if block in my_body:
    is_move_safe["left"] = False

  # Check if top of head is my body
  block = {"x": my_head["x"], "y": my_head["y"] + 1}
  if block in my_body:
    is_move_safe["up"] = False

  # Check if bottom of head is my body
  block = {"x": my_head["x"], "y": my_head["y"] - 1}
  if block in my_body:
    is_move_safe["down"] = False

  # TODO: Step 3 - Prevent your Battlesnake from colliding with other Battlesnakes
  opponents = game_state['board']['snakes']
  # print("GAME STATE!!")
  # print(game_state)
  # print("PRINT OPPONENT LOOK HERE")
  # print(opponents)
  # only collide if we're bigger than the next snake
  our_body_length = len(my_body)
  # print("My body: {}".format(my_body))
  # print("My body length: {}".format(our_body_length))

  for opponent in opponents:
    # if we're bigger than that snake, we don't have to worry about where their body is
    # so only have to check if we're smaller than our opponent
    their_body = opponent['body']
    their_body_length = len(their_body)
    # print("Their body: {}".format(opponent['body']))
    # print("Their body length: {}".format(their_body_length))
    # print(our_body_length < their_body_length)
    if our_body_length <= their_body_length:
      # check if moving right will make us collide
      block = {"x": my_head["x"] + 1, "y": my_head["y"]}
      # print("block: {}".format(block))
      if block in their_body:
        is_move_safe["right"] = False

      # check if moving left will make us collide
      block = {"x": my_head["x"] - 1, "y": my_head["y"]}
      # print("block: {}".format(block))
      if block in their_body:
        is_move_safe["left"] = False

      # check if moving up will make us collide
      block = {"x": my_head["x"], "y": my_head["y"] + 1}
      # print("block: {}".format(block))
      if block in their_body:
        is_move_safe["up"] = False

      # check if moving down will make us collide
      block = {"x": my_head["x"], "y": my_head["y"] - 1}
      # print("block: {}".format(block))
      # print("b")
      if block in their_body:
        is_move_safe["down"] = False

      # Also need to account for if a future move will make us collide.
      # so if a snake is heading right for a while, there's a chance
      # it's going to keep heading right (?locality of reference - spatial?),
      # so we should avoid moving that way.
      # maybe instead of random movements, have it follow the opposite direction
      # until it has to turn??
      # Maybe if there's a snake close to us, we should start moving in opp direction

  print("Is move safe: {}".format(is_move_safe))
  # Are there any safe moves left?
  safe_moves = []
  for move, isSafe in is_move_safe.items():
    if isSafe:
      safe_moves.append(move)

  if len(safe_moves) == 0:
    print(f"MOVE {game_state['turn']}: No safe moves detected! Moving down")
    return {"move": "down"}

  # Choose a random move from the safe ones
  next_move = random.choice(safe_moves)

  # TODO: Step 4 - Move towards food instead of random, to regain health and survive longer
  # food = game_state['board']['food']

  # # we need to eat at least once every 100 moves
  # turn = game_state['turn']

  # TODO: Step 5 - Think about movements in the future before deciding on a move
  # need to consider if the snake will be trapped by the outer walls and/or it's own body

  print(f"MOVE {game_state['turn']}: {next_move}")
  print("")
  return {"move": next_move}


# Start server when `python main.py` is run
if __name__ == "__main__":
  from server import run_server

  run_server({"info": info, "start": start, "move": move, "end": end})
