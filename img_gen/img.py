from PIL import Image, ImageDraw, ImageFont
import random
import math

def get_img(num_slices):
    # Größe des Bildes
    WIDTH, HEIGHT = 4000, 4000

    # Farben
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)

    # Erstelle ein leeres Bild
    image = Image.new("RGB", (WIDTH, HEIGHT), WHITE)
    draw = ImageDraw.Draw(image)

    # Zeichne das Zirkusrad
    center_x, center_y = WIDTH // 2, HEIGHT // 2
    radius = min(center_x, center_y) - 50
    angle_per_slice = 360 / num_slices

    font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 60)  # Beispiel-Pfad zur Schriftart

    text_radius = radius + 50  # Abstand der Zahlen zum Rand

    for i in range(num_slices):
        start_angle = i * angle_per_slice
        end_angle = (i + 1) * angle_per_slice
        color = tuple(random.randint(0, 255) for _ in range(3))  # Zufällige Farbe
        draw.pieslice(
            (center_x - radius, center_y - radius, center_x + radius, center_y + radius),
            start_angle,
            end_angle,
            fill=color,
            outline=BLACK,
        )

        # Berechne den Mittelpunkt des Sektors für die Position der Zahl
        sector_middle_angle = (start_angle + end_angle) / 2
        sector_middle_radians = math.radians(sector_middle_angle)
        text_x = center_x + int(text_radius * math.cos(sector_middle_radians))
        text_y = center_y + int(text_radius * math.sin(sector_middle_radians))

        # draw.text((text_x, text_y), str(i+1), font=font, fill=BLACK)

    # Speichere das Bild als PNG
    image.save("spin.png")

# Anzahl der Sektoren im Kreis
# num_slices = 12  # Hier kannst du die Anzahl der Sektoren anpassen
# get_img(num_slices)
