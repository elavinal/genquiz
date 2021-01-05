# GenQuiz, a Moodle XML quiz generator from questions in a YAML file.
# Copyright (C) 2021 Emmanuel Lavinal
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

# TODO: Use the save image feature in generate_code_image() function

import base64
from pathlib import Path
from pygments import highlight
from pygments.lexers.c_cpp import CLexer
from pygments.formatters import HtmlFormatter
from pygments.formatters import ImageFormatter

def generate_code_image(question, save_image=False):
    # Start of the question
    start_str = '<![CDATA[' + question['text1']
    # Generate file name from question name
    Path('img').mkdir(parents=True, exist_ok=True)
    if save_image:
        fname = "img/" + question['qname'].replace(" ", "-") + ".png"
    else:
        fname = "img/out.png"
    # Use pygments to highlight the code and generate image
    with open(fname, "wb") as png_file:
        highlight(question['code'],
                  CLexer(),
                  ImageFormatter(line_pad=4, image_pad=5, line_numbers=False),
                  png_file)
    # Encode image as a base64 string
    with open(fname, 'rb') as image_file:
        encoded_str = base64.b64encode(image_file.read()).decode('UTF-8')
        img_str = '<img alt="code-fig" src="data:image/png;base64,{}">'.format(encoded_str)
    # End of the question
    if 'text2' in question:
        end_str = question['text2'] + ']]>'
    else:
        end_str = ']]>'
    return start_str + img_str + end_str

def question_type(type, name):
    str = '<question type="{}"><name><text>{}</text></name>'.format(type, name)
    str += '<defaultgrade>1</defaultgrade>'
    return str

def question_text(question):
    str = '<questiontext format="html"><text>'
    if 'code' in question:
        str += generate_code_image(question)
    else:
        str += '<![CDATA[' + question['text1'] + ']]>'
    str += '</text></questiontext>'
    return str

def question_answer(answer, format='html'):
    str = '<answer fraction="{}" format="{}">'.format(answer['fraction'], format)
    str += '<text><![CDATA[{}]]></text>'.format(answer['text'])
    if 'feedback' in answer:
        str += '<feedback format="html"><text><![CDATA[{}]]></text>'\
               '</feedback>'.format(answer['feedback'])
    if 'tolerance' in answer:
        str += '<tolerance>{}</tolerance>'.format(answer['tolerance'])
    str += '</answer>'
    return str

def general_feedback(question):
    str = ''
    if 'feedback' in question:
            str += '<generalfeedback format="html">'
            str += '<text><![CDATA[{}]]></text>'.format(question['feedback'])
            str += '</generalfeedback>'
    return str

def make_category(question):
    q = '<question type="category"><category><text>$course$/{}</text>'\
        '</category></question>'.format(question['qname'].replace(' ','_'))
    return q

def make_question_multichoice(question):
    # Name and type
    q = question_type('multichoice', question['qname'])
    if question['type'] == 'single':
        q += '<single>true</single>'
    else:
        q += '<single>false</single>'
    # Text
    q += question_text(question)
    # Answers
    q += general_feedback(question)
    q += '<shuffleanswers>1</shuffleanswers>'
    q += '<answernumbering>none</answernumbering>'
    for answer in question['answers']:
        q += question_answer(answer)
    q += '</question>'
    return q

def make_question_numerical(question):
    # Name and type
    q = question_type('numerical', question['qname'])
    # Text
    q += question_text(question)
    # Answers
    q += general_feedback(question)
    for answer in question['answers']:
        q += question_answer(answer, format='moodle_auto_format')
    q += '</question>'
    return q

def make_question_shortanswer(question):
    # Name and type
    q = question_type('shortanswer', question['qname'])
    # Text
    q += question_text(question)
    # Answers
    q += general_feedback(question)
    for answer in question['answers']:
        q += question_answer(answer, format='moodle_auto_format')
    q += '</question>'
    return q

def make_question_matching(question):
    # Name and type
    q = question_type('matching', question['qname'])
    # Text
    q += question_text(question)
    # Answers
    q += general_feedback(question)
    q += '<shuffleanswers>true</shuffleanswers>'
    for subquestion in question['subquestions']:
        q += '<subquestion format="html">'
        q += '<text><![CDATA[{}]]></text>'.format(subquestion['text'])
        q += '<answer><text><![CDATA[{}]]></text>'.format(subquestion['answer'])
        q += '</answer></subquestion>'
    q += '</question>'
    return q
