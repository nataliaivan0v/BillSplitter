import decimal

def main():
    menu_items = []
    total_total = 0

    print("Hello!")
    print("Enter dish names and their prices separated by a space:")
    items = input().split()

    for i in range(0, len(items), 2):
        menu_items.append([i // 2, 0, float(items[i + 1])])
        total_total += float(items[i + 1])

    print("Enter the tax of the bill:")
    tax = float(input())
    print("Enter the tip of the bill:")
    tip = float(input())

    print("Enter the names of the people eating separated by spaces:")
    names = input().split()

    for i in range(0, len(items), 2):
        print(f"{i // 2}: {items[i]}")
    print()

    people = []
    for i, name in enumerate(names):
        print(f"{name}, enter the number(s) corresponding to the dish(es) you ate:")
        input_values = input().split()
        person = [i]
        for j in input_values:
            for item in menu_items:
                if item[0] == int(j):
                    item[1] += 1
            person.append(int(j))
        people.append(person)

    for i, name in enumerate(names):
        total = 0
        person = people[i]

        for j in range(1, len(person)):
            menu_item = person[j]
            for m in range(len(menu_items)):
                food = menu_items[m]
                if menu_item == food[0]:
                    total += food[2] / food[1]

        percent_of_bill = total / total_total
        total += round(percent_of_bill * tip, 2)
        total += round(percent_of_bill * tax, 2)

        print(f"{name} owes ${total}")

if __name__ == "__main__":
    main()