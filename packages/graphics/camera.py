from pygame import Vector2

from .const import DRAW_SCREEN_SIZE_X, DRAW_SCREEN_SIZE_Y, CAMERA_OFFSET_MOVE_AREA, \
    MAP_SIZE_PX_X, MAP_SIZE_PX_Y, CAMERA_OFFSET_SPEED

from .mouse import Mouse

class Camera:
    def __init__(self):
        self.__mouse = Mouse()
        self.__camera_offset = Vector2(0, 0)
        self.__dest_camera_offset = Vector2(0, 0)
        self.__real_camera_offset = Vector2(0, 0)

    def update(self):
        self.__mouse.update()
        self.__update_camera_offset()

    def get_offset(self):
        return self.__camera_offset

    def __update_camera_offset(self):
        
        if self.__mouse.pos.x > DRAW_SCREEN_SIZE_X - CAMERA_OFFSET_MOVE_AREA:
            self.__dest_camera_offset.x -= CAMERA_OFFSET_SPEED
        elif self.__mouse.pos.x < CAMERA_OFFSET_MOVE_AREA:
            self.__dest_camera_offset.x += CAMERA_OFFSET_SPEED

        if self.__mouse.pos.y > DRAW_SCREEN_SIZE_Y - CAMERA_OFFSET_MOVE_AREA:
            self.__dest_camera_offset.y -= CAMERA_OFFSET_SPEED
        elif self.__mouse.pos.y < CAMERA_OFFSET_MOVE_AREA:
            self.__dest_camera_offset.y += CAMERA_OFFSET_SPEED

        self.__dest_camera_offset.x = max(
            self.__dest_camera_offset.x, -(MAP_SIZE_PX_X - DRAW_SCREEN_SIZE_X))
        self.__dest_camera_offset.y = max(
            self.__dest_camera_offset.y, -(MAP_SIZE_PX_Y - DRAW_SCREEN_SIZE_Y))
        self.__dest_camera_offset.x = min(self.__dest_camera_offset.x, 0)
        self.__dest_camera_offset.y = min(self.__dest_camera_offset.y, 0)

        self.__real_camera_offset += (self.__dest_camera_offset - self.__real_camera_offset) / 20
        self.__camera_offset = Vector2(
            int(self.__real_camera_offset.x), int(self.__real_camera_offset.y)) 