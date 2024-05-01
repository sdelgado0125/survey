from flask import Flask, request, render_template, redirect, url_for, flash, session
from surveys import satisfaction_survey
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config['SECRET_KEY'] = 'survey_key'

debug = DebugToolbarExtension(app)

responses = []


@app.route('/')
def base():
    return render_template('base.html')

@app.route('/start', methods=['GET','POST'])
def start_survey():
    session['responses'] = []
    

    if request.method == 'POST':
        return redirect(url_for('question', question_number = 0))
    return render_template('start_page.html', survey_title='Customer Satisfaction Survey', instructions='Please fill out a survey about your experience with us.')

@app.route('/questions/<int:question_number>', methods=['GET', 'POST'])
def question(question_number):

    current_question = satisfaction_survey.questions[question_number]

    if request.method == 'POST':
        
        choice = request.form['answer']
        responses = session.get('responses', [])
        responses.append(choice)
        session['responses'] = responses

        next_question = question_number + 1
        if next_question < len(satisfaction_survey.questions):
            return redirect(url_for('question', question_number=next_question))
        else:
            return redirect(url_for('thank_you'))
    
    if question_number != len(responses):
        flash('Please answer the questions in order.')
        return redirect(url_for('question', question_number=len(responses)))
        
    return render_template('questions.html', question_number=question_number, current_question=current_question)

@app.route('/answer', methods = ['GET','POST'])
def thank_you():
    responses = session.get('responses', [])
    return render_template("thankyou.html", responses=responses)
    

if __name__ == '__main__':
    app.run(debug=True)
