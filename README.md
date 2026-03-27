# 🕺 DTW Analysis
K-pop 직캠 영상을 기반으로 전문가 관절 좌표를 추출하고,  
DTW(Dynamic Time Warping) 알고리즘을 활용하여 사용자 동작과의 유사도를 분석하는 후처리 시스템입니다.

---

## 🛠️ 기술 스택
- Python 3.10.20
- MediaPipe 0.10.33 — 관절 좌표 추출 (Pose Landmarker Heavy 모델)
- OpenCV — 영상 처리
- FastDTW — 동작 유사도 분석
- NumPy — 좌표 정규화 및 행렬 연산

---

## 📂 프로젝트 구조
```
dtw-analysis/
├── data/
│   ├── json/                            # 관절 좌표 JSON 데이터
│   │   ├── love-dive_0s-73s.json        # 팀원 제공 원본 데이터
│   │   ├── expert_lovedive.json         # MediaPipe 추출 데이터
│   │   └── expert_lovedive_visible.json # visibility 필터링 데이터
│   └── videos/                          # 전문가 직캠 영상 (git 제외)
├── notebooks/
│   ├── 01_extract_keypoints.ipynb       # MediaPipe 관절 좌표 추출
│   ├── 02_preprocessing.ipynb           # Visibility 필터링
│   └── 03_dtw_experiment.ipynb          # DTW 유사도 실험
├── post_analyzer.py                     # 팀원 JSON 구조 초기 분석 파일
├── .gitignore
└── README.md
```

---

## ⚙️ 환경 설정

### 1. conda 환경 활성화
```
conda activate kpop
```

### 2. 패키지 설치
```
pip install mediapipe opencv-python fastdtw scipy numpy
```

### 3. Jupyter 실행
```
cd dtw-analysis/notebooks
jupyter notebook
```
실행 후 `Kernel → Change Kernel → Python (kpop)` 선택

---

## 🚀 실행 순서

### Step 1 — 관절 좌표 추출 (`01_extract_keypoints.ipynb`)
1. `VIDEO_PATH`에 전문가 직캠 영상 경로 설정
2. `OUTPUT_PATH`에 저장할 JSON 경로 설정
3. `extract_keypoints()` 함수 실행
> 결과: `expert_{곡명}.json` — 프레임별 33개 관절 좌표 저장

### Step 2 — Visibility 필터링 (`02_preprocessing.ipynb`)
1. `INPUT_PATH`에 Step 1 결과 JSON 경로 설정
2. `apply_visibility_filter()` 함수 실행 (threshold=0.5)
> 결과: `expert_{곡명}_visible.json` — 신뢰 관절만 필터링

### Step 3 — DTW 유사도 분석 (`03_dtw_experiment.ipynb`)
1. `EXPERT_PATH`에 Step 2 결과 JSON 경로 설정
2. `normalize_landmarks()` — 골반 중심 정규화
3. `build_normalized_sequence()` — DTW 입력 시퀀스 생성
4. `fastdtw()` — 유사도 계산
5. `dtw_to_score()` — 0~100점 변환
> 결과: 동작 유사도 점수 산출

---

## 📊 실험 결과 (Love Dive 기준)
| 항목 | 결과 |
|---|---|
| 총 프레임 수 | 4,369 프레임 |
| 신뢰 관절 비율 | 92.4% (threshold=0.5) |
| 정규화 시퀀스 shape | (2720, 22) |
| 동일 구간 유사도 | 100.0점 |
| 상이 구간 유사도 | 55.33점 |

---

## 📝 개발 배경
팀원이 제공한 JSON 데이터(`love-dive_0s-73s.json`)를 분석하는 과정에서  
`visibility` 값이 전부 `false`로 추출되는 문제를 발견하였다.  
원인 분석 결과 MediaPipe 버전 차이로 인한 API 변경 문제였으며,  
최신 API(`Pose Landmarker Heavy`)로 재구현하여 해결하였다.
