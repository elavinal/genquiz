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
MAX_LEN_MULTICOL = 20

def clean_html(text, line_break=True):
    # escaping characters for LaTeX
    temp = text.replace('{','\\{').replace('}','\\}')
    temp = temp.replace('&', '\\&')
    temp = temp.replace('<p>','')
    # parsing some html tags
    if line_break:
        temp = temp.replace('</p>','\\\\')
    else:
        temp = temp.replace('</p>','')
    temp = temp.replace('<code>','\\texttt{').replace('</code>','}')
    temp = temp.replace('<b>','\\textbf{').replace('</b>','}')
    return temp

def clean_qname(name):
    rep1 = name.replace('-', '')
    rep2 = rep1.replace('1', 'one').\
                replace('2', 'two').\
                replace('3', 'three').\
                replace('4', 'four').\
                replace('5', 'five').\
                replace('6', 'six')
    return rep2

def generate_verbatimbox(code, name):
    tex = '\\begin{myverbbox}{\\' + name + '}\n'
    tex += code
    # tex += '\n'
    tex += '\\end{myverbbox}\n'
    return tex

def check_multicol(answers):
    for a in answers:
        text_nocode = str(a['text']).replace('<code>', '').replace('</code>', '')
        if len(text_nocode) > MAX_LEN_MULTICOL:
            return False
    return True

def question_answer(answer):
    if answer['fraction'] > 0:
        a = '\\correctchoice{' + clean_html(str(answer['text'])) + '}\n'
    else:
        a = '\\wrongchoice{' + clean_html(str(answer['text'])) + '}\n'
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
        q += '[3pt]\n\\hspace*{1em}\\fbox{\\' + qname + '}\\\\ \n'
        if 'text2' in question:
            q += clean_html(question['text2'], line_break=False)
            q += '\n'
    # Answers
    multicol = check_multicol(question['answers'])
    if multicol:
        q += '\\setlength{\\columnseprule}{0pt}\n'
        q += '\\setlength{\\columnsep}{0pt}\n'
        q += '\\begin{multicols}{2}\n'
    q += '\\begin{choices}\n'
    for answer in question['answers']:
         q += question_answer(answer)
    q += '\\end{choices}\n'
    if multicol:
        q += '\\end{multicols}\n'
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
