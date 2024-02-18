from flask import Flask, render_template, request
import sys
import os

# Add the directory containing producer.py to the Python path
sys.path.append("./streaming_pipeline")
from producer import produce_message
app = Flask(__name__)

# Define module names and IDs
module_names = ['Module 1: Containerization and Infrastructure as Code','Module 2: Workflow Orchestration','Workshop 1: Data Ingestion', 'Module 3: Data Warehouse','Module 4: Analytics Engineering','Module 5: Batch processing' ,'Module 6: Streaming' ,'Workshop 2: Stream Processing with SQL', 'Project_Evaluation' , 'Project_Submission', 'Workshop 3: Piperider']
module_ids = ['m1','m2','w1','m3','m4','m5','m6','w2','p_eval','p_sub','w3']

@app.route('/')
def index():
    return render_template('index.html', module_names=module_names, module_ids=module_ids)

@app.route('/submit', methods=['POST'])
def submit():
    module_id = request.form['module_name']
    username = request.form['username']
    time_spent_lectures = request.form['time_spent_lectures']
    time_spent_homework = request.form['time_spent_homework']
    scores = request.form['scores']
    
    # Find the module name corresponding to the module ID
    module_name = module_names[module_ids.index(module_id)]
    
    
    # Create a key-value pair message
    key = f"{module_id}-{username}"
    value = f"Module Name: {module_name}, Module ID: {module_id}, Username: {username}, Time Spent on Homework: {time_spent_homework}, Time Spent on Lectures: {time_spent_lectures}, Scores: {scores}"
   
    # Produce the message to a Kafka topic
    produce_message('shekhar-iq-form-submissions', key, value)


    return "Form submitted successfully!"

if __name__ == '__main__':
    app.run(debug=True)
