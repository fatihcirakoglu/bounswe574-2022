import math
import re
from django.utils.html import strip_tags
from wikidata.client import Client
from typing import List

def count_words(html_string):
    word_string = strip_tags(html_string)
    matching_words = re.findall(r'\w+', word_string)
    count = len(matching_words)
    return count


def get_read_time(html_string):
    count = count_words(html_string)
    read_time_min = math.ceil(count/200.0) #assuming 200wpm reading
    return int(read_time_min)

def column_exists(column: str, column_list: list) -> bool:
    if column in column_list:
        return True


def get_qcode_keywords(qcode: str) -> List:
    user_keywords = []
    client = Client() 
    entity = client.get(qcode, load=True)
    instance_of = client.get('P31')
    instances = entity.getlist(instance_of)
    for instance in instances:
        if str(instance.id) not in user_keywords:
            user_keywords.append(str(instance.id))
    subclass_of = client.get('P279')
    subclasses = entity.getlist(subclass_of)
    for subclass in subclasses:
        if str(instance.id) not in user_keywords:
            user_keywords.append(str(subclass.id))
    return user_keywords