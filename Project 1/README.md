#transform.py
transform.py on execution will create "transformed.csv" which will contain the table 'list of of super bowl champions' from the wikipedia page - "https://en.wikipedia.org/wiki/List_of_Super_Bowl_champions"

#clean.py
clean.py takes a dataset as command line argument and cleans all the data into a new file cleaned.txt

Based on the conditions given for last names implemented split method with delimiters. Added the last_name as key and corresponding courses as its value and printed the results onto the new file cleaned.txt with a proper format

#query.py
query.py takes a cleaned dataset and professor name as command line arguments and prints corresponding result on terminal

This script performs 3 queries

Query 1: To get the distinct courses all the courses from the list
were compared with each other and jaccard index was calculated for each comparison
and if index was less than 0.6 then they are different courses
so all the different courses were added to the 'cleaned_list'
Its length is returned as the total no. of distinct courses

Query 2: For a given professor name to print his courses
Iterating over the dictionary and finding the key == professor name
and returning the corresponding value as his/her list of courses

Query 3: For the given professor if has more than 5 courses, it returns professor with closest teaching interests
else, It returns two professors with closest teaching interests among them
idf method is used to find the inverse document frequency so it takes a courses name and returns
only important words from the course name

we get the courses of given professor using idf(So we get only important words from professor's course list) and
compare it with all the other professor's course in the list
then calculate a sum for every two professors and save it into "jaccard_values"
finding the maximum value from the "jaccard_value" gives us the professor with closest interest with given professor

If the professor does not have more than 5 courses, We take all the professors with courses greater than 5
and compare each professor courses with other professors and add it into "jaccard_values"
Then iterating over the "jaccard_values" and finding maximum value gives two professors with closest teaching interests

