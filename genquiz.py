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

# TODO: Add target language option: C, Python...

import argparse
import sys
import yaml
import xml.dom.minidom
import output_html
import output_moodle_xml

VERSION = '0.1'

def make_quiz(input_file, output):
    quiz = ''
    with open(input_file) as yaml_file:
        data = yaml.load(yaml_file, Loader=yaml.FullLoader)
        # data = list of questions (each question is a dict)
        # print(data)
        error = False
        i = 0
        for q in data:
            if q['type'] == 'category':
                qstring = output.make_category(q)
            elif q['type'] == 'multi' or q['type'] == 'single':
                qstring = output.make_question_multichoice(q)
            elif q['type'] == 'numerical':
                qstring = output.make_question_numerical(q)
            elif q['type'] == 'shortanswer':
                qstring = output.make_question_shortanswer(q)
            elif q['type'] == 'matching':
                qstring = output.make_question_matching(q)
            else:
                error = True
            if not error:
                quiz += qstring
                # print(qstring)
                print('Question {} added.'.format(q['qname']))
                i += 1
            else:
                print('Error: unknown question type for {}.'.format(q['qname']))
                error = False
    print('=> Total number of questions: {}'.format(i))
    return quiz

def gen_html_preview(input_file_list, output_file):
    quiz = output_html.make_html_header()
    for input_file in input_file_list:
        quiz += make_quiz(input_file, output_html)
    quiz += output_html.make_html_footer()
    with open(output_file, "wt") as html_file:
        print("Generating HTML file...")
        html_file.write(quiz)
        print("Done (cf. {}).".format(output_file))

def gen_moodle_xml(input_file_list, output_file):
    quiz = '<quiz>'
    for input_file in input_file_list:
        quiz += make_quiz(input_file, output_moodle_xml)
    quiz += '</quiz>'
    dom = xml.dom.minidom.parseString(quiz)
    with open(output_file, "wt") as xml_file:
        print("Generating XML file...")
        dom.writexml(xml_file, addindent="  ", newl="\n", encoding="UTF-8")
        print("Done (cf. {}).".format(output_file))

# =============================================================================
# Main function
# =============================================================================
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('input-file', nargs='+',
        help='specify the YAML input file(s) containing the questions')
    parser.add_argument('-f', '--format', choices=['moodle','html'],
        default='moodle',
        help='specify the output format: Moodle XML (default) or HTML preview')
    parser.add_argument('-o', '--output', metavar='FILE',
                        help='write output to FILE (default to out.*)')
    parser.add_argument('-v', '--version', action='version',
                        version='%(prog)s ' + VERSION)
    args = parser.parse_args()
    # print(args)
    format = args.format
    if args.output != None:
        output_file = args.output
    else:
        output_file = ('out.xml' if format == 'moodle' else 'out.html')
    input_file_list = vars(args)['input-file']

    if format == 'moodle':
        gen_moodle_xml(input_file_list, output_file)
    elif format == 'html':
        gen_html_preview(input_file_list, output_file)
    else:
        print("Error, unknown format.")

if __name__ == "__main__":
    main()
