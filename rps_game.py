import random

# 전적을 저장할 딕셔너리
stats = {"승": 0, "무": 0, "패": 0}
options = ["가위", "바위", "보"]

print("🕹️ 가위바위보 게임을 시작합니다! (종료하려면 '그만' 입력)")

while True:
    # 1. 사용자 입력 받기
    user_choice = input("\n가위, 바위, 보 중 하나를 선택하세요: ")
    
    if user_choice == "그만":
        break
    
    if user_choice not in options:
        print("❌ 잘못된 입력입니다. 다시 입력해주세요.")
        continue

    # 2. 컴퓨터의 선택 (랜덤)
    computer_choice = random.choice(options)
    print(f"🤖 컴퓨터: {computer_choice}")

    # 3. 승패 판정 로직
    if user_choice == computer_choice:
        print("🤝 비겼습니다!")
        stats["무"] += 1
    elif (user_choice == "가위" and computer_choice == "보") or \
         (user_choice == "바위" and computer_choice == "가위") or \
         (user_choice == "보" and computer_choice == "바위"):
        print("🎉 이겼습니다!")
        stats["승"] += 1
    else:
        print("😭 졌습니다...")
        stats["패"] += 1

    # 4. 현재 승률 계산
    total = sum(stats.values())
    win_rate = (stats["승"] / total) * 100
    print(f"📊 현재 전적: {stats['승']}승 {stats['무']}무 {stats['패']}패 (승률: {win_rate:.1f}%)")

print("\n👋 게임을 종료합니다. 즐거우셨나요?")