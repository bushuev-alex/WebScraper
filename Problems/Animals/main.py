# read animals.txt
# and write animals_new.txt

with open('animals.txt', 'r') as animals:
    with open('animals_new.txt', 'a') as animals_new:
        for line in animals:
            animals_new.write(line.strip() + ' ')
