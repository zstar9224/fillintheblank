import random
import pandas as pd
import re

def OnOff(prob=0.5):
    return 1 if random.uniform(0, 1.0) > prob else 0

def VerseWithBlanks(verse):
    verse_with_blanks = []
    answer_in_blanks  = []
    kk = 0

    # 초기 On/Off
    on_off = OnOff()

    # [  ] 패턴 찾기
    p = re.compile(r'\[(.*?)\]')
    for m in p.finditer(verse):
        # 괄호 밖의 단어들은 괄호([]) 앞에 나오는 단어들을 추가한다.
        if kk < m.start():
            verse_with_blanks.append(verse[kk:m.start()])

        # On/Off 확률을 적용
        #   1: 괄호를 적용하지 않는다.
        #   0: 괄호를 적용한다.
        if on_off == 1:
            verse_with_blanks.append(m.group()[1:-1])
        else:
            num_characters = m.end() - m.start() - 2
            verse_with_blanks.append('[' + '_' * (num_characters + 5)  + ']')
            answer_in_blanks.append(m.group())

        on_off ^= 1
        kk = m.end()

    # 마지막에 괄호 밖의 단어들이 남아있다면 추가한다.
    if kk <= len(verse):
        verse_with_blanks.append(verse[kk:])

    return (' '.join(verse_with_blanks), answer_in_blanks)

if __name__ == "__main__":
    df = pd.read_csv('Navigator_Bible60.csv', encoding='utf-8')

    while True:
        section = input(f'\n성경암송 문제를 시작합니다. 문제 섹션을 입력해주세요: a/b/c/d/e/[all]....')
        print('\n')

        if (section  == '') or (section == 'all'):
            section_df = df
            break
        elif len(section) == 1:
            section = section.upper()
            if section in ['A', 'B', 'C', 'D', 'E']:
                section_df = df[df['제목'].str[0] == section]
                break

        print(f'잘못 입력하셨습니다.')

    for idx, row in section_df.iterrows():
        verse = row['성경구절']
        verse_with_blanks, answer_in_blanks = VerseWithBlanks(verse)
        print(f'\n{idx}: {verse_with_blanks}')
        input()
        print(f'\t\t 정답:  {",  ".join(answer_in_blanks)}')
