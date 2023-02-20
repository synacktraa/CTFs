import sys

import re
import requests

URL = sys.argv[1]
# making a request to the target site
res = requests.get(URL)
# storing the UTF-8 decoded content
content = res.content.decode()

for idx in range(12):
	# To set the correct order for accessing the array named p, the statement loops through the indices 0 to 11.
	shift = fr"p\[{idx}\]" 
	
	# searches for `p[idx] === 520XX` pattern, splits it with `=== ` delimiter
	# and captures the second element which is `520XX` and converts it into
	# integer and then subtracts it with 0xCafe which is 51966 in decimal value
	# and the result is an ascii value which consists of all the english numbers,
	# alphabets and symbols 
	ascii_value = int(re.search(
		shift + r" === [0-9]{5}", 
		content
	).group(0).split("=== ")[1]) - 0xCafe # decimal: 51966

	# using inbuilt chr() function we can convert ascii value to human readable strings
	# using end="" as second parameter in print function, so that it doesn't print
	# new line after every character
	print(chr(ascii_value), end="")
