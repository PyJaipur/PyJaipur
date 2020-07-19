# PyJaipur Weekly Questions

## 1. Check whether a string starts and ends with a same character or not.

```py 
x = input("Enter any String: ")
if x[0] == x[-1]:
    print("Starts and Ends with same character: ",x[0])
else:
    print("Nope...different characters")
```

## 2. Remove duplicate words from the sentence .

```py
print(" ".join(set(input("Enter any sentence: ").split())))
```

### 3. Validate your email address .

```py
import re
email = input("Enter your mail id: ")
reg = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
if (re.search(reg,email)):
    print("Valid Email Format")
else:
    print("Incorrect Email")        
```

### 5. Determine whether the url is valid or not.

```py
import validators
url = input("Enter any url: ")
if validators.url(url):
    print("Url is valid")
else:
    print("Url is not Valid")
```
