"""practice_survey.csv 생성 — 1장 1.5.3 실습용 합성 자료.

실재 응답이 아니라 전부 난수로 만든 연습용 자료다. 300명, 네 변수
(id, gender, age, trust). 본문 1.5.3의 실행 결과(남성 143 / 여성 157)가
이 파일에서 나온 값이다.

    python3 make_practice_survey.py > practice_survey.csv

이 스크립트는 자료의 **출처 기록**이지 배포 수단이 아니다. 독자에게는
practice_survey.csv 파일 자체를 준다 — 아래 주의 참조.

주의 (재현 범위):
    Python 공식 문서는 random 모듈에 대해, 버전 간 재현이 보장되는 것은
    random() 메서드뿐이며 나머지 알고리즘과 seeding 함수는 변경될 수 있다고
    명시한다. 이 스크립트가 쓰는 choice()·randint()는 그 보장 밖이다.
    2026-08-09 기준 Python 3.9.6 / 3.11.15 에서 동일한 파일이 나오는 것을
    확인했으나(md5 9199d8f81d1e62d01b2c179a8fc062ea), 먼 미래의 Python에서도
    같으리라는 보장은 없다. 그래서 CSV 파일을 함께 보관한다.
"""

import csv
import random
import sys

N = 300
SEED = 2026

random.seed(SEED)

w = csv.writer(sys.stdout, lineterminator="\n")
w.writerow(["id", "gender", "age", "trust"])
for i in range(1, N + 1):
    # 뽑는 순서가 곧 난수열의 소비 순서다. 순서를 바꾸면 다른 파일이 나온다.
    gender = random.choice(["남성", "여성"])
    age = random.randint(19, 79)
    trust = random.randint(1, 5)
    w.writerow([i, gender, age, trust])
