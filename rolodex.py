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

entries = {}
entry_no = 0

# Beginning of user interaction
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
  split_name = new_name.split()
  entry_no += 1
  entries[entry_no] = split_name[0].lower
  entries[entry_no] = Entry(new_name, new_phone, new_address, new_bday, new_notes)
  print("Created new entry")


print(entries[1])