
from quiz_data import create_default_quizzes


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


def show_quizzes(quizzes):
    if len(quizzes) == 0:
        print("등록된 퀴즈가 없습니다.")
        return

    print(f"\n등록된 퀴즈 목록 (총 {len(quizzes)}개)")

    for i in range(len(quizzes)):
        print(f"{i + 1}. {quizzes[i].question}")


def main():
    quizzes = create_default_quizzes()

    try:
        while True:
            menu()
            choice = get_number("선택: ", 1, 5)

            if choice == 1:
                play_quiz(quizzes)
            elif choice == 2:
                print("퀴즈 추가 (구현 예정)")
            elif choice == 3:
               show_quizzes(quizzes)
            elif choice == 4:
                print("점수 확인 (구현 예정)")
            elif choice == 5:
                print("프로그램을 종료합니다.")
                break

    except (KeyboardInterrupt, EOFError):
        print("\n입력이 중단되어 안전하게 종료합니다.")


if __name__ == "__main__":
    main()
