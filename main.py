# coding: cp1252

import os
import json
import subprocess
from clickup import create_task

# Execute the second script as a subprocess
subprocess.run(['python', 'fetch_members.py'])

def link(uri, label=None):
    if label is None: 
        label = uri
    parameters = ''

    # OSC 8 ; params ; URI ST <name> OSC 8 ;; ST 
    escape_mask = '\033]8;{};{}\033\\{}\033]8;;\033\\'

    return escape_mask.format(parameters, uri, label)

# Function to load configuration from JSON file
def load_config(file_path='config.json'):
    with open(file_path, 'r') as file:
        return json.load(file)

def ask_question(question, valid_answers=None):
    while True:
        answer = input(question + ' ').strip().lower()
        if valid_answers and answer not in valid_answers:
            print("I'm sorry that is an invalid answer, please try again.")
        else:
            return answer
            
def find_user_id_by_email(email):
    try:
        with open('members.json', 'r') as json_file:
            members = json.load(json_file)
            for member in members:
                if member['email'] == email:
                    return member['user_id']
            return None
    except FileNotFoundError:
        print("The file members.json does not exist. Please run fetch_members.py first.")
        return None

def troubleshoot_irev():
    # Load the configuration
    config = load_config()
    sales_id = config.get('sales_id')
    mkt_id = config.get('mkt_id')
    it_id = config.get('it_id')
    ts_id = config.get('ts_id')
    api_key = config.get('api_key')

    ts_email = input("What is your email? ")
    while True:
        ts_userid = find_user_id_by_email(ts_email)
        if ts_userid:
            print(f"The user ID for email {ts_email} is {ts_userid}.")
            travel_specialist = ask_question('What is your full name?')
            market = ask_question('What is your market?')
            destination = ask_question('What brand do you work for?')
            planned_irev = ask_question('Are you making your planned iRev?', ['yes', 'no'])
            if planned_irev == 'yes':
                roas = ask_question('Is your ROAS above 100%?', ['yes', 'no'])
                if roas == 'yes':
                    occupancy = ask_question('Do you have any occupancy left?', ['yes', 'no'])
                    if occupancy == 'yes':
                        name = f'[Rock my iRev] ROAS is above 100% for {travel_specialist}'
                        description = f'Let {travel_specialist} know whether we can increase the spending or not'
                        priority = 3  # Assuming 2 corresponds to high priority
                        assignees = [find_user_id_by_email('louis.poissant@venturatravel.org')]  # Replace 'USER_ID' with the actual ID of the user
                        try:
                            task_url = create_task(api_key, sales_id, name, description, priority, assignees)
                            if task_url:
                                print('Your trip is performing great! We even have potential to sell more. Louis is checking whether we can increase the spending to push your trip a bit more and will let you know!')
                            else:
                                print('Error Connecting to ClickUp')
                        except Exception as e:
                            print(f'An error occurred while creating the task: {e}')
                    else:
                        print('Your trip is performing great! We would even have potential to sell more, if we had more departures open. If you have the chance to open up new departures, do a quick check with Louis to see whether we can push your trip a bit more.')
                else:
                    name = f'[Rock my iRev] ROAS request for {travel_specialist}'
                    description = f'Check how to improve ROAS for {travel_specialist} in the {market} market for the brand {destination}'
                    priority = 3  # Assuming 2 corresponds to high priority
                    assignees = [find_user_id_by_email('louis.poissant@venturatravel.org')]  # Replace 'USER_ID' with the actual ID of the user
                    try:
                        task_url = create_task(api_key, mkt_id, name, description, priority, assignees)
                        if task_url:
                            print('As long as ROAS is not above 100% we can’t push your destination more, but good news: you are on plan, so no need to worry. However, Marketing is now checking how to improve ROAS. Follow up on their task here: {task_url}')
                        else:
                            print('Error Connecting to ClickUp')
                    except Exception as e:
                        print(f'An error occurred while creating the task: {e}')
            else:
                receiving_deals = ask_question('Are you receiving enough deals?', ['yes', 'no'])
                if receiving_deals == 'yes':
                    conversion_rate = ask_question('Is your conversion rate Deal-Booking below plan?', ['yes', 'no'])
                    if conversion_rate == 'yes':
                        
                        hubspot_response = ask_question('Is your Hubspot response time below 24 hours?', ['yes', 'no'])
                        if hubspot_response == 'yes':
                            aircall_response = ask_question('Is your Aircall response rate above 80%?', ['yes', 'no'])
                            if aircall_response == 'yes':
                                reservations = ask_question('Do you have reservations that need a push to close?', ['yes', 'no'])
                                if reservations == 'yes':
                                    name = f'[Rock my iRev] Review the cost structure of your trip'
                                    description = f'Check the market price and cost calculation and make sure your trip is profitable Are real flight cost above the EFC? Did you recently apply many discounts on the reservations for this trip? Where they all really necessary? If you have a doubt, ask your manager to review with you.'
                                    priority = 3
                                    assignees = [ts_userid]
                                    try:
                                        task_url = create_task(api_key, ts_id, name, description, priority, assignees)
                                        if task_url:
                                            print(f'Make sure to send all invoices and follow up with outstanding payments to get the iRev that is currently in the pipeline confirmed. Here is the clickup task: {task_url}')
                                        else:
                                            print('Error Connecting to ClickUp')
                                    except Exception as e:
                                        print(f'An error occurred while creating the task: {e}')
                                    print('We figured out that the deals are not converting well. Now, let’s see whether the ones that convert bring enough iRev, or whether we also need to fix the iRev per pax.')
                                    irev_average = ask_question('Is your average iRev per reservation below plan?', ['yes', 'no'])
                                    if irev_average == 'yes':
                                        name = f'[Rock my iRev] Review the cost structure of your trip'
                                        description = f'Check the market price and cost calculation and make sure your trip is profitable Are real flight cost above the EFC? Did you recently apply many discounts on the reservations for this trip? Where they all really necessary? If you have a doubt, ask your manager to review with you.'
                                        priority = 3
                                        assignees = [ts_userid]
                                        try:
                                            task_url = create_task(api_key, ts_id, name, description, priority, assignees)
                                            if task_url:
                                                print('You need to review the pricing of your trip. Please check cost and price, and make sure flight costs and operations have not increased. Here is a link to a clickup task we created for you:')
                                                print(task_url)
                                            else:
                                                print('Error Connecting to ClickUp')
                                        except Exception as e:
                                            print(f'An error occurred while creating the task: {e}')
                                    else:
                                        name = f'[Rock my iRev] iRev is low although all metrics look good'
                                        description = f'Investigate and give an update to {travel_specialist}.'
                                        priority = 3
                                        assignees = [find_user_id_by_email('kim@venturatravel.org')]
                                        try:
                                            task_url = create_task(api_key, sales_id, name, description, priority, assignees)
                                            if task_url:
                                                print(f'We reached a dead end. Based on your answers, iRev should not be below plan. The Sales team is now investigating further. You can follow up here: {task_url}')
                                            else:
                                                print('Error Connecting to ClickUp')
                                        except Exception as e:
                                            print(f'An error occurred while creating the task: {e}')
                                else:
                                    name = f'[Rock my iRev] iRev is low although all metrics look good'
                                    description = f'Investigate and give an update to {travel_specialist}.'
                                    priority = 3
                                    assignees = [find_user_id_by_email('kim@venturatravel.org')]
                                    try:
                                        task_url = create_task(api_key, sales_id, name, description, priority, assignees)
                                        if task_url:
                                            print(f'We reached a dead end. Based on your answers, iRev should not be below plan. The Sales team is now investigating further. You can follow up here: {task_url}')
                                        else:
                                            print('Error Connecting to ClickUp')
                                    except Exception as e:
                                        print(f'An error occurred while creating the task: {e}')                                                      
                            else:
                                name = f"[Rock my iRev] {travel_specialist}'s phone response is below 80%."
                                description = f"Please review whether you can identify a reason and give recommendations."
                                priority = 3
                                assignees = [find_user_id_by_email('maxime.fournier@venturatravel.org')]
                                try:
                                    task_url = create_task(api_key, sales_id, name, description, priority, assignees)
                                    if task_url:
                                        print(f'Task pushed successfully to the Sales Team')
                                        print(f'{task_url}')
                                        name = f'[Rock my iRev]  I confirm that I have reviewed and implemented best practice for phone communication.'
                                        description = f'I have blocked phone hours and focus hours in my calendar and are sure that whenever I am not available (lunch, team meeting) my phone line is covered by someone else. I am always setting myself as unavailable as soon as I am not able to pick up a call (leaving the desk, team meeting).'
                                        priority = 3
                                        assignees = [ts_userid]
                                        try:
                                            task_url = create_task(api_key, ts_id, name, description, priority, assignees)
                                            if task_url:
                                                print('Probably some of your leads are giving up after not being able to reach you. Read the following vHelp to learn how to improve your phone availability and confirm that you have implemented the steps. At the same time, the sales team is reviewing whether they can identify anything you could improve and will let you know.')
                                                print(f'Your Task: {task_url}')
                                                print('https://vhelp.venturatravel.org/en/productsandsales/salesmanagement/sales-advanced')
                                            else:
                                                print('Error Connecting to ClickUp')
                                        except Exception as e:
                                            print(f'An error occurred while creating the task: {e}')
                                    else:
                                        print('Error Connecting to ClickUp')
                                except Exception as e:
                                    print(f'An error occurred while creating the task: {e}')
                                print('Now let’s see whether we can identify even more room for improvement, looking at your other Sales KPIs...')
                                reservations = ask_question('Do you have reservations that need a push to close?', ['yes', 'no'])
                                if reservations == 'yes':
                                    name = f'[Rock my iRev] Review the cost structure of your trip'
                                    description = f'Check the market price and cost calculation and make sure your trip is profitable Are real flight cost above the EFC? Did you recently apply many discounts on the reservations for this trip? Where they all really necessary? If you have a doubt, ask your manager to review with you.'
                                    priority = 3
                                    assignees = [ts_userid]
                                    try:
                                        task_url = create_task(api_key, ts_id, name, description, priority, assignees)
                                        if task_url:
                                            print(f'Make sure to send all invoices and follow up with outstanding payments to get the iRev that is currently in the pipeline confirmed. Here is the clickup task: {task_url}')
                                        else:
                                            print('Error Connecting to ClickUp')
                                    except Exception as e:
                                        print(f'An error occurred while creating the task: {e}')
                                    print('We figured out that the deals are not converting well. Now, let’s see whether the ones that convert bring enough iRev, or whether we also need to fix the iRev per pax.')
                                    irev_average = ask_question('Is your average iRev per reservation below plan?', ['yes', 'no'])
                                    if irev_average == 'yes':
                                        print('You need to review the pricing of your trip. Please check cost and price, and make sure flight costs and operations have not increased. Create a ClickUp task for this!')
                                    else:
                                        name = f'[Rock my iRev] iRev is low although all metrics look good'
                                        description = f'Investigate and give an update to {travel_specialist}.'
                                        priority = 3
                                        assignees = [find_user_id_by_email('kim@venturatravel.org')]
                                        try:
                                            task_url = create_task(api_key, sales_id, name, description, priority, assignees)
                                            if task_url:
                                                print(f'We reached a dead end. Based on your answers, iRev should not be below plan. The Sales team is now investigating further. You can follow up here: {task_url}')
                                            else:
                                                print('Error Connecting to ClickUp')
                                        except Exception as e:
                                            print(f'An error occurred while creating the task: {e}')
                                else:
                                    name = f'[Rock my iRev] iRev is low although all metrics look good'
                                    description = f'Investigate and give an update to {travel_specialist}.'
                                    priority = 3
                                    assignees = [find_user_id_by_email('kim@venturatravel.org')]
                                    try:
                                        task_url = create_task(api_key, sales_id, name, description, priority, assignees)
                                        if task_url:
                                            print(f'We reached a dead end. Based on your answers, iRev should not be below plan. The Sales team is now investigating further. You can follow up here: {task_url}')
                                        else:
                                            print('Error Connecting to ClickUp')
                                    except Exception as e:
                                        print(f'An error occurred while creating the task: {e}')
                        else:
                            name = f'[Rock my iRev]  I confirm that I have reviewed and implemented best practice for email communication.'
                            description = f'I know which templates to use for recurring topics and am actively using them, I know how to filter for new email tasks and am always tackling them first.'
                            priority = 3
                            assignees = [ts_userid]
                            try:
                                task_url = create_task(api_key, ts_id, name, description, priority, assignees)
                                if task_url:
                                    name = f'[Rock my iRev] {travel_specialist} email response time is above 24 hours.'
                                    description = f'Please review whether you can identify a reason and give recommendations.'
                                    priority = 3
                                    assignees = [find_user_id_by_email('maxime.fournier@venturatravel.org')]
                                    try:
                                        task_url = create_task(api_key, ts_id, name, description, priority, assignees)
                                        if task_url:
                                            print('The issue might be that your competition is faster than you in responding to clients, so leads are no longer interested when you reach out to them. Make sure to always answer new emails within 24 hours. Check out this vHelp to learn how to achieve this. At the same time, the Sales team is reviewing whether they can identify anything you could improve and will let you know.')
                                            print('https://vhelp.venturatravel.org/en/productsandsales/salesmanagement/sales-advanced')
                                        else:
                                            print('Error Connecting to ClickUp')
                                    except Exception as e:
                                        print('Error')
                                else:
                                    print('Error Connecting to ClickUp')
                            except Exception as e:
                                print(f'An error occurred while creating the task: {e}')
                            print('Now let’s see whether we can identify even more room for improvement, looking at your other Sales KPIs...')
                            aircall_response = ask_question('Is your Aircall response rate above 80%?', ['yes', 'no'])
                            if aircall_response == 'yes':
                                reservations = ask_question('Do you have reservations that need a push to close?', ['yes', 'no'])
                                if reservations == 'yes':
                                    name = f'[Rock my iRev] Review the cost structure of your trip'
                                    description = f'Check the market price and cost calculation and make sure your trip is profitable Are real flight cost above the EFC? Did you recently apply many discounts on the reservations for this trip? Where they all really necessary? If you have a doubt, ask your manager to review with you.'
                                    priority = 3
                                    assignees = [ts_userid]
                                    try:
                                        task_url = create_task(api_key, ts_id, name, description, priority, assignees)
                                        if task_url:
                                            print(f'Make sure to send all invoices and follow up with outstanding payments to get the iRev that is currently in the pipeline confirmed. Here is the clickup task: {task_url}')
                                        else:
                                            print('Error Connecting to ClickUp')
                                    except Exception as e:
                                        print(f'An error occurred while creating the task: {e}')
                                    print('We figured out that the deals are not converting well. Now, let’s see whether the ones that convert bring enough iRev, or whether we also need to fix the iRev per pax.')
                                    irev_average = ask_question('Is your average iRev per reservation below plan?', ['yes', 'no'])
                                    if irev_average == 'yes':
                                        name = f'[Rock my iRev] Review the cost structure of your trip'
                                        description = f'Check the market price and cost calculation and make sure your trip is profitable Are real flight cost above the EFC? Did you recently apply many discounts on the reservations for this trip? Where they all really necessary? If you have a doubt, ask your manager to review with you.'
                                        priority = 3
                                        assignees = [ts_userid]
                                        try:
                                            task_url = create_task(api_key, ts_id, name, description, priority, assignees)
                                            if task_url:
                                                print('You need to review the pricing of your trip. Please check cost and price, and make sure flight costs and operations have not increased. Here is a link to a clickup task we created for you:')
                                                print(task_url)
                                            else:
                                                print('Error Connecting to ClickUp')
                                        except Exception as e:
                                            print(f'An error occurred while creating the task: {e}')
                                    else:
                                        name = f'[Rock my iRev] iRev is low although all metrics look good'
                                        description = f'Investigate and give an update to {travel_specialist}.'
                                        priority = 3
                                        assignees = [find_user_id_by_email('kim@venturatravel.org')]
                                        try:
                                            task_url = create_task(api_key, sales_id, name, description, priority, assignees)
                                            if task_url:
                                                print(f'We reached a dead end. Based on your answers, iRev should not be below plan. The Sales team is now investigating further. You can follow up here: {task_url}')
                                            else:
                                                print('Error Connecting to ClickUp')
                                        except Exception as e:
                                            print(f'An error occurred while creating the task: {e}')
                                else:
                                    name = f'[Rock my iRev] iRev is low although all metrics look good'
                                    description = f'Investigate and give an update to {travel_specialist}.'
                                    priority = 3
                                    assignees = [find_user_id_by_email('kim@venturatravel.org')]
                                    try:
                                        task_url = create_task(api_key, sales_id, name, description, priority, assignees)
                                        if task_url:
                                            print(f'We reached a dead end. Based on your answers, iRev should not be below plan. The Sales team is now investigating further. You can follow up here: {task_url}')
                                        else:
                                            print('Error Connecting to ClickUp')
                                    except Exception as e:
                                        print(f'An error occurred while creating the task: {e}')                                                      
                            else:
                                name = f"[Rock my iRev] {travel_specialist}'s phone reposnse is below 80%."
                                description = f"Please review whether you can identify a reason and give recommendations."
                                priority = 3
                                assignees = [find_user_id_by_email('maxime.fournier@venturatravel.org')]
                                try:
                                    task_url = create_task(api_key, sales_id, name, description, priority, assignees)
                                    if task_url:
                                        print(f'Task pushed successfully to the Sales Team')
                                        print(f'{task_url}')
                                        name = f'[Rock my iRev]  I confirm that I have reviewed and implemented best practice for phone communication.'
                                        description = f'I have blocked phone hours and focus hours in my calendar and are sure that whenever I am not available (lunch, team meeting) my phone line is covered by someone else. I am always setting myself as unavailable as soon as I am not able to pick up a call (leaving the desk, team meeting).'
                                        priority = 3
                                        assignees = [ts_userid]
                                        try:
                                            task_url = create_task(api_key, ts_id, name, description, priority, assignees)
                                            if task_url:
                                                print('Probably some of your leads are giving up after not being able to reach you. Read the following vHelp to learn how to improve your phone availability and confirm that you have implemented the steps. At the same time, the sales team is reviewing whether they can identify anything you could improve and will let you know.')
                                                print(f'Your Task: {task_url}')
                                                print('https://vhelp.venturatravel.org/en/productsandsales/salesmanagement/sales-advanced')
                                            else:
                                                print('Error Connecting to ClickUp')
                                        except Exception as e:
                                            print(f'An error occurred while creating the task: {e}')
                                except Exception as e:
                                    print(f'An error occurred while creating the task: {e}')
                                print('Now let’s see whether we can identify even more room for improvement, looking at your other Sales KPIs...')
                                reservations = ask_question('Do you have reservations that need a push to close?', ['yes', 'no'])
                                if reservations == 'yes':
                                    name = f'[Rock my iRev] Review the cost structure of your trip'
                                    description = f'Check the market price and cost calculation and make sure your trip is profitable Are real flight cost above the EFC? Did you recently apply many discounts on the reservations for this trip? Where they all really necessary? If you have a doubt, ask your manager to review with you.'
                                    priority = 3
                                    assignees = [ts_userid]
                                    try:
                                        task_url = create_task(api_key, ts_id, name, description, priority, assignees)
                                        if task_url:
                                            print(f'Make sure to send all invoices and follow up with outstanding payments to get the iRev that is currently in the pipeline confirmed. Here is the clickup task: {task_url}')
                                        else:
                                            print('Error Connecting to ClickUp')
                                    except Exception as e:
                                        print(f'An error occurred while creating the task: {e}')
                                    print('We figured out that the deals are not converting well. Now, let’s see whether the ones that convert bring enough iRev, or whether we also need to fix the iRev per pax.')
                                    irev_average = ask_question('Is your average iRev per reservation below plan?', ['yes', 'no'])
                                    if irev_average == 'yes':
                                        name = f'[Rock my iRev] Review the cost structure of your trip'
                                        description = f'Check the market price and cost calculation and make sure your trip is profitable Are real flight cost above the EFC? Did you recently apply many discounts on the reservations for this trip? Where they all really necessary? If you have a doubt, ask your manager to review with you.'
                                        priority = 3
                                        assignees = [ts_userid]
                                        try:
                                            task_url = create_task(api_key, ts_id, name, description, priority, assignees)
                                            if task_url:
                                                print('You need to review the pricing of your trip. Please check cost and price, and make sure flight costs and operations have not increased. Here is a link to a clickup task we created for you:')
                                                print(task_url)
                                            else:
                                                print('Error Connecting to ClickUp')
                                        except Exception as e:
                                            print(f'An error occurred while creating the task: {e}')
                                    else:
                                        name = f'[Rock my iRev] iRev is low although all metrics look good'
                                        description = f'Investigate and give an update to {travel_specialist}.'
                                        priority = 3
                                        assignees = [find_user_id_by_email('kim@venturatravel.org')]
                                        try:
                                            task_url = create_task(api_key, sales_id, name, description, priority, assignees)
                                            if task_url:
                                                print(f'We reached a dead end. Based on your answers, iRev should not be below plan. The Sales team is now investigating further. You can follow up here: {task_url}')
                                            else:
                                                print('Error Connecting to ClickUp')
                                        except Exception as e:
                                            print(f'An error occurred while creating the task: {e}')
                                else:
                                    name = f'[Rock my iRev] iRev is low although all metrics look good'
                                    description = f'Investigate and give an update to {travel_specialist}.'
                                    priority = 3
                                    assignees = [find_user_id_by_email('kim@venturatravel.org')]
                                    try:
                                        task_url = create_task(api_key, sales_id, name, description, priority, assignees)
                                        if task_url:
                                            print(f'We reached a dead end. Based on your answers, iRev should not be below plan. The Sales team is now investigating further. You can follow up here: {task_url}')
                                        else:
                                            print('Error Connecting to ClickUp')
                                    except Exception as e:
                                        print(f'An error occurred while creating the task: {e}')
                    else:
                        irev_average = ask_question('Is your average iRev per reservation below plan?', ['yes', 'no'])
                        if irev_average == 'yes':
                            name = f'[Rock my iRev] Review the cost structure of your trip'
                            description = f'Check the market price and cost calculation and make sure your trip is profitable Are real flight cost above the EFC? Did you recently apply many discounts on the reservations for this trip? Where they all really necessary? If you have a doubt, ask your manager to review with you.'
                            priority = 3
                            assignees = [ts_userid]
                            try:
                                task_url = create_task(api_key, ts_id, name, description, priority, assignees)
                                if task_url:
                                    print('You need to review the pricing of your trip. Please check cost and price, and make sure flight costs and operations have not increased. Here is a link to a clickup task we created for you:')
                                    print(task_url)
                                else:
                                    print('Error Connecting to ClickUp')
                            except Exception as e:
                                print(f'An error occurred while creating the task: {e}')
                        else:
                            name = f'[Rock my iRev] iRev is low although all metrics look good'
                            description = f'Investigate and give an update to {travel_specialist}.'
                            priority = 3
                            assignees = [find_user_id_by_email('kim@venturatravel.org')]
                            try:
                                task_url = create_task(api_key, sales_id, name, description, priority, assignees)
                                if task_url:
                                    print(f'We reached a dead end. Based on your answers, iRev should not be below plan. The Sales team is now investigating further. You can follow up here: {task_url}')
                                else:
                                    print('Error Connecting to ClickUp')
                            except Exception as e:
                                print(f'An error occurred while creating the task: {e}')
                else:
                    sessions = ask_question('Do you have enough sessions?', ['yes', 'no'])
                    if sessions == 'no':
                        name = f'[Rock my iRev] iRev is low although all metrics look good'
                        description = f'Investigate and give an update to {travel_specialist}.'
                        priority = 3
                        assignees = [find_user_id_by_email('kim@venturatravel.org')]
                        try:
                            task_url = create_task(api_key, mkt_id, name, description, priority, assignees)
                            if task_url:
                                print(f'We have a problem with acquisition! The Marketing team is investigating now and will let you know how they will address the issue. You can follow up here: {task_url}.')
                            else:
                                print('Error Connecting to ClickUp')
                        except Exception as e:
                            print(f'An error occurred while creating the task: {e}')
                        print('Now, let’s see whether the sessions we get on the website are converting well!')
                        conversion_rates = ask_question('Is one of your conversion rates (S-QS, QS-MQL, MQL-Deal) below plan?', ['yes', 'no'])
                        if conversion_rates == 'no':
                            print('Wonderful! You are on track. The marketing team will continue to investigate the acquisition issue.')
                        else:
                            conversion_rate_below_plan = ask_question('Which conversion rate is below plan?', ['S-QS', 'MQL-Deal', 'QS-MQL'])
                            if conversion_rate_below_plan == 'S-QS':
                                name = f'[Rock my iRev] Check whether your offer is still attractive'
                                description = f'Re-calculate the market price. Is your price still attractive compared to the competition? If not, adapt it! Is everything displayed correctly on your trip landing page? If not, fix it or report a bug. Subtask: Is it time to publish a new departure? If so, do it!'
                                priority = 3
                                assignees = [ts_userid]
                                try:
                                    task_url = create_task(api_key, sales_id, name, description, priority, assignees)
                                    if task_url:
                                        print(f"Looks like people don’t stay long enough on your landing pages. Please do these three checks: {task_url}")
                                        name = f'[Rock my iRev] Please check the landing pages related to this TS’s trips.'
                                        description = f'Investigate and give an update to {travel_specialist}.'
                                        priority = 3
                                        assignees = [find_user_id_by_email('maximilian.vonmeister@venturatravel.org')]
                                        try:
                                            task_url = create_task(api_key, mkt_id, name, description, priority, assignees)
                                            if task_url:
                                                print(f"At the same time, the Marketing team is checking whether they can spot some issues on the landing page. You can follow up here: (link to ClickUp)")
                                            else:
                                                print('Error Connecting to ClickUp')
                                        except Exception as e:
                                            print(f'An error occurred while creating the task: {e}')
                                    else:
                                        print('Error Connecting to ClickUp')
                                except Exception as e:
                                    print(f'An error occurred while creating the task: {e}')
                            if conversion_rate_below_plan == 'MQL-Deal':
                                name = f'[Rock my iRev] Check the contact options on your landing pages'
                                description = f'Fill out the contact form on your TLP, do you receive the message in HubSpot? If not, report a bug. Schedule a video call with yourself. Did it work? If not, report a bug. Does everything work well? If not, report a bug. Check the future departure forecast. Is it time to publish a new departure? If so, do it!'
                                priority = 3
                                assignees = [ts_userid]
                                try:
                                    task_url = create_task(api_key, sales_id, name, description, priority, assignees)
                                    if task_url:
                                        print(f"Looks like people don’t stay long enough on your landing pages. Please do these three checks: {task_url}")
                                        name = f'[Rock my iRev] The MQLs for the brand; {destination} do not convert into Deals as planned.'
                                        description = f'Investigate and give an update to {travel_specialist}.'
                                        priority = 3
                                        assignees = [find_user_id_by_email('sophie.vandermeulen@venturatravel.org')]
                                        try:
                                            task_url = create_task(api_key, mkt_id, name, description, priority, assignees)
                                            if task_url:
                                                print(f"At the same time, the Marketing team is checking whether they can spot some issues on the landing page. You can follow up here: (link to ClickUp)")
                                            else:
                                                print('Error Connecting to ClickUp')
                                        except Exception as e:
                                            print(f'An error occurred while creating the task: {e}')
                                    else:
                                        print('Error Connecting to ClickUp')
                                except Exception as e:
                                    print(f'An error occurred while creating the task: {e}')
                                print("Looks like not enough people are reaching out to us. Please do these four checks: (link to ClickUp)")
                                print("At the same time, the Marketing team is checking on their end what the issue could be. You can follow up here: (link to ClickUp)")
                            if conversion_rate_below_plan == 'QS-MQL':
                                name = f'[Rock my iRev] The traffic for the brand; {destination} do not convert into MQLs as planned.'
                                description = f'Please investigate, and let {travel_specialist} know what you will do to address this issue'
                                priority = 3
                                assignees = [find_user_id_by_email('sophie.vandermeulen@venturatravel.org')]
                                try:
                                    task_url = create_task(api_key, mkt_id, name, description, priority, assignees)
                                    if task_url:
                                       print('We have a problem with lead generation! The Marketing team is investigating now and will let you know how they will address the issue.')
                                    else:
                                        print('Error Connecting to ClickUp')
                                except Exception as e:
                                    print(f'An error occurred while creating the task: {e}')
                    else:
                        conversion_rate_below_plan = ask_question('Which conversion rate is below plan?', ['S-QS', 'MQL-Deal', 'QS-MQL'])
                        if conversion_rate_below_plan == 'S-QS':
                                name = f'[Rock my iRev] Check whether your offer is still attractive'
                                description = f'Re-calculate the market price. Is your price still attractive compared to the competition? If not, adapt it! Is everything displayed correctly on your trip landing page? If not, fix it or report a bug. Subtask: Is it time to publish a new departure? If so, do it!'
                                priority = 3
                                assignees = [ts_userid]
                                try:
                                    task_url = create_task(api_key, sales_id, name, description, priority, assignees)
                                    if task_url:
                                        print(f"Looks like people don’t stay long enough on your landing pages. Please do these three checks: {task_url}")
                                        name = f'[Rock my iRev] Please check the landing pages related to this TS’s trips.'
                                        description = f'Investigate and give an update to {travel_specialist}.'
                                        priority = 3
                                        assignees = [find_user_id_by_email('maximilian.vonmeister@venturatravel.org')]
                                        try:
                                            task_url = create_task(api_key, mkt_id, name, description, priority, assignees)
                                            if task_url:
                                                print(f"At the same time, the Marketing team is checking whether they can spot some issues on the landing page. You can follow up here: (link to ClickUp)")
                                            else:
                                                print('Error Connecting to ClickUp')
                                        except Exception as e:
                                            print(f'An error occurred while creating the task: {e}')
                                    else:
                                        print('Error Connecting to ClickUp')
                                except Exception as e:
                                    print(f'An error occurred while creating the task: {e}')
                        if conversion_rate_below_plan == 'MQL-Deal':
                            name = f'[Rock my iRev] Check the contact options on your landing pages'
                            description = f'Fill out the contact form on your TLP, do you receive the message in HubSpot? If not, report a bug. Schedule a video call with yourself. Did it work? If not, report a bug. Does everything work well? If not, report a bug. Check the future departure forecast. Is it time to publish a new departure? If so, do it!'
                            priority = 3
                            assignees = [ts_userid]
                            try:
                                task_url = create_task(api_key, sales_id, name, description, priority, assignees)
                                if task_url:
                                    print(f"Looks like people don’t stay long enough on your landing pages. Please do these three checks: {task_url}")
                                    name = f'[Rock my iRev] The MQLs for the brand; {destination} do not convert into Deals as planned.'
                                    description = f'Investigate and give an update to {travel_specialist}.'
                                    priority = 3
                                    assignees = [find_user_id_by_email('sophie.vandermeulen@venturatravel.org')]
                                    try:
                                        task_url = create_task(api_key, mkt_id, name, description, priority, assignees)
                                        if task_url:
                                            print(f"At the same time, the Marketing team is checking whether they can spot some issues on the landing page. You can follow up here: (link to ClickUp)")
                                        else:
                                            print('Error Connecting to ClickUp')
                                    except Exception as e:
                                        print(f'An error occurred while creating the task: {e}')
                                else:
                                    print('Error Connecting to ClickUp')
                            except Exception as e:
                                print(f'An error occurred while creating the task: {e}')
                            print("Looks like not enough people are reaching out to us. Please do these four checks: (link to ClickUp)")
                            print("At the same time, the Marketing team is checking on their end what the issue could be. You can follow up here: (link to ClickUp)")
                        if conversion_rate_below_plan == 'QS-MQL':
                            name = f'[Rock my iRev] The traffic for the brand; {destination} do not convert into MQLs as planned.'
                            description = f'Please investigate, and let {travel_specialist} know what you will do to address this issue'
                            priority = 3
                            assignees = [find_user_id_by_email('sophie.vandermeulen@venturatravel.org')]
                            try:
                                task_url = create_task(api_key, mkt_id, name, description, priority, assignees)
                                if task_url:
                                   print('We have a problem with lead generation! The Marketing team is investigating now and will let you know how they will address the issue.')
                                else:
                                    print('Error Connecting to ClickUp')
                            except Exception as e:
                                print(f'An error occurred while creating the task: {e}')
        else:
            print(f"Error: No user found with email {ts_email}. Please restart program")

if __name__ == "__main__":
    troubleshoot_irev()
