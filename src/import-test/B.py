import A as one

print("top-level in B.py")
one.func()

if __name__ == "__main__":
    print("B.py가 직접 실행")
else:
    print("B.py가 임포트되어 사용됨")


# https://hashcode.co.kr/questions/3/if-__name__-__main__%EC%9D%80-%EC%99%9C%EC%93%B0%EB%82%98%EC%9A%94