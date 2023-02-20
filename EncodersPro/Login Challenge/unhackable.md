# Login Challenge `Encoderspro`

![Login Challenge](https://user-images.githubusercontent.com/91981716/219969210-60c75f41-1b0e-41d8-9ddc-02e12e5894cc.png)


We've to bypass the login form, we can try bruteforcing but before that let's check the source code. 

> Press CTRL + Shift + I and go to sources tab
---
`This CheckPassword() function looks interesting.`

```js
// checkPassword() function takes user input and performs
// some calculations to check if it's the right password.
const checkPassword = () => {

    const v = document.getElementById("password").value;
    const p = Array.from(v).map(a => 0xCafe + a.charCodeAt(0));

    if(p[0] === 52014 &&
        p[6] === 52065 &&
        p[5] === 52063 &&
        p[1] === 52086 &&
        p[9] === 52064 &&
        p[10] === 52074 &&
        p[4] === 52038 &&
        p[3] === 52076 &&
        p[8] === 52063 &&
        p[7] === 52073 &&
        p[2] === 52051 &&
        p[11] === 52067) {
        window.location.replace(v + ".html");
    } else {
        alert("Wrong password!");
    }
}
```
---
```js
const v = document.getElementById("password").value;
```
 variable `v` stores the user given password

```js
const p = Array.from(v).map(a => 0xCafe + a.charCodeAt(0));
```
`Array.from()` function is used to convert a string to array `map()` method creates a new instance of the given array and adds `51966` (`0xCafe` in hex) with the ASCII value of every element.

```js
if(p[0] === 52014 &&
    p[6] === 52065 &&
    p[5] === 52063 &&
    p[1] === 52086 &&
    p[9] === 52064 &&
    p[10] === 52074 &&
    p[4] === 52038 &&
    p[3] === 52076 &&
    p[8] === 52063 &&
    p[7] === 52073 &&
    p[2] === 52051 &&
    p[11] === 52067) {
    window.location.replace(v + ".html");
} else {
    alert("Wrong password!");
}
```
It looks like the password is of `12` characters. This `IF` statement checks if every element matches certain number and if it does, it changes the window location to `user given password (variable v)`.html

---

> Given that we know each character in the password is added by either 0xCafe or 51966, we can simply subtract each element in the variable p by the same number and sort them in ascending order. Since performing this task manually is boring, let's utilize Python to automate the process.

```py
import sys

import re
import requests

URL = sys.argv[1]
res = requests.get(URL)
content = res.content.decode()

for idx in range(12):
	
  shift = fr"p\[{idx}\]" 

  ascii_value = int(re.search(
      shift + r" === [0-9]{5}", 
      content
  ).group(0).split("=== ")[1]) - 0xCafe

  print(chr(ascii_value), end="")
```

---

Making a request to the target site and storing the output in content variable
```py
URL = sys.argv[1]
res = requests.get(URL)
content = res.content.decode()
```
***

To set the correct order for accessing the array named p, the statement loops through the indices 0 to 11.
```py
for idx in range(12):
  shift = fr"p\[{idx}\]" 
```
***
Searches for the pattern `"p[idx] === 520XX"`, splits it using the delimiter `"=== "`, and then extracts the second element, which is `520XX`. This value is converted to an integer, and then subtracted from 0xCafe (which has a decimal value of 51966). The resulting ASCII value contains English numbers, alphabets, and symbols. 
```py
  ascii_value = int(re.search(
      shift + r" === [0-9]{5}", 
      content
  ).group(0).split("=== ")[1]) - 0xCafe
```
***
Converting the ASCII value to human-readable strings using the built-in `chr()` function in Python. To prevent the `print()` function from printing a new line after every character, we can pass `end=""` as the second parameter to the function.
```py
  print(chr(ascii_value), end="")
```

----
Run this script
```sh
python3 get_password.py "[Login Challenge URL]"
```
Output
```sh
0xUnHackable
```
