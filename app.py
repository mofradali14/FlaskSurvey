from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey

app = Flask(__name__)
app.config['SECRET_KEY'] = 'survey'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)


@app.route('/')
def home():
    title = satisfaction_survey.title
    instructions = satisfaction_survey.instructions
    return render_template('home.html', title=title, instructions=instructions)


@app.route('/start', methods=['POST'])
def start():
    session['responses'] = []
    return redirect('/questions/0')


@app.route('/questions/<int:q_num>')
def survey_question(q_num):
    responses = session.get('responses')
    if (len(responses) == len(satisfaction_survey.questions)):
        return redirect("/done")

    if (len(responses) != q_num):
        flash(
            f"Invalid question ID: {q_num}. You've been redirected to question {len(responses)}")
        return redirect(f"/questions/{len(responses)}")

    question = satisfaction_survey.questions[q_num]
    return render_template('question.html', question=question)


@app.route('/answer', methods=['POST'])
def answer_handler():

    answer = request.form['answer']
    responses = session['responses']
    responses.append(answer)
    session['responses'] = responses
    if (len(responses) == len(satisfaction_survey.questions)):
        return redirect('/done')
    else:
        return redirect(f'/questions/{len(responses)}')


@app.route('/done')
def done():
    return render_template('done.html')
