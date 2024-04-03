from tkinter import *
from tkinter import ttk, messagebox
import sqlite3

class CourseClass:
    def __init__(self, root):
        self.root = root
        self.root.title("Evaluation Dashboard")
        
        # Get the screen width and height
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        # Set the geometry to occupy the entire screen
        self.root.geometry(f"{screen_width}x{screen_height}+0+0")
        self.root.config(bg="#f0f0f0")
        self.root.focus_force()

        # Title
        title = Label(self.root, text="Evaluation Dashboard", font=("Arial", 20, "bold"), bg="#2196f3", fg="white")
        title.pack(fill=X)

        # Variables
        self.var_course = StringVar()
        self.var_duration = StringVar()
        self.var_charges = StringVar()
        self.var_search = StringVar()

        # Labels for course name, duration, charges, and description
        lbl_courseName = Label(self.root, text="Enrollment", font=("Arial", 12), bg="#f0f0f0")
        lbl_courseName.place(x=50, y=70)

        lbl_duration = Label(self.root, text="Name", font=("Arial", 12), bg="#f0f0f0")
        lbl_duration.place(x=250, y=70)

        lbl_charges = Label(self.root, text="Marks", font=("Arial", 12), bg="#f0f0f0")
        lbl_charges.place(x=450, y=70)

        lbl_description = Label(self.root, text="Remark", font=("Arial", 12), bg="#f0f0f0")
        lbl_description.place(x=650, y=70)

        # Entry fields for course name, duration, charges, and description
        self.txt_courseName = Entry(self.root, textvariable=self.var_course, font=("Arial", 12), bg='lightyellow')
        self.txt_courseName.place(x=50, y=100, width=150)

        txt_duration = Entry(self.root, textvariable=self.var_duration, font=("Arial", 12), bg='lightyellow')
        txt_duration.place(x=250, y=100, width=150)

        txt_charges = Entry(self.root, textvariable=self.var_charges, font=("Arial", 12), bg='lightyellow')
        txt_charges.place(x=450, y=100, width=150)

        self.txt_description = Text(self.root, font=("Arial", 12), bg='lightyellow', height=2)
        self.txt_description.place(x=650, y=100, width=300)

        # Button Frame
        btn_frame = Frame(self.root, bg="#f0f0f0")
        btn_frame.place(x=50, y=150, width=900)

        self.btn_add = Button(btn_frame, text='Save', font=("Arial", 12, "bold"), bg="#4CAF50", fg="white",
                              cursor="hand2", command=self.add)
        self.btn_add.grid(row=0, column=0, padx=5)

        self.btn_update = Button(btn_frame, text='Update', font=("Arial", 12, "bold"), bg="#FFA500", fg="white",
                                 cursor="hand2", command=self.update)
        self.btn_update.grid(row=0, column=1, padx=5)

        self.btn_delete = Button(btn_frame, text='Delete', font=("Arial", 12, "bold"), bg="#f44336", fg="white",
                                 cursor="hand2", command=self.delete)
        self.btn_delete.grid(row=0, column=2, padx=5)

        self.btn_clear = Button(btn_frame, text='Clear', font=("Arial", 12, "bold"), bg="#808080", fg="white",
                                cursor="hand2", command=self.clear)
        self.btn_clear.grid(row=0, column=3, padx=5)

        # Search Panel
        search_frame = Frame(self.root, bg="#f0f0f0")
        search_frame.place(x=50, y=200, width=900)

        lbl_search_courseName = Label(search_frame, text="Course name", font=("Arial", 12), bg="#f0f0f0")
        lbl_search_courseName.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        txt_search_courseName = Entry(search_frame, textvariable=self.var_search, font=("Arial", 12),
                                      bg='lightyellow')
        txt_search_courseName.grid(row=0, column=1, padx=10, pady=10, sticky="w")

        btn_search = Button(search_frame, text='Search', font=("Arial", 12, "bold"), bg="#2196f3", fg="white",
                            cursor="hand2", command=self.search)
        btn_search.grid(row=0, column=2, padx=10, pady=5)

        # Course Table
        table_frame = Frame(self.root, bg="#f0f0f0")
        table_frame.place(x=50, y=250, width=900, height=550)

        scroll_y = Scrollbar(table_frame, orient=VERTICAL)
        scroll_x = Scrollbar(table_frame, orient=HORIZONTAL)

        self.CourseTable = ttk.Treeview(table_frame, columns=("cid", "name", "duration", "charges", "description"),
                                        yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)

        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)

        scroll_x.config(command=self.CourseTable.xview)
        scroll_y.config(command=self.CourseTable.yview)

        self.CourseTable.heading("cid", text="Sr no.")
        self.CourseTable.heading("name", text="Enrollment")
        self.CourseTable.heading("duration", text="Name")
        self.CourseTable.heading("charges", text="Marks")
        self.CourseTable.heading("description", text="Remark")

        self.CourseTable["show"] = 'headings'

        self.CourseTable.column("cid", width=100)
        self.CourseTable.column("name", width=150)
        self.CourseTable.column("duration", width=100)
        self.CourseTable.column("charges", width=100)
        self.CourseTable.column("description", width=250)

        self.CourseTable.pack(fill=BOTH, expand=1)
        self.CourseTable.bind("<ButtonRelease-1>", self.get_data)
        self.show()

    def clear(self):
        self.show()
        self.var_course.set("")
        self.var_duration.set("")
        self.var_charges.set("")
        self.var_search.set("")
        self.txt_description.delete('1.0', END)
        self.txt_courseName.config(state=NORMAL)

    def delete(self):
        con = sqlite3.connect(database="rms.db")
        cur = con.cursor()
        try:
            if self.var_course.get() == "":
                messagebox.showerror("Error", "Enrollment number should be required", parent=self.root)
            else:
                cur.execute("select * from course where name=?", (self.var_course.get(),))
                row = cur.fetchone()
                if row is None:
                    messagebox.showerror("Error", "Please select a student from the list", parent=self.root)
                else:
                    op = messagebox.askyesno("Confirm", "Do you really want to delete?", parent=self.root)
                    if op:
                        cur.execute("DELETE FROM course WHERE name=?", (self.var_course.get(),))
                        con.commit()
                        messagebox.showinfo("Delete", "Data deleted successfully", parent=self.root)
                        self.clear()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}")

    def get_data(self, ev):
        self.txt_courseName.config(state='readonly')
        r = self.CourseTable.focus()
        content = self.CourseTable.item(r)
        row = content["values"]
        self.var_course.set(row[1])
        self.var_duration.set(row[2])
        self.var_charges.set(row[3])
        self.txt_description.delete('1.0', END)
        self.txt_description.insert(END, row[4])

    def add(self):
        con = sqlite3.connect(database="rms.db")
        cur = con.cursor()
        try:
            # Check the number of existing entries
            cur.execute("SELECT COUNT(*) FROM course")
            count = cur.fetchone()[0]
            if count >= 4:
                messagebox.showwarning("Limit Exceeded", "Maximum 4 entries allowed.", parent=self.root)
            else:
                if self.var_course.get() == "":
                    messagebox.showerror("Error", "Enrollment number should be required", parent=self.root)
                else:
                    cur.execute("select * from course where name=?", (self.var_course.get(),))
                    row = cur.fetchone()
                    if row is not None:
                        messagebox.showerror("Error", "Enrollment number already exists", parent=self.root)
                    else:
                        cur.execute("insert into course (name, duration, charges, description) values(?,?,?,?)", (
                            self.var_course.get(),
                            self.var_duration.get(),
                            self.var_charges.get(),
                            self.txt_description.get("1.0", END)
                        ))
                        con.commit()
                        messagebox.showinfo("Success", "Student added successfully", parent=self.root)
                        self.show()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}")

    def update(self):
        con = sqlite3.connect(database="rms.db")
        cur = con.cursor()
        try:
            if self.var_course.get() == "":
                messagebox.showerror("Error", "Enrollment number should be required", parent=self.root)
            else:
                cur.execute("select * from course where name=?", (self.var_course.get(),))
                row = cur.fetchone()
                if row is None:
                    messagebox.showerror("Error", "Select a student from the list", parent=self.root)
                else:
                    cur.execute("update course set duration=?,charges=?,description=? where name=?",
                                (
                                    self.var_duration.get(),
                                    self.var_charges.get(),
                                    self.txt_description.get("1.0", END),
                                    self.var_course.get(),
                                ))
                    con.commit()
                    messagebox.showinfo("Success", "Data updated successfully", parent=self.root)
                    self.show()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}")

    def show(self):
        con = sqlite3.connect(database="rms.db")
        cur = con.cursor()
        try:
            cur.execute("select * from course")
            rows = cur.fetchall()
            self.CourseTable.delete(*self.CourseTable.get_children())
            for row in rows:
                self.CourseTable.insert('', END, values=row)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}")

    def search(self):
        con = sqlite3.connect(database="rms.db")
        cur = con.cursor()
        try:
            cur.execute(f"select * from course where name LIKE '%{self.var_search.get()}%'")
            rows = cur.fetchall()
            self.CourseTable.delete(*self.CourseTable.get_children())
            for row in rows:
                self.CourseTable.insert('', END, values=row)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}")


if __name__ == "__main__":
    root = Tk()
    obj = CourseClass(root)
    root.mainloop()
