import os
import ast
import pandas as pd
import numpy as np

os.getcwd()
os.chdir('/Users/jael/Desktop/SCHOOL/cv1014/archive')


def setupDataframe():

    global metadata
    metadata = pd.read_csv('./data/movies_metadata.csv',
                           low_memory=False, header=0)

    shownMovies = metadata.copy(
    ).loc[metadata['vote_count'] >= metadata['vote_count'].quantile(0.85)]
    shownMovies['wr'] = shownMovies.apply(weighted_rating, axis=1)
    shownMovies = shownMovies.sort_values('wr', ascending=False)

    shownMovies['genres'] = shownMovies['genres'].apply(ast.literal_eval)
    shownMovies['year'] = pd.to_datetime(metadata['release_date'], errors='coerce').apply(
        lambda x: str(x).split('-')[0] if x != np.nan else np.nan)

    return shownMovies


def menu():
    print("""
          1: VIEW TOP MOVIES
          2: TOP MOVIES BY GENRE
          3: TOP MOVIES BY LANGUAGE
          4: TOP MOVIES BY YEAR
          5: BASED ON OTHER MOVIES YOU'VE LIKED
          6: EXIT """)


def menu2():
    print("""
          1: ENGLISH
          2: FRENCH
          3: CHINESE""")


def weighted_rating(x):
    v = x['vote_count']
    r = x['vote_average']
    c = metadata['vote_average'].mean().astype(int)
    m = metadata['vote_count'].quantile(0.9)

    return ((v/(v+m) * r) + (m/(m+v) * c))


def conversion(data):
    array = []
    for row in data:
        array.append(row['name'])
    return array


def series(x):
    return pd.Series(x, dtype=object)


def main(df):

    shownMovies = df

    print("Welcome to EN2_6's movie recommendation system!!")
    print("How can we help to filter movies for you?")

    option = True

    while option:
        menu()
        choice = int(input('Please enter your choice [1-5] : '))

        if choice == 1:
            num = int(input("How many top movies do you want to see? "))
            shownMovies = shownMovies.sort_values(
                by=['vote_average'], ascending=False)
            shownMovies = shownMovies[['title', 'vote_average']].head(num)
            print(shownMovies.to_string(index=False))

            buffer = input("Press any key to continue.")
            continue

        elif choice == 2:
            gen = input("What genre are you looking for? ").capitalize()
            num = int(input("How many movies do you want to see? "))

            shownMovies['genres'] = shownMovies['genres'].apply(conversion)

            s = shownMovies.genres.apply(
                series).stack().reset_index(level=1, drop=True)
            s.name = 'genre'

            shownMovies = shownMovies.drop('genres', axis=1).join(s)

            x = shownMovies[shownMovies.genre ==
                            gen].sort_values('wr', ascending=False)

            print(x['title'].head(num).to_string(index=False))

            buffer = input("Press enter to continue.")
            continue

        elif choice == 3:
            print("Please choose the language you want to view!")
            menu2()
            lan = int(input("Which language do you want to view? "))
            num = int(input("How many movies do you want to see? "))

            l = shownMovies.original_language.apply(
                series).stack().reset_index(level=1, drop=True)
            l.name = 'lang'
            shownMovies = shownMovies.drop('original_language', axis=1).join(l)

            if lan == 1:
                x = shownMovies[shownMovies.lang == 'en']
                print(x['title'].head(num).to_string())
                buffer = input("Press enter to continue.")

            elif lan == 2:
                x = shownMovies[shownMovies.lang == 'fr']
                print(x['title'].head(num).to_string())
                buffer = input("Press enter to continue.")

            elif lan == 3:
                x = shownMovies[shownMovies.lang == 'zh']
                print(x['title'].head(num).to_string())
                buffer = input("Press enter to continue.")

            else:
                print("We're unable to compute that request. Please try again :)")

            continue

        elif choice == 4:

            year = input("Please enter a year (2017 or earlier): ")
            num = int(input("How many movies do you want to see? "))

            l = shownMovies.year.apply(
                series).stack().reset_index(level=1, drop=True)
            l.name = 'year'
            shownMovies = shownMovies.drop('year', axis=1).join(l)
            x = shownMovies[shownMovies.year == year]

            print(f"Here are the top movies released in {year}")
            print(x['title'].head(num).to_string())

            buffer = input("Press enter to continue.")
            continue

        elif choice == 5:
            break

        elif choice == 6:
            option = False
            print(
                "Thank you for using our system, we hope it has helped you! Have a nice day :D")
            break
        else:
            print("We're unable to compute that request. Please try again :)")

    return None


if __name__ == '__main__':
    df = setupDataframe()
    main(df)

# 'C:/Users/nkoh9/OneDrive/Desktop/archive'
