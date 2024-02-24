import sqlite3 #virtual DB

#GUI LIbrary and its Elements
from tkinter import Tk, Button, Entry,Label, messagebox, Frame


def CreateDB(filename: str):
    '''This fx is to create Database filename = name of .db file'''

    #Estd. Connection to Database file
    connection = sqlite3.connect(filename)

    #creating a cursor instance
    Control=connection.cursor()

    #Creating tables
    Control.execute("CREATE TABLE ROOMS (RoomId int primary key, Hostel varchar(5), no_of_students int check (no_of_students<=5));")

    Control.execute("CREATE TABLE CHOTHES (Cloth_id int primary key, Type varchar(10));")

    Control.execute("CREATE TABLE LAUNDRY (RoomId int , Cloth_id int , Status varchar(3), CONSTRAINT ROOM_FK foreign key(RoomId) references ROOMS(RoomId) , CONSTRAINT ROOM_FK foreign key(Cloth_id) references CLOTHES(Cloth_id));")

    #saving the changes
    connection.commit()

    #closing the conection
    connection.close()

def SampleDataInsert(filename: str):
    '''this fx is to insert sample data in Database. filename = name of .db file'''

    #Estd. Connection to Database file
    connection = sqlite3.connect(filename)

    #creating a cursor instance
    Control=connection.cursor()

    #inserting data
    Control.execute("""INSERT INTO ROOMS values(1, "A", 4), (2,"B", 2), (3,"C", 4);""")

    Control.execute("""INSERT INTO CHOTHES values(1,"Shirt"),(2, "Pant"), (3, "Tie"), (4, "Blazer");""")
    
    #saving the changes
    connection.commit()
    
    #closing the conection
    connection.close()

def insertItem(Item: str, Room: int):
    '''this fx inserts data on database
        Item = Name_of_Cloth - (Shirt/Pant/Tie)
        Room = int - Room number
        '''
    
    #Estd. Connection to Database file
    connection = sqlite3.connect("database.db")

    #creating a cursor instance
    control = connection.cursor()

    #taking tuples from Table Clothes
    Itemids=control.execute("Select Cloth_id from CLOTHES;")
    Items=control.execute("Select Type from CLOTHES;")

    #checking if entered item in database
    if Item not in Items:
        #show error
        messagebox.showerror("Invalid Item!", "The Item Entered is Invalid! :( ")
    
    else:
        #creating a dict of that tuples
        Item_Dict=dict(zip(Items, Itemids))

    #retriving itemid
    Itemid=Item_Dict.get(Item)

    #insert item in table
    control.execute(f"""INSERT into LAUNDRY values({Room},{int(Itemid)} ,"Yes");""")

    #saving the changes
    control.commit()

    #confirmation
    messagebox.showinfo("Sucess", "Sucessfully added item in list! :) ")

    #close the connection
    connection.close()


def deleteItem(Item: str, Room:int):
    '''this fx delete data on database
    Item = str - Name of Cloth eg. (Shirt/Pant/Tie)
    Room = int - Room number
    '''

    #Estd. Connection to Database file
    connection = sqlite3.connect("database.db")

    #creating a cursor instance
    control = connection.cursor()

    #taking tuples from Table Clothes
    Itemids=control.execute("Select Cloth_id from CLOTHES;")
    Items=control.execute("Select Type from CLOTHES;")

    #checking if entered item in database
    if Item not in Items:
        #show error
        messagebox.showerror("Invalid Item!", "The Item Entered is Invalid! :( ")
    
    else:
        #creating a dict of that tuples
        Item_Dict=dict(zip(Items, Itemids))

    #retriving itemid
    Itemid=Item_Dict.get(Item)

    #deleting that item for database
    control.execute(f"""delete from LAUNDRY where RoomId = {Room} and Cloth_id = {int(Itemid)};""")

    #saving the changes
    control.commit()

    #confirmation
    messagebox.showinfo("Sucess", "Sucessfully Returned item if it was exist in database! :) ")

    #close the connection
    connection.close()

class Laundry(Tk):
    def __init__(self, *args):

        super().__init__(*args)

        self.title("Laundry System!")
    
    def init_Elements(self):

        self.fstFrame=Frame(self)
        self.sndFrame=Frame(self)

        self.selectItemLabel=Label(master=self.fstFrame, text="Select Item: ")
        self.selectItemEntry=Entry(master=self.fstFrame)

        self.selectRoomLabel=Label(master=self.sndFrame, text="Select Room: ")
        self.selectRoomEntry=Entry(master=self.sndFrame)

        self.addButton=Button(text="Add", command=self.addItem)

        self.removeButton=Button(text="Remove", command=self.removeItem)

    def packItems(self):
        self.fstFrame.pack()
        self.sndFrame.pack()

        self.selectItemLabel.pack(side="left")
        self.selectItemEntry.pack(side="left")
        
        self.selectRoomLabel.pack(side="left")
        self.selectRoomEntry.pack(side="left")

        self.addButton.pack()
        self.removeButton.pack()


    def StartApp(self):
        self.mainloop()

    def addItem(self):

        ItemName=self.selectItemEntry.get()
        RoomNo=self.selectRoomEntry.get()

        try:
            RoomNo=int(RoomNo)
        except ValueError:
            messagebox.showerror("Invalid Input", "Please Enter a valid Integer in Room Number")
        
        insertItem(ItemName, RoomNo)
    def removeItem(self):

        ItemName=self.selectItemEntry.get()
        RoomNo=self.selectRoomEntry.get()

        try:
            RoomNo=int(RoomNo)
        except ValueError:
            messagebox.showerror("Invalid Input", "Please Enter a valid Integer in Room Number")
        
        deleteItem(ItemName, RoomNo)


if __name__ =="__main__":
    
    #<-------- Initlizing Items -------->
    
    # CreateDB("database.db ")
    # SampleDataInsert("database.db")

    screen=Laundry()

    screen.init_Elements()

    screen.packItems()

    screen.StartApp()

