
import copy
import dataclasses
from enum import Enum, IntEnum
from pickle import NONE
from random import randrange
from secrets import randbelow
from time import sleep
from tkinter import Canvas, Event, Misc, Tk
import tkinter
from turtle import update
from typing import Callable, Optional

BLOCK_UNIT = 4
FIELD_WIDTH = 14
FIELD_HEIGHT = 22
VIEW_UNIT_SIZE = 25


class BlockPattern(Enum):
    PATTERN_I = [
        [0, 1, 0, 0],
        [0, 1, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 0, 0]
    ]
    PATTERN_L = [
        [0, 0, 0, 0],
        [0, 0, 1, 0],
        [0, 0, 1, 1],
        [0, 0, 0, 0]
    ]
    PATTERN_SQUARE = [
        [0, 0, 0, 0],
        [0, 0, 1, 1],
        [0, 0, 1, 1],
        [0, 0, 1, 1]
    ]
    PATTERN_CHAOS = [
        [0, 0, 1, 0],
        [0, 0, 1, 1],
        [0, 0, 1, 1],
        [0, 0, 0, 1]
    ]
    PATTERN_CHAOS_2 = [
        [0, 1, 1, 1],
        [0, 0, 1, 1],
        [0, 0, 0, 1],
        [0, 0, 0, 0]
    ]

    @classmethod
    def createRandomPattern(cls) -> 'BlockPattern':
        patterns = list(map(lambda pattern: pattern, cls))
        return patterns[randrange(len(patterns))]


class BlockManager:
    def __init__(self, block_unit: int, field_width: int) -> None:
        self.__current_pattern: BlockPattern
        self.__rotate_count: int
        self.x: int
        self.y: int
        self.block_unit: int = block_unit
        self.__field_width: int = field_width
        self.create_new_block()

    def create_new_block(self) -> None:
        self.__current_pattern: BlockPattern = BlockPattern.createRandomPattern()
        self.__rotate_count: int = 0  # 右に回転させた回数
        self.x: int = randrange(self.__field_width - 2 - self.block_unit) + 1
        self.y: int = 0

    def current_state(self) -> list[list[int]]:
        state = self.__current_pattern.value

        for count in range(self.__rotate_count):
            state = self.__rotate_once(state)

        return state

    def __rotate_once(self, state) -> list[list[int]]:
        rotate_pattern_values = [
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0]
        ]
        for y in range(self.block_unit):
            for x in range(self.block_unit):
                rotate_pattern_values[y][x] = self.__current_pattern.value[(
                    self.block_unit - 1) - x][y]
        return rotate_pattern_values

    def update_rotate(self) -> None:
        self.__rotate_count = (self.__rotate_count + 1) % 4

    def move_right(self) -> None:
        self.x = self.x + 1

    def move_left(self) -> None:
        self.x = self.x - 1

    def move_down(self) -> None:
        self.y = self. y + 1


class FieldManager:

    @dataclasses.dataclass(frozen=True)
    class LineUp:
        start_position_y: int
        count: int

    FIELD_STATE_NONE = 0  # 何もないフィールド
    FIELD_STATE_BLOCK = 1  # 動いている状態のブロックがあるフィールド
    FIELD_STATE_WALL = 2  # 壁があるフィールドフィールド
    FIELD_STATE_STONE = 3  # 動かなくなった状態のブロックあるフィールド
    LINE_UP_BLOCK_FIELD_ROW_VALUE = [2, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 2]

    def __init__(self) -> None:
        self.game_field: list[list[int]] = [
            [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
            [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
            [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
            [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
            [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
            [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
            [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
            [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
            [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
            [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
            [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
            [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
            [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
            [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
            [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
            [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
            [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
            [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
            [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
            [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
            [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
            [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
            [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
            [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
        ]
        self.field_width = len(self.game_field[0])
        self.field_height = len(self.game_field)
        self.is_exist_block = False

    def __create_initial_field_row_value(self) -> list[int]:
        return [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2]

    def check_lined_up(self) -> Optional[LineUp]:
        count = 0
        start_y = -1

        for y in range(self.field_height):
            if self.game_field[y] == self.LINE_UP_BLOCK_FIELD_ROW_VALUE:
                count = count + 1
                if start_y == -1:
                    start_y = y

        if start_y != -1:
            return FieldManager.LineUp(start_position_y=start_y, count=count)

        return None

    def take_down(self, line_up: LineUp) -> None:
        current_game_field = copy.deepcopy(self.game_field)
        for position_y in range(line_up.start_position_y):
            self.game_field[position_y +
                            line_up.count] = current_game_field[position_y]

    def erase_the_blocks_lined_up(self, line_up: LineUp) -> None:
        erase_start_position_y = line_up.start_position_y
        for index in range(line_up.count):
            self.game_field[erase_start_position_y +
                            index] = self.__create_initial_field_row_value()

    def put_blocks(self, block_manager: BlockManager) -> None:
        block_current_state = block_manager.current_state()
        for vertical_index in range(block_manager.block_unit):
            for horizontal_index in range(block_manager.block_unit):
                if block_current_state[vertical_index][horizontal_index] == self.FIELD_STATE_BLOCK:
                    self.game_field[block_manager.y + vertical_index][block_manager.x +
                                                                      horizontal_index] = self.FIELD_STATE_BLOCK
        self.is_exist_block = True

    def clear_blocks(self) -> None:
        for y in range(self.field_height):
            for x in range(self.field_width):
                if self.game_field[y][x] == self.FIELD_STATE_BLOCK:
                    self.game_field[y][x] = self.FIELD_STATE_NONE

    def cheng_block_to_stone(self) -> None:
        for y in range(self.field_height):
            for x in range(self.field_width):
                if self.game_field[y][x] == self.FIELD_STATE_BLOCK:
                    self.game_field[y][x] = self.FIELD_STATE_STONE
                    self.is_exist_block = False


class FieldView:
    def __init__(self, field_manager: FieldManager, unit_size: int, root: Tk) -> None:
        self.field_manager: FieldManager = field_manager
        self.unit_size: int = unit_size
        self.root = root
        self.canvas: Canvas = tkinter.Canvas(
            root,
            width=self.unit_size * self.field_manager.field_width,
            height=self.unit_size * self.field_manager.field_height,
            background="white"
        )
        self.canvas.pack()

    def __draw_one_block(self, color: str, x: int, y: int, margin: int) -> None:
        start_x = x * self.unit_size
        start_y = y * self.unit_size
        self.canvas.create_rectangle(
            start_x + margin,
            start_y + margin,
            start_x + self.unit_size - margin,
            start_y + self.unit_size - margin,
            fill=color
        )

    def draw_field(self) -> None:
        self.canvas.delete("all")
        for y in range(self.field_manager.field_height):
            for x in range(self.field_manager.field_width):
                if self.field_manager.game_field[y][x] == FieldManager.FIELD_STATE_BLOCK:
                    self.__draw_one_block(color="orange", x=x, y=y, margin=0)
                if self.field_manager.game_field[y][x] == FieldManager.FIELD_STATE_STONE:
                    self.__draw_one_block(color="skyblue", x=x, y=y, margin=0)
                if self.field_manager.game_field[y][x] == FieldManager.FIELD_STATE_WALL:
                    self.__draw_one_block(color="grey", x=x, y=y, margin=0)


class CollideJudgement:
    def __init__(self, game_field: list[list[int]]) -> None:
        self.game_field = game_field

    def __is_collide_by_values(self, values: list[list[int]], x: int, y: int, block_unit: int) -> bool:
        for vertical_index in range(block_unit):
            for horizontal_index in range(block_unit):
                if values[vertical_index][horizontal_index] == FieldManager.FIELD_STATE_BLOCK:
                    field_state = self.game_field[y +
                                                  vertical_index][x + horizontal_index]
                    if field_state == FieldManager.FIELD_STATE_WALL or field_state == FieldManager.FIELD_STATE_STONE:
                        return True
        return False

    def is_bottom_collide(self, block_manager: BlockManager) -> bool:
        return self.__is_collide_by_values(
            values=block_manager.current_state(),
            x=block_manager.x,
            y=block_manager.y+1,
            block_unit=block_manager.block_unit
        )

    def is_top_collide(self, block_manager: BlockManager) -> bool:
        return self.__is_collide_by_values(
            values=block_manager.current_state(),
            x=block_manager.x,
            y=block_manager.y-1,
            block_unit=block_manager.block_unit
        )

    def is_left_collide(self, block_manager: BlockManager) -> bool:
        return self.__is_collide_by_values(
            values=block_manager.current_state(),
            x=block_manager.x-1,
            y=block_manager.y,
            block_unit=block_manager.block_unit
        )

    def is_right_collide(self, block_manager: BlockManager) -> bool:
        return self.__is_collide_by_values(
            values=block_manager.current_state(),
            x=block_manager.x+1,
            y=block_manager.y,
            block_unit=block_manager.block_unit
        )

    def is_rotate_collide(self, block_manager: BlockManager) -> bool:
        rotate_pattern_values = [
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0]
        ]
        for y in range(block_manager.block_unit):
            for x in range(block_manager.block_unit):
                rotate_pattern_values[y][x] = block_manager.current_state()[
                    (block_manager.block_unit - 1) - x][y]
        return self.__is_collide_by_values(values=rotate_pattern_values, x=x, y=y, block_unit=block_manager.block_unit)

    def is_collide(self, block_manager: BlockManager) -> bool:
        return self.__is_collide_by_values(
            values=block_manager.current_state(),
            x=block_manager.x,
            y=block_manager.y,
            block_unit=block_manager.block_unit
        )


class GameTaskManager:
    KEY_MOVE_LEFT = "a"
    KEY_MOVE_RIGHT = "d"
    KEY_ROTATE = "r"
    KEY_GAME_FINISH = "f"
    is_move_left = False
    is_move_right = False
    is_rotate = False
    line_up: Optional[FieldManager.LineUp] = None
    is_complete_take_down = True
    frame_count = 0
    is_game_over = False

    def __init__(self, field_manager: FieldManager, root: Tk) -> None:
        self.field_manager = field_manager
        self.collide_judgement = CollideJudgement(field_manager.game_field)
        self.block_manager: BlockManager
        self.root = root
        self.root.bind("<KeyPress>", self.key_press)

    def key_press(self, e: Event) -> None:
        if e.char == self.KEY_MOVE_LEFT:
            self.is_move_left = True
            self.is_move_right = False
            self.is_rotate = False
        if e.char == self.KEY_MOVE_RIGHT:
            self.is_move_left = False
            self.is_move_right = True
            self.is_rotate = False
        if e.char == self.KEY_ROTATE:
            self.is_move_left = False
            self.is_move_right = False
            self.is_rotate = True
        if e.char == self.KEY_GAME_FINISH:
            self.is_game_over = True

    def updateTask(self) -> None:
        if not self.is_complete_take_down:
            self.field_manager.take_down(self.line_up)
            self.is_complete_take_down = True
            self.line_up = None
            return
        else:
            self.line_up = self.field_manager.check_lined_up()
        if self.line_up != None:
            self.field_manager.erase_the_blocks_lined_up(self.line_up)
            self.is_complete_take_down = False
            return
        if not self.field_manager.is_exist_block:
            self.block_manager = BlockManager(
                block_unit=BLOCK_UNIT, field_width=FIELD_WIDTH-2)
            if self.collide_judgement.is_collide(self.block_manager):
                self.is_game_over = True
                self.field_manager.put_blocks(self.block_manager)
        self.move_block_to_rotate()
        self.move_block_to_left()
        self.move_block_to_right()
        if self.frame_count % 5 == 0:
            self.move_block_to_down()
        self.frame_count = self.frame_count + 1

    def move_block_to_down(self) -> None:
        if self.collide_judgement.is_bottom_collide(self.block_manager):
            self.field_manager.cheng_block_to_stone()
        else:
            self.block_manager.move_down()
            self.field_manager.clear_blocks()
            self.field_manager.put_blocks(self.block_manager)

    def move_block_to_left(self) -> None:
        if not self.is_move_left:
            return
        if not self.collide_judgement.is_left_collide(self.block_manager):
            self.block_manager.move_left()
            self.field_manager.clear_blocks()
            self.field_manager.put_blocks(self.block_manager)
        self.is_move_left = False

    def move_block_to_right(self) -> None:
        if not self.is_move_right:
            return
        if not self.collide_judgement.is_right_collide(self.block_manager):
            self.block_manager.move_right()
            self.field_manager.clear_blocks()
            self.field_manager.put_blocks(self.block_manager)
        self.is_move_right = False

    def move_block_to_rotate(self) -> None:
        if not self.is_rotate:
            return
        if not self.collide_judgement.is_rotate_collide(self.block_manager):
            self.block_manager.update_rotate()
            self.field_manager.clear_blocks()
            self.field_manager.put_blocks(self.block_manager)
        self.is_rotate = False


class GameRoop:
    def __init__(self) -> None:
        self.root = tkinter.Tk()
        self.field_manager = FieldManager()
        self.game_task_manager = GameTaskManager(
            field_manager=self.field_manager,
            root=self.root
        )
        self.field_view = FieldView(
            field_manager=self.field_manager,
            unit_size=VIEW_UNIT_SIZE,
            root=self.root
        )

    def start(self) -> None:
        while not self.game_task_manager.is_game_over:
            sleep(0.1)
            self.update()
            self.field_view.root.update()
        self.root.mainloop()
        self.root.quit()

    def update(self) -> None:
        self.game_task_manager.updateTask()
        self.field_view.draw_field()


game_roop = GameRoop()
game_roop.start()
