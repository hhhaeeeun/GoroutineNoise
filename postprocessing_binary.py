import numpy as np
input_path = "251115_results_10000_100_1.bin"   # 파일명
output_path = "trim3_lower4bits_1byte.bin"
ver = 5
# 1 : 20000제거 & trim 3%
# 2 : 20000제거 & trim 3% + 8비트로 합체
# 3 : 하위 4비트만
# 4 : 20000제거 하고 하위 4비트만
# 5 : 2비트 후처리 후 8비트로 합체

if ver == 1:
    # ===== 1. 데이터 로드 =====
    raw = np.fromfile(input_path, dtype=np.int32)

    # ===== 2. deterministic 값(20000) 제거 =====
    data = raw[raw != 20000]

    # ===== 3. 하위 3% Trim 적용 =====
    cut = np.percentile(data, 3)
    trimmed = data[data >= cut]

    # ===== 4. 하위 4비트 추출 =====
    lower4 = trimmed & 0x0F   # 0b1111

# ===== 5. uint8 형태로 변환하여 저장 =====
    lower4 = lower4.astype(np.uint8)

    lower4.tofile(output_path)

# ===== 6. 요약 출력 =====
    print("✅ 하위 4비트 추출 완료!")
    print("원본 샘플:", len(raw))
    print("20000 제거 후:", len(data))
    print("Trim 3% 적용 후:", len(trimmed))
    print("저장된 바이트 수:", len(lower4))
    print("출력 파일:", output_path)


elif ver == 2:
# ===== 1. 데이터 로드 =====
    raw = np.fromfile(input_path, dtype=np.int32)

# ===== 2. deterministic 값(20000) 제거 =====
    data = raw[raw != 20000]

# ===== 3. Trim 3% 적용 =====
    cut = np.percentile(data, 3)
    trimmed = data[data >= cut]

# ===== 4. 하위 4비트 추출 =====
    lower4 = (trimmed & 0x0F).astype(np.uint8)

# ===== 5. nibble를 2개씩 묶기 위한 padding =====
    if len(lower4) % 2 == 1:
        lower4 = np.append(lower4, 0)  # 0으로 패딩

# ===== 6. 2개씩 묶어서 1바이트 패킹 =====
    paired = lower4.reshape(-1, 2)
    packed_bytes = ((paired[:,0] << 4) | paired[:,1]).astype(np.uint8)

# ===== 7. 파일 저장 =====
    packed_bytes.tofile(output_path)

# ===== 8. 요약 정보 출력 =====
    print("✅ 하위 4비트 2개 → 1바이트 패킹 완료!")
    print("원본 샘플:", len(raw))
    print("20000 제거 후:", len(data))
    print("Trim 3% 적용 후:", len(trimmed))
    print("하위 4비트 샘플 수:", len(lower4))
    print("저장된 바이트 수:", len(packed_bytes))
    print("출력 파일:", output_path)

elif ver == 3:

    # ===== 1. RAW 데이터 로드 =====
    raw = np.fromfile(input_path, dtype=np.int32)

    # ===== 2. 하위 4비트 추출 =====
    lower4 = (raw & 0x0F).astype(np.uint8)

    # ===== 3. 1바이트씩 그대로 저장 =====
    output_path = "raw_1byte.bin"
    lower4.tofile(output_path)

    # ===== 4. 요약 출력 =====
    print("✅ RAW 하위 4비트 저장 완료!")
    print("원본 샘플:", len(raw))
    print("저장된 바이트 수:", len(lower4))
    print("출력 파일:", output_path)

elif ver == 4:
    # ===== 1. 데이터 로드 =====
    input_path = "251124_results_10000_200_1.bin"   # 필요하면 파일명 변경
    raw = np.fromfile(input_path, dtype=np.int32)

    # ===== 2. deterministic 값(20000) 제거 =====
    data = raw[raw != 20000]

    # ===== 3. 하위 4비트 추출 =====
    lower4 = (data & 0x0F).astype(np.uint8)

    # ===== 4. 1바이트씩 그대로 저장 =====
    lower4.tofile(output_path)

    # ===== 5. 요약 출력 =====
    print("✅ Trim 없는 하위 4비트 추출 완료!")
    print("원본 샘플:", len(raw))
    print("20000 제거 후:", len(data))
    print("저장된 바이트 수:", len(lower4))
    print("출력 파일:", output_path)

elif ver == 5:
# ===== 1. 데이터 로드 =====
    raw = np.fromfile(input_path, dtype=np.int32)

    # ===== 2. 20000 값 제거 (경쟁 미발생 deterministic 값) =====
    data = raw[raw != 20000]

    print("원본 샘플 수:", len(raw))
    print("20000 제외 후 샘플 수:", len(data))

    # ===== 3. 분위수(25%, 50%, 75%) 계산 =====
    q25 = np.percentile(data, 25)
    q50 = np.percentile(data, 50)
    q75 = np.percentile(data, 75)

    print("Q1 (25%):", q25)
    print("Q2 (50%):", q50)
    print("Q3 (75%):", q75)

    # ===== 4. 분위수 구간을 2비트 코드(0~3)로 매핑 =====
    # 0 -> 00, 1 -> 01, 2 -> 10, 3 -> 11 에 해당
    codes = np.zeros(len(data), dtype=np.uint8)

    codes[(data >= q25) & (data < q50)] = 1   # 01
    codes[(data >= q50) & (data < q75)] = 2   # 10
    codes[data >= q75]                    = 3 # 11

    # (참고: data < q25 인 구간은 기본값 0 → 00)

    # ===== 5. 2비트 코드 4개를 1바이트로 패킹 =====
    # 길이가 4의 배수가 아니면 뒤를 0으로 패딩
    pad_len = (-len(codes)) % 4
    if pad_len > 0:
        codes = np.pad(codes, (0, pad_len), mode="constant")

    codes_4 = codes.reshape(-1, 4)

    # 각 2비트 코드 배치:
    # [c0 c1 c2 c3] → [c0<<6 | c1<<4 | c2<<2 | c3]
    packed_bytes = (
        (codes_4[:, 0] << 6) |
        (codes_4[:, 1] << 4) |
        (codes_4[:, 2] << 2) |
        (codes_4[:, 3]      )
    ).astype(np.uint8)

    # ===== 6. 바이너리 파일로 저장 =====
    packed_bytes.tofile(output_path)

    print("패킹된 바이트 수:", len(packed_bytes))
    print("출력 파일:", output_path)