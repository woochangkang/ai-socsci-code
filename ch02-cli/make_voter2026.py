"""voter2026.csv 생성 — 2장 2.4.1 CLAUDE.md 예시가 가리키는 합성 자료.

실재 조사가 아니라 전부 난수로 만든 연습용 자료다. 500명, 아홉 변수
(id, gender, age, region, ideology, q1, q2, q3, wt).
그 예시가 말하는 함정을 일부러 심어 두었다.
  · 수치형 결측을 -9로 코딩
  · region의 결측은 문자 "무응답"
  · q3은 역코딩 문항 (1~5 척도)
  · wt는 정규화되지 않은 가중치 (합 != n)

    python3 make_voter2026.py > voter2026.csv
"""

import csv
import random
import sys

N = 500
SEED = 2026

random.seed(SEED)

w = csv.writer(sys.stdout, lineterminator="\n")
w.writerow(["id", "gender", "age", "region", "ideology", "q1", "q2", "q3", "wt"])
for i in range(1, N + 1):
    gender = random.choice(["남성", "여성"])
    age = random.randint(19, 79)
    region = "무응답" if random.random() < 0.04 else random.choice(
        ["서울", "경기·인천", "충청", "호남", "영남", "강원·제주"])
    # 이념: 0~10, 6%는 무응답 -9
    ideology = -9 if random.random() < 0.06 else random.randint(0, 10)
    q1 = -9 if random.random() < 0.03 else random.randint(1, 5)
    q2 = -9 if random.random() < 0.03 else random.randint(1, 5)
    q3 = -9 if random.random() < 0.03 else random.randint(1, 5)   # 역코딩 문항
    wt = round(random.uniform(0.4, 2.1), 3)
    w.writerow([i, gender, age, region, ideology, q1, q2, q3, wt])
