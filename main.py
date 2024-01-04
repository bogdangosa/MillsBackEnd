from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from Constants import constants
from Services.Services import Services

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

games_list = []


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


@app.post("/create_game")
async def create_game(game_difficulty: int = 0):
    services = Services()
    services.start_game(game_difficulty)
    game_id = len(games_list)
    games_list.append(services)
    print("Created a new game with id:"+str(game_id))
    return {
        "status": constants.SUCCESS_CODE,
        "game_id": game_id
    }


@app.post("/place_pawn")
async def create_game(game_id: int = 0,position: int = 0):
    try:
        services = games_list[game_id]
        services.add_pawn_to_board(position)
    except ValueError as error:
        print(error)
        return error
    return {
        "status": constants.SUCCESS_CODE,
    }


@app.get("/get_table")
async def get_table(game_id: int = 0):
    services = games_list[game_id]
    return {
        "table_data":services.get_table_data(),
        "status": constants.SUCCESS_CODE,
    }


@app.get("/get_game_state")
async def get_game_state(game_id: int = 0):
    services = games_list[game_id]
    return {
        "status": constants.SUCCESS_CODE,
        "game_state":services.get_game_state()
    }


@app.post("/move_pawn")
async def move_pawn(game_id: int = 0,position: int = 0,direction: str = 'r'):
    services = games_list[game_id]
    try:
        services.move_pawn(position, direction)
    except ValueError as error:
        print(error)
        return error
    return {
        "status": constants.SUCCESS_CODE,
    }


@app.post("/remove_pawn")
async def remove_pawn(game_id: int = 0,position: int = 0):
    services = games_list[game_id]
    try:
        services.remove_pawn_from_board(position)
    except ValueError as error:
        print(error)
        return error
    return {
        "status": constants.SUCCESS_CODE,
    }


@app.get("/get_possible_directions_from_position")
async def get_possible_directions_from_position(game_id: int = 0,position: int = 0):
    services = games_list[game_id]
    try:
        possible_directions = services.get_possible_directions_from_position(position)
        return {
            "status": constants.SUCCESS_CODE,
            "possible_directions":possible_directions
        }
    except ValueError as error:
        print(error)
        return error
