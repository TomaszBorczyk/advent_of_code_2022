def main():
    resources = []

    data = open("input.txt", "r", encoding="utf-8")
    total = 0
    
    for line in data:
        if line.strip() == "":
            resources.append(total)
            total = 0
        else:
            total += int(line.strip())

    return resources
            

if __name__ == "__main__":
    res = main()
    
