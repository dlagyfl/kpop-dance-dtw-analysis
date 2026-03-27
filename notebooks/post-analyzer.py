import json
import numpy as np

# ================================================
# STEP 1: JSON 파일 불러오기
# ================================================

def load_pose_json(filepath):
    """
    JSON 파일을 읽어서 파이썬이 다룰 수 있는 딕셔너리로 변환합니다.
    딕셔너리 = 열쇠(key)로 값을 찾는 자료구조 (예: data['songId'])
    """
    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data


# ================================================
# STEP 2: 기본 정보 출력 (데이터 파악용)
# ================================================

def print_summary(data):
    """
    JSON 데이터의 기본 구조를 사람이 읽기 쉽게 출력합니다.
    """
    print("=== 기본 정보 ===")
    print(f"곡 ID        : {data['songId']}")
    print(f"시작 ~ 종료  : {data['startTime']}초 ~ {data['endTime']}초")
    print(f"전체 프레임  : {data['totalFrames']}개")
    print(f"FPS          : {data['fps']}")
    print(f"실제 저장된 프레임 수: {len(data['landmarks'])}개")

    # 첫 번째 프레임 구조 확인
    first_frame = data['landmarks'][0]
    print(f"\n=== 첫 번째 프레임 ===")
    print(f"프레임 번호  : {first_frame['frame']}")
    print(f"타임스탬프   : {first_frame['timestamp']}초")
    print(f"랜드마크 개수: {len(first_frame['landmarks'])}개")
    print(f"첫 번째 관절 : {first_frame['landmarks'][0]}")


# ================================================
# STEP 3: 유효 프레임 필터링 (전처리 핵심)
# ================================================

def filter_valid_frames(data):
    """
    visible=False인 관절이 하나라도 있는 프레임을 제거합니다.
    
    왜 필요한가?
    - visible=False → MediaPipe가 관절을 감지하지 못한 상태
    - 이 데이터를 DTW에 넣으면 거리 계산이 오염됨
    """
    valid_frames = []

    for frame in data['landmarks']:
        # 해당 프레임의 모든 관절이 visible=True인지 확인
        all_visible = all(lm['visible'] for lm in frame['landmarks'])
        
        if all_visible:
            valid_frames.append(frame)

    total = len(data['landmarks'])
    valid = len(valid_frames)

    print(f"\n=== 프레임 필터링 결과 ===")
    print(f"전체 프레임  : {total}개")
    print(f"유효 프레임  : {valid}개")
    print(f"제거된 프레임: {total - valid}개")
    print(f"유효 비율    : {valid / total * 100:.1f}%")

    return valid_frames


# ================================================
# 실행 구간 (여기서부터 실제로 돌아가는 부분)
# ================================================

if __name__ == "__main__":
    
    # 1. JSON 파일 불러오기
    data = load_pose_json("data/love-dive_0s-73s.json")
    
    # 2. 기본 정보 출력
    print_summary(data)
    
    # 3. 유효 프레임 필터링
    valid_frames = filter_valid_frames(data)