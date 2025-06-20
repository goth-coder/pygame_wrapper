# Game Components for the Pygame Wrapper
import math
import random

import pygame
import pymunk

# Ball
BALL_COLOR = (220, 40, 40)  # More natural red
BALL_EDGE_COLOR = (120, 0, 0)
BALL_HIGHLIGHT_COLOR = (255, 255, 255, 60)

# Colors
BROWN = (150, 100, 50)
DARK_BROWN = (100, 60, 20)
GRAY = (200, 200, 200)
DARK_GRAY = (100, 100, 100)

# Crate
CRATE_SIZE_MULTIPLIER = 10
CRATE_X_COLOR = (255, 0, 0)  # Red for the "X" on the crate

# Domino
DOMINO_COLOR = (230, 230, 230)  # Light concrete
DOMINO_EDGE_COLOR = (80, 80, 80)

# Lever
LEVER_LEFT_RATIO = 0.4
LEVER_RIGHT_RATIO = 0.6
LEVER_COLLISION_TYPE = 2  # Unique collision type for the lever

# Seesaw
SEESAW_COLOR = (160, 170, 180)  # Steel base
SEESAW_EDGE_COLOR = (90, 100, 110)
SEESAW_PIVOT_COLOR = (60, 60, 60)


class Ball:
    """
    Represents a ball in a Pymunk physics space.
    Args:
        space: The Pymunk space to add the ball to.
        x (float): The x-coordinate of the ball's position.
        y (float): The y-coordinate of the ball's position.
        radius (int, optional): The radius of the ball. Defaults to 15.
    Attributes:
        body: The Pymunk body of the ball.
        shape: The Pymunk shape of the ball.
        radius: The radius of the ball.
    Methods:
        draw(screen): Draws the ball on the given Pygame screen.
    """

    def __init__(self, space, x, y, radius=15):
        mass = 10
        moment = pymunk.moment_for_circle(mass, 0, radius)
        self.body = pymunk.Body(mass, moment)
        self.body.position = (x, y)
        self.shape = pymunk.Circle(self.body, radius)
        self.shape.elasticity = 1.0
        self.shape.friction = 0.5
        self.shape.collision_type = 1
        space.add(self.body, self.shape)
        self.radius = radius

        ## Pre-render the rock texture
        # Create a "rock canvas" surface
        self.image = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
        center = (radius, radius)

        # Base color
        pygame.draw.circle(self.image, BALL_COLOR, center, radius)

        # Irregular edge stroke
        pygame.draw.circle(self.image, BALL_EDGE_COLOR, center, radius, 2)
        # Add subtle highlight
        pygame.draw.circle(
            self.image, BALL_HIGHLIGHT_COLOR, (radius - 4, radius - 4), radius // 3
        )

    def draw(self, surface):
        """
        Draws the rotated image of the object onto the given surface based on its current position and angle.
        """
        angle_degrees = math.degrees(self.body.angle)  # radians to degrees

        # Rotate the image
        rotated_image = pygame.transform.rotate(self.image, -angle_degrees)

        # Place the center of the image at the projectile physical position
        rect = rotated_image.get_rect(
            center=(int(self.body.position.x), int(self.body.position.y))
        )

        # Draw the rotated image
        surface.blit(rotated_image, rect)


class Catapult:
    """
    A class representing a simple catapult arm using pymunk physics.
    Attributes:
        space: The pymunk.Space object for physics simulation.
        pivot: The (x, y) position of the catapult's pivot point.
        stick_length: Length of the catapult arm.
        stick_thickness: Thickness of the catapult arm.
    Methods:
        create_arm(): Initializes the catapult arm and attaches it to the space.
        draw(screen): Draws the catapult arm and base on the given pygame screen.
    """

    def __init__(self, space, pivot, stick_length=150, stick_thickness=5):
        self.space = space
        self.pivot = pivot
        self.stick_length = stick_length
        self.stick_thickness = stick_thickness
        self.mass, self.base_w, self.base_h = 500, 80, 20
        self.moment = pymunk.moment_for_segment(
            self.mass, (0, 0), (-stick_length, 0), stick_thickness
        )
        self.create_arm()

    def create_arm(self):
        """
        Creates the arm body and its shapes, adds them to the simulation space, and attaches the arm to a pivot joint.
        """

        # Create the arm body and shape
        self.arm_body = pymunk.Body(self.mass, self.moment)
        self.arm_body.position = self.pivot
        self.arm_body.angular_velocity = 46
        self.arm_shape = pymunk.Segment(
            self.arm_body, (0, 0), (-self.stick_length, 0), self.stick_thickness
        )
        self.arm_shape.friction = 0.8

        # Create a stopper shape at the tip
        self.stopper_shape = pymunk.Segment(
            self.arm_body,
            (-self.stick_length, 0),
            (-self.stick_length - 15, -25),
            self.stick_thickness,
        )
        self.stopper_shape.friction, self.stopper_shape.elasticity = 0.5, 0.2

        # Create another stopper before the tip
        self.stopper_shape2 = pymunk.Segment(
            self.arm_body,
            (-self.stick_length + 20, 0),
            (-self.stick_length + 35, -25),
            self.stick_thickness,
        )
        self.stopper_shape2.friction, self.stopper_shape2.elasticity = 0.5, 0.2

        self.space.add(
            self.arm_body, self.arm_shape, self.stopper_shape, self.stopper_shape2
        )

        # Pivot joint to keep the arm attached to the pivot point
        self.space.add(
            pymunk.PivotJoint(self.arm_body, self.space.static_body, self.pivot)
        )

    def draw(self, screen):
        """
        Draws a stylized catapult with improved visuals.
        """

        # Draw arm and stoppers with a darker border (fake shadow)
        for shape, color in [
            (self.arm_shape, BROWN),
            (self.stopper_shape, DARK_BROWN),
            (self.stopper_shape2, DARK_BROWN),
        ]:
            a = self.arm_body.local_to_world(shape.a)
            b = self.arm_body.local_to_world(shape.b)

            # Shadow/border
            pygame.draw.line(screen, (60, 40, 20), a, b, self.stick_thickness + 5)
            # Main colored beam
            pygame.draw.line(screen, color, a, b, self.stick_thickness + 3)

        # Draw base with border effect
        base_x, base_y = (
            self.pivot[0] - self.base_w // 2,
            self.pivot[1] - self.base_h // 2,
        )
        base_rect = pygame.Rect(base_x, base_y, self.base_w, self.base_h)
        pygame.draw.rect(screen, (90, 50, 20), base_rect.inflate(4, 4))  # border
        pygame.draw.rect(screen, BROWN, base_rect)  # main base

        # Add bolts on the base
        for dx in [-self.base_w // 3, 0, self.base_w // 3]:
            bolt_center = (self.pivot[0] + dx, base_y + self.base_h - 16)
            pygame.draw.circle(screen, GRAY, bolt_center, 4)

        # Draw wheels with layered shading
        for dx in [-30, 30]:
            center = (self.pivot[0] + dx, self.pivot[1] + 15)
            pygame.draw.circle(screen, DARK_GRAY, center, 10)  # outer tire
            pygame.draw.circle(screen, GRAY, center, 7)  # metal hub
            pygame.draw.circle(screen, (220, 220, 220), center, 3)  # bolt center

        # Optional: add a metal tip to the throwing arm
        tip_pos = self.arm_body.local_to_world(self.arm_shape.b)
        pygame.draw.circle(screen, (120, 120, 120), tip_pos, 5)


class Crate:
    """
    Represents a physics-based crate with mass, size, and drawing capabilities for use in a Pymunk simulation.
    """

    def __init__(self, space, position, mass=1):
        self.mass = mass
        self.size = mass * CRATE_SIZE_MULTIPLIER
        moment = pymunk.moment_for_box(mass, (self.size * 2, self.size * 2))
        self.body = pymunk.Body(mass, moment)
        self.body.position = position

        # Create a box shape for the crate
        self.shape = pymunk.Poly.create_box(self.body, (self.size * 2, self.size * 2))
        self.shape.elasticity = 0.6
        self.shape.friction = 0.8
        space.add(self.body, self.shape)

    def draw(self, surface):
        """
        Draws the object's shape onto the given surface, including an "X" on the crate.
        Args:
            surface: The Pygame surface to draw on.
        """
        pts = [self.body.local_to_world(v) for v in self.shape.get_vertices()]
        pygame.draw.polygon(surface, DARK_BROWN, pts)
        pygame.draw.lines(surface, BROWN, True, pts, 2)

        # Draw an "X" on the crate
        if len(pts) == 4:
            pygame.draw.line(surface, CRATE_X_COLOR, pts[0], pts[2], 3)
            pygame.draw.line(surface, CRATE_X_COLOR, pts[1], pts[3], 3)

    def draw_mass_label(self, surface):
        """
        Draws the mass label above the object's position on the given surface.
        """
        font = pygame.font.SysFont("Arial", 20)

        x, y = self.body.position
        label = font.render(f"{self.mass} kg", True, GRAY)
        surface.blit(label, (x - label.get_width() // 2, y - self.size * 2 - 10))


class Domino:
    def __init__(self, space, x, y, width=15, height=100):
        """
        Initialize a rectangular object in the given Pymunk space at (x, y) with specified width and height.
        """
        mass = 10
        moment = pymunk.moment_for_box(mass, (width, height))
        self.body = pymunk.Body(mass, moment)
        self.body.position = (x, y)
        self.shape = pymunk.Poly.create_box(self.body, (width, height))
        self.shape.elasticity = 0.4
        self.shape.friction = 0.8
        space.add(self.body, self.shape)
        self.width = width
        self.height = height

    def draw(self, screen):
        """
        Draws the rotated rectangle (domino) on the given Pygame screen.
        Args:
            screen: The Pygame surface to draw on.
        """
        half_w = self.width / 2
        half_h = self.height / 2
        corners = [
            (-half_w, -half_h),
            (half_w, -half_h),
            (half_w, half_h),
            (-half_w, half_h),
        ]
        rotated_corners = []
        for x, y in corners:
            rot_x = x * math.cos(self.body.angle) - y * math.sin(self.body.angle)
            rot_y = x * math.sin(self.body.angle) + y * math.cos(self.body.angle)
            rot_x += self.body.position.x
            rot_y += self.body.position.y
            rotated_corners.append((rot_x, rot_y))

        # Draw the domino
        pygame.draw.polygon(screen, DOMINO_COLOR, rotated_corners)
        pygame.draw.polygon(screen, DOMINO_EDGE_COLOR, rotated_corners, 2)


class Lever:
    def __init__(
        self,
        space,
        pivot_point,
        length,
        thickness,
        load,
        effort,
        mass=10.0,
    ):
        """
        Initialize a lever object with a pivot point, length, thickness, and mass in the given Pymunk space.
        """

        self.length = length
        self.thickness = thickness
        self.mass = mass
        self.pivot_point = pivot_point
        self.load = load
        self.effort = effort
        left_length = length * LEVER_LEFT_RATIO
        right_length = length * LEVER_RIGHT_RATIO

        moment = pymunk.moment_for_segment(
            mass, (-left_length, 0), (right_length, 0), thickness
        )

        self.body = pymunk.Body(self.mass, moment)
        self.body.position = pivot_point
        self.shape = pymunk.Segment(
            self.body, (-left_length, 0), (right_length, 0), thickness
        )

        self.shape.friction = 0.8
        self.shape.collision_type = LEVER_COLLISION_TYPE
        # Create holder shapes at specified offsets from the left tip (manually, no loop)
        # Holder 1
        holder1 = pymunk.Segment(
            self.body,
            (-self.length * LEVER_LEFT_RATIO + -5, 5),
            (-self.length * LEVER_LEFT_RATIO + -5, -20),
            self.thickness,
        )
        holder1.friction, holder1.elasticity = 0.5, 0.2

        # Calculate local positions for load and effort
        load_x = self.load.body.position.x
        effort_x = self.effort.body.position.x
        lever_x = self.body.position.x

        load_local_x = load_x - lever_x
        effort_local_x = effort_x - lever_x

        load_half_width = self.load.size
        effort_half_width = self.effort.size

        # Holder 2
        holder2 = pymunk.Segment(
            self.body,
            (load_local_x + load_half_width + 5, 5),
            (load_local_x + load_half_width + 5, -20),
            self.thickness,
        )
        holder2.friction, holder2.elasticity = 0.5, 0.2

        # Holder 3
        holder3 = pymunk.Segment(
            self.body,
            (effort_local_x - effort_half_width - 5, 5),
            (effort_local_x - effort_half_width - 5, -20),
            self.thickness,
        )
        holder3.friction, holder3.elasticity = 0.5, 0.2

        # Holder 4
        holder4 = pymunk.Segment(
            self.body,
            (-self.length * LEVER_LEFT_RATIO + 355, 5),
            (-self.length * LEVER_LEFT_RATIO + 355, -20),
            self.thickness - 5,  # Tiny correction for the last holder
        )
        holder4.friction, holder4.elasticity = 0.5, 0.2

        holder4.collision_type = LEVER_COLLISION_TYPE

        self.holder_shapes = [holder1, holder2, holder3, holder4]

        # For backward compatibility with existing code
        self.holder_shape = self.holder_shapes[0]
        self.holder_shape2 = self.holder_shapes[1]
        self.holder_shape3 = self.holder_shapes[2]
        self.holder_shape4 = self.holder_shapes[3]

        space.add(
            self.body,
            self.shape,
            self.holder_shape,
            self.holder_shape2,
            self.holder_shape3,
            self.holder_shape4,
        )

        pivot_joint = pymunk.PivotJoint(self.body, space.static_body, self.pivot_point)
        space.add(pivot_joint)

    def draw(self, screen):
        """
        Draws a stylized lever with holders.
        """
        for shape in [self.shape] + self.holder_shapes:
            a = self.body.local_to_world(shape.a)
            b = self.body.local_to_world(shape.b)

            # Shadow/border
            pygame.draw.line(screen, DARK_BROWN, a, b, self.thickness + 5)
            # Main colored beam
            pygame.draw.line(screen, BROWN, a, b, self.thickness + 3)


class Platform:
    """
    Represents a static platform in the Pymunk physics space.
    Args:
        space: The Pymunk space to add the platform to.
        x (float): The x-coordinate of the platform's center.
        y (float): The y-coordinate of the platform's center.
        width (int): The width of the platform.
        height (int): The height of the platform.
    """

    def __init__(self, space, x, y, length=100, thickness=20, angle=0):
        self.body = pymunk.Body(body_type=pymunk.Body.STATIC)
        self.body.position = (x, y)
        self.body.angle = math.radians(angle)
        self.length = length
        self.thickness = thickness
        self.shape = pymunk.Poly.create_box(self.body, (length, thickness))
        self.shape.elasticity = 0.4
        self.shape.friction = 0.8
        space.add(self.body, self.shape)

        # Precompute speckles for texture
        padding = 2  # Distance away from edges

        self.speckles = []
        for _ in range(18):
            rx = random.uniform(-self.length / 2 + padding, self.length / 2 - padding)
            ry = random.uniform(
                -self.thickness / 2 + padding, self.thickness / 2 - padding
            )
            color = (
                (random.randint(130, 180),) * 3
                if random.random() < 0.7
                else (80, 80, 80)
            )
            radius = random.randint(1, 2)
            self.speckles.append((rx, ry, color, radius))

    def draw(self, screen):
        half_w = self.length / 2
        half_h = self.thickness / 2
        corners = [
            (-half_w, -half_h),
            (half_w, -half_h),
            (half_w, half_h),
            (-half_w, half_h),
        ]
        rotated_corners = []
        for x, y in corners:
            rot_x = x * math.cos(self.body.angle) - y * math.sin(self.body.angle)
            rot_y = x * math.sin(self.body.angle) + y * math.cos(self.body.angle)
            rot_x += self.body.position.x
            rot_y += self.body.position.y
            rotated_corners.append((rot_x, rot_y))

        # Concrete/asphalt texture: speckles
        pygame.draw.polygon(screen, SEESAW_COLOR, rotated_corners)
        for rx, ry, color, radius in self.speckles:
            # Rotate point
            px = (
                rx * math.cos(self.body.angle)
                - ry * math.sin(self.body.angle)
                + self.body.position.x
            )
            py = (
                rx * math.sin(self.body.angle)
                + ry * math.cos(self.body.angle)
                + self.body.position.y
            )
            pygame.draw.circle(screen, color, (int(px), int(py)), radius)
        pygame.draw.polygon(screen, SEESAW_EDGE_COLOR, rotated_corners, 2)


class Projectile:
    """
    Similar to the Ball, it represents a projectile with a circular shape in a Pymunk physics simulation.
    Attributes:
        radius (int): The radius of the projectile.
        body (pymunk.Body): The physics body of the projectile.
        shape (pymunk.Circle): The shape attached to the body.
    Methods:
        draw(surf): Draws the projectile on the given Pygame surface.
    """

    def __init__(self, space, position, radius=18.5):
        self.space = space
        self.x, self.y = position
        self.radius = radius
        self.mass = 100
        self.on_ground = False  # Track ground contact

        # Create the projectile body and shape
        self.body = pymunk.Body(
            self.mass, pymunk.moment_for_circle(self.mass, 0, radius)
        )
        self.body.position = (self.x, self.y)
        self.shape = pymunk.Circle(self.body, radius)
        self.shape.density, self.shape.elasticity, self.shape.friction = 1, 0.4, 0.8
        space.add(self.body, self.shape)

        ## Pre-render the rock texture
        # Create a "rock canvas" surface
        self.image = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
        center = (radius, radius)

        # Base rock color
        pygame.draw.circle(self.image, (100, 100, 100), center, radius)

        # Irregular edge stroke
        pygame.draw.circle(self.image, (60, 60, 60), center, radius, 2)

        ## Texture details
        # Add random speckles
        for _ in range(12):
            angle = random.uniform(0, 2 * math.pi)
            dist = random.uniform(0, radius * 0.8)
            dot_x = int(center[0] + math.cos(angle) * dist)
            dot_y = int(center[1] + math.sin(angle) * dist)
            pygame.draw.circle(self.image, (70, 70, 70), (dot_x, dot_y), 1)

        # Draw a few random crack lines
        for _ in range(3):
            start_angle = random.uniform(0, 2 * math.pi)
            end_angle = start_angle + random.uniform(0.5, 5.0)
            start = (
                center[0] + math.cos(start_angle) * (radius * 0.4),
                center[1] + math.sin(start_angle) * (radius * 0.4),
            )
            end = (
                center[0] + math.cos(end_angle) * (radius * 0.8),
                center[1] + math.sin(end_angle) * (radius * 0.8),
            )
            pygame.draw.line(self.image, (30, 30, 30), start, end, 2)

    def draw(self, surface):
        """
        Draws the rotated image of the object onto the given surface based on its current position and angle.
        """
        angle_degrees = math.degrees(self.body.angle)  # radians to degrees

        # Rotate the image
        rotated_image = pygame.transform.rotate(self.image, -angle_degrees)

        # Place the center of the image at the projectile physical position
        rect = rotated_image.get_rect(
            center=(int(self.body.position.x), int(self.body.position.y))
        )

        # Draw the rotated image
        surface.blit(rotated_image, rect)


class Seesaw:
    """
    A class representing a seesaw in a 2D physics simulation using pymunk and pygame.
    Attributes:
        body: The pymunk body of the seesaw.
        shape: The pymunk shape of the seesaw.
        pivot: The joint connecting the seesaw to the static body.
        width: The width of the seesaw.
        height: The height of the seesaw.
    Methods:
        draw(screen): Draws the seesaw with a steel texture and pivot on the given pygame screen.
    """

    def __init__(self, space, x, y, width=10, height=150):
        mass = 15
        moment = pymunk.moment_for_box(mass, (width, height))
        self.body = pymunk.Body(mass, moment)
        self.body.position = (x, y)

        self.shape = pymunk.Poly.create_box(self.body, (width, height))
        self.shape.elasticity = 0.4
        self.shape.friction = 0.8
        space.add(self.body, self.shape)
        self.pivot = pymunk.PinJoint(space.static_body, self.body, (x, y), (0, 0))
        space.add(self.pivot)
        limit = pymunk.RotaryLimitJoint(
            space.static_body, self.body, math.radians(-35), math.radians(35)
        )  # radians
        space.add(limit)
        self.width = width
        self.height = height

    def draw(self, screen):
        half_w = self.width / 2
        half_h = self.height / 2
        corners = [
            (-half_w, -half_h),
            (half_w, -half_h),
            (half_w, half_h),
            (-half_w, half_h),
        ]
        rotated_corners = []
        for x, y in corners:
            rot_x = x * math.cos(self.body.angle) - y * math.sin(self.body.angle)
            rot_y = x * math.sin(self.body.angle) + y * math.cos(self.body.angle)
            rot_x += self.body.position.x
            rot_y += self.body.position.y
            rotated_corners.append((rot_x, rot_y))

        # Steel texture: gradient stripes
        for i in range(6):
            frac = i / 5
            color = (
                int(SEESAW_COLOR[0] * (1 - frac) + 220 * frac),
                int(SEESAW_COLOR[1] * (1 - frac) + 220 * frac),
                int(SEESAW_COLOR[2] * (1 - frac) + 220 * frac),
            )
            # Interpolate between two corners for stripe
            x1 = rotated_corners[0][0] * (1 - frac) + rotated_corners[1][0] * frac
            y1 = rotated_corners[0][1] * (1 - frac) + rotated_corners[1][1] * frac
            x2 = rotated_corners[3][0] * (1 - frac) + rotated_corners[2][0] * frac
            y2 = rotated_corners[3][1] * (1 - frac) + rotated_corners[2][1] * frac
            pygame.draw.line(screen, color, (x1, y1), (x2, y2), 3)
        pygame.draw.polygon(screen, SEESAW_EDGE_COLOR, rotated_corners, 2)
        pygame.draw.circle(
            screen,
            SEESAW_PIVOT_COLOR,
            (int(self.body.position.x), int(self.body.position.y)),
            10,
        )


class Trigger:
    """
    Create a static, invisible rectangular trigger at a given position for collision detection.
    Args:
        space: The Pymunk space.
        position: (x, y) center of the trigger.
        width: Width of the trigger area.
        height: Height of the trigger area.
        on_trigger: Callback on collision.
    """

    def __init__(self, space, position, width=40, height=20, on_trigger=None):
        self.space = space
        self.position = position
        self.width = width
        self.height = height
        self.on_trigger = on_trigger  # Custom callback on collision
        center_x = position[0] + width / 2
        center_y = position[1] + height / 2

        self.body = pymunk.Body(body_type=pymunk.Body.STATIC)
        self.body.position = (center_x, center_y)

        self.shape = pymunk.Poly.create_box(self.body, (width, height))
        self.shape.sensor = True
        self.shape.collision_type = 99  # Unique collision type for the trigger

        space.add(self.body, self.shape)

        # Register collision handler
        space.on_collision(1, 99, begin=self._handle_collision)

    def _handle_collision(self, arbiter, space, data):
        if self.on_trigger:
            self.on_trigger(arbiter, space, data)
        self.remove()  # Optional: auto-remove after trigger
        return False  # Prevents physics response

    def remove(self):
        """Remove the trigger from the simulation space."""
        self.space.remove(self.body, self.shape)
