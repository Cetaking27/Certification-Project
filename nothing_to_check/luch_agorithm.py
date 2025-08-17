<<<<<<< HEAD
def verify_card_number(card_number):
    sum_of_odd_digits = 0
    card_number_reversed = card_number[::-1]
    odd_digits = card_number_reversed[::2]

    for digit in odd_digits:
        sum_of_odd_digits += int(digit)

    sum_of_even_digits = 0
    even_digits = card_number_reversed[1::2]
    for digit in even_digits:
        number = int(digit) * 2
        if number >= 10:
            number = (number // 10) + (number % 10)
        sum_of_even_digits += number
    total = sum_of_odd_digits + sum_of_even_digits
    print(total)
    return total % 10 == 0

def main():
    card_number = '4111-1111-4555-1141'
    card_translation = str.maketrans({'-': '', ' ': ''})
    translated_card_number = card_number.translate(card_translation)

    if verify_card_number(translated_card_number):
        print('VALID!')
    else:
        print('INVALID!')

main()
=======

#The Luhn algorithm validator assists in checking and distinguishing the valid numbers from the mistyped or incorrect inputs. It is a method widely used by government and corporate entities to eliminate accidental errors by customers or users while using credit cards or identification numbers for online payments or transactions. 

#The Luhn algorithm calculator generates a checksum or checking key that is a single digit dependent determined by the sum of the sequence of numbers given. This check key is sometimes similar to the sequence’s last digit for verification purposes.

#The Luhn algorithm formula for verification of identification numbers includes the following steps,


#Step 1 –  The sequence of numbers starting from the first number on the right or the rightmost number is multiplied by two or doubled, and this follows for every second number from the first rightmost number. 
#Step 2 –  If the double of a digit is equal to or larger than 10, then the sum of the resultant double digit numbers is taken,
#Step 3 – Next step is to calculate the total of all the resultants that we have after multiplying by 2,
#Step 4 –  After realizing the sum of all digits, the check key or control digit ‘x’ equals = x = (10 – (x mod 10) mod 10). Thus, the value of ‘x’ is the checksum or check key according to Luhn Algorithm to verify a given sequence of numbers. Usually, the ‘x’ is the last digit of the identification number sequence that the algorithm determines. 

*/



def verify_card_number(card_number):
    sum_of_odd_digits = 0
    card_number_reversed = card_number[::-1]
    odd_digits = card_number_reversed[::2]

    for digit in odd_digits:
        sum_of_odd_digits += int(digit)

    sum_of_even_digits = 0
    even_digits = card_number_reversed[1::2]
    for digit in even_digits:
        number = int(digit) * 2
        if number >= 10:
            number = (number // 10) + (number % 10)
        sum_of_even_digits += number
    total = sum_of_odd_digits + sum_of_even_digits
    print(total)
    return total % 10 == 0

def main():
    card_number = '4111-4672-4555-1241'
    card_translation = str.maketrans({'-': '', ' ': ''})
    translated_card_number = card_number.translate(card_translation)

    if verify_card_number(translated_card_number):
        print('VALID!')
    else:
        print('INVALID!')

main()
>>>>>>> 712b70b1eb5a857fa9eef1170c9a9387a0dbb15a
