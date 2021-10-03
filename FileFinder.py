import pyodbc
import shutil
import os

# 9/30/21 -- Elliott Meyer -- New Program: Finds and moves test files for user-input list of FileTemplates or FileGroupTemplates

def Menu():
    loop = True
    while loop:
        print()
        print("Are you looking for FileTemplates or FileGroupTemplates?")
        print()
        print("1. FTs")
        print("2. FGTs")
        print("3. Exit")
        resp = input()

        # FT logic
        if int(resp) == 1:
            print()
            print("Please enter the FileTemplate or list of FileTemplates, separated by commas, for which you need test files:")
            FTs = input()
            # I don't think spaces in the input would hurt anything, but it'd be an easy fix if so
            FTs = FTs.split(',')

            for FileTemplate in FTs:
                # Check to see if FT is legit
                query = "select * from DEMetadata.dbo.nHSourceFileTemplate where FileTemplateID = "+FileTemplate
                cursor.execute(query)
                RawFTData = cursor.fetchall()

                if len(RawFTData) == 0:
                    print()
                    print("Sorry, no nHSourceFileTemplate record located for FileTemplate "+FileTemplate)
                    continue

                # LastFileID used to move backwards through Instance recs w/ Status 3 when FileNotFound
                LastFileID = 99999999999
                loop1 = True
                while loop1:
                    query = "select max(FileID) from DEMetadata.dbo.nHSourceFileInstance where FileTemplateID = "+FileTemplate+" and FileStatusID = 3 and FileID < "+LastFileID
                    cursor.execute(query)
                    RawFileID = cursor.fetchall()

                    FileID = 0
                    for x in RawFileID:
                        for y in x:
                            FileID = y

                    if FileID == 0:
                        print()
                        print("Sorry, there are no more Instance records with FileStatusID 3 for FileTemplate "+FileTemplate+"; you'll have to look elsewhere.")
                        loop1 = False
                    else:
                        Source = Build_FileSource(FileID,FileTemplate)

                        if os.path.isfile(Source):
                            shutil.copy(Source,Destination)
                            loop1 = False
                        else:
                            LastFileID = FileID

        # FGT logic          
        elif int(resp) == 2:
            print()
            print("Please enter the FileGroupTemplate or list of FileGroupTemplates, separated by commas, for which you need test files:")
            FGTs = input()
            FGTs = FGTs.split(',')

            for FileGroupTemplate in FGTs:
                # Check to see if FGT is legit
                query = "select FileTemplateID from DEMetadata.dbo.nHSourceFileTemplate where FileGroupTemplateID = "+FileGroupTemplate+" and FileDescription not like '%merged%'"
                cursor.execute(query)
                RawFileTemplateIDs = cursor.fetchall()

                if len(RawFileTemplateIDs) == 0:
                    print()
                    print("Sorry, no FileTemplates found for FileGroupTemplate "+FileGroupTemplate)
                    continue

                # NumOfFTs used to make sure all files pulled belong to the same FileGroupID
                NumOfFTs = len(RawFileTemplateIDs)

                # LastFileGroupID used to move backwards through Instance recs w/ Status 3 when FileNotFound
                LastFileGroupID = 99999999999
                loop2 = True
                while loop2:
                    query = "select max(FileGroupID) from DEMetadata.dbo.nHSourceFileGroupInstance where FileGroupTemplateID = "+FileGroupTemplate+" and FileStatusID = 3 and FileGroupID < "+LastFileGroupID
                    cursor.execute(query)
                    RawFileGroupID = cursor.fetchall()

                    FileGroupID = 0
                    for x in RawFileGroupID:
                        for y in x:
                            FileGroupID = y

                    if FileGroupID == 0:
                        print()
                        Print("Sorry, there are no more Instance records with a FileStatusID 3 for FileGroupTemplate "+FileGroupTemplate+"; you'll have to look elsewhere.")
                        loop2 = False
                    else:
                        query = "select FileID, FileTemplateID from DEMetadata.dbo.nHSourceFileInstance where FileGroupID = "+FileGroupID+" and ActualFileName not like '%merged%'"
                        cursor.execute(query)
                        RawFileSet = cursor.fetchall()

                        counter = 0
                        for x in RawFileSet:
                            Source = Build_FileSource(x[0],x[1])

                            if os.path.isfile(Source):
                                counter += 1
                        # If counter != NumOfFTs, > 0 of the files were missing, so go to next FileGroupID
                        if counter == NumOfFTs:
                            for x in RawFileSet:
                                Source = Build_FileSource(x[0],x[1])
                                shutil.copy(Source,Destination)
                            loop2 = False
                        else:
                            LastFileGrouipID = FileGroupID

        else:
            print()
            print("Thanks, hope you found the files you needed!")
            loop = False


# Builds FilePath Source for each FileTemplate-FileID combination
def Build_FileSource(fileid,template):
    query = "select FileLoadPath from DEMetadata.dbo.nHSourceFileTemplate where FileTemplateID = "+template
    cursor.execute(query)
    RawFilePath = cursor.fetchall()

    FilePath = 0
    for x in RawFilePath:
        for y in x:
            FilePath = y
    
    query = "select ActualFileName from DEMetadata.dbo.nHSourceFileInstance where FileID = "+fileid
    cursor.execute(query)
    RawFileName = cursor.fetchall()

    FileName = 0
    for x in RawFileName:
        for y in x:
            FileName = y

    Source = "\\\p10dataexfs01\DEOtherPHI"+FilePath[FilePath.find('\\'):]+"Archives\\"+FileName
    return Source



# Beginning of script

# Connection established at beginning and closed at end; if it would be better to open & close connection for each query, that would be an easy change
conn_str = "driver={SQL SERVER}; server=P10STDEDB00AAGL; database=DEMetadata; trusted_connection=YES;"
conn = pyodbc.connect(conn_str)
cursor = conn.cursor()

Destination = "C:\data"
if not os.path.isdir(Destination):
    os.mkdir(Destination)

print()
print("Hello, let's find some files!")

Menu()

conn.close()








