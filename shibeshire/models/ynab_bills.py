import requests
from datetime import date, timedelta, datetime
from time import strptime
import config


def main():
    start_date = input("Enter the first date: ")
    dates = get_dates(start_date)
    start_date = dates[0]
    end_date = dates[1]
    if start_date is False or end_date is False:
        print('Invalid Date Format')
    else:
        print("Bills due between " + start_date + " and " + end_date)
        print(get_bills(start_date, end_date))


def get_dates(date: date) -> list:
    # accepts a date as input. returns a list with two elements; the date entered and the date 13 days in the future
    dates = []

    try:
        start_date = datetime.strptime(date, config.time_format)
        end_date = (start_date + timedelta(days=13)).strftime(config.time_format)
        dates.append(start_date.strftime(config.time_format))
        dates.append(end_date)
        return dates
    except ValueError as err:
        return err


def get_bills(first_date: date, last_date: date) -> str:
    # make lists from the date strings for comparing the day in the ynab notes field
    first_date_elements = first_date.split("-")
    last_date_elements = last_date.split("-")
    # format the dates for comparison
    formatted_first_date = strptime(first_date, config.time_format)
    formatted_last_date = strptime(last_date, config.time_format)

    first_month = int(first_date_elements[0])
    first_day = int(first_date_elements[1])
    first_year = int(first_date_elements[2])
    last_month = int(last_date_elements[0])
    last_year = int(last_date_elements[2])

    # initialize defaults. since we set aside mortgage through the month, add it manually
    total = config.mortgage_amount
    bills_list = f"{first_date} Mortgage {config.mortgage_amount} \n"
    entry = ''

    # call ynab api
    headers = {"Authorization": "Bearer " + config.ynab_api_key}
    api_url = f"https://api.youneedabudget.com/v1/budgets/{config.budget_id}/categories/"
    response = requests.get(api_url, headers=headers).json()

    # get the data from the Shared Bills category group
    for group_id in response["data"]["category_groups"]:
        if (group_id["name"]) == "Shared Bills":
            # the "categories" key contains the bills
            bills = group_id["categories"]

    for entry in bills:
        due_day = int(entry["note"])
        bill = entry["name"]
        # ynab does't store the decimal so divide by 1000 and then divide by 2 since we split bills
        amount = round(entry["goal_target"]/1000/2, 2)

        # only the day is kept in ynab so that it doesn't have to be edited every month
        # here we build a proper date string and format it for comparison
        # if the due day is less than the first day, the due date is in the next month
        if due_day < first_day:
            due_date = str(last_month) + "-" + str(due_day) + "-" + str(last_year)
        else:
            due_date = str(first_month) + "-" + str(due_day) + "-" + str(first_year)
        formatted_due_date = strptime(due_date, config.time_format)

        # if a bill due date falls between the first and last date and is not the mortgage, append it to the bills list
        if formatted_due_date >= formatted_first_date and formatted_due_date \
                < formatted_last_date and bill != "Mortgage":
            entry = f"{due_date} {bill} {amount}"
            bills_list += entry + "\n"
            total += amount

    total = round(total, 2)
    return f"Bills due between {first_date} and {last_date}\n" + bills_list + 'total = ' + str(total)


if __name__ == '__main__':
    main()
