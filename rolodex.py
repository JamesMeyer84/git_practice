import csv

# Entry Class definition
class Entry:
  def __init__(self, name, phone, address, bday, notes):
    self.name = name
    self.phone = phone
    self.address = address
    self.bday = bday
    self.notes = notes

  def __repr__(self):
    return self.name

#Objects will be stored in entries dict
entries = {}
entry_no = 0

def new_entry(name, phone, address, bday, notes):
  global entry_no
  split_name = name.split()
  entry_no += 1
  entries[entry_no] = split_name[0]
  entries[entry_no] = Entry(name, phone, address, bday, notes)
  

# Ask the user for filename, and open said file
print('Hello!  Which file would you like to review?')
filename = input()
with open(filename+'.csv','r') as rolodex:
  rolodex_contents = csv.reader(rolodex)
  next(rolodex_contents)
  
  for entry in rolodex_contents:
    print(entry)


print('Hello! What would you like to do today: Add, Delete, Update, or Display?')
resp = input()


if resp == 'Add':
  print('What is the new entry\'s name?')
  new_name = input()
  print('What is the new entry\'s phone number?')
  new_phone = input()
  print('Please enter new entry\'s address:')
  new_address = input()
  print('Please enter new entry\'s birthday:')
  new_bday = input()
  print('Please enter any notes:')
  new_notes = input()
  #New object creation
  new_entry(new_name, new_phone, new_address, new_bday, new_notes)
  print("Created new entry")


#print(entries[1])
