from pyrebase import *
from tkinter import *
from tkinter.messagebox import *
from tkinter.scrolledtext import *
import matplotlib.pyplot as plt
import requests
import bs4

firebaseConfig = {
	"apiKey": "AIzaSyA5mqnUwH0Vwzq1IiAVbIattmtlu0DKwFI",
	"authDomain": "studentmanagementsystem-7c64b.firebaseapp.com",
	"databaseURL": "https://studentmanagementsystem-7c64b-default-rtdb.asia-southeast1.firebasedatabase.app",
	"projectId": "studentmanagementsystem-7c64b",
	"storageBucket": "studentmanagementsystem-7c64b.appspot.com",
	"messagingSenderId": "412244357570",
	"appId": "1:412244357570:web:366e023e228399a522a65b"
	}

firebase = initialize_app(firebaseConfig)
db = firebase.database()

def f1():
	add_window.deiconify()
	main_window.withdraw()
def f2():
	main_window.deiconify()
	add_window.withdraw()

def add():
	info = {}
	try:
		rno = aw_ent_rno.get()
		name = aw_ent_name.get()
		marks = aw_ent_marks.get()
		if (not rno.isdigit()) or (len(rno) == 0) or (int(rno) <= 0):
			showerror("Roll No Issue", "Invalid roll no") 		
			aw_ent_rno.delete(0, END)
			aw_ent_rno.focus()
			return
		if (not name.isalpha()) or (len(name) < 2):
			showerror("Name Issue", "Invalid name") 
			aw_ent_name.delete(0, END)
			aw_ent_name.focus()
			return
		if (not marks.isdigit()) or (len(marks) == 0) or (int(marks) < 0) or (int(marks) > 100): 
			showerror("Marks Issue", "Invalid marks")
			aw_ent_marks.delete(0, END)
			aw_ent_marks.focus()
			return
		data = db.child("student").get()
		if data.pyres is not None and rno in data.val():
			showerror("Error", "Roll No Already Exists")
		else:
			info = {"rno": int(rno), "name": name, "marks": int(marks)}
			db.child("student").child(rno).set(info)
			showinfo("Success", "Record created")
		
		aw_ent_rno.delete(0, END)
		aw_ent_name.delete(0, END)
		aw_ent_marks.delete(0, END)
		aw_ent_rno.focus()
	except Exception as e:
		showerror("Error", str(e))
def view():
	view_window.deiconify()
	main_window.withdraw() 		
	vw_st_data.delete(1.0, END)
	info = {}
	try:
		data = db.child("student").get()
		#print(data.val())
		if data.pyres:
			for d in data.each():
				'''if d.val() is None:
					continue'''
				info = str(d.val()) + "\n"
				vw_st_data.insert(INSERT, info)
		else:
			showerror("Error", "No data")
	except Exception as e:
		showerror("Error", str(e))
def f4():
	main_window.deiconify()
	view_window.withdraw()
def f5():
	update_window.deiconify()
	main_window.withdraw()
def f6():
	main_window.deiconify()
	update_window.withdraw()
def f7():
	delete_window.deiconify()
	main_window.withdraw()
def f8():
	main_window.deiconify()
	delete_window.withdraw()
def charts():
	info = {}
	try:
		data = db.child("student").get()
		name = ""
		marks = int()
		name_list = []
		marks_list = []
		if data.pyres:
			for d in data.each():
				info = d.val()
				name = info.get("name")
				marks = info.get("marks")
				name_list.append(name)
				marks_list.append(marks)
		else:
			showerror("Error", "No data")

		plt.bar(name_list, marks_list, width=0.7, color=["red", "green", "blue"])
		plt.ylim(0, 105)
		plt.xlabel("Students")
		plt.ylabel("Marks")
		plt.title("Batch Information")
		plt.show()

	except Exception as e:
		showerror("Error", str(e))
def update():
	info = {}
	try:
		rno = uw_ent_rno.get()
		name = uw_ent_name.get()
		marks = uw_ent_marks.get()
		if (not rno.isdigit()) or (len(rno) == 0) or (int(rno) <= 0):
			showerror("Roll No Issue", "Invalid roll no") 		
			uw_ent_rno.delete(0, END)
			uw_ent_rno.focus()
			return
		if (not name.isalpha()) or (len(name) < 2):
			showerror("Name Issue", "Invalid name") 
			uw_ent_name.delete(0, END)
			uw_ent_name.focus()
			return
		if (not marks.isdigit()) or (len(marks) == 0) or (int(marks) < 0) or (int(marks) > 100): 
			showerror("Marks Issue", "Invalid marks")
			uw_ent_marks.delete(0, END)
			uw_ent_marks.focus()
			return
		data = db.child("student").get()
		if data.pyres is not None and rno in data.val() :
			info = {"rno": int(rno), "name": name, "marks": int(marks)}
			db.child("student").child(rno).update(info)
			showinfo("Success", "Record updated")
		else:
			showerror("Error","Record not found")

		uw_ent_rno.delete(0, END)
		uw_ent_name.delete(0, END)
		uw_ent_marks.delete(0, END)
		uw_ent_rno.focus()
	except Exception as e:
		showerror("Error", str(e))
def delete():
	try:
		rno = dw_ent_rno.get()
		if (not rno.isdigit()) or (len(rno) == 0) or (int(rno) <= 0):
			showerror("Roll No Issue", "Invalid roll no") 		
			dw_ent_rno.delete(0, END)
			dw_ent_rno.focus()
			return
		data = db.child("student").get()
		if data.pyres is not None and rno in data.val():
			db.child("student").child(rno).remove()
			showinfo("Success","Record deleted")
		else:
			showerror("Error","Record not found")
		dw_ent_rno.delete(0, END)
		dw_ent_rno.focus()
	except Exception as e:
		showerror("Error", str(e))

main_window = Tk()
main_window.title("S. M. S")
main_window.geometry("500x530+650+225")
main_window.configure(bg="antique white")

try:
	wa = "https://ipinfo.io/"
	res = requests.get(wa)
	data = res.json()

	location_name = "Location: " + data['city'] + "," + " " + data['country']

except Exception as e:
	print("Issue", e)
	location_name = "Location: Error\t "
try:
	api_key = "6aec4029e4a643f15b82009ac24ae555"
	base_url = "http://api.openweathermap.org/data/2.5/weather?q="
	city_name = "Mumbai"

	complete_url = base_url + city_name + "&appid=" + api_key + "&units=metric"

	res = requests.get(complete_url)
	data = res.json()

	tmp = " Temp: " + str(data['main']['temp']) + " °C"

except Exception as e:
	print("Issue", e)
	tmp = "       Temp: Error"
try:
	wa = "https://www.brainyquote.com/quote_of_the_day"
	res = requests.get(wa)
	
	data = bs4.BeautifulSoup(res.text, "html.parser")

	info = data.find("img", {"class":"p-qotd"})

	quote = "QOTD: " + info["alt"]

except Exception as e:
	print("Issue", e)
	quote = "QOTD: Error "

fa = ("Arial", 15)

mw_frm_loc_tmp = Frame(main_window, bd=2, relief=SOLID, bg="antique white")
mw_frm_loc_tmp.place(x=11.5, y=370, width=475, height=50)
mw_lbl_loc = Label(mw_frm_loc_tmp, text=location_name + "                    " + tmp, font=fa, bg="antique white", pady=7, padx=5)
mw_lbl_loc.grid(pady=3)
mw_frm_qotd = Frame(main_window, bd=2, relief=SOLID, bg="antique white")
mw_frm_qotd.place(x=11.5, y=430, width=475, height=90)
mw_lbl_qotd = Label(mw_frm_qotd, text=quote, font=fa, bg="antique white", wraplength=475, pady=7, padx=5)
mw_lbl_qotd.grid(pady=2)

f = ("Arial", 18, "bold")

mw_btn_add = Button(main_window, text="Add", bd=3.5, font=f, width=10, command=f1)
mw_btn_add.pack(pady=8)
mw_btn_view = Button(main_window, text="View", bd=3.5, font=f, width=10, command=view)
mw_btn_view.pack(pady=8)
mw_btn_update = Button(main_window, text="Update", bd=3.5, font=f, width=10, command=f5)
mw_btn_update.pack(pady=8)
mw_btn_delete = Button(main_window, text="Delete", bd=3.5, font=f, width=10, command=f7)
mw_btn_delete.pack(pady=8)
mw_btn_charts = Button(main_window, text="Charts", bd=3.5, font=f, width=10, command=charts)
mw_btn_charts.pack(pady=8)

add_window = Toplevel(main_window, bg="antique white")
add_window.title("Add Stu.")
add_window.geometry("500x530+650+225")

aw_lbl_rno = Label(add_window, text="Enter Roll No:", font=f, bg="antique white")
aw_ent_rno = Entry(add_window, bd=5, width=29, font=f)
aw_lbl_name = Label(add_window, text="Enter Name:", font=f, bg="antique white")
aw_ent_name = Entry(add_window, bd=5, width=29, font=f)
aw_lbl_marks = Label(add_window, text="Enter Marks:", font=f, bg="antique white")
aw_ent_marks = Entry(add_window, width=29, bd=5, font=f)
aw_btn_save = Button(add_window, text=" Save ", width=10, bd=3.5, font=f, command=add)
aw_btn_back = Button(add_window, text="Back", width=10, bd=3.5, font=f, command=f2)
aw_lbl_rno.pack(pady=8)
aw_ent_rno.pack(pady=8)
aw_lbl_name.pack(pady=8)
aw_ent_name.pack(pady=8)
aw_lbl_marks.pack(pady=8)
aw_ent_marks.pack(pady=8)
aw_btn_save.pack(pady=12)
aw_btn_back.pack(pady=3)

add_window.withdraw()

view_window = Toplevel(main_window, bg="antique white")
view_window.title("View Stu.")
view_window.geometry("500x530+650+225")

vw_st_data = ScrolledText(view_window, width=33, height=12, font=f, bg="white")
vw_btn_back = Button(view_window, text="Back", width=10, bd=3.5, font=f, command=f4)
vw_st_data.pack(pady=20)
vw_btn_back.pack(pady=8)

view_window.withdraw()

update_window = Toplevel(main_window, bg="antique white")
update_window.title("Update Stu.")
update_window.geometry("500x530+650+225")

uw_lbl_rno = Label(update_window, text="Enter Roll No:", font=f, bg="antique white")
uw_ent_rno = Entry(update_window, width=29, bd=5, font=f)
uw_lbl_name = Label(update_window, text="Enter Name:", font=f, bg="antique white")
uw_ent_name = Entry(update_window, width=29, bd=5, font=f)
uw_lbl_marks = Label(update_window, text="Enter Marks:", font=f, bg="antique white")
uw_ent_marks = Entry(update_window, width=29, bd=5, font=f)
uw_btn_update = Button(update_window, text="Update", width=10, bd=3.5, font=f, command=update)
uw_btn_back = Button(update_window, text="Back", width=10, bd=3.5, font=f, command=f6)
uw_lbl_rno.pack(pady=8)
uw_ent_rno.pack(pady=8) 
uw_lbl_name.pack(pady=8) 
uw_ent_name.pack(pady=8)
uw_lbl_marks.pack(pady=8) 
uw_ent_marks.pack(pady=8)
uw_btn_update.pack(pady=12)
uw_btn_back.pack(pady=3)

update_window.withdraw()

delete_window = Toplevel(main_window, bg="antique white")
delete_window.title("Delete Stu.")
delete_window.geometry("500x530+650+225")

dw_lbl_rno = Label(delete_window, text="Enter Roll No:", font=f, bg="antique white")
dw_ent_rno = Entry(delete_window, width=29, bd=5, font=f)
dw_btn_delete = Button(delete_window, text="Delete", width=10, bd=3.5, font=f, command=delete)
dw_btn_back = Button(delete_window, text="Back", width=10, bd=3.5, font=f, command=f8)
dw_lbl_rno.pack(pady=8)
dw_ent_rno.pack(pady=8) 
dw_btn_delete.pack(pady=12)
dw_btn_back.pack(pady=3)

delete_window.withdraw()

main_window.mainloop()
