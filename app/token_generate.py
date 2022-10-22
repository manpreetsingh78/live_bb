import random
import string

def random_char(y):
    return ''.join(random.choice(string.ascii_letters) for x in range(y)).lower()
def random_number(d):
        num_min = ''
        for i in range(d):
            num_min += '1'
        num_max = ''
        for i in range(d):
            num_max += '9'

        return random.randint(int(num_min),int(num_max))
def tokengenerate():
    b = str(random_number(2)) + 'fac' + str(random_number(3)) + '-' + str(random_number(3)) + 'e' + '-' +  str(random_number(2)) + 'fd' + '-' + str(random_number(1)) + 'af' + str(random_number(1)) + '-' + 'b' + str(random_number(2)) + 'a' + str(random_number(8))

    return (b)

if __name__ == '__main__':
    tokengenerate()
