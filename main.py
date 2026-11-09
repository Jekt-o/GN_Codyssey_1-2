from quiz import Quiz
from quiz_data import create_default_quizzes
import json
import os
from tempfile import NamedTemporaryFile
from pathlib import Path

STATE_FILE = Path(__file__).resolve().parent / "state.json"

def write_atomic(path, payload):
    temp = NamedTemporaryFile(dir=path.parent, delete=False)
    temporary_path = Path(temp.name)
    try:
        with temp:
            temp.write(payload)
            temp.flush()
            os.fsync(temp.fileno())
        os.replace(temporary_path, path)
    finally:
        temporary_path.unlink(missing_ok=True)


def decode_state(payload):
    data = json.loads(payload.decode("utf-8"))
    if not isinstance(data, dict):
        raise ValueError("잘못된 데이터 구조")

    raw_quizzes = data["quizzes"]
    best_score = data["best_score"]

    if not isinstance(raw_quizzes, list):
        raise ValueError("퀴즈 목록 형식 오류")

    quizzes = []

    for item in raw_quizzes:
        question = item["question"]
        choices = item["choices"]
        answer = item["answer"]

        if (not isinstance(question, str)
            or not question.strip()
            or not isinstance(choices, list)
            or len(choices) != 4
            or not all(isinstance(c, str) and c.strip() for c in choices)
            or type(answer) is not int
            or not 1 <= answer <= 4):
            raise ValueError("퀴즈 데이터 형식 오류")

        quizzes.append(Quiz(question, choices, answer))

    if best_score is not None:
        if (type(best_score) not in (int, float)
            or not 0 <= best_score <= 100):
            raise ValueError("최고 점수 형식 오류")

    return quizzes, best_score


def menu():
    print("\n================================")
    print("       Python 퀴즈 게임")
    print("================================")
    print("1. 퀴즈 풀기")
    print("2. 퀴즈 추가")
    print("3. 퀴즈 목록")
    print("4. 점수 확인")
    print("5. 종료")
    print("================================")


def get_number(message, minimum, maximum):
    while True:
        value = input(message).strip()

        if value == "":
            print("입력값이 없습니다. 다시 입력하세요.")
            continue

        try:
            value = int(value)
        except ValueError:
            print("숫자를 입력하세요.")
            continue

        if minimum <= value <= maximum:
            return value

        print(f"{minimum}~{maximum} 사이의 숫자를 입력하세요.")


def play_quiz(quizzes):
    if len(quizzes) == 0:
        print("등록된 퀴즈가 없습니다.")
        return

    score = 0
    print(f"\n퀴즈를 시작합니다! (총 {len(quizzes)}문제)")

    for i in range(len(quizzes)):
        print(f"\n[문제 {i + 1}]")
        quizzes[i].show()

        answer = get_number("정답 입력: ", 1, 4)

        if quizzes[i].check_answer(answer):
            print("정답입니다!")
            score += 1
        else:
            print(f"오답입니다! 정답은 {quizzes[i].answer}번입니다.")

    total = len(quizzes)
    result = score / total * 100

    print("\n================================")
    print(f"결과: {total}문제 중 {score}문제 정답!")
    print(f"점수: {result:.0f}점")
    print("================================")

    return result


def show_quizzes(quizzes):
    if len(quizzes) == 0:
        print("등록된 퀴즈가 없습니다.")
        return

    print(f"\n등록된 퀴즈 목록 (총 {len(quizzes)}개)")

    for i in range(len(quizzes)):
        print(f"{i + 1}. {quizzes[i].question}")


def add_quiz(quizzes):
    def read_text(prompt):
        while True:
            text = input(prompt).strip()
            if text:
                return text
            print("입력값이 없습니다. 다시 입력하세요.")

    question = read_text("문제: ")
    choices = [read_text(f"선택지 {i}: ") for i in range(1, 5)]
    answer = get_number("정답 번호 (1~4): ", 1, 4)

    quizzes.append(Quiz(question, choices, answer))
    print("퀴즈가 추가되었습니다 !")


def show_best_score(best_score):
    if best_score is None:
        print("아직 퀴즈를 풀지 않았습니다.")
    else:
        print(f"최고 점수: {best_score:.0f}점")


class QuizGame:
    def __init__(self):
        self.quizzes = create_default_quizzes()
        self.best_score = None
        self.load_state()

    def show_menu(self):
        menu()
    
    def save_state(self):
        data = {
            "quizzes": [
                {
                    "question": quiz.question,
                    "choices": quiz.choices,
                    "answer": quiz.answer
                }
                for quiz in self.quizzes
            ],
            "best_score": self.best_score
            }

        try:
            payload = json.dumps(data, ensure_ascii=False, indent=4).encode("utf-8")
            try:
                previous = STATE_FILE.read_bytes()
            except FileNotFoundError:
                previous = None
            if previous is not None and previous != payload:
                try:
                    decode_state(previous)
                except (ValueError, KeyError, TypeError, IndexError):
                    pass  # 손상된 원본으로 정상 백업을 교체하지 않는다.
                else:
                    write_atomic(STATE_FILE.with_suffix(".json.bak"), previous)
            if previous != payload:
                write_atomic(STATE_FILE, payload)
            print("데이터가 저장되었습니다.")
        except (OSError, TypeError, ValueError) as error:
            print(f"데이터 저장 실패: {error}")

    def load_state(self):
        try:
            quizzes, best_score = decode_state(STATE_FILE.read_bytes())
            self.quizzes = quizzes
            self.best_score = best_score
            print(f"저장된 퀴즈 {len(quizzes)}개를 불러왔습니다.")

        except FileNotFoundError:
            print("저장된 파일이 없어 기본 퀴즈를 사용합니다.")

        except (OSError, UnicodeError, ValueError,
                KeyError, TypeError) as error:
            print(f"파일 오류: {error}")
            print("기본 퀴즈 데이터로 복구합니다.")
            self.quizzes = create_default_quizzes()
            self.best_score = None

    def play(self):
        score = play_quiz(self.quizzes)

        if score is not None:
            if self.best_score is None or score > self.best_score:
                self.best_score = score
                print("새로운 최고 점수입니다 !")

            self.save_state()

    def add(self):
        add_quiz(self.quizzes)
        self.save_state()

    def list_quizzes(self):
        show_quizzes(self.quizzes)

    def show_score(self):
        show_best_score(self.best_score)

    def run(self):
        try:
            while True:
                self.show_menu()
                choice = get_number("선택: ", 1, 5)

                if choice == 1:
                    self.play()
                elif choice == 2:
                    self.add()
                elif choice == 3:
                    self.list_quizzes()
                elif choice == 4:
                    self.show_score()
                elif choice == 5:
                    print("프로그램을 종료합니다.")
                    break

        except (KeyboardInterrupt, EOFError):
            print("\n입력이 중단되어 안전하게 종료합니다.")

        finally:
            self.save_state()

def main():
    game = QuizGame()
    game.run()


if __name__ == "__main__":
    main()