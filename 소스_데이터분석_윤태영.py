import os
import json
from typing import Tuple, Dict, List

def load_data(file_path: str) -> Dict[str, str]:
    if not os.path.exists(file_path):
        return {}
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_data(file_path: str, data: Dict[str, str]) -> None:
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def add_word(data: Dict[str, str], word: str, meaning: str) -> Tuple[bool, str]:
    if len(data) >= 5:
        return False, '최대 5개 단어만 저장할 수 있습니다.'
    if word.lower() in data:
        return False, '이미 등록되었습니다.'
    data[word.lower()] = meaning
    return True, ''

def search_word(data: Dict[str, str], keyword: str) -> List[Tuple[str, str]]:
    results = [(word, meaning) for word, meaning in data.items() if word.startswith(keyword.lower())]
    return results

def update_word(data: Dict[str, str], word: str, new_meaning: str) -> Tuple[bool, str]:
    if word.lower() not in data:
        return False, '단어를 검색할 수 없습니다.'
    data[word.lower()] = new_meaning
    return True, '단어의 뜻을 수정 하였습니다'

def delete_word(data: Dict[str, str], word: str) -> Tuple[bool, str]:
    if word.lower() not in data:
        return False, '단어를 검색할 수 없습니다.'
    del data[word.lower()]
    return True, '단어를 삭제 하였습니다'

def list_words(data: Dict[str, str], ascending: bool = True) -> List[Tuple[str, str]]:
    return sorted(data.items(), key=lambda x: x[0], reverse=not ascending)

def get_word_statistics(data: Dict[str, str]) -> Tuple[int, str, List[str]]:
    word_count = len(data)
    longest_word = max(data.keys(), key=lambda x: len(x), default='')
    sorted_words = sorted(data.keys(), key=lambda x: len(x), reverse=True)
    return word_count, longest_word, sorted_words

def main():
    file_path = 'wordbook.json'
    data = load_data(file_path)

    while True:
        print('''
        1. 저장
        2. 검색
        3. 수정
        4. 삭제
        5. 목록
        6. 통계
        7. 종료
        ''')

        choice = input('선택하세요: ').strip()

        if choice == '1':
            word = input('단어를 입력하세요: ').strip()
            meaning = input('뜻을 입력하세요: ').strip()
            success, msg = add_word(data, word, meaning)
            print(msg)

        elif choice == '2':
            keyword = input('검색할 단어를 입력하세요: ').strip()
            results = search_word(data, keyword)
            if not results:
                print('단어를 검색할 수 없습니다.')
            else:
                for word, meaning in results:
                    print(f'단어: {word}, 뜻: {meaning}')
        elif choice == '3':
            word = input('수정할 단어를 입력하세요: ').strip()
            new_meaning = input('새로운 뜻을 입력하세요: ').strip()
            success, msg = update_word(data, word, new_meaning)
            print(msg)
        elif choice == '4':
            word = input('삭제할 단어를 입력하세요: ').strip()
            success, msg = delete_word(data, word)
            print(msg)

        elif choice == '5':
            print('1. 오름차순\n2. 내림차순')
            order = input('정렬 순서를 선택하세요: ').strip()
            if order == '1':
                word_list = list_words(data)
            else:
                word_list = list_words(data, ascending=False)
            for word, meaning in word_list:
                print(f'단어: {word}, 뜻: {meaning}')

        elif choice == '6':
            word_count, longest_word, sorted_words = get_word_statistics(data)
            print(f'저장된 단어 갯수: {word_count}')
            print(f'단어의 문자수가 가장 많은 단어: {longest_word}')
            print('단어 글자수 내림차순 출력:')
            for word in sorted_words:
                print(word)

        elif choice == '7':
            save_data(file_path, data)
            print('프로그램을 종료합니다.')
            break

        else:
            print('잘못된 입력입니다. 다시 시도하세요.')

if __name__ == "__main__":
    main()