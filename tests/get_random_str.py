import random, string


def get_random_str(length):
   letters = string.ascii_lowercase
   return ''.join(random.choice(letters) for i in range(length))

def randint(lenght):
   return random.randint(10^lenght, 10^(lenght+1)-1)