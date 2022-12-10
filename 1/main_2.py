from typing import List

def top_3(res: List[int]) -> List[int]:
    s = sorted(res, reverse=True)
    return s[0:3]


if __name__ == "__main__":
    from main import main

    r = main()
    t3 = top_3(r)
    s3 = sum(t3)
    print(s3)
