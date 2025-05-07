import cv2
import numpy as np


class ImageClickZoom:
    def order_points_clockwise(self, pts):
        rect = np.zeros((4, 2), dtype="float32")
        pts = np.array(pts)
        s = pts.sum(axis=1)
        rect[0] = pts[np.argmin(s)]
        rect[2] = pts[np.argmax(s)]
        diff = np.diff(pts, axis=1)
        rect[1] = pts[np.argmin(diff)]
        rect[3] = pts[np.argmax(diff)]
        return rect

    def __init__(self, image, scale_init=0.5, screen_w=None, screen_h=None):
        self.image = image
        self.original = image.copy()
        self.scale = scale_init
        self.min_scale = 0.1
        self.max_scale = 3.0
        self.offset = [0, 0]
        self.drag_start = None
        self.window_name = "Click 4 Corners - Zoom & Drag (press q to quit)"
        self.clicked_points = []
        self.screen_w = screen_w
        self.screen_h = screen_h

    def show(self):
        cv2.namedWindow(self.window_name)
        cv2.setMouseCallback(self.window_name, self.mouse_callback)
        disp_h, disp_w = int(self.image.shape[0] * self.scale), int(self.image.shape[1] * self.scale)
        win_x = max((self.screen_w - disp_w) // 2, 0)
        win_y = max((self.screen_h - disp_h) // 2, 0)
        cv2.moveWindow(self.window_name, win_x, win_y)

        while True:
            disp_img = self.get_display_image()
            for pt in self.clicked_points:
                x, y = self.world_to_screen(pt)
                cv2.circle(disp_img, (x, y), 5, (0, 0, 255), -1)
            cv2.imshow(self.window_name, disp_img)
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q') or len(self.clicked_points) == 4:
                break
        cv2.destroyWindow(self.window_name)
        return self.clicked_points

    def get_display_image(self):
        h, w = self.image.shape[:2]
        view = cv2.resize(self.image, (int(w * self.scale), int(h * self.scale)))
        return view

    def world_to_screen(self, pt):
        return (int(pt[0] * self.scale), int(pt[1] * self.scale))

    def screen_to_world(self, x, y):
        return (int(x / self.scale), int(y / self.scale))

    def mouse_callback(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            world_pt = self.screen_to_world(x, y)
            if len(self.clicked_points) < 4:
                self.clicked_points.append(world_pt)
                print(f"Point {len(self.clicked_points)}: {world_pt}")
        elif event == cv2.EVENT_MOUSEWHEEL:
            if flags > 0:
                self.scale *= 1.1
            else:
                self.scale *= 0.9
            self.scale = max(self.min_scale, min(self.scale, self.max_scale))
        elif event == cv2.EVENT_RBUTTONDOWN:
            self.drag_start = (x, y)
        elif event == cv2.EVENT_MOUSEMOVE and self.drag_start:
            dx = x - self.drag_start[0]
            dy = y - self.drag_start[1]
            self.offset[0] += dx
            self.offset[1] += dy
            self.drag_start = (x, y)
        elif event == cv2.EVENT_RBUTTONUP:
            self.drag_start = None