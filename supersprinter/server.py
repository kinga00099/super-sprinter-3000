from flask import Flask, render_template, redirect, request
import csv

app = Flask(__name__)


# reads the csv file containing the stories, return them as a list
def get_user_stories_from_file():
    list_of_stories = []
    with open("stories.csv", "r") as file:
        stories = csv.reader(file)
        for line in stories:
            list_of_stories.append(line)
    return list_of_stories


#calculate a new max id
def calculate_max_id():
    list_of_stories = get_user_stories_from_file()
    maximum_id = 0
    for story in list_of_stories:
        if int(story[0]) > int(maximum_id):
            maximum_id = int(story[0])
    maximum_id += 1
    return maximum_id


#get various data from the user, return it as a list, used when adding new US and when updating an US
def input_story_data():
    story_title = request.form['Story title']
    user_story = request.form['User story']
    acceptance_criteria = request.form['Acceptance criteria']
    business_value = request.form['Business value']
    estimation = request.form['Estimation']
    status = request.form['Status']
    list_of_story_data = [story_title, user_story, acceptance_criteria, business_value, estimation, status]
    return list_of_story_data


#main page: list all user stories as a table using list.html
@app.route('/')
@app.route('/list')
def list_user_stories():
    list_of_stories = get_user_stories_from_file()
    len_of_list_of_stories = len(list_of_stories)
    return render_template('list.html', list_of_stories=list_of_stories, len_of_list_of_stories=len_of_list_of_stories)


#/story page: add new user story, method: GET
@app.route('/story')
def add_new_story():
    return render_template('form.html')


#story page: add new _US, method is now POST instead of GET
# post mellé get a listába, majd returnnél if get: render template, post: return redirect
@app.route('/story', methods=['POST'])
def get_data_for_new_user_story():
    list_of_new_story_data = input_story_data()
    id = list(str(calculate_max_id()))
    new_user_story = id + list_of_new_story_data

    with open('stories.csv', 'a', newline='') as file:    # 'a' opens the file for appending
        csv_writer = csv.writer(file)
        csv_writer.writerow(new_user_story)
    return redirect('/')            #redirect to main page


#/story page by its ID: update user story, method: GET
@app.route('/story/<int:id>')
def get_story_page_by_id(id):
    list_of_stories = get_user_stories_from_file()
    return render_template('form.html', id=id, list_of_stories=list_of_stories)


#/story page by its ID: update user story, method: POST
@app.route('/story/<int:id>', methods=['POST'])    #int conversion required!
def update_user_story(id):
    list_of_story_data = input_story_data()
    updated_story = list(str(id)) + list_of_story_data
    list_of_user_stories = get_user_stories_from_file()
    line_to_update = 0

    for story in list_of_user_stories:
        if story[0] == updated_story[0]:
            break
        else:
            line_to_update += 1

    list_of_user_stories[line_to_update] = updated_story

    with open('stories.csv', 'w', newline='') as file:
        csv_writer = csv.writer(file)
        csv_writer.writerows(list_of_user_stories)
    return redirect('/')


#runs Flask
if __name__ == '__main__':
    app.secret_key = 'asd123' #is this important here? ---> to ask!!!!
    app.run(
        debug=True,  # as in the tutorial --> to ask!!
        port=5000  # Set port
    )
