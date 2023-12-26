import pandas as pd
from tkinter import Tk, filedialog, Button, Label

# Function to handle selecting the source CSV file
def select_source_file():
    source_file_path = filedialog.askopenfilename(title="Select Source CSV File", filetypes=[("CSV Files", "*.csv")])
    source_file_label.config(text=source_file_path) # Update the label text with the selected file path

# Function to handle selecting the destination CSV file
def select_destination_file():
    destination_file_path = filedialog.askopenfilename(title="Select Destination CSV File", filetypes=[("CSV Files", "*.csv")])
    destination_file_label.config(text=destination_file_path) # Update the label text with the selected file path

# Function to handle moving the data from source to destination
def move_data():
    # Get the selected source and destination file paths
    source_file_path = source_file_label.cget("text")
    destination_file_path = destination_file_label.cget("text")

    # Check if the source or destination file paths are empty
    if not source_file_path or not destination_file_path:
        print("Source or destination file not selected.")
        return

    # Read the source CSV file using pandas
    source_df = pd.read_csv(source_file_path)

    # Check if the required fields exist in the source file
    source_required_fields = ["Name", "Type", "Data Type", "Address"]
    missing_fields = [field for field in source_required_fields if field not in source_df.columns]

    if missing_fields:
        print("The following fields are missing in the source file:", missing_fields)
        return

    # Read the destination CSV file using pandas
    destination_df = pd.read_csv(destination_file_path, skiprows=6)

    # Create a new DataFrame with the rows from the source file
    rows_to_append = []

    # Iterate through each row of the source table
    for index, row in source_df.iterrows():
    # Assign each field under their respective columns to their respective variable
        name = row["Name"]
        IO_type = row["Type"]
        data_type = row["Data Type"]
        address = row["Address"]

        # Append the row to the list of rows to be added
        rows_to_append.append({"TYPE": "TAG", "SCOPE": '', "NAME": address, "DESCRIPTION": name, "DATATYPE": data_type, "ATTRIBUTES": "(RADIX := Decimal, Constant := false, ExternalAccess := Read/Write)"})

        # Print the value added to the column and row of the destination file for testing purposes
        print(f"Added 'TAG' to TYPE column for row {index+1} in the destination file.")

    # Convert the list of rows to a DataFrame
    rows_df = pd.DataFrame(rows_to_append)

    # Concatenate the rows DataFrame with the destination DataFrame
    destination_df = pd.concat([destination_df, rows_df], ignore_index=True)

    ## Save the updated destination DataFrame to the destination file
    #destination_df.to_csv(destination_file_path, index=False)

    # Save the updated destination DataFrame to the destination file, skipping the first 6 rows
    destination_df.to_csv(destination_file_path, index=False, mode='a', header=False)

    # Print a message indicating the data move process completion
    print("Data move process completed successfully.")



# Create Tkinter window
root = Tk()

# Button for selecting the source CSV file
select_source_button = Button(root, text="Select Source CSV File", command=select_source_file)
select_source_button.pack()

# Label to display the selected source file path
source_file_label = Label(root, text="No source file selected")
source_file_label.pack()

# Button for selecting the destination CSV file
select_destination_button = Button(root, text="Select Destination CSV File", command=select_destination_file)
select_destination_button.pack()

# Label to display the selected destination file path
destination_file_label = Label(root, text="No destination file selected")
destination_file_label.pack()

# Button for moving the data
move_data_button = Button(root, text="Move Data", command=move_data)
move_data_button.pack()

# Run the Tkinter event loop
root.mainloop()
