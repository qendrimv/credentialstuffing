# credentialstuffing

Template for testing your website against credential stuffing.

# Features

- Multithreads
- Build in proxy scraper - you can load proxies from file or let the script scrape new proxies every 10 minutes
- Calculates the average of successful requests per minute
- Supports http, socks4 and socks5 proxies

# How to use?

Open templte.py and the only thing that is required to be changed is the stuff inside the instance main function.
You will need to add the the headers, url & success/fail keys. Take a look at the examples provided and look at the main function inside the class to have a better understanding.

# MacOS
ctypes.windll.kernel32.SetConsoleTitleW is being used to show the stats and only works on windows. If you are on Mac you can use a alternative option or you can just print the stats to the screen.

# Disclaimer
Running credential stuffing or DDoS attacks on sites you don't own or you don't have permission to test is illegal. Everything provided was to help developers and pentesters to test their websites in order to make them more secure.
