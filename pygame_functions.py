import pygame

def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

def draw_img_on_rect(screen, path_to_img, left, top, width, height):
    img = pygame.image.load(path_to_img)
    img = pygame.transform.scale(img, (width, height))
    screen.blit(img, (left, top))

def draw_transparent_img(screen, path_to_img, left, top, width, height):
    img = pygame.image.load(path_to_img)
    img = pygame.transform.scale(img, (width, height))
    img.set_alpha(160)
    screen.blit(img, (left, top))

def draw_checkmark_on_menu(screen, menu_rect):
    confirm_rect = pygame.Rect(menu_rect.left + menu_rect.width / 2 - 25, menu_rect.top + menu_rect.height - 70, 50, 50)
    draw_img_on_rect(screen, f'images/Assets/CheckMark.png', confirm_rect.left, confirm_rect.top, confirm_rect.width, confirm_rect.height)

    return confirm_rect