import requests
from datetime import timedelta, datetime
from time import strptime
import config
import click


def main():
    cli(prog_name="ynab")


@click.command()
@click.option("--start-date", "-d", type=str, required=True)
def cli(start_date):
    try:
        dates = get_dates(start_date)
        start_date = dates[0]
        end_date = dates[1]

        message = get_bills(start_date, end_date)
        click.echo("Sending bills list to discord")
        send_to_discord(message)
    except ValueError as err:
        print(err)


def get_dates(first_date: str) -> list:
    # accepts a date as input. returns a list with two elements; the date entered and the date 13 days in the future

    first_date = datetime.strptime(first_date, config.time_format)
    dates = []

    try:
        end_date = first_date + timedelta(days=13)
        dates.append(first_date)
        dates.append(end_date)
        return dates
    except ValueError as err:
        return err


def get_bills(first_date: datetime, last_date: datetime) -> str:

    # initialize defaults. since we set aside mortgage through the month, add it manually
    total = config.mortgage_amount
    bills_list = f"Mortgage {config.mortgage_amount} \n"

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
        # if the due day is less than the first day, the due date is in the next month
        if due_day < int(first_date.date().day):
            due_date = str(last_date.date().month) + "-" + str(due_day) + "-" + str(last_date.date().year)
        else:
            due_date = str(first_date.date().month) + "-" + str(due_day) + "-" + str(first_date.date().year)

        # format dates for comparison
        formatted_due_date = strptime(due_date, config.time_format)
        formatted_first_date = strptime(str(first_date), "%Y-%m-%d %H:%M:%S")
        formatted_last_date = strptime(str(last_date), "%Y-%m-%d %H:%M:%S")
        # if a bill due date falls between the first and last date and is not the mortgage, append it to the bills list
        if formatted_due_date >= formatted_first_date and formatted_due_date \
                < formatted_last_date and bill != "Mortgage":
            bills_list_entry = f"{bill} {amount}"
            bills_list += bills_list_entry + "\n"
            total += amount

    total = round(total, 2)
    return f"Bills due between {first_date.strftime('%m-%d')} and {last_date.strftime('%m-%d')}\n" + bills_list + 'total = ' + str(total)


def send_to_discord(bills_list):
    message = {
            "username": "Beels",
            "embeds": [
                {
                    "title": bills_list,
                    "color": 1206538
                }
            ]
        }

    requests.post(url=config.webhook_url, headers={"Content-Type": "application/json"}, json=message)


if __name__ == '__main__':
    main()
