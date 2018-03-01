import re
import sys
import math

''' This method calculates the jaccard index for any given two strings considers both words and characters'''
def jaccard_index(first_course, second_course):
    first_course = first_course.replace("&", "and")
    second_course = second_course.replace("&", "and")
    first_course = first_course.replace("intro.", "introduction")
    second_course = second_course.replace("intro.", "introduction")
    first_course = first_course.replace("Intro.", "introduction")
    second_course = second_course.replace("Intro.", "introduction")
    first_course = first_course.replace("Intro", "introduction")
    second_course = second_course.replace("Intro", "introduction")
    first_course = first_course.replace("intro", "introduction")
    second_course = second_course.replace("intro", "introduction")
    a1 = first_course.replace(" ", "")
    b1 = second_course.replace(" ", "")
    if a1 == b1:
        return True
    else:
        intersection1 = 0
        if len(a1) > len(b1):
            size = len(b1)
        else:
            size = len(a1)
        for x in range(0, size):
            if a1[x].lower() == b1[x].lower():
                intersection1 += 1
        jaccard_character_index = float(intersection1) / (len(a1) + len(b1) - intersection1)
        if jaccard_character_index > 0.8:
            return True
    jaccard_word_index = jaccard_word_wise(first_course, second_course)
    if jaccard_word_index >= 0.6 or jaccard_character_index >= 0.6:
        return True
    else:
        return False

''' This method calculates jaccard by considering only words'''
def jaccard_word_wise(first_course, second_course):
    course1_words = re.compile('\w+').findall(first_course)
    course2_words = re.compile('\w+').findall(second_course)
    for x in range(0, len(course1_words)):
        course1_words[x] = course1_words[x].lower()
    for x in range(0, len(course2_words)):
        course2_words[x] = course2_words[x].lower()
    course1_set = set(course1_words)
    course2_set = set(course2_words)
    intersection2 = course1_set.intersection(course2_set)
    jaccard_index = float(len(intersection2)) / (len(course1_set) + len(course2_set) - len(intersection2))
    return jaccard_index


'''returns the list of courses from the course dictionary'''
def get_uncleaned_list(course_dictionary):
    uncleaned_list = []
    for key, value in course_dictionary.items():
        for v in value:
            uncleaned_list.append(v)
    return uncleaned_list


'''returns all the distinct courses from a given list'''
def get_list(uncleaned_list):
    cleaned_list = []
    x = 0
    while True:
        y = 0
        while True:
            if (jaccard_index(uncleaned_list[x], uncleaned_list[y])) == False:
                if uncleaned_list[x] not in cleaned_list:
                    cleaned_list.append(uncleaned_list[x])
            else:
                uncleaned_list.remove(uncleaned_list[y])
            y = y + 1
            if y >= len(uncleaned_list):
                break
        x = x + 1
        if x >= len(uncleaned_list):
            break
    return cleaned_list


'''returns the no. of words present in a list'''
def get_count_of_words(course_list):
    total_count = 0
    for item in course_list:
        words = re.compile('\w+').findall(item)
        total_count += len(words)
    return total_count

'''returns only the important words from the "course_name" comparing with the "course_list"'''
def idf(course_name, course_list):
    frequent_words = ''
    t_count = get_count_of_words(course_list)
    for word in course_name.split():
        count = 0
        for course in course_list:
            if word in course:
                count += 1
        word_frequency = count/t_count
        idf = math.log(t_count)/word_frequency
        idf = idf / 1000
        if idf > 0.5 and word not in frequent_words:
            frequent_words += " " + str(word)
    return frequent_words


'''Query 1 returns count of distinct courses'''
def query1(course_dict):
    uncleaned_list = []
    for key, value in course_dict.items():
        for v in value:
            uncleaned_list.append(v)

    cleaned_list = get_list(uncleaned_list)
    return len(cleaned_list)

'''returns all the courses taught by given professor'''
def query2(course_dict, professor_name):
    list_of_courses = ""
    for key, value in course_dict.items():
        key = key.lower().strip()
        temp = professor_name.split()
        for t in temp:
            if key == t:
                for v in value:
                    list_of_courses += str(v) + ", "
    list_of_courses = list_of_courses[:-2]
    return list_of_courses

'''For a given professor returns the professor with closest teaching interests'''
def query3(course_dict, professor_name):
    if professor_name != 'none':
        jaccard_values = {}
        professor_name = professor_name.capitalize()
        prof1_courses = []
        course_list = get_uncleaned_list(course_dict)
        for item in course_dict[professor_name]:
            prof1_courses.append(idf(item, course_list))
        for key, value in course_dict.items():
            if key != professor_name and len(value) >= 5:
                sum = 0
                for a in range(0, len(prof1_courses)):
                    for b in range(0, len(value)):
                        sum += jaccard_word_wise(prof1_courses[a], value[b])
                sum = sum/(len(prof1_courses) * len(value))
                sum = sum*100
                jaccard_values[key] = sum
        high_val = max(jaccard_values.values())
        high_key = [k for k, v in jaccard_values.items() if v == high_val]

        return high_key
    else:
        jaccard_values = {}
        high_val = 0
        for p1_key, p1_val in course_dict.items():
            if len(p1_val) >= 5:
                for p2_key, p2_val in course_dict.items():
                    if len(p2_val) > 4 and p1_key != p2_key:
                        sum = 0
                        for a in range(0, len(p1_val)):
                            for b in range(0, len(p2_val)):
                                sum += jaccard_word_wise(p1_val[a], p2_val[b])
                        sum = sum / (len(p1_val) * len(p2_val))
                        sum = sum * 100
                        jaccard_values[p1_key] = {}
                        jaccard_values[p1_key][p2_key] = sum
                        if jaccard_values[p1_key][p2_key] > high_val:
                            high_val = jaccard_values[p1_key][p2_key]
                            prof1_name = p1_key
                            prof2_name = p2_key
        return prof1_name, prof2_name

if len(sys.argv) < 2:
    print("Invalid number of command line arguments")
    exit()

file_path = sys.argv[1]

course_catalog = {}
with open(file_path) as fp:
    line = fp.readline()
    while line:
        prof = line.split("-")[0]
        prof = prof.strip()
        courses = (line.split('-')[1]).split("|")
        for c in courses:
            c = c.strip()
            if prof in course_catalog:
                course_catalog[prof].append(c)
            else:
                course_catalog[prof] = [c]
        line = fp.readline()
    fp.close()

course_count = query1(course_catalog)
arg_size = len(sys.argv)
prof_name = ''
for x in range(2, arg_size):
    prof_name += sys.argv[x].lower().strip() + " "
list_of_courses = query2(course_catalog, prof_name)

uncleaned_list = get_uncleaned_list(course_catalog)


print("Query 1: Total no. of Distinct courses: " + str(course_count))
if len(list_of_courses) == 0:
    print("Query 2: Invalid Professor name")
else:
    print("Query 2: List of Courses taught by Prof. " + str(prof_name) + ": " + str(list_of_courses))
for key, value in course_catalog.items():
    key = key.lower().strip()
    for n in prof_name.split():
        if key == n:
            if len(value) < 5:
                p1, p2 = query3(course_catalog, 'none')
                print("Query 3: Prof." + str(p1) + " and Prof." + str(p2) + " have closest teaching interests")
            else:
                prof2 = query3(course_catalog, key)
                print("Query 3: The Professor with most aligned teaching interest with Prof." + str(prof_name).capitalize() + ": Prof." + str(prof2[0].capitalize()))
