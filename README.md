# genquiz
Generate a Moodle quiz from questions in a YAML file.

## Overview
`genquiz` is a Moodle quiz generator ([Moodle XML format](https://docs.moodle.org/310/en/Moodle_XML_format)) that reads questions from a YAML text file. It was designed to handle in particular computer science questions that include code snippets. These snippets are obfuscated as PNG images so that students can't copy-paste the code in an editor to execute it.

The `questions.yaml` file presents examples of questions related to the C programming language. Currently, `genquiz` supports _multiple choice_, _numerical_, _short answer_ and _matching_ question types.

## Requirements
The generic syntax highlighter [Pygments](https://pygments.org/).

## Installing
Just clone the git repository...

## Running the example
Run the following command:

    $ python genquiz.py moodle questions.yaml

This will generate the `out.xml` file that you can directly import in Moodle.

You can also generate an HTML preview of the questions:

    $ python genquiz.py html questions.yaml

Note that the generated `out.html` file is not strictly compliant to HTML 4.01 but it's enough to have a preview of the questions in a browser :)

## Licence

(c) 2021 Emmanuel Lavinal (University of Toulouse).
Distributed under the [GPL](http://www.gnu.org/copyleft/gpl.html "GNU General Public License") version 3.
