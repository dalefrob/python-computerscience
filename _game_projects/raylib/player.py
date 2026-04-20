from pyray import *
import math

LOOK_SENSITIVITY = 0.003
GRAVITY = 9.0
FLOOR_Y = 0.0
JUMP_STRENGTH = 5.0

class Player:

    forward = Vector3(0, 0, -1)
    up = Vector3(0, 1, 0)

    def __init__(self, position = Vector3(0,0,0), gamemap = None):
        self.gamemap = gamemap
        self.position = position
        self.rotation_angle : float = 0.0
        self.look_rotation = Vector2(0, 0)
        self.speed = 3.0
        self.turn_speed = 24.0
        self.velocity = Vector3(0,0,0)
        self.on_floor = False

        self.camera = Camera3D(
            self.position,
            vector3_add(self.position, self.forward),
            self.up,
            60.0,
            CameraProjection.CAMERA_PERSPECTIVE
        )

    def get_bounding_box(self, offset = Vector3(0,0,0)):
        min = vector3_add(self.position, Vector3(-0.2, -0.4, -0.2))
        min = vector3_add(min, offset)
        max = vector3_add(self.position, Vector3(0.2, 0.4, 0.2))
        max = vector3_add(max, offset)
        return BoundingBox(min, max)

    def rotate(self, amount):
        self.rotation_angle -= amount

    def check_map_collision(self, offset) -> bool:
        if not self.gamemap: return False

        map = self.gamemap
        half = Vector3(0.5, 0.5, 0.5)
        mybbox = self.get_bounding_box(offset)

        for y in range(len(map)):
            for x in range(len(map[y])):
                if map[y][x] == 1:
                    wall_pos = Vector3(x, 0, y)
                    min = vector3_subtract(wall_pos, half)
                    max = vector3_add(wall_pos, half)
                    bbox = BoundingBox(min, max)
                    if check_collision_boxes(mybbox, bbox):
                        return True
        return False
    
    def get_aabb_penetration(self, offset=Vector3(0, 0, 0)):
        """
        Returns a correction Vector3 to push the player out of any overlapping walls.
        Returns zero vector if no collision.
        """
        if not self.gamemap:
            return Vector3(0, 0, 0)

        correction = Vector3(0, 0, 0)
        half = Vector3(0.5, 0.5, 0.5)
        mybbox = self.get_bounding_box(offset)

        for y in range(len(self.gamemap)):
            for x in range(len(self.gamemap[y])):
                if self.gamemap[y][x] != 1:
                    continue

                wall_pos = Vector3(x, 0, y)
                bbox = BoundingBox(
                    vector3_subtract(wall_pos, half),
                    vector3_add(wall_pos, half)
                )

                if not check_collision_boxes(mybbox, bbox):
                    continue

                # Overlap on each axis
                overlap_x = min(mybbox.max.x, bbox.max.x) - max(mybbox.min.x, bbox.min.x)
                overlap_z = min(mybbox.max.z, bbox.max.z) - max(mybbox.min.z, bbox.min.z)

                # Push out along the axis of least penetration
                if overlap_x < overlap_z:
                    # Push in X
                    if mybbox.min.x < bbox.min.x:
                        correction.x -= overlap_x
                    else:
                        correction.x += overlap_x
                else:
                    # Push in Z
                    if mybbox.min.z < bbox.min.z:
                        correction.z -= overlap_z
                    else:
                        correction.z += overlap_z

        return correction

    def update(self):
        dt = get_frame_time()
        direction = Vector3(0, 0, 0)

        # --- Mouse look ---
        # Accumulate raw mouse delta into a 2D look_rotation vector.
        # x = yaw (left/right), y = pitch (up/down)
        delta = get_mouse_delta()
        self.look_rotation = vector2_subtract(self.look_rotation, delta)

        # Clamp pitch accumulator to just under 90 degrees to prevent gimbal flip.
        # We clamp the raw pixel accumulator, not the angle, so we divide by sensitivity.
        MAX_PITCH = (math.pi / 2 - 0.001) / LOOK_SENSITIVITY
        self.look_rotation.y = clamp(self.look_rotation.y, -MAX_PITCH, MAX_PITCH)

        # Convert accumulated yaw pixels to an angle and rotate the base forward
        # vector around the world up axis to get a flat horizontal facing direction.
        yaw_angle = (self.look_rotation.x * LOOK_SENSITIVITY) % (2 * math.pi)
        forward_direction = vector3_rotate_by_axis_angle(self.forward, self.up, yaw_angle)

        # Right vector is perpendicular to forward in the horizontal plane.
        # Cross product of forward x up gives the right-hand side direction.
        right_direction = vector3_cross_product(forward_direction, self.up)

        # Pitch the forward direction up/down around the right axis.
        # This is only used for the camera target — movement stays flat.
        pitch_angle = self.look_rotation.y * LOOK_SENSITIVITY
        pitch_vector = vector3_rotate_by_axis_angle(forward_direction, right_direction, pitch_angle)

        # --- Input ---
        # Accumulate a wish direction from WASD.
        # We only use X/Z components of the facing vectors so movement stays flat
        # regardless of where the player is looking vertically.
        if is_key_down(KeyboardKey.KEY_W):
            direction.x += forward_direction.x
            direction.z += forward_direction.z
        if is_key_down(KeyboardKey.KEY_S):
            direction.x -= forward_direction.x
            direction.z -= forward_direction.z
        if is_key_down(KeyboardKey.KEY_A):
            direction.x -= right_direction.x
            direction.z -= right_direction.z
        if is_key_down(KeyboardKey.KEY_D):
            direction.x += right_direction.x
            direction.z += right_direction.z

        # --- Jump ---
        # Read on_floor from last frame before resetting it.
        # is_key_pressed only fires on the frame the key goes down, preventing hold-to-fly.
        if is_key_pressed(KeyboardKey.KEY_SPACE) and self.on_floor:
            self.velocity.y = JUMP_STRENGTH

        # Reset on_floor — it must be re-earned by a collision check this frame.
        # This correctly detects the moment the player walks off an edge.
        self.on_floor = False

        # --- XZ velocity ---
        # Recompute horizontal velocity from input each frame so it feels responsive.
        # Y velocity is intentionally left alone here — it persists across frames
        # so gravity and jump momentum accumulate correctly.
        if vector3_length(direction) > 0:
            move = vector3_scale(vector3_normalize(direction), self.speed)
            self.velocity.x = move.x
            self.velocity.z = move.z
        else:
            self.velocity.x = 0
            self.velocity.z = 0

        # --- Gravity ---
        # Accumulate downward acceleration into Y velocity each frame.
        # We check velocity.y > 0 (ascending) rather than on_floor (which is False
        # at this point) so gravity doesn't bleed into the frame a jump starts on.
        self.velocity.y -= GRAVITY * dt

        # --- Collision ---
        # Test each axis independently using the next-frame displacement as an offset.
        # Separating axes allows sliding along walls instead of stopping dead.

        # X: probe one axis at a time with the scaled displacement
        if self.check_map_collision(Vector3(self.velocity.x * dt, 0, 0)):
            self.velocity.x = 0

        # Z: same approach
        if self.check_map_collision(Vector3(0, 0, self.velocity.z * dt)):
            self.velocity.z = 0

        # Y: only test downward movement for landing — upward is handled separately
        # to prevent the floor geometry eating jump impulse on the launch frame.
        if self.velocity.y < 0 and self.check_map_collision(Vector3(0, self.velocity.y * dt, 0)):
            self.on_floor = True
            self.velocity.y = 0

        # Ceiling: if moving upward and hitting something, kill upward velocity.
        if self.velocity.y > 0 and self.check_map_collision(Vector3(0, self.velocity.y * dt, 0)):
            self.velocity.y = 0

        # --- Apply velocity ---
        # Multiply by dt here (not earlier) so velocity is in units/second throughout.
        self.position = vector3_add(self.position, vector3_scale(self.velocity, dt))

        # --- Floor fallback ---
        # Flat floor at FLOOR_Y as a safety net in case there's no floor geometry.
        # Runs after position update so we clamp the final position, not a prediction.
        if self.position.y <= FLOOR_Y:
            self.position.y = FLOOR_Y
            self.velocity.y = 0
            self.on_floor = True

        # --- Camera ---
        # Position follows the player origin. Target uses the pitched look vector
        # so vertical mouse movement tilts the view without affecting movement.
        self.camera.position = self.position
        self.camera.target = vector3_add(self.position, pitch_vector)