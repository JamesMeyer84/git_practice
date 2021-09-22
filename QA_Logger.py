##9/18/21 -- Elliott Meyer -- New program, QA Logger.  Will allow QA analysts to input their testing notes & queries; records are saved to tables in the QADetails DB.

import pyodbc

# Menu; prompts for input, calls helper methods to verify that input, and calls the methods that insert & update records
def Menu():
    loop = True
    while loop:
        print()
        print("Please make a selection. Listen carefully, as our menu options have changed:")
        print()
        print("1. Add a record")
        print("2. Edit a record")
        print("3. None of the above")
        resp = input()

        if int(resp) == 1:
            func = 'add'
            loop1 = True
            while loop1:
                print()
                print("Would you like to add an Issue, a Test Step, or a Query?")
                print()
                print("1. Add Issue")
                print("2. Add Test Step")
                print("3. Add Query")
                print("4. Wait, what were my original choices?")
                resp = input()

                if int(resp) == 1:
                    print()
                    New_Issue()

                elif int(resp) == 2:
                    issue_id, truth = Verify_Issue(func)

                    if truth:
                        New_Test_Step(issue_id)

                elif int(resp) == 3:
                    issue_id, truth = Verify_Issue(func)

                    if truth:
                        step_id, more_truth = Verify_Test_Step(issue_id,func)

                        if more_truth:
                            New_Query(issue_id,step_id)

                else:
                    loop1 = False
                            
        elif int(resp) == 2:
            func = 'edit'
            loop2 = True
            while loop2:
                print()
                print("Would you like to edit an Issue, Test Step, or Query record?")
                print()
                print("1. Edit Issue")
                print("2. Edit Test Step")
                print("3. Edit Query")
                print("4. Nevermind, go back")
                resp = input()

                if int(resp) == 1:
                    issue_id, truth = Verify_Issue(func)

                    if truth:
                        loop3 = True
                        while loop3:
                            print()
                            print("Which field would you like to edit?")
                            print()
                            print("1. Dev")
                            print("2. QA")
                            print("3. BegDate")
                            print("4. EndDate")
                            print("5. Notes")
                            print("6. IRIS_Release")
                            print("7. UATTesting")
                            print("8. ProdTesting")
                            print("9. Nevermind, that's too many options.")
                            resp = input()

                            if int(resp) == 1:
                                field = 'Dev'
                                Issues_Editor(issue_id,field)
                            elif int(resp) == 2: 
                                field = 'QA'
                                Issues_Editor(issue_id,field)
                            elif int(resp) == 3:
                                field = 'BegDate'
                                Issues_Editor(issue_id,field)
                            elif int(resp) == 4:
                                field = 'EndDate'
                                Issues_Editor(issue_id,field)
                            elif int(resp) == 5:
                                field = 'Notes'
                                Issues_Editor(issue_id,field)
                            elif int(resp) == 6:
                                field = 'IRIS_Release'
                                Issues_Editor(issue_id,field)
                            elif int(resp) == 7:
                                field = 'UATTesting'
                                Issues_Editor(issue_id,field)
                            elif int(resp) == 8:
                                field = 'ProdTesting'
                                Issues_Editor(issue_id,field)
                            else:
                                loop3 = False

                
                elif int(resp) == 2:
                    issue_id, truth = Verify_Issue(func)

                    if truth:
                        step_id, more_truth = Verify_Test_Step(issue_id,func)

                        if more_truth:
                            loop4 = True
                            while loop4:
                                print()
                                print("Which field would you like to edit?")
                                print()
                                print("1. Details")
                                print("2. Notes")
                                print("3. That's it?  Nevermind.")
                                resp = input()

                                if int(resp) == 1:
                                    field = 'Details'
                                    Test_Steps_Editor(issue_id,step_id,field)
                                elif int(resp) == 2:
                                    field = 'Notes'
                                    Test_Steps_Editor(issue_id,step_id,field)
                                else:
                                    loop4 = False

                elif int(resp) == 3:
                    issue_id, truth = Verify_Issue(func)

                    if truth:
                        step_id, more_truth = Verify_Test_Step(issue_id,func)

                        if more_truth:
                            query_id, ultimate_truth = Verify_Query(issue_id,step_id)

                            if ultimate_truth:
                                loop5 = True
                                while loop5:
                                    print()
                                    print("Which field would you like to edit?")
                                    print()
                                    print("1. Query")
                                    print("2. Environment")
                                    print("3. Notes")
                                    print("4. Not a lot of options.  Let's go back.")
                                    resp = input()

                                    if int(resp) == 1:
                                        field = 'Query'
                                        Queries_Editor(issue_id,step_id,query_id,field)
                                    elif int(resp) == 2:
                                        field = 'Environment'
                                        Queries_Editor(issue_id,step_id,query_id,field)
                                    elif int(resp) == 3:
                                        field = 'Notes'
                                        Queries_Editor(issue_id,step_id,query_id,field)
                                    else:
                                        loop5 = False

                else:
                    loop2 = False

        else:
            loop = False


# Prompts user for input to construct a new record to insert into the [QADetails].[dbo].[Issues]
def New_Issue():
    print()
    print("Which IRIS release does this issue belong to?")
    release = input()
    print()
    print("What is the issue's JIRA Card number?")
    card_no = input()
    print()
    print("Who was the developer for this issue?")
    dev = input()
    print()
    print("Who is doing QA testing for this issue?")
    qa = input()
    print()
    print("On what date did QA testing begin?")
    beg_dt = input()
    print()
    print("Has testing been completed? (Yes/No)")
    yn = input()
    end_dt = ''

    if yn.lower() == 'yes':
        print()
        print("On what date was QA testing completed?")
        end_dt = input()

    print()
    print("What are the UAT Testing procedures for this Issue?")
    uat = input()
    uat = uat.replace("'","''")
    print()
    print("What are the Prod Testing procedures for this Issue?")
    prod = input()
    prod = prod.replace("'","''")
    print()
    print("Do you have any issue-related notes to add? (Yes/No)")
    yn = input()
    notes = ''

    if yn.lower() == 'yes':
        print()
        print("Ok, let's hear 'em")
        notes = input()
        notes = notes.replace("'","''")
    
    query = "insert into QADetails.dbo.Issues (IssueID,CardNum,Dev,QA,BegDate,EndDate,Notes,IRIS_Release,UATTesting,ProdTesting) values (0,'"+card_no+"','"+dev+"','"+qa+"','"+beg_dt+"','"+end_dt+"','"+notes+"','"+release+"','"+uat+"','"+prod+"')"
    cursor.execute(query)
    conn.commit()

    print()
    print("Issue record created.  Would you care to add a Test Step record related to this Issue? (Yes/No)")
    yn = input()

    if yn.lower() == 'yes':
        query = "select max(IssueID) from QADetails.dbo.Issues"
        cursor.execute(query)
        dataset = cursor.fetchall()
        issue_id = 0
        for x in dataset:
            for y in x:
                issue_id = str(y)
        
        New_Test_Step(issue_id)


# Prompts user for input to construct a new record to insert into [QADetails].[dbo].[TestSteps]
def New_Test_Step(IssueID):
    print()
    print("Please enter the details associated with this Test Step:")
    details = input()
    details = details.replace("'","''")
    print()
    print("Do you have any Test Step-related notes to add? (Yes/No)")
    yn = input()
    notes = ''

    if yn.lower() == 'yes':
        print()
        print("Well get on with it then...")
        notes = input()
        notes = notes.replace("'","''")

    query = "insert into QADetails.dbo.TestSteps (IssueID,StepID,Details,Notes) values ("+IssueID+",0,'"+details+"','"+notes+"')"
    cursor.execute(query)
    conn.commit()

    print()
    print("Test Step record created.  Would you care to add a Query record related to this Test Step? (Yes/No)")
    yn = input()

    if yn.lower() == 'yes':
        query = 'select max(StepID) from QADetails.dbo.TestSteps where IssueID = '+IssueID
        cursor.execute(query)
        dataset = cursor.fetchall()
        step_id = 0
        for x in dataset:
            for y in x:
                step_id = str(y)

        New_Query(IssueID,step_id)

    print()
    print("Would you care to add another Test Step record for the same Issue? (Yes/No)")
    yn = input()

    if yn.lower() == 'yes':
        New_Test_Step(IssueID)


# Prompts user for input to construct a new record to insert into [QADetails].[dbo].[Queries]
def New_Query(IssueID, StepID):
    print()
    print("Please enter the query you wish to document:")
    user_query = input()
    user_query = user_query.replace("'","''")
    print()
    print("In which environment should this query be run?")
    env = input()
    print()
    print("Do you have any Query-related notes to add? (Yes/No)")
    yn = input()
    notes = ''

    if yn.lower() == 'yes':
        print()
        print("Verbose, eh?")
        notes = input()
        notes = notes.replace("'","''")

    query = "insert into QADetails.dbo.Queries (IssueID,StepID,QueryID,Query,Environment,Notes) values ("+IssueID+","+StepID+",0,'"+user_query+"','"+env+"','"+notes+"')"
    cursor.execute(query)
    conn.commit()

    print()
    print("Query record created.  Would you care to add another Query record for the same Test Step? (Yes/No)")
    yn = input()

    if yn.lower() == 'yes':
        New_Query(IssueID, StepID)


# Helper method to prompt user to verify retrieved Issue
def Verify_Issue(func):
    if func == 'add':
        print()
        print("Please enter the IssueID for the Issue to which you wish to add a Test Step:")
        issue_id = input()
    else:
        print()
        print("Please enter the IssueID for the Issue you wish to edit:")
        issue_id = input()
    
    query = 'select CardNum from QADetails.dbo.Issues where IssueID = '+issue_id
    cursor.execute(query)
    dataset = cursor.fetchall()
    card_no = 0

    for x in dataset:
        for y in x:
            card_no = y

    if card_no == 0:
        print()
        print("I'm sorry, that IssueID doesn't exist")
        return 0, False
    else:
        print()
        print("This Issue is related to JIRA Card "+str(card_no)+"; is this correct? (Yes/No)")
        yn = input()

        if yn.lower() == 'yes':
            return issue_id, True
        else:
            return 0, False

# Helper method to prompt user to verify retrieved Test Step
def Verify_Test_Step(IssueID,func):
    if func == 'add':
        print()
        print("Please enter the StepID for the Test Step to which you wish to add a Query:")
        step_id = input()
    else:
        print()
        print("Please enter the StepID for the Test Step you wish to edit:")
        step_id = input()
    
    query = "select Details from QADetails.dbo.TestSteps where IssueID = "+IssueID+" and StepID = "+step_id
    cursor.execute(query)
    dataset = cursor.fetchall()
    details = 0

    for x in dataset:
        for y in x:
            details = y

    if details == 0:
        print()
        print("I'm sorry, that Test Step doesn't exist")
        return 0, False
    else:
        print()
        print("The Details of this Test Step are:")
        print()
        print("--->  "+details+"  <---")
        print()
        print("Is this the correct Test Step? (Yes/No)?")
        yn = input()
        
        if yn.lower() == 'yes':
            return step_id, True
        else:
            return 0, False


# Helper method to prompt user to verify retrieved Query
def Verify_Query(IssueID,StepID):
    print()
    print("Please enter the QueryID for the Query you wish to edit:")
    query_id = input()

    query = "select Query from QADetails.dbo.Queries where IssueID = "+IssueID+" and StepID = "+StepID+" and QueryID = "+query_id
    cursor.execute(query)
    dataset = cursor.fetchall()
    details = 0

    for x in dataset:
        for y in x:
            details = y

    if details == 0:
        print()
        print("I'm sorry, that Query doesn't exist")
        return 0, False
    else:
        print()
        print("This is the Query returned:")
        print()
        print("--->  "+details+"  <---")
        print()
        print("Is this the correct Query? (Yes/No)")
        yn = input()

        if yn.lower() == 'yes':
            return query_id, True
        else:
            return 0, False


# Displays contents of the field to be edited and asks user to verify overwrite & enter new data
def Edit_Check(Contents):
    print()
    print("The current contents of that field are:")
    print()
    print("--->  "+Contents+"  <---")
    print()
    print("Are you sure you wish to overwrite? (Yes/No)")
    yn = input()
    data = ''

    if yn.lower() == 'yes':
        print()
        print("Please enter the new value for the field:")
        data = input()
        data = data.replace("'","''")

    return data


# Updates specified Issues field with specified value for specified IssueID
def Issues_Editor(IssueID,Field):
    query = "select "+Field+" from QADetails.dbo.Issues where IssueID = "+IssueID
    cursor.execute(query)
    dataset = cursor.fetchall()
    data = ''

    for x in dataset:
        for y in x:
            data = y

    data = Edit_Check(data)

    if len(data) > 0:
        query = "update QADetails.dbo.Issues set "+Field+" = '"+data+"' where IssueID = "+IssueID
        cursor.execute(query)
        conn.commit()
        print()
        print("The "+Field+" field has been successfully updated")


# Updates specified TestSteps field with specified value for specified IssueID+StepID
def Test_Steps_Editor(IssueID,StepID,Field):
    query = "select "+Field+" from QADetails.dbo.TestSteps where IssueID = "+IssueID+" and StepID = "+StepID
    cursor.execute(query)
    dataset = cursor.fetchall()
    data = ''

    for x in dataset:
        for y in x:
            data = y

    data = Edit_Check(data)

    if len(data) > 0:
        query = "update QADetails.dbo.TestSteps set "+Field+" = '"+data+"' where IssueID = "+IssueID+" and StepID = "+StepID
        cursor.execute(query)
        conn.commit()
        print()
        print("The "+Field+" field has been successfully updated")


# Updates specified Queries field with specified value for specified IssueID+StepID+QueryID
def Queries_Editor(IssueID,StepID,QueryID,Field):
    query = "select "+Field+" from QADetails.dbo.Queries where IssueID = "+IssueID+" and StepID = "+StepID+" and QueryID = "+QueryID
    cursor.execute(query)
    dataset = cursor.fetchall()
    data = ''

    for x in dataset:
        for y in x:
            data = y

    data = Edit_Check(data)

    if len(data) > 0:
        query = "update QADetails.dbo.Queries set "+Field+" = '"+data+"' where IssueID = "+IssueID+" and StepID = "+StepID+" and QueryID = "+QueryID
        cursor.execute(query)
        conn.commit()
        print()
        print("The "+Field+" field has been successfully updated")


# Beginning of script
conn_str = "driver={SQL SERVER}; server=DESKTOP-NNSRI02\SQLEXPRESS; database=QADetails; trusted_connection=YES;"
conn = pyodbc.connect(conn_str)
cursor = conn.cursor()

print("Welcome, and thank you for using Elliott Meyer's QA Logger!")

Menu()

print()
print("Thank you for using Elliott Meyer's QA Logger!")
conn.close()



























