# Task 5.1

def sort_content(source, destination):
    with open(source, 'r') as f:
        data = sorted(f.readlines())
    with open(destination, 'w') as f:
        f.writelines(data)

sort_content('../data/unsorted_names.txt', '../data/sorted_names.txt')