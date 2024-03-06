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

    Control.execute("CREATE TABLE CLOTHES (Cloth_id int primary key, Type varchar(10));")

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

    Control.execute("""INSERT INTO CLOTHES values(1,"Shirt"),(2, "Pant"), (3, "Tie"), (4, "Blazer");""")
    
    #saving the changes
    connection.commit()
    
    #closing the conection
    connection.close()

def insertItem(Item: str, Room: int):
    '''this fx inserts data on database
        Item = Name_of_Cloth - (Shirt/Pant/Tie)
        Room = int - Room number
        '''
    #for making Consistent case in database
    Item=Item.capitalize()

    #Estd. Connection to Database file
    connection = sqlite3.connect("database.db")

    #creating a cursor instance
    control = connection.cursor()

    #taking tuples from Table Clothes
    Itemids=control.execute("Select Cloth_id, Type from CLOTHES;")

    #converting cursor obj to a iterable list/tuple
    Itemids = Itemids.fetchall()

    #mapping type with id record = [Cloth_id, Type]
    Item_Dict = {record[1]:record[0] for record in Itemids}

    #checking if entered item in database
    if Item not in Item_Dict.keys():
        #show error
        messagebox.showerror("Invalid Item!", "The Item Entered is Invalid! :( ")
        #return the fx
        return
    
    #retriving itemid
    Itemid=Item_Dict.get(Item)

    #insert item in table
    control.execute(f"""INSERT into LAUNDRY values({Room},{Itemid} ,"Yes");""")

    #saving the changes
    connection.commit()

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
    Itemids=control.execute("Select Cloth_id, Type from CLOTHES;")

    #converting cursor obj to a iterable list/tuple
    Itemids = Itemids.fetchall()

    #mapping type with id record = [Cloth_id, Type]
    Item_Dict = {record[1]:record[0] for record in Itemids}

    #checking if entered item in database
    if Item not in Item_Dict.keys():
        #show error
        messagebox.showerror("Invalid Item!", "The Item Entered is Invalid! :( ")
        #return the fx
        return
    
    #retriving itemid
    Itemid=Item_Dict.get(Item)

    #deleting that item for database
    control.execute(f"""delete from LAUNDRY where RoomId = {Room} and Cloth_id = {int(Itemid)};""")

    #saving the changes
    connection.commit()

    #confirmation
    messagebox.showinfo("Sucess", "Sucessfully Returned item if it was exist in database! :) ")

    #close the connection
    connection.close()

class Laundry(Tk):

    def __init__(self, *args):

        #calling parents condtructor
        super().__init__(*args)

        #setting title of screen
        self.title("Laundry System!")
    
    def init_Elements(self):
        '''this fx creates tk elements'''
        #frames containers
        self.fstFrame=Frame(self)
        self.sndFrame=Frame(self)

        #Item Entry and label
        self.selectItemLabel=Label(master=self.fstFrame, text="Select Item: ")
        self.selectItemEntry=Entry(master=self.fstFrame)

        #Room Label and Entry
        self.selectRoomLabel=Label(master=self.sndFrame, text="Select Room: ")
        self.selectRoomEntry=Entry(master=self.sndFrame)

        #Add and remove buttons
        self.addButton=Button(text="Add", command=self.addItem)
        self.removeButton=Button(text="Remove", command=self.removeItem)

    def packItems(self):
        '''this fx packs buttons in screen'''

        #packing frames
        self.fstFrame.pack()
        self.sndFrame.pack()

        #Item label and entry packing
        self.selectItemLabel.pack(side="left")
        self.selectItemEntry.pack(side="left")
        
        #packing room label and entry
        self.selectRoomLabel.pack(side="left")
        self.selectRoomEntry.pack(side="left")

        #packing buttons
        self.addButton.pack()
        self.removeButton.pack()


    def StartApp(self):
        #event loop
        self.mainloop()

    def addItem(self):
        '''fx executes when add button is clicked'''

        #get values of Entry boxes
        ItemName=self.selectItemEntry.get()
        RoomNo=self.selectRoomEntry.get()

        #try converting Room no to int if it is not possible throw error and return
        try:
            RoomNo=int(RoomNo)
        except ValueError:
            messagebox.showerror("Invalid Input", "Please Enter a valid Integer in Room Number")
            return
        #call insertItemfx
        insertItem(ItemName, RoomNo)

    def removeItem(self):
        '''fx executes when remove button is clicked'''
        ItemName=self.selectItemEntry.get()
        RoomNo=self.selectRoomEntry.get()
        #try converting Room no to int if it is not possible throw error and return
        try:
            RoomNo=int(RoomNo)
        except ValueError:
            messagebox.showerror("Invalid Input", "Please Enter a valid Integer in Room Number")
            return
        # call insertItemfx
        deleteItem(ItemName, RoomNo)


if __name__ =="__main__":
    
    #<-------- Initlizing Items -------->
    
    # CreateDB("database.db ")
    # SampleDataInsert("database.db")

    screen=Laundry()

    screen.init_Elements()

    screen.packItems()

    screen.StartApp()

