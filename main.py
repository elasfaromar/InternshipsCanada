import pygame
import sys
import csv
import webbrowser

# Initialize Pygame
pygame.init()

# Set up the display
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Internships Canada")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIGHT_BLUE = (173, 216, 230)
DARK_GRAY = (169, 169, 169)

# Fonts
font = pygame.font.SysFont(None, 40)
small_font = pygame.font.SysFont(None, 30)

# Function to draw text on the Pygame surface
def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

# Function to display buttons
def draw_button(button, surface):
    if button["rect"].collidepoint(pygame.mouse.get_pos()):
        pygame.draw.rect(surface, button["hover_color"], button["rect"])
    else:
        pygame.draw.rect(surface, button["color"], button["rect"])
    draw_text(button["label"], small_font, BLACK, surface, button["rect"].x + 10, button["rect"].y + 10)

# Function to load internship data from a CSV file
def load_internships_from_file(file_path):
    internships = []
    try:
        with open(file_path, 'r') as file:
            reader = csv.reader(file)
            # Skip the header row if there is one
            next(reader)  # Comment this out if the CSV doesn't have a header
            for row in reader:
                # Each row is already split by commas
                internships.append(row)
    except FileNotFoundError:
        print(f"Error: {file_path} not found.")
    return internships


# Function to display internship listings (updated to show 3 at a time)
def draw_internships(surface, internships, start_index):
    draw_text("Internship Listings", font, BLACK, surface, 50, 50)
    y_offset = 100  # Starting Y position for the first job listing
    end_index = min(start_index + 3, len(internships))  # Show only 3 listings

    for i in range(start_index, end_index):
        company = internships[i][0]
        location = internships[i][1]
        title = internships[i][2]
        link = internships[i][3]
        age = internships[i][4]

        draw_text("%.60s" % (title), small_font, BLACK, surface, 100, y_offset)
        draw_text("%.25s - %.25s" % (company, location), small_font, BLACK, surface, 100, y_offset + 30)
        draw_text(f"{age}", small_font, DARK_GRAY, surface, 100, y_offset + 60)

        # Create a clickable button for the link
        link_rect = pygame.Rect(100, y_offset + 90, 200, 30)  # Button rectangle
        pygame.draw.rect(surface, LIGHT_BLUE, link_rect)  # Draw the button
        draw_text(f"Open Link", small_font, WHITE, surface, link_rect.x + 5, link_rect.y + 5)  # Draw text on the button


        # Store link info for later click detection
        link_buttons.append((link_rect, link))  # Save the button and corresponding link

        # Adjust y_offset for the next listing
        y_offset += 140

# Function to check for button clicks and open links
def handle_link_clicks():
    mouse_pos = pygame.mouse.get_pos()
    mouse_click = pygame.mouse.get_pressed()

    if mouse_click[0]:  # Left mouse button clicked
        for rect, url in link_buttons:
            if rect.collidepoint(mouse_pos):  # If the click is on a link button
                webbrowser.open(url)  # Open the link in a web browser

# Buttons and their positions (for the main menu)
buttons = [
    {"label": "Find Internships", "rect": pygame.Rect(300, 150, 250, 50), "color": LIGHT_BLUE, "hover_color": DARK_GRAY},
    #{"label": "Browse Listings", "rect": pygame.Rect(300, 230, 250, 50), "color": LIGHT_BLUE, "hover_color": DARK_GRAY},
    #{"label": "Create Resume", "rect": pygame.Rect(300, 310, 250, 50), "color": LIGHT_BLUE, "hover_color": DARK_GRAY},
    #{"label": "Apply & Track", "rect": pygame.Rect(300, 390, 250, 50), "color": LIGHT_BLUE, "hover_color": DARK_GRAY},
]

# Main loop
def main():
    current_page = "menu"  # State to track whether we're on the menu or showing internships
    internships = load_internships_from_file('canada_1.csv')  # Load internships from the text file
    start_index = 0  # Tracks the first internship to display
    
    # Initialize the list for link buttons
    global link_buttons
    link_buttons = []

    # Arrow button rectangles
    left_arrow = pygame.Rect(50, screen_height - 80, 60, 40)
    right_arrow = pygame.Rect(screen_width - 110, screen_height - 80, 60, 40)

    # Back button (on the internship listings page)
    back_button = {"label": "Back", "rect": pygame.Rect(0, 0, 100, 40), "color": LIGHT_BLUE, "hover_color": DARK_GRAY}

    running = True
    while running:
        screen.fill(WHITE)  # Background color

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if current_page == "menu":
                    # Check for button clicks only on the menu page
                    for button in buttons:
                        if button["rect"].collidepoint(mouse_pos):
                            if button["label"] == "Find Internships":
                                current_page = "internships"  # Switch to internship listings
                elif current_page == "internships":
                    # Handle navigation clicks
                    if left_arrow.collidepoint(mouse_pos):
                        # Move back in the list if possible
                        if start_index > 0:
                            start_index -= 1
                    if right_arrow.collidepoint(mouse_pos):
                        # Move forward in the list if possible
                        if start_index < len(internships) - 3:
                            start_index += 1
                    # Handle back button click
                    if back_button["rect"].collidepoint(mouse_pos):
                        current_page = "menu"  # Go back to the main menu

        if current_page == "menu":
            # Draw the menu buttons
            draw_text("Internships Canada", font, BLACK, screen, 50, 50)
            for button in buttons:
                draw_button(button, screen)
        elif current_page == "internships":
            # Clear previous link_buttons and redraw internship listings (only 3 at a time)
            link_buttons = []
            draw_internships(screen, internships, start_index)

            # Draw navigation arrows
            pygame.draw.rect(screen, DARK_GRAY, left_arrow)
            draw_text("<", small_font, WHITE, screen, left_arrow.x + 15, left_arrow.y + 5)

            pygame.draw.rect(screen, DARK_GRAY, right_arrow)
            draw_text(">", small_font, WHITE, screen, right_arrow.x + 15, right_arrow.y + 5)

            # Draw the back button
            draw_button(back_button, screen)

        # Check for link clicks
        handle_link_clicks()

        # Update display
        pygame.display.flip()

if __name__ == "__main__":
    main()
