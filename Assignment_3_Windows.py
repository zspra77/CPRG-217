import win32print
import win32api
import win32ui
import traceback

def list_printers():
    """
    List all available printers and return their names.

    Returns:
        list: A list of printer names.
    """
    try:
        # Enumerate all printers (local and network-connected)
        printers = win32print.EnumPrinters(win32print.PRINTER_ENUM_LOCAL | win32print.PRINTER_ENUM_CONNECTIONS)
        printer_names = [printer[2] for printer in printers]
        
        # Display available printers
        print("\nAvailable Printers:")
        for i, name in enumerate(printer_names, 1):
            print(f"{i}. {name}")
        
        return printer_names
    except Exception as e:
        print(f"Error listing printers: {e}")
        traceback.print_exc()
        return []

def set_default_printer(printer_name):
    """
    Set the default printer.

    Args:
        printer_name (str): The name of the printer to set as default.
    """
    try:
        win32print.SetDefaultPrinter(printer_name)
        print(f"\nDefault printer set to: {printer_name}")
    except Exception as e:
        print(f"Failed to set default printer: {e}")
        traceback.print_exc()

def get_printer_status(printer_name):
    """
    Retrieve and display the status of a specific printer.

    Args:
        printer_name (str): The name of the printer to check.
    """
    try:
        # Open the printer
        printer_handle = win32print.OpenPrinter(printer_name)
        if not printer_handle:
            print(f"Failed to open printer: {printer_name}")
            return
        
        # Get printer information
        printer_info = win32print.GetPrinter(printer_handle, 2)
        status = printer_info['Status']
        print(f"\nPrinter '{printer_name}' Status: {status}")
    except Exception as e:
        print(f"Failed to get printer status: {e}")
        traceback.print_exc()

def print_test_page(printer_name):
    """
    Print a simple test page to the specified printer using win32ui.

    Args:
        printer_name (str): The name of the printer to print to.
    """
    try:
        # Create a device context for the printer
        hprinter = win32ui.CreateDC()
        hprinter.CreatePrinterDC(printer_name)

        # Start the document
        hprinter.StartDoc("Test Page")

        # Start a page
        hprinter.StartPage()

        # Print text
        hprinter.TextOut(100, 100, "Hello, this is a test page.")

        # End the page and document
        hprinter.EndPage()
        hprinter.EndDoc()

        print(f"\nTest page sent to printer: {printer_name}")
    except Exception as e:
        print(f"Failed to print test page: {e}")
        traceback.print_exc()

def cancel_print_jobs(printer_name):
    """
    Cancel all print jobs in the printer's queue.

    Args:
        printer_name (str): The name of the printer to cancel jobs for.
    """
    try:
        # Open the printer
        printer_handle = win32print.OpenPrinter(printer_name)
        if not printer_handle:
            print(f"Failed to open printer: {printer_name}")
            return
        
        # Enumerate and cancel all jobs
        jobs = win32print.EnumJobs(printer_handle, 0, 10, 1)
        for job in jobs:
            print(f"Cancelling job ID {job['JobId']} on printer {printer_name}")
            win32print.SetJob(printer_handle, job['JobId'], 0, None, win32print.JOB_CONTROL_CANCEL)
        print(f"\nAll print jobs canceled on {printer_name}")
    except Exception as e:
        print(f"Failed to cancel print jobs: {e}")
        traceback.print_exc()

def display_menu():
    """
    Display the action menu for the selected printer.
    """
    print("\nSelect an action:")
    print("1. Set as Default Printer")
    print("2. Get Printer Status")
    print("3. Print Test Page")
    print("4. Cancel All Print Jobs")
    print("5. Select Another Printer")
    print("6. Exit")

def main():
    """
    Main function to run the printer management script.
    """
    while True:
        # List available printers
        printers = list_printers()
        if not printers:
            print("No printers found. Exiting.")
            break

        # Prompt user to select a printer
        try:
            choice = input("\nEnter the number of the printer you want to manage (or 'q' to quit): ").strip()
            if choice.lower() == 'q':
                print("Exiting.")
                break

            printer_index = int(choice) - 1
            if printer_index < 0 or printer_index >= len(printers):
                print("Invalid selection. Please try again.")
                continue

            printer_name = printers[printer_index]
            print(f"\nSelected Printer: {printer_name}")

            # Display action menu
            while True:
                display_menu()
                action = input("Enter your choice: ").strip()

                if action == '1':
                    set_default_printer(printer_name)
                elif action == '2':
                    get_printer_status(printer_name)
                elif action == '3':
                    print_test_page(printer_name)
                elif action == '4':
                    cancel_print_jobs(printer_name)
                elif action == '5':
                    break  # Go back to printer selection
                elif action == '6':
                    print("Exiting.")
                    return
                else:
                    print("Invalid choice. Please try again.")

        except ValueError:
            print("Invalid input. Please enter a number.")
        except Exception as e:
            print(f"An error occurred: {e}")
            traceback.print_exc()

if __name__ == "__main__":
    main()