import re


def verification_date_of_birth(recognized_str):
    """Функция для подтверждения корректности даты рорждения
    """
    pattern_for_digits = re.compile('\d{1,4}')

    dict_month = {"январ": "01", "феврал": "02", "март": "03", "апрел": "04", "май": "05", "мая": "05", "июн": "06",
                  "июл": "07", "авгус": "08", "сентяб": "09", "октяб": "10", "нояб": "11", "декаб": "12"}

    result_year, result_month, result_day = None, None, None
    finded_digits = re.findall(pattern_for_digits, recognized_str)
    for elem in finded_digits:
        if elem == '0':
            finded_digits.remove(elem)

    for numbers in finded_digits:
        if int(numbers) > 31:
            result_year = int(numbers)
            finded_digits.remove(numbers)

    for key in dict_month.keys():
        if key in recognized_str:
            result_month = dict_month[key]

    if result_month is not None and len(finded_digits) == 1:
        result_day = finded_digits[0]

    if result_month is None and len(finded_digits) == 2:
        result_day = finded_digits[0]
        result_month = finded_digits[1]

    if result_day is None or result_month is None or result_year is None:
        return False
    else:
        result_year, result_month, result_day = str(result_year), str(result_month), str(result_day)
        if len(result_year) == 2:
            result_year = '19' + result_year
        if len(result_month) == 1:
            result_month = '0' + result_month
        if len(result_day) == 1:
            result_day = '0' + result_day
        final_result = ".".join([result_day, result_month, result_year])
        return final_result


print(verification_date_of_birth('13 0 9 1989 года'))
