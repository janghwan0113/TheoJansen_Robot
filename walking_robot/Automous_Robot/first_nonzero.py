import numpy as np

def first_nonzero(arr, axis, invalid_val=-1):
    arr = np.flipud(arr)  # 사진뒤집어주는 코드
    mask = arr != 0  # 숫자가 255인 것은 True(1), 0인 것은 False(0)
    # 가로축 기준으로, 최댓값(1)의 위치를 반환, 만약 1을 발견하지 못하면 뚫려있다는 의미이므로 height 값을 반환
    return np.where(mask.any(axis=axis), mask.argmax(axis=axis), invalid_val)
