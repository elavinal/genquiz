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

DEFAULT_GROUP = 'my_group'

def clean_html(text):
    rep1 = text.replace('<p>','').replace('</p>','\\\\')
    rep2 = rep1.replace('<code>','\\texttt{').replace('</code>','}')
    return rep2

def clean_qname(name):
    return name.replace('-', '')

def generate_verbatimbox(code, name):
    tex = '\\begin{myverbbox}{\\' + name + '}\n'
    tex += code
    # tex += '\n'
    tex += '\\end{myverbbox}\n'
    return tex

def question_answer(answer):
    if answer['fraction'] > 0:
        a = '\\correctchoice{' + clean_html(answer['text']) + '}\n'
    else:
        a = '\\wrongchoice{' + clean_html(answer['text']) + '}\n'
    return a

def make_question_multichoice(question):
    # Name and type
    qname = clean_qname(question['qname'])
    q = '\\element{' + DEFAULT_GROUP + '}{\n'
    if question['type'] == 'single':
        q += '\\begin{question}{' + qname + '}\n'
    else:
        q += '\\begin{questionmult}{' + qname + '}\n'
    # Text
    q += clean_html(question['text1']) + '\n'
    box = ''
    if 'code' in question:
        box = generate_verbatimbox(question['code'], qname)
        q += '\\hspace*{1em}\\fbox{\\' + qname + '}\\\\ \n'
        if 'text2' in question:
            q += clean_html(question['text2'])
            q += '\n'
    # Answers
    q += '\\begin{choices}\n'
    for answer in question['answers']:
         q += question_answer(answer)
    q += '\\end{choices}\n'
    if question['type'] == 'single':
        q += '\\end{question}\n}\n'
    else:
        q += '\\end{questionmult}\n}\n'
    sep = '\n% ==================================================\n'
    return sep + box + q

def make_category(question):
    # TODO: use the category as a group of questions?
    print('Warning: "category" not implemented for AMC output')
    return ''

def make_question_numerical(question):
    print('Warning: question type "numerical" not implemented for AMC output')
    return ''

def make_question_shortanswer(question):
    print('Warning: question type "shortanswer" not implemented for AMC output')
    return ''

def make_question_matching(question):
    print('Warning: question "matching" type not implemented for AMC output')
    return ''
