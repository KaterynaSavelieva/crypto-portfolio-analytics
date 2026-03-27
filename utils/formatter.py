from tabulate import tabulate

def print_table(df):
    print(tabulate(df, headers='keys', tablefmt='plain'))


def print_header(title):
    print(f"\n======={title}=======")

def print_table_titel(df, title):
   table_str = tabulate(df, headers='keys', tablefmt='plain',showindex=False)
   width =len(table_str.split('\n')[0])     # Breite der Tabelle

   print("\n"+"="*width)
   print(title.center(width))
   print("="*width)

   print (table_str)
   print("="*width+"\n")
