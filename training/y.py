
s1 = "learning python is not so difficult as we think"

def rev_str(s1):
    elements = s1.split(" ")
    reversed_elements = list()
    for i in range(0, len(elements)):
        if i % 2 == 0:
            reversed_elements.append(elements[i][::-1])
        else:
            reversed_elements.append(elements[i])

    print(" ".join(reversed_elements))
rev_str(s1)