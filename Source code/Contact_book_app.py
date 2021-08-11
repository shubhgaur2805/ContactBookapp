from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from PIL import Image,ImageTk
from PIL import *
import PIL
import sqlite3
import csv
import pandas as pd

root=Tk()
root.title("Contact book app")
root.geometry("780x620")
root["bg"]="peach puff"
root.iconbitmap("book.ico")
#define sqlite3 db
conn=sqlite3.connect("contact.db")
my_cursor=conn.cursor()

try:
	my_cursor.execute("CREATE TABLE contactapp(firstname text, lastname text, contact integer, email text,image_add varchar(1000))")
except:
	print("Created")


#add ttk style
style=ttk.Style()
#add theme
style.theme_use("clam")
#add style
style.configure("Treeview",
	background="white",
	foreground="black",
	rowheight="25",
	fieldbackground="white"
	)
#style selected for select
style.map("Treeview",background=[('selected','blue')])


my_tree=ttk.Treeview(root)
my_tree.pack()
	#define columns
my_tree["columns"]=("ID","First_Name","Last_Name","Contact","Email","OID")

	#format columns
my_tree.column("#0",width=100)        #stretch=NO)
my_tree.column("ID",width=50,anchor=CENTER)
my_tree.column("First_Name",width=100,anchor=W)
my_tree.column("Last_Name",width=100,anchor=W)
my_tree.column("Contact",width=100,anchor=W)
my_tree.column("Email",width=200,anchor=W)
my_tree.column("OID",width=50,anchor=CENTER)

	#heading
my_tree.heading("#0",text="Photo",anchor=W)
my_tree.heading("ID",text=" SNo",anchor=W)
my_tree.heading("First_Name",text="First_Name",anchor=W)
my_tree.heading("Last_Name",text="Last_Name",anchor=W)
my_tree.heading("Contact",text="Contact",anchor=W)
my_tree.heading("Email",text="Email",anchor=W)
my_tree.heading("OID",text="OID",anchor=W)

#create frame
frame_1=Frame(root,background="peach puff")
frame_1.pack(pady=10)

#user define functions

def add_data_tree():
	#add data
	conn=sqlite3.connect("contact.db")
	my_cursor=conn.cursor()
	my_cursor.execute("SELECT *,oid FROM contactapp ORDER BY firstname")
	result=my_cursor.fetchall()

	my_tree.tag_configure("oddrow",background="white")
	my_tree.tag_configure("evenrow",background="peach puff")

	global count, img_lst,lb_total
	count=0
	img_lst=[]
	for record in result:
		if count %2 == 0:
			if record[4]:
				img_icon=Image.open(record[4])
				z="logo"+str(count)+".ico"
				icon_sizes=[(30,30)]
				img_icon.save(z,sizes=icon_sizes)
				#img_lst.append(z)
				img_lst.append(ImageTk.PhotoImage(file=z))
				my_tree.insert(parent='',index='end',iid=count,text="",image=img_lst[-1] ,values=(count,record[0],record[1],record[2],record[3],record[5]),tags=("evenrow",))
				count+=1
			else:
				my_tree.insert(parent='',index='end',iid=count,text="" , values=(count,record[0],record[1],record[2],record[3],record[5]),tags=("evenrow",))
				count+=1
		else:
			if record[4]:
				img_icon=Image.open(record[4])
				z="logo"+str(count)+".ico"
				icon_sizes=[(30,30)]
				img_icon.save(z,sizes=icon_sizes)
				#img_lst.append(z)
				img_lst.append(ImageTk.PhotoImage(file=z))
				my_tree.insert(parent='',index='end',iid=count,text="",image=img_lst[-1] ,values=(count,record[0],record[1],record[2],record[3],record[5]),tags=("oddrow",))
				count+=1
			else:
				my_tree.insert(parent='',index='end',iid=count,text="" , values=(count,record[0],record[1],record[2],record[3],record[5]),tags=("oddrow",))
				count+=1

	lb_total.config(text="Total Contacts: "+str(count))

global Entry_image
Entry_image=""
def up_image():
	global Entry_image
	Entry_image=filedialog.askopenfilename(initialdir="/tkinter/img",title="Select file",filetypes=(("png files","*.png"),("jpg files","*.jpg"),("All files","*.*")))

def add():
	global Entry_image, count, img_lst
	conn=sqlite3.connect("contact.db")
	my_cursor=conn.cursor()
	my_cursor.execute("INSERT INTO contactapp VALUES(:fname,:lname,:contact,:email,:img_ad)",
	{
	"fname" : Entry_name.get(),
	"lname" : Entry_last.get(),
	"contact" : Entry_contact.get(),
	"email" : Entry_email.get(),
	"img_ad" : Entry_image
	})

	conn.commit()
	conn.close()

	for i in my_tree.get_children():
		my_tree.delete(i)

	#calling
	add_data_tree()

	Entry_name.delete(0,END)
	Entry_last.delete(0,END)
	Entry_contact.delete(0,END)
	Entry_email.delete(0,END)
	Entry_image=""


def delete():
	x=my_tree.selection()
	for i in x:
		z=my_tree.item(i)
		delete_itm = z["values"][-1]
		conn=sqlite3.connect("contact.db")
		my_cursor=conn.cursor()
		my_cursor.execute("DELETE FROM contactapp WHERE oid =" + str(delete_itm))
		conn.commit()
		conn.close()
	for j in x:
		my_tree.delete(j)

	for i in my_tree.get_children():
		my_tree.delete(i)
	#calling
	add_data_tree()

def search_name():
		query = search_entry.get()
		selection=[]
		for child in my_tree.get_children():
			if query.lower() in my_tree.item(child)['values'][1].lower():
				#print(my_tree.item(child)['values'])
				selection.append(child)
		my_tree.selection_set(selection)


def excel_data():
		conn=sqlite3.connect("contact.db")
		my_cursor=conn.cursor()
		my_cursor.execute("SELECT *,oid FROM contactapp ORDER BY firstname")
		result=my_cursor.fetchall()
		field=["First_Name","Last_Name","Contact","Email","Image","OId"]
		with open("contact_book.csv","w",newline="") as f:
			w=csv.writer(f,dialect="excel")
			w.writerow(field)
			for i in result:
				w.writerow(i)
		conn.commit()
		conn.close()

def update_select():
		global Entry_image,get_oid
		x=my_tree.selection()
		z=my_tree.item(x)
		get_oid=z["values"][-1]
		sql="SELECT * FROM contactapp WHERE oid="+str(get_oid)
		conn=sqlite3.connect("contact.db")
		my_cursor=conn.cursor()
		my_cursor.execute(sql)
		result1=my_cursor.fetchall()
		conn.commit()
		conn.close()

		#calling
		update_tree()
		
		for record in result1:
			Entry_name_update.insert(0,record[0])
			Entry_last_update.insert(0,record[1])
			Entry_contact_update.insert(0,record[2])
			Entry_email_update.insert(0,record[3])
			Entry_image=record[4]

def updatedb_tree():
		global Entry_image,showwin
		conn=sqlite3.connect("contact.db")
		my_cursor=conn.cursor()
		my_cursor.execute("""UPDATE contactapp SET firstname = :fname, lastname =:lname, contact=:contact1, email=:email1,image_add=:img_a WHERE oid = :oid""",
					{ "fname" : Entry_name_update.get() ,
					  "lname" : Entry_last_update.get() ,
					  "contact1" : Entry_contact_update.get(), 
					  "email1" : Entry_email_update.get(), 
					  "img_a" : Entry_image, 
					  "oid" : str(get_oid)
					  })
		conn.commit()
		conn.close()
		Entry_name_update.delete(0,END)
		Entry_last_update.delete(0,END)
		Entry_contact_update.delete(0,END)
		Entry_email_update.delete(0,END)
		Entry_image=""

		for i in my_tree.get_children():
			my_tree.delete(i)

		#calling
		add_data_tree()

		showwin.destroy()

def update_tree():
	global showwin
	showwin=Tk()
	showwin.title("Update")
	showwin.iconbitmap("book.ico")
	showwin.geometry("400x400")
	showwin["bg"]="peach puff"

	global Entry_name_update
	global Entry_email_update
	global Entry_last_update
	global Entry_contact_update
	#enter name
	label_name_update=Label(showwin,text="Update First Name:",font=("Helvetica",15),bg="peach puff")
	label_name_update.grid(row=2,column=1,padx=10,pady=5,sticky=W)
	Entry_name_update=Entry(showwin,font=("Helvetica",10))
	Entry_name_update.grid(row=2,column=2,padx=10,pady=5)

	#enter last name
	label_last_update=Label(showwin,text="Update Last Name:",font=("Helvetica",15),bg="peach puff")
	label_last_update.grid(row=3,column=1,padx=10,pady=5,sticky=W)
	Entry_last_update=Entry(showwin,font=("Helvetica",10))
	Entry_last_update.grid(row=3,column=2,padx=10,pady=5)

	#enter contact
	label_contact_update=Label(showwin,text="Update Contact:",font=("Helvetica",15),bg="peach puff")
	label_contact_update.grid(row=4,column=1,padx=10,pady=5,sticky=W)
	Entry_contact_update=Entry(showwin,font=("Helvetica",10))
	Entry_contact_update.grid(row=4,column=2,padx=10,pady=5)

	#enter email
	label_email_update=Label(showwin,text="Update Email:",font=("Helvetica",15),bg="peach puff")
	label_email_update.grid(row=5,column=1,padx=10,pady=5,sticky=W)
	Entry_email_update=Entry(showwin,font=("Helvetica",10))
	Entry_email_update.grid(row=5,column=2,padx=10,pady=5)

	#enter image
	label_image=Label(showwin,text="Update Image:",font=("Helvetica",15),bg="peach puff")
	label_image.grid(row=6,column=1,padx=10,pady=5,sticky=W)
	Enter_image=Button(showwin,text="Upload",font=("Helvetica",12),command=up_image,bg="peach puff",relief=GROOVE,bd=10)
	Enter_image.grid(row=6,column=2,padx=10,pady=5)

	updatebutton=Button(showwin,text="Update DataBase",command=updatedb_tree,bg="peach puff",relief=GROOVE,bd=10,width=50).grid(row=7,column=1,columnspan=3,padx=10,pady=15)


def import_data():
	try:
		open_file=filedialog.askopenfilename(initialdir="/tkinter/img",title="Import Data",filetypes=(("CSV files","*.csv"),("All Files","*.*")))
		conn=sqlite3.connect("contact.db")
		my_cursor=conn.cursor()
		a_file=open(open_file)
		rows=csv.reader(a_file)
		my_cursor.executemany("INSERT INTO contactapp VALUES(?,?,?,?,?)",rows)
		conn.commit()
		conn.close()
	except:
		print("Ohh contact Creator")
	add_data_tree()


#Add into db

lb_total=Label(frame_1,text="Total Contacts: "+ str(0),font=("Helvetica",12,"bold"),bg="black",fg="white")
lb_total.grid(row=0,column=1,sticky=W,pady=5,padx=10)

lb_main=Label(frame_1,text="Add Contact",font=("Helvatica",20,"bold"),bg="peach puff")
lb_main.grid(row=1,column=1,columnspan=2)

lb_main1=Label(frame_1,text="Operations",font=("Helvetica",20,"bold"),bg="peach puff")
lb_main1.grid(row=1,column=6,columnspan=2)

#enter name
label_name=Label(frame_1,text="Enter First Name:",font=("Helvetica",15,"bold"),bg="peach puff")
label_name.grid(row=2,column=1,padx=10,pady=5,sticky=W)
Entry_name=Entry(frame_1,font=("Helvetica",12))
Entry_name.grid(row=2,column=2,padx=10,pady=5)

#enter last name
label_last=Label(frame_1,text="Enter Last Name:",font=("Helvetica",15,"bold"),bg="peach puff")
label_last.grid(row=3,column=1,padx=10,pady=5,sticky=W)
Entry_last=Entry(frame_1,font=("Helvetica",12))
Entry_last.grid(row=3,column=2,padx=10,pady=5)

#enter contact
label_contact=Label(frame_1,text="Enter Contact:",font=("Helvetica",15,"bold"),bg="peach puff")
label_contact.grid(row=4,column=1,padx=10,pady=5,sticky=W)
Entry_contact=Entry(frame_1,font=("Helvetica",12))
Entry_contact.grid(row=4,column=2,padx=10,pady=5)

#enter email
label_email=Label(frame_1,text="Enter Email:",font=("Helvetica",15,"bold"),bg="peach puff")
label_email.grid(row=5,column=1,padx=10,pady=5,sticky=W)
Entry_email=Entry(frame_1,font=("Helvetica",12))
Entry_email.grid(row=5,column=2,padx=10,pady=5)

#enter image add
label_image=Label(frame_1,text="Add Image:",font=("Helvetica",15,"bold"),bg="peach puff")
label_image.grid(row=6,column=1,padx=10,pady=5,sticky=W)
Enter_bt=Button(frame_1,text="Upload",font=("Helvetica",12),command=up_image,bg="peach puff",relief=GROOVE,bd=10)
Enter_bt.grid(row=6,column=2,padx=10,pady=5)
#global lb_img, Entry_image
#on=PhotoImage(file=Entry_image)
#lb_img=Label(frame_1,image=on)
#lb_img.grid(row=7,column=2,padx=10,pady=5)	

#entry search
label_search=Label(frame_1,text="Search",font=("Helvetica",15,"bold"),bg="peach puff")
label_search.grid(row=2,column=6)
search_entry=Entry(frame_1,font=("Helvetica",12))
search_entry.grid(row=2,column=7,pady=5,padx=10)

search_button=Button(frame_1,text="Search",command=search_name,bg="peach puff",relief=GROOVE,bd=10,).grid(row=3,column=7,padx=10,pady=5)
addbutton=Button(frame_1,text="ADD",command=add,bg="peach puff",relief=GROOVE,bd=10,width=8).grid(row=4,column=6,padx=10,pady=5)
deletebutton=Button(frame_1,text="Delete DB",command=delete,bg="peach puff",relief=GROOVE,bd=10,width=8).grid(row=4,column=7,padx=10,pady=5)
updatebutton=Button(frame_1,text="Update DB",command=update_select,bg="peach puff",relief=GROOVE,bd=10,width=8).grid(row=5,column=6,padx=10,pady=5)
save_to_excel=Button(frame_1,text="Export to CSV",command=excel_data,bg="peach puff",relief=GROOVE,bd=10,width=12).grid(row=5,column=7,padx=10,pady=5)
import_data_button=Button(frame_1,text="Import from CSV",command=import_data,bg="peach puff",relief=GROOVE,bd=10,width=15).grid(row=6,column=6,columnspan=2,pady=10,padx=5)
add_data_tree()

conn.close()

root.mainloop()