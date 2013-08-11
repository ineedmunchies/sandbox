#!/usr/bin/env python
# -*- coding: latin-1 -*-
import pickle
import sys
import webbrowser
import re

DIFFICULTIES = {'easy':0, 'intermediate':1, 'hard':2, 'difficult':2}

def is_num(number):
    try:
        int(number)
    except ValueError:
        return False
    return True


def unpickle_file(file_name):
    pickled_file = open(file_name, 'r')
    unpickled_object = pickle.load(pickled_file)
    pickled_file.close()
    return unpickled_object


def parse_post(post):
    index_start = post['title'].find('#') + 1
    index_end = post['title'][index_start:].find(' ')

    if index_end == -1:
        index_end = index_start + 1
    else:
        index_end = index_start + index_end

    index = post['title'][index_start:index_end]
    title = post['title']
    url = post['url']
    return index, title, url


def get_post_difficulty(title):
    difficulty = None
    for difficulty_level in DIFFICULTIES.keys():
        if difficulty_level in title.lower():
            difficulty = difficulty_level
            break
    return difficulty


def remove_nth_letter_from_string(string, n):
    return string[:n] + string[n+1:]

def strip_title(title):
    n = 0
    drop_character = False
    for c in title:
# if character is opening bracket begin dropping
        if c == '[':
            drop_character = True

# if character is closing bracket stop dropping
        if c == ']':
            title = remove_nth_letter_from_string(title, n)
            drop_character = False
            continue

        if drop_character:
            title = remove_nth_letter_from_string(title, n)
        else:
            n += 1

    return title

def create_challenges_dictionary(reddit_posts):
    challenges = {}
    for post in reddit_posts:
        if "challenge #" in post['title'].lower():
            index, title, url = parse_post(post)

            difficulty = get_post_difficulty(title)
            title = strip_title(title)
            if not index in challenges.keys():
                if is_num(index):
                    challenges[index] = {}
                else:
                    continue

            if difficulty:
                challenges[index][difficulty] = {'title':title, 'url':url}
 
    return challenges


def get_row_contents(challenges, index):
    LINK = u'<a href="{0}">{1}</a>'
# Find out how many difficulties there were that week, and sort them in 
# ascending order
    available_difficulties = sorted(challenges[index].keys(), 
                                    key=lambda diff: DIFFICULTIES[diff])

# Place each difficulty in the appropriate place in the list, leaving a blank
# in the list if a challenge of that difficulty was not added that week (or found
# by the parser)
    weekly_challenges = [''] * 3

    for difficulty in sorted(DIFFICULTIES.keys(),
                             key=lambda diff: DIFFICULTIES[diff]):
        if difficulty in available_difficulties:
            challenge = challenges[index][difficulty]
            diff_index = DIFFICULTIES[difficulty]
            weekly_challenges[diff_index] = (LINK.format(challenge['url'], 
                                             challenge['title']))

    return weekly_challenges


def create_table_from_challenges(challenges):
    TABLE_HEADER = u'<table border=1>\n<tr><th>Easy</th><th>Medium</th><th>Hard</th></tr>\n'
    ROW = u'<tr><td>{0}</td><td>{1}</td><td>{2}</td><tr>\n'
    webpage = u''
    webpage += TABLE_HEADER

    for index in sorted(challenges.keys(), key=int):
        row_contents = get_row_contents(challenges, index)

        webpage += ROW.format(*row_contents)

    return webpage


def write_page_to_file(page_content, filename):
    html_file = open(filename, 'w')
    html_file.write(page_content.encode('utf8'))
    html_file.close()


def main():
    reddit_posts = unpickle_file('reddit.pickle')
    challenges = create_challenges_dictionary(reddit_posts)
    page_content = create_table_from_challenges(challenges)
    write_page_to_file(page_content, 'reddit.html')
    webbrowser.open_new("reddit.html")


if __name__ == '__main__':
    main()
