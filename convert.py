import dataclasses
import csv
import datetime
import os
import re


SAVE_DIR = f'./result_{datetime.datetime.now().isoformat()}'

@dataclasses.dataclass
class Answer:
    text: str
    number: int
    is_correct: bool


@dataclasses.dataclass
class Question:
    text: str
    answers: list['Answer']


@dataclasses.dataclass
class Section:
    title: str
    questions: list['Question']


def main():
    sections: list[Section] = read_markdown()

    os.mkdir(SAVE_DIR)
    save_sections_to_csv(sections, SAVE_DIR)


def save_sections_to_csv(sections: list[Section], directory_for_save: str):
    for section in sections:
        with open(os.path.join(directory_for_save, section.title + '.csv'), 'w') as file_section:
            file_section_csv = csv.writer(file_section, delimiter=';', quoting=csv.QUOTE_ALL)

            for question in section.questions:
                front_card = question.text + '\n' + '\n'.join([f'{answer.number}. {answer.text}' for answer in question.answers])
                back_card = ','.join([str(answer.number) for answer in question.answers if answer.is_correct])

                file_section_csv.writerow([front_card, back_card])


def read_markdown() -> list[Section]:
    result: list[Section] = []

    with open('cards.md') as cards_in_md_file:
        while (line := cards_in_md_file.readline()):
            line = line.strip()
            if line == "":
                continue

            if line.startswith('# '):
                title = line[2:]
                title = re.sub(r'\{\#.+\}$', '', title)

                result.append(Section(title, list()))
            elif line.startswith('### '):
                text = line[4:]
                result[-1].questions.append(Question(text, list()))
            elif line[0].isdigit():
                number = int(line[0])
                text = line[3:]
                is_correct = False
                if text.startswith('**'):
                    is_correct = True
                    text = text[2:-2]

                result[-1].questions[-1].answers.append(Answer(text, number, is_correct))
            else:
                print('Error string')

    return result


if __name__ == '__main__':
    main()