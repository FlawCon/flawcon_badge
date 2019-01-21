from fcb import Event, RESOLUTION


class App:
    def __init__(self):
        self.circle_radius = 10
        self.circle_x = 0
        self.circle_y = 0
        self.changed = False

    def change_x(self, n):
        new_x = self.circle_x + n
        new_x = max(new_x, self.circle_radius)
        new_x = min(new_x, RESOLUTION[0][0] - self.circle_radius)
        self.circle_x = new_x
        self.changed = True

    def change_y(self, n):
        new_y = self.circle_y + n
        new_y = max(new_y, self.circle_radius)
        new_y = min(new_y, RESOLUTION[0][1] - self.circle_radius)
        self.circle_y = new_y
        self.changed = True

    def change_radius(self, n):
        new_radius = self.circle_radius + n
        new_radius = max(new_radius, 0)
        new_radius = min(new_radius, 50)
        self.circle_radius = new_radius
        self.changed = True

    def handle_event(self, evt):
        if evt.is_special:
            if evt.special == Event.UP:
                self.change_x(-1)
            elif evt.special == Event.DOWN:
                self.change_x(1)
            elif evt.special == Event.LEFT:
                self.change_y(-1)
            elif evt.special == Event.RIGHT:
                self.change_y(1)
            elif evt.special == Event.BUTTON_A:
                self.change_radius(1)
            elif evt.special == Event.BUTTON_B:
                self.change_radius(-1)

    def redraw(self, gfx):
        if self.changed:
            gfx.fill_rect(0, 0, RESOLUTION[0][0], RESOLUTION[0][1])
            gfx.circle(self.circle_x, self.circle_y, self.circle_radius, 1)
            self.changed = False
            return True
        return False
