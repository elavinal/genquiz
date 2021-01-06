# genquiz
Generate a Moodle quiz from questions in a YAML file.

## Overview
`genquiz` is a Moodle quiz generator ([Moodle XML format](https://docs.moodle.org/310/en/Moodle_XML_format)) that reads questions from a YAML text file. It was designed to handle in particular computer science questions that include code snippets. These snippets are obfuscated as PNG images so that students can't copy-paste the code in an editor to execute it.

The [questions.yaml](./questions.yaml) file presents examples of questions related to the C programming language. Currently, `genquiz` supports _multiple choice_, _numerical_, _short answer_ and _matching_ question types.

## Requirements
The generic syntax highlighter [Pygments](https://pygments.org/).

## Installing
Just clone the git repository...

## Running the example
Run the following command:

    $ python genquiz.py questions.yaml

This will generate the `out.xml` file that you can directly import in Moodle.

You can also generate an HTML preview of the questions:

    $ python genquiz.py -f html questions.yaml

Note that the generated `out.html` file is not strictly compliant to HTML 4.01 but it's enough to have a preview of the questions in a browser :)

## Using multiple input files
You can specify multiple input files that will be merged into a single output.
Each file can for instance belong to a specific category of questions.
For example:

    $ python genquiz.py -o test-spring-2021.xml cat1.yaml cat2.yaml cat3.yaml

## Licence

(c) 2021 Emmanuel Lavinal (University of Toulouse).
Distributed under the [GPL](http://www.gnu.org/copyleft/gpl.html "GNU General Public License") version 3.
