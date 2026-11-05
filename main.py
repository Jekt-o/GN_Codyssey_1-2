
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


def get_choice():
    while True:
        choice = input("선택: ").strip()

        if choice == "":
            print("입력값이 없습니다. 다시 입력하세요.")
            continue

        try:
            choice = int(choice)
        except ValueError:
            print("숫자를 입력하세요.")
            continue

        if 1 <= choice <= 5:
            return choice

        print("1~5 사이의 숫자를 입력하세요.")


def main():
    try:
        while True:
            menu()
            choice = get_choice()

            if choice == 1:
                print("퀴즈 풀기 (구현 예정)")
            elif choice == 2:
                print("퀴즈 추가 (구현 예정)")
            elif choice == 3:
                print("퀴즈 목록 (구현 예정)")
            elif choice == 4:
                print("점수 확인 (구현 예정)")
            elif choice == 5:
                print("프로그램을 종료합니다.")
                break

    except (KeyboardInterrupt, EOFError):
        print("\n입력이 중단되어 안전하게 종료합니다.")


if __name__ == "__main__":
    main()
