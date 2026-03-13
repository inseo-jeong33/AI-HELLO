import random

def start_game():
    secret_number = random.randint(1, 100) # 1~100 사이 랜덤 숫자
    attempts = 0
    
    print("🤖: 1부터 100 사이의 숫자를 맞춰보세요!")

    while True:
        guess = int(input("숫자를 입력하세요: "))
        attempts += 1

        if guess < secret_number:
            print("⬆️ UP! 더 큰 숫자예요.")
        elif guess > secret_number:
            print("⬇️ DOWN! 더 작은 숫자예요.")
        else:
            print(f"🎉 정답입니다! {attempts}번 만에 맞히셨네요!")
            break

start_game()