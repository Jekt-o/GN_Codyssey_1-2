
from quiz import Quiz


def create_default_quizzes():
    quizzes = [
        Quiz(
            "CPU의 주요 역할은 무엇인가?",
            ["데이터 영구 저장", "명령어 처리", "화면 출력", "네트워크 연결"],
            2
        ),
        Quiz(
            "전원이 꺼지면 저장 내용이 사라지는 메모리는?",
            ["SSD", "HDD", "RAM", "ROM"],
            3
        ),
        Quiz(
            "Python에서 리스트를 나타내는 기호는?",
            ["{}", "()", "[]", "<>"],
            3
        ),
        Quiz(
            "2진수 1010을 10진수로 변환하면?",
            ["8", "9", "10", "11"],
            3
        ),
        Quiz(
            "HTTP 상태 코드 404의 의미는?",
            ["요청 성공", "서버 오류", "접근 금지", "요청한 리소스 없음"],
            4
        )
    ]

    return quizzes
