from Crypto.Hash.MD5 import new

while True:
    text = input('>')
    print(new(text.encode()).hexdigest())
