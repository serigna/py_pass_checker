
import hashlib
import requests
import re
import argparse

# Initialize parser
parser = argparse.ArgumentParser()

# Adding optional argument
parser.add_argument("--show-hash", action="store_true")

# Read arguments from command line
args = parser.parse_args()

url = 'https://api.pwnedpasswords.com/range'

while True:
    while len(password := input('Enter your password (or \'exit\' to quit): ')) >= 8 \
            and password != 'exit':

        hashed_pass = hashlib.sha1(password.encode()).hexdigest()
        if args.show_hash is not False:
            print('Your hashed password is:',
                  hashed_pass)
        print('Checking...')

        upd_url = url + f'/{hashed_pass[:5]}'

        response = requests.get(upd_url)

        test = response.text
        test_1 = test.split()
        reg_cmpl = re.compile(r':(.*)')
        total_amount = 0

        # print(len(test_1))
        if test_1:
            for item in test_1:
                re_result = re.search(reg_cmpl, item)
                if int(re_result.group(1)) > total_amount:
                    total_amount = int(re_result.group(1))

        if total_amount:
            print('Your password has been pwned! '
                  f'The password '
                  f'appears {total_amount} times in data breaches.')
        else:
            print('Good news! Your password hasn\'t been pwned.')

    if password == 'exit':
        print('Goodbye!')
        break
    else:
        print('Your password is too short. '
              'Please enter a password of at least 8 characters.')
