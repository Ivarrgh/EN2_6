import os
import ast
import pandas as pd
import numpy as np
import pygame
import pygame_gui

# os.getcwd()
# os.chdir('/Users/jael/Desktop/SCHOOL/cv1014/archive')

metadata = pd.read_csv('movies_metadata.csv', low_memory=False)

pygame.init()

pygame.display.set_caption('Movie Recommendator')
screen = pygame.display.set_mode((800, 600))

background = pygame.Surface((800, 600))
background.fill(pygame.Color('#191919'))

main_manager = pygame_gui.UIManager(
    (800, 600), '/Users/jael/Desktop/SCHOOL/cv1014/theme_two.json')
top_movie_manager = pygame_gui.UIManager(
    (800, 600), '/Users/jael/Desktop/SCHOOL/cv1014/theme_one.json')
top_movie_manager_2 = pygame_gui.UIManager(
    (800, 600), '/Users/jael/Desktop/SCHOOL/cv1014/theme_one.json')
movie_genre_manager = pygame_gui.UIManager(
    (800, 600), '/Users/jael/Desktop/SCHOOL/cv1014/theme_one.json')
movie_genre_manager_2 = pygame_gui.UIManager(
    (800, 600), '/Users/jael/Desktop/SCHOOL/cv1014/theme_one.json')
production_manager = pygame_gui.UIManager(
    (800, 600), '/Users/jael/Desktop/SCHOOL/cv1014/theme_one.json')
production_manager_2 = pygame_gui.UIManager(
    (800, 600), '/Users/jael/Desktop/SCHOOL/cv1014/theme_one.json')
release_date_manager = pygame_gui.UIManager(
    (800, 600), '/Users/jael/Desktop/SCHOOL/cv1014/theme_one.json')
release_date_manager_2 = pygame_gui.UIManager(
    (800, 600), '/Users/jael/Desktop/SCHOOL/cv1014/theme_one.json')
login_manager = pygame_gui.UIManager(
    (800, 600), '/Users/jael/Desktop/SCHOOL/cv1014/theme_one.json')


def weighted_rating(x):
    v = x['vote_count']
    r = x['vote_average']
    c = metadata['vote_average'].mean()
    m = metadata['vote_count'].quantile(0.9)

    return ((v/(v+m) * r) + (m/(m+v) * c))


def conversion(data):
    array = []
    for row in data:
        array.append(row['name'])
    return array


def series(x):
    return pd.Series(x, dtype=object)


FONT = pygame.font.Font(None, 32)
COLOR_INACTIVE = pygame.Color('lightskyblue3')
COLOR_ACTIVE = pygame.Color('dodgerblue2')


class InputBox:

    def __init__(self, x, y, w, h, text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = COLOR_INACTIVE
        self.text = text
        self.entered_pass = ''
        self.txt_surface = FONT.render(text, True, self.color)
        self.active = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.active = False
            # Change the current color of the input box.
            self.color = COLOR_ACTIVE if self.active else COLOR_INACTIVE
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    print(self.text)

                    if (self.text == password):
                        admin = True

                    print(self.text)
                    print(admin)
                    self.text = ''
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                # Re-render the text.
                self.txt_surface = FONT.render(self.text, True, self.color)

    def getPass(self):
        return self.entered_pass

    def update(self):
        # Resize the box if the text is too long.
        width = max(200, self.txt_surface.get_width()+10)
        self.rect.w = width

    def draw(self, screen):
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        # Blit the rect.
        pygame.draw.rect(screen, self.color, self.rect, 2)


shownMovies = metadata.copy(
).loc[metadata['vote_count'] >= metadata['vote_count'].quantile(0.9)]
shownMovies['wr'] = shownMovies.apply(weighted_rating, axis=1)
shownMovies = shownMovies.sort_values('wr', ascending=False).head(200)

shownMovies['genres'] = shownMovies['genres'].apply(ast.literal_eval)
shownMovies['genres'] = shownMovies['genres'].apply(conversion)
shownMovies['production_companies'] = shownMovies['production_companies'].apply(
    ast.literal_eval)
shownMovies['production_companies'] = shownMovies['production_companies'].apply(
    conversion)
shownMovies['year'] = pd.to_datetime(metadata['release_date'], errors='coerce').apply(
    lambda x: str(x).split('-')[0] if x != np.nan else np.nan)

s = shownMovies.genres.apply(series).stack().reset_index(level=1, drop=True)
s.name = 'genre'
shownMovies_gen = shownMovies.drop('genres', axis=1).join(s)

studio = shownMovies.production_companies.apply(
    series).stack().reset_index(level=1, drop=True)
studio.name = 'studioS'
shownMovies_prod = shownMovies.drop(
    'production_companies', axis=1).join(studio)

l = shownMovies.year.apply(series).stack().reset_index(level=1, drop=True)
l.name = 'year'
shownMovies_yr = shownMovies.drop('year', axis=1).join(l)

manager = {
    "LOGIN": login_manager,
    "MAIN": main_manager,
    "TOP_MOVIE": top_movie_manager,
    "TOP_MOVIE_2": top_movie_manager_2,
    "MOVIE_GENRE": movie_genre_manager,
    "MOVIE_GENRE_2": movie_genre_manager_2,
    "PRODUCTION": production_manager,
    "PRODUCTION_2": production_manager_2,
    "RELEASE_DATE": release_date_manager,
    "RELEASE_DATE_2": release_date_manager_2
}

menu_title = pygame_gui.elements.ui_label.UILabel(text="NOTFLIX",
                                                  relative_rect=pygame.Rect(
                                                      (0, 200), (800, 50)),
                                                  manager=main_manager)
menu_title_2 = pygame_gui.elements.ui_text_box.UITextBox(html_text="<font size='3.5' color='#ffffff'><em>Anytime, Anywhere</em></font>", relative_rect=pygame.Rect((322, 260), (155, 50)),
                                                         manager=main_manager)


login_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((50, 50), (240, 50)),
                                            text='Login',
                                            manager=main_manager)

view_top_movie = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((280, 300), (240, 50)),
                                              text='View Top Movies',
                                              manager=main_manager)

view_num_title = pygame_gui.elements.ui_label.UILabel(text="How many movies do you want to see?",
                                                      relative_rect=pygame.Rect(
                                                          (175, 170), (450, 40)),
                                                      manager=top_movie_manager)
view_10 = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((300, 250), (180, 40)),
                                       text='top 10',
                                       manager=top_movie_manager)
view_20 = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((300, 300), (180, 40)),
                                       text='top 20',
                                       manager=top_movie_manager)
view_50 = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((300, 350), (180, 40)),
                                       text='top 50',
                                       manager=top_movie_manager)
view_100 = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((300, 400), (180, 40)),
                                        text='top 100',
                                        manager=top_movie_manager)
back_main_1 = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((100, 500), (100, 40)),
                                           text='Back',
                                           manager=top_movie_manager)
back_menu_1 = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((100, 500), (100, 40)),
                                           text='Back',
                                           manager=top_movie_manager_2)


top_movie_genres = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((280, 350), (240, 50)),
                                                text='Filter By Genres',
                                                manager=main_manager)
view_gen_title = pygame_gui.elements.ui_label.UILabel(text="Choose a genre to explore.",
                                                      relative_rect=pygame.Rect(
                                                          (175, 170), (450, 40)),
                                                      manager=movie_genre_manager)
view_rom = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((310, 250), (180, 40)),
                                        text='romance',
                                        manager=movie_genre_manager)
view_cri = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((310, 300), (180, 40)),
                                        text='crime',
                                        manager=movie_genre_manager)
view_thr = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((310, 350), (180, 40)),
                                        text='thriller',
                                        manager=movie_genre_manager)
view_com = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((310, 400), (180, 40)),
                                        text='comedy',
                                        manager=movie_genre_manager)
view_ani = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((310, 450), (180, 40)),
                                        text='animation',
                                        manager=movie_genre_manager)
view_mys = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((310, 500), (180, 40)),
                                        text='mystery',
                                        manager=movie_genre_manager)
back_main_2 = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((100, 500), (100, 40)),
                                           text='Back',
                                           manager=movie_genre_manager)
back_menu_2 = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((100, 500), (100, 40)),
                                           text='Back',
                                           manager=movie_genre_manager_2)


production_studio = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((280, 400), (240, 50)),
                                                 text='Filter By Production Studios',
                                                 manager=main_manager)
view_ps_title = pygame_gui.elements.ui_label.UILabel(text="Choose the studio whose",
                                                     relative_rect=pygame.Rect(
                                                         (225, 150), (350, 40)),
                                                     manager=production_manager)
view_ps_title_2 = pygame_gui.elements.ui_label.UILabel(text="movie you want to see.",
                                                       relative_rect=pygame.Rect(
                                                           (225, 190), (350, 40)),
                                                       manager=production_manager)
view_wd = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((310, 275), (180, 40)),
                                       text='Walt Disney',
                                       manager=production_manager)
view_wb = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((310, 325), (180, 40)),
                                       text='Warner Brothers',
                                       manager=production_manager)
view_up = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((310, 375), (180, 40)),
                                       text='Universal Pictures',
                                       manager=production_manager)
back_main_3 = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((100, 500), (100, 40)),
                                           text='Back',
                                           manager=production_manager)
back_menu_3 = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((100, 500), (100, 40)),
                                           text='Back',
                                           manager=production_manager_2)

release_dates = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((280, 450), (240, 50)),
                                             text='Filter By Released Years',
                                             manager=main_manager)
view_rd_title = pygame_gui.elements.ui_label.UILabel(text="Choose to view top movies",
                                                     relative_rect=pygame.Rect(
                                                         (225, 150), (350, 40)),
                                                     manager=release_date_manager)
view_rd_title_2 = pygame_gui.elements.ui_label.UILabel(text="produced within each year.",
                                                       relative_rect=pygame.Rect(
                                                           (225, 190), (350, 40)),
                                                       manager=release_date_manager)
view_yrs = pygame_gui.elements.ui_drop_down_menu.UIDropDownMenu(options_list=["2017", "2016", "2015", "2014", "2013", "2012", "2011", "2010", "2009", "2008", "2007", "2006", "2005", "2004", "2003", "2002", "2001", "2000"],
                                                                starting_option="Select a Year",
                                                                relative_rect=pygame.Rect(
                                                                    (280, 300), (240, 50)),
                                                                manager=release_date_manager,
                                                                expansion_height_limit=200)


back_main_4 = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((100, 500), (100, 40)),
                                           text='Back',
                                           manager=release_date_manager)
back_menu_4 = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((100, 500), (100, 40)),
                                           text='Back',
                                           manager=release_date_manager_2)
login_back_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((100, 500), (100, 40)),
                                                 text='Back',
                                                 manager=login_manager)
login_title = pygame_gui.elements.ui_label.UILabel(text="Login",
                                                   relative_rect=pygame.Rect(
                                                       (0, 200), (800, 50)),
                                                   manager=login_manager)
password_input = InputBox(280, 300, 240, 50)


clock = pygame.time.Clock()
password = "1234"
admin = False
is_running = True
current_screen = "MAIN"


while is_running:
    time_delta = clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False

        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED:
                if event.text == "2017":
                    current_screen = "RELEASE_DATE_2"
                    x = shownMovies_yr[shownMovies_yr.year == '2017']

                    yr = ''
                    count = 1
                    for row in x[['title']].head(10).iterrows():
                        yr += str(count) + '. ' + row[1].title + '<br>'
                        count += 1

                    results = pygame_gui.elements.UITextBox(yr, relative_rect=pygame.Rect((280, 150), (260, 300)),
                                                            manager=release_date_manager_2)

                elif event.text == "2016":
                    current_screen = "RELEASE_DATE_2"
                    x = shownMovies_yr[shownMovies_yr.year == '2016']

                    yr = ''
                    count = 1
                    for row in x[['title']].head(10).iterrows():
                        yr += str(count) + '. ' + row[1].title + '<br>'
                        count += 1

                    results = pygame_gui.elements.UITextBox(yr, relative_rect=pygame.Rect((280, 150), (260, 300)),
                                                            manager=release_date_manager_2)
                elif event.text == "2015":
                    current_screen = "RELEASE_DATE_2"
                    x = shownMovies_yr[shownMovies_yr.year == '2015']

                    yr = ''
                    count = 1
                    for row in x[['title']].head(10).iterrows():
                        yr += str(count) + '. ' + row[1].title + '<br>'
                        count += 1

                    results = pygame_gui.elements.UITextBox(yr, relative_rect=pygame.Rect((280, 150), (260, 300)),
                                                            manager=release_date_manager_2)
                elif event.text == "2014":
                    current_screen = "RELEASE_DATE_2"
                    x = shownMovies_yr[shownMovies_yr.year == '2014']

                    yr = ''
                    count = 1
                    for row in x[['title']].head(10).iterrows():
                        yr += str(count) + '. ' + row[1].title + '<br>'
                        count += 1

                    results = pygame_gui.elements.UITextBox(yr, relative_rect=pygame.Rect((280, 150), (260, 300)),
                                                            manager=release_date_manager_2)

                elif event.text == "2013":
                    current_screen = "RELEASE_DATE_2"
                    x = shownMovies_yr[shownMovies_yr.year == '2013']

                    yr = ''
                    count = 1
                    for row in x[['title']].head(10).iterrows():
                        yr += str(count) + '. ' + row[1].title + '<br>'
                        count += 1

                    results = pygame_gui.elements.UITextBox(yr, relative_rect=pygame.Rect((280, 150), (260, 300)),
                                                            manager=release_date_manager_2)

                elif event.text == "2012":
                    current_screen = "RELEASE_DATE_2"
                    x = shownMovies_yr[shownMovies_yr.year == '2012']

                    yr = ''
                    count = 1
                    for row in x[['title']].head(10).iterrows():
                        yr += str(count) + '. ' + row[1].title + '<br>'
                        count += 1

                    results = pygame_gui.elements.UITextBox(yr, relative_rect=pygame.Rect((280, 150), (260, 300)),
                                                            manager=release_date_manager_2)

                elif event.text == "2011":
                    current_screen = "RELEASE_DATE_2"
                    x = shownMovies_yr[shownMovies_yr.year == '2011']

                    yr = ''
                    count = 1
                    for row in x[['title']].head(10).iterrows():
                        yr += str(count) + '. ' + row[1].title + '<br>'
                        count += 1

                    results = pygame_gui.elements.UITextBox(yr, relative_rect=pygame.Rect((280, 150), (260, 300)),
                                                            manager=release_date_manager_2)

                elif event.text == "2010":
                    current_screen = "RELEASE_DATE_2"
                    x = shownMovies_yr[shownMovies_yr.year == '2010']

                    yr = ''
                    count = 1
                    for row in x[['title']].head(10).iterrows():
                        yr += str(count) + '. ' + row[1].title + '<br>'
                        count += 1

                    results = pygame_gui.elements.UITextBox(yr, relative_rect=pygame.Rect((280, 150), (260, 300)),
                                                            manager=release_date_manager_2)

                elif event.text == "2009":
                    current_screen = "RELEASE_DATE_2"
                    x = shownMovies_yr[shownMovies_yr.year == '2009']

                    yr = ''
                    count = 1
                    for row in x[['title']].head(10).iterrows():
                        yr += str(count) + '. ' + row[1].title + '<br>'
                        count += 1

                    results = pygame_gui.elements.UITextBox(yr, relative_rect=pygame.Rect((280, 150), (260, 300)),
                                                            manager=release_date_manager_2)

                elif event.text == "2008":
                    current_screen = "RELEASE_DATE_2"
                    x = shownMovies_yr[shownMovies_yr.year == '2008']

                    yr = ''
                    count = 1
                    for row in x[['title']].head(10).iterrows():
                        yr += str(count) + '. ' + row[1].title + '<br>'
                        count += 1

                    results = pygame_gui.elements.UITextBox(yr, relative_rect=pygame.Rect((280, 150), (260, 300)),
                                                            manager=release_date_manager_2)

                elif event.text == "2007":
                    current_screen = "RELEASE_DATE_2"
                    x = shownMovies_yr[shownMovies_yr.year == '2007']

                    yr = ''
                    count = 1
                    for row in x[['title']].head(10).iterrows():
                        yr += str(count) + '. ' + row[1].title + '<br>'
                        count += 1

                    results = pygame_gui.elements.UITextBox(yr, relative_rect=pygame.Rect((280, 150), (260, 300)),
                                                            manager=release_date_manager_2)

                elif event.text == "2006":
                    current_screen = "RELEASE_DATE_2"
                    x = shownMovies_yr[shownMovies_yr.year == '2006']

                    yr = ''
                    count = 1
                    for row in x[['title']].head(10).iterrows():
                        yr += str(count) + '. ' + row[1].title + '<br>'
                        count += 1

                    results = pygame_gui.elements.UITextBox(yr, relative_rect=pygame.Rect((280, 150), (260, 300)),
                                                            manager=release_date_manager_2)

                elif event.text == "2005":
                    current_screen = "RELEASE_DATE_2"
                    x = shownMovies_yr[shownMovies_yr.year == '2005']

                    yr = ''
                    count = 1
                    for row in x[['title']].head(10).iterrows():
                        yr += str(count) + '. ' + row[1].title + '<br>'
                        count += 1

                    results = pygame_gui.elements.UITextBox(yr, relative_rect=pygame.Rect((280, 150), (260, 300)),
                                                            manager=release_date_manager_2)

                elif event.text == "2004":
                    current_screen = "RELEASE_DATE_2"
                    x = shownMovies_yr[shownMovies_yr.year == '2004']

                    yr = ''
                    count = 1
                    for row in x[['title']].head(10).iterrows():
                        yr += str(count) + '. ' + row[1].title + '<br>'
                        count += 1

                    results = pygame_gui.elements.UITextBox(yr, relative_rect=pygame.Rect((280, 150), (260, 300)),
                                                            manager=release_date_manager_2)

                elif event.text == "2003":
                    current_screen = "RELEASE_DATE_2"
                    x = shownMovies_yr[shownMovies_yr.year == '2003']

                    yr = ''
                    count = 1
                    for row in x[['title']].head(10).iterrows():
                        yr += str(count) + '. ' + row[1].title + '<br>'
                        count += 1

                    results = pygame_gui.elements.UITextBox(yr, relative_rect=pygame.Rect((280, 150), (260, 300)),
                                                            manager=release_date_manager_2)

                elif event.text == "2002":
                    current_screen = "RELEASE_DATE_2"
                    x = shownMovies_yr[shownMovies_yr.year == '2002']

                    yr = ''
                    count = 1
                    for row in x[['title']].head(10).iterrows():
                        yr += str(count) + '. ' + row[1].title + '<br>'
                        count += 1

                    results = pygame_gui.elements.UITextBox(yr, relative_rect=pygame.Rect((280, 150), (260, 300)),
                                                            manager=release_date_manager_2)

                elif event.text == "2001":
                    current_screen = "RELEASE_DATE_2"
                    x = shownMovies_yr[shownMovies_yr.year == '2001']

                    yr = ''
                    count = 1
                    for row in x[['title']].head(10).iterrows():
                        yr += str(count) + '. ' + row[1].title + '<br>'
                        count += 1

                    results = pygame_gui.elements.UITextBox(yr, relative_rect=pygame.Rect((280, 150), (260, 300)),
                                                            manager=release_date_manager_2)

                elif event.text == "2000":
                    current_screen = "RELEASE_DATE_2"
                    x = shownMovies_yr[shownMovies_yr.year == '2000']

                    yr = ''
                    count = 1
                    for row in x[['title']].head(10).iterrows():
                        yr += str(count) + '. ' + row[1].title + '<br>'
                        count += 1

                    results = pygame_gui.elements.UITextBox(yr, relative_rect=pygame.Rect((280, 150), (260, 300)),
                                                            manager=release_date_manager_2)

            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == view_top_movie:
                    current_screen = "TOP_MOVIE"

                elif event.ui_element == view_10:
                    current_screen = "TOP_MOVIE_2"
                    top_movie_manager_2.clear_and_reset()
                    top_10 = ''
                    count = 1
                    for row in shownMovies[['title']].head(10).iterrows():
                        top_10 += str(count) + '. ' + row[1].title + '<br>'
                        count += 1
                    results = pygame_gui.elements.UITextBox(top_10, relative_rect=pygame.Rect((280, 150), (260, 300)),
                                                            manager=top_movie_manager_2)
                    back_menu_1 = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((100, 500), (100, 40)),
                                                               text='Back',
                                                               manager=top_movie_manager_2)

                elif event.ui_element == view_20:
                    current_screen = "TOP_MOVIE_2"
                    top_movie_manager_2.clear_and_reset()
                    top_20 = ''
                    count = 1
                    for row in shownMovies[['title']].head(20).iterrows():
                        top_20 += str(count) + '. ' + row[1].title + '<br>'
                        count += 1
                    results = pygame_gui.elements.UITextBox(top_20, relative_rect=pygame.Rect((280, 150), (260, 300)),
                                                            manager=top_movie_manager_2)
                    back_menu_1 = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((100, 500), (100, 40)),
                                                               text='Back',
                                                               manager=top_movie_manager_2)

                elif event.ui_element == view_50:
                    current_screen = "TOP_MOVIE_2"
                    top_movie_manager_2.clear_and_reset()
                    top_50 = ''
                    count = 1
                    for row in shownMovies[['title']].head(50).iterrows():
                        top_50 += str(count) + '. ' + row[1].title + '<br>'
                        count += 1
                    results = pygame_gui.elements.UITextBox(top_50, relative_rect=pygame.Rect((280, 150), (260, 300)),
                                                            manager=top_movie_manager_2)
                    back_menu_1 = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((100, 500), (100, 40)),
                                                               text='Back',
                                                               manager=top_movie_manager_2)

                elif event.ui_element == view_100:
                    current_screen = "TOP_MOVIE_2"
                    top_movie_manager_2.clear_and_reset()
                    top_100 = ''
                    count = 1
                    for row in shownMovies[['title']].head(100).iterrows():
                        top_100 += str(count) + '. ' + row[1].title + '<br>'
                        count += 1
                    results = pygame_gui.elements.UITextBox(top_100, relative_rect=pygame.Rect((280, 150), (260, 300)),
                                                            manager=top_movie_manager_2)
                    back_menu_1 = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((100, 500), (100, 40)),
                                                               text='Back',
                                                               manager=top_movie_manager_2)

                elif event.ui_element == top_movie_genres:
                    current_screen = "MOVIE_GENRE"

                elif event.ui_element == view_rom:
                    current_screen = "MOVIE_GENRE_2"
                    x = shownMovies_gen[shownMovies_gen.genre == 'Romance'].sort_values(
                        'wr', ascending=False)

                    rom = ''
                    count = 1
                    for row in x[['title']].head(10).iterrows():
                        rom += str(count) + '. ' + row[1].title + '<br>'
                        count += 1

                    results_rom = pygame_gui.elements.UITextBox(rom, relative_rect=pygame.Rect((280, 150), (260, 300)),
                                                                manager=movie_genre_manager_2)

                elif event.ui_element == view_cri:
                    current_screen = "MOVIE_GENRE_2"
                    x = shownMovies_gen[shownMovies_gen.genre == 'Crime'].sort_values(
                        'wr', ascending=False)

                    cri = ''
                    count = 1
                    for row in x[['title']].head(10).iterrows():
                        cri += str(count) + '. ' + row[1].title + '<br>'
                        count += 1

                    results_cri = pygame_gui.elements.UITextBox(cri, relative_rect=pygame.Rect((280, 150), (260, 300)),
                                                                manager=movie_genre_manager_2)

                elif event.ui_element == view_thr:
                    current_screen = "MOVIE_GENRE_2"
                    x = shownMovies_gen[shownMovies_gen.genre == 'Thriller'].sort_values(
                        'wr', ascending=False)

                    thr = ''
                    count = 1
                    for row in x[['title']].head(10).iterrows():
                        thr += str(count) + '. ' + row[1].title + '<br>'
                        count += 1

                    results_thr = pygame_gui.elements.UITextBox(thr, relative_rect=pygame.Rect((280, 150), (260, 300)),
                                                                manager=movie_genre_manager_2)

                elif event.ui_element == view_ani:
                    current_screen = "MOVIE_GENRE_2"
                    x = shownMovies_gen[shownMovies_gen.genre == 'Animation'].sort_values(
                        'wr', ascending=False)

                    ani = ''
                    count = 1
                    for row in x[['title']].head(10).iterrows():
                        ani += str(count) + '. ' + row[1].title + '<br>'
                        count += 1

                    results_ani = pygame_gui.elements.UITextBox(ani, relative_rect=pygame.Rect((280, 150), (260, 300)),
                                                                manager=movie_genre_manager_2)

                elif event.ui_element == view_mys:
                    current_screen = "MOVIE_GENRE_2"
                    x = shownMovies_gen[shownMovies_gen.genre == 'Mystery'].sort_values(
                        'wr', ascending=False)

                    mys = ''
                    count = 1
                    for row in x[['title']].head(10).iterrows():
                        mys += str(count) + '. ' + row[1].title + '<br>'
                        count += 1

                    results_mys = pygame_gui.elements.UITextBox(mys, relative_rect=pygame.Rect((280, 150), (260, 300)),
                                                                manager=movie_genre_manager_2)

                elif event.ui_element == view_com:
                    current_screen = "MOVIE_GENRE_2"
                    x = shownMovies_gen[shownMovies_gen.genre == 'Romance'].sort_values(
                        'wr', ascending=False)

                    com = ''
                    count = 1
                    for row in x[['title']].head(10).iterrows():
                        com += str(count) + '. ' + row[1].title + '<br>'
                        count += 1

                    results_com = pygame_gui.elements.UITextBox(com, relative_rect=pygame.Rect((280, 150), (260, 300)),
                                                                manager=movie_genre_manager_2)

                elif event.ui_element == production_studio:
                    current_screen = "PRODUCTION"

                elif event.ui_element == view_wd:
                    current_screen = "PRODUCTION_2"
                    x = shownMovies_prod[shownMovies_prod.studioS == "Walt Disney Pictures"].sort_values(
                        'wr', ascending=False)

                    wd = ''
                    count = 1
                    for row in x[['title']].head(10).iterrows():
                        wd += str(count) + '. ' + row[1].title + '<br>'
                        count += 1

                    results_wd = pygame_gui.elements.UITextBox(wd, relative_rect=pygame.Rect((280, 150), (260, 300)),
                                                               manager=production_manager_2)

                elif event.ui_element == view_wb:
                    current_screen = "PRODUCTION_2"
                    x = shownMovies_prod[shownMovies_prod.studioS == "Warner Bros."].sort_values(
                        'wr', ascending=False)

                    wb = ''
                    count = 1
                    for row in x[['title']].head(10).iterrows():
                        wb += str(count) + '. ' + row[1].title + '<br>'
                        count += 1

                    results_wb = pygame_gui.elements.UITextBox(wb, relative_rect=pygame.Rect((280, 150), (260, 300)),
                                                               manager=production_manager_2)

                elif event.ui_element == view_up:
                    current_screen = "PRODUCTION_2"
                    x = shownMovies_prod[shownMovies_prod.studioS == "Universal Pictures"].sort_values(
                        'wr', ascending=False)

                    up = ''
                    count = 1
                    for row in x[['title']].head(10).iterrows():
                        up += str(count) + '. ' + row[1].title + '<br>'
                        count += 1

                    results_up = pygame_gui.elements.UITextBox(up, relative_rect=pygame.Rect((280, 150), (260, 300)),
                                                               manager=production_manager_2)

                elif event.ui_element == login_button:
                    current_screen = "LOGIN"
                    logintitle = login_title
                    loginback = login_back_button
                    done = False
                    while not done:
                        for event in pygame.event.get():
                            password_input.handle_event(event)
                            password_input.update()

                        screen.fill((30, 30, 30))
                        password_input.draw(screen)
                        pygame.display.flip()
                        clock.tick(30)

                elif event.ui_element == back_main_1 or event.ui_element == back_main_2 or event.ui_element == back_main_3 or event.ui_element == back_main_4 or event.ui_element == login_back_button:
                    current_screen = "MAIN"

                elif event.ui_element == back_menu_1:
                    current_screen = "TOP_MOVIE"

                elif event.ui_element == back_menu_2:
                    current_screen = "MOVIE_GENRE"

                elif event.ui_element == back_menu_3:
                    current_screen = "PRODUCTION"

                elif event.ui_element == back_menu_4:
                    current_screen = "RELEASE_DATE"

        manager[current_screen].process_events(event)

    manager[current_screen].update(time_delta)

    screen.blit(background, (0, 0))
    manager[current_screen].draw_ui(screen)

    pygame.display.update()
pygame.quit()
