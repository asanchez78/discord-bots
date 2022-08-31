from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
from datetime import timedelta, datetime

# If modifying these scopes, delete the file token.json.
SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'


def main():
    # start_date = input("Enter the first date: ")
    start_date = '11-6-2020'
    dates = get_dates(start_date)
    start_date = dates[0]
    end_date = dates[1]
    if start_date is False or end_date is False:
        print('Invalid Date Format')
    else:
        print(bills(start_date, end_date))


def get_dates(date):
    # accepts a date as input. returns a list with two elements; the date entered and the date two weeks in the future
    date_elements = date.split('-')
    dates = []
    if len(date_elements) < 3:
        return False
    if len(date_elements[0]) < 4:
        if len(date_elements[2]) < 4:
            return False
        date = datetime.strptime(date, "%m-%d-%Y")
        end_date = (date + timedelta(days=14)).strftime("%Y-%m-%d")
        start_date = date.strftime("%Y-%m-%d")
        dates.append(start_date)
        dates.append(end_date)
        return dates


def bills(first_date, last_date):
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    store = file.Storage('models/token.json')
    creds = store.get()
    total = 0
    start = first_date + 'T08:00:00Z'
    end = last_date + 'T00:00:00.00Z'
    bills_list = ''
    mortgage = 0
    entry = ''

    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('models/credentials.json', SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('calendar', 'v3', http=creds.authorize(Http()))

    # Call the Calendar API
    events_result = service.events().list(calendarId='292n0fe5nb86p33bt68aap1th8@group.calendar.google.com',
                                          timeMin=start, timeMax=end, singleEvents=True, orderBy='startTime').execute()
    events = events_result.get('items', [])

    for event in events:
        due_date = event['start'].get('dateTime', event['start'].get('date'))
        event_str = str(event['summary'])
        amount = event_str.split("$")
        bill = amount[0]

        # if amount array has more than one element, it has a bill amount
        if len(amount) > 1:
            # if the bill is not mortgage, divide it by two and add it to the total
            if bill != 'Mortgage - ':
                try:
                    half_amount = round(float(amount[1]) / 2, 2)
                    total = total + half_amount
                except ValueError:
                    print("Error parsing bill amount")
                entry = f"{due_date} {bill}{half_amount}"
                bills_list += entry + '\n'
            # if the bill is mortgage, just add the amount to the total
            if bill == 'Mortgage - ':
                mortgage = float(amount[1])
                entry = f"{due_date} {bill}{amount[1]}"
                bills_list += entry + '\n'
                total = total + mortgage
    total = round(total, 2)
    return bills_list + 'total = ' + str(total)


if __name__ == '__main__':
    main()
