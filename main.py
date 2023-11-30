import os
import csv
import json
import psycopg2

conn = psycopg2.connect("dbname=FundsManagementDB user=postgres password=633804735")
cur = conn.cursor()

'''##########################JSON MANIPULATION##########################'''
def loadCategories():
    jsonFile = json.load(open('categories.json'))
    return jsonFile['categories']

def addInflowCategory(category):
    jsonFile = json.load(open('categories.json'))
    jsonFile['categories']['inflow'].append(category)
    os.remove('categories.json')
    with open('categories.json', 'w') as f:
        json.dump(jsonFile, f, indent=4)

def addOutflowCategory(category):
    jsonFile = json.load(open('categories.json'))
    jsonFile['categories']['outflow'].append(category)
    os.remove('categories.json')
    with open('categories.json', 'w') as f:
        json.dump(jsonFile, f, indent=4)

'''##########################TRANSACTION MANIPULATION##########################'''
def getExpensesCSV(filename):
    expenses = []
    with open(f"csv/{filename}.csv", 'r') as file:
        csvreader = csv.reader(file)
        for row in csvreader:
            expenses.append(row)
    return expenses[::-1]

def main(filename):
    expenses = getExpensesCSV(filename)
    for expense in expenses:
        date = '{year}-{month}-{day}'.format(year = expense[0].split('/')[2], month = expense[0].split('/')[1], day = expense[0].split('/')[0]) 
        origin = expense[4]
        if expense[5]:
            nature = True
            amount = float(expense[5])
        else:
            nature = False
            amount = float(expense[6])
        if nature:
            categories = loadCategories()['outflow']
            #print('Date         Source          Expenditure     Amount')
            print(f'{date}    {origin}    {nature}    {amount}')
            for category in categories:
                print(f'{categories.index(category)+1} - {category}')
            print(f'{len(categories)+1} - Add another category')
            choice = int(input('What?:> '))
            if choice <= len(categories):
                category = categories[choice-1]
                cur.execute('INSERT INTO AccountBalanceManagement (amount, date, source, description, expenditure) VALUES (%s,%s,%s,%s,%s)', (amount, date, category, origin, True))
                conn.commit()
            elif choice == len(categories)+1:
                newCategory = input('New category:> ')
                addOutflowCategory(newCategory)
                cur.execute('INSERT INTO AccountBalanceManagement (amount, date, source, description, expenditure) VALUES (%s,%s,%s,%s,%s)', (amount, date, newCategory, origin, True))
                conn.commit()
        else:
            categories = loadCategories()['inflow']
            print(f'{date}    {origin}    {nature}    {amount}')
            for category in categories:
                print(f'{categories.index(category)+1} - {category}')
            print(f'{len(categories)+1} - Add another category')
            choice = int(input('What?:> '))
            if choice <= len(categories):
                category = categories[choice-1]
                cur.execute('INSERT INTO AccountBalanceManagement (amount, date, source, description, expenditure) VALUES (%s,%s,%s,%s,%s)', (amount, date, category, origin, False))
                conn.commit()
            elif choice == len(categories)+1:
                newCategory = input('New category:> ')
                addInflowCategory(newCategory)
                cur.execute('INSERT INTO AccountBalanceManagement (amount, date, source, description, expenditure) VALUES (%s,%s,%s,%s,%s)', (amount, date, newCategory, origin, False))
                conn.commit()


def dump_expenses():
    
    cur.execute('SELECT * FROM accountbalancemanagement WHERE change_id > 101 AND expenditure = true ORDER BY change_id')

    with open('expenses.csv', 'w') as csvfile:
        fieldnames = ['description', 'category']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for record in cur:
            writer.writerow({'description':record[4],'category':record[2]})
    

if __name__ == '__main__':
    #main('transactions5')
    dump_expenses()
