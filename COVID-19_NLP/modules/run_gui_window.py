from datetime import datetime
from tkinter import *

tk = Tk()
text = Text(tk, height=30, width=50, bg='light gray')
entry = Entry(tk, width=65, bd=5)
vsb = Scrollbar(orient="vertical", command=text.yview)
text.configure(yscrollcommand=vsb.set)
vsb.pack(side="right", fill="y")
text.pack(side="left", fill="both", expand=True)

def process_keyword():
    var = BooleanVar(value=False)
    
    text.insert(END,"What keyword would you like to search?")
    keyword = entry.get()
    var.set(True)
    print("waiting...")
    tk.wait_variable(var)
    print("done waiting.")
    text.insert(END, '\n{}\n'.format(keyword))
    entry.delete(0, END)
    return keyword

def check_date_format(date):
    try:
        datetime.strptime(date, '%m-%d-%Y')
    except ValueError:
        raise ValueError("Incorrect data format, should be mm-dd-YYYY")
        get_dates()
    return date

def get_dates():
    text.insert(END, "What are the starting and ending dates for your search? (mm-dd-YYYY)")
    start_date = check_date_format(entry.get())
    entry.delete(0, END)
    end_date = check_date_format(entry.get())

def process_dates():
    start_date, end_date = get_dates()
    text.insert(END, '\n{} ---> {}\n'.format(start_date, end_date))
    entry.delete(0, END)
    return start_date, end_date

def is_number(price_value):
    try:
        price = float(price_value)
        return price
    except ValueError:
        return 0

def process_num_per_month(number_source):
    text.insert(END, "How many " + number_source + " do you want to search per month?")
    num_per_month = entry.get()
    entry.delete(0, END)
    if is_number(num_per_month) <= 0:
        process_num_per_month()
    return num_per_month

def health_pub_analysis():
    text.insert(END,"\n\n1. MedRxiv health publication scraping/analysis with a keyword graph\n\n")
    keyword = process_keyword()
    start_date, end_date = process_dates()
    pubs_per_month = process_num_per_month('publications')

def twitter_analysis():
    text.insert(END,"\n\n1. MedRxiv health publication scraping/analysis with a keyword graph\n\n")
    keyword = process_keyword()
    start_date, end_date = process_dates()
    tweets_per_month = process_num_per_month('tweets')

def combined_analysis():
    keyword = process_keyword()
    start_date, end_date = process_dates()
    pubs_per_month = process_num_per_month('publications')
    tweets_per_month = process_num_per_month('tweets')

def process_graph():
    entry.delete(0, END)
    keyword = process_keyword()

def program_command(text):
    if text == '1':
        health_pub_analysis()
    elif text == '2':
        twitter_analysis()
    elif text == '3':
        combined_analysis()
    elif text == '4':
        process_graph()

def process_command(text):
    ''' Given a string, returns a string in response. '''
    text = text.strip().lower()
    if text in {'1', '2', '3', '4'}:
        return text
    elif text in {'quit', 'exit'}:
        return
    else:
        return text

def main():
    ''' Main entry point of the program: create the windows and
        kick off the event loop '''
    
    canvas = Canvas(tk, width=400, height=200, bg='white')
    canvas.pack()

    text.pack()

    def process_callback(*args):
        ''' Callback that's called when the user presses enter or
            clicks the button. '''

        # figure out what the response to the input should be
        response = process_command(entry.get())
        text.see("end")
        if response is None:
            tk.quit()
            tk.destroy()
            return
        elif response in {'1', '2', '3', '4'}:
            entry.destroy()
            program_command(response)
        
        # write the response
        text.insert(END, '\n{}\n'.format(response))
        
        # clear the input field
        entry.delete(0, END)

    entry.pack()
    entry.focus()
    entry.bind('<Return>', process_callback)

    btn = Button(tk, width=50, bd=3, bg='dark gray', text='Submit',
                    command=process_callback)
    btn.pack()

    text.insert(END, "HealthPub/Tweet NLP Analysis Chart Generator\n\n""What would you like to do?\n\n"
    "1. MedRxiv health publication scraping/analysis with a keyword graph\n"
    "2. Twitter tweet scraping/analysis with a keyword graph\n3. Options 1 and 2 together\n"
    "4. Creating a keyword graph from already available NLP keyword csv files located in the "
    "\"nlp_keywords\" folder.")

    tk.mainloop()

if __name__ == '__main__':
    main()