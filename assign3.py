#import pywin32 modules to allow windows OS interaction
import subprocess
import win32print
import win32api
import win32ui
import win32gui
import win32file
import traceback
import time



#logs messages to a log file using win32file
def log_message(message):
    try:
        # Open (or create) the log file in append mode
        log_file_path = "C:\\printer_log.txt"  
        file_handle = win32file.CreateFile(
            log_file_path,
            win32file.GENERIC_WRITE,
            0,  
            None,
            win32file.OPEN_ALWAYS,
            win32file.FILE_ATTRIBUTE_NORMAL,
            None
        )
        # appends message to end of file and timestamps it 
        win32file.SetFilePointer(file_handle, 0, win32file.FILE_END)
        log_entry = f"{time.strftime('%Y-%m-%d %H:%M:%S')} - {message}\n"
        win32file.WriteFile(file_handle, log_entry.encode('utf-8'))
        win32file.CloseHandle(file_handle)
    except Exception as e:
        error_message(f"logging Error", "Error logging message: {e}")



# Creates a popup error box with title and contents and sends error meesages to be logged
def error_message(title, message):
    win32gui.MessageBox(0, message, title, 0x10)
    log_message(f"ERROR - {title}: {message}")



def list_printers():
    """
    List all available printers and return their names.
    """
    try:
        printers = win32print.EnumPrinters(win32print.PRINTER_ENUM_LOCAL | win32print.PRINTER_ENUM_CONNECTIONS)
        printer_names = [printer[2] for printer in printers]

        if not printer_names:
            error_message("Printer Error", "No printers found. Exiting.")
            log_message("ERROR - No printers found.")
            return []

        print("\nAvailable Printers:")
        for i, name in enumerate(printer_names, 1):
            print(f"{i}. {name}")
        
        log_message(f"Listed printers: {', '.join(printer_names)}")
        return printer_names
    except Exception as e:
        error_message("Printer Error", f"Error listing printers: {e}")
        traceback.print_exc()
        log_message(f"ERROR - Failed to list printers: {e}")
        return []



def set_default_printer(printer_name):
    """
    Set the default printer.
    """
    try:
        win32print.SetDefaultPrinter(printer_name)
        print(f"\nDefault printer set to: {printer_name}")
        log_message(f"Default printer set to: {printer_name}")
    except Exception as e:
        error_message("Printer Error", f"Failed to set default printer: {e}")
        traceback.print_exc()
        log_message(f"ERROR - Failed to set default printer: {e}")



def get_printer_status(printer_name):
    """
    Retrieve and display the status of a specific printer.
    """
    try:
        printer_handle = win32print.OpenPrinter(printer_name)
        if not printer_handle:
            error_message("Printer Error", f"Failed to open printer: {printer_name}")
            log_message(f"ERROR - Failed to open printer: {printer_name}")
            return
        
        printer_info = win32print.GetPrinter(printer_handle, 2)
        status = printer_info['Status']
        print(f"\nPrinter '{printer_name}' Status: {status}")
        log_message(f"Printer '{printer_name}' Status: {status}")
    except Exception as e:
        error_message("Printer Error", f"Failed to get printer status: {e}")
        traceback.print_exc()
        log_message(f"ERROR - Failed to get printer status: {e}")



def print_test_page(printer_name):
    """
    Print a simple test page to the specified printer using win32ui.
    """
    try:
        hprinter = win32ui.CreateDC()
        hprinter.CreatePrinterDC(printer_name)

        hprinter.StartDoc("Test Page")
        hprinter.StartPage()
        hprinter.TextOut(100, 100, "Hello, this is a test page.")
        hprinter.EndPage()
        hprinter.EndDoc()

        print(f"\nTest page sent to printer: {printer_name}")
        log_message(f"Test page sent to printer: {printer_name}")
    except Exception as e:
        error_message("Printer Error", f"Failed to print test page: {e}")
        traceback.print_exc()
        log_message(f"ERROR - Failed to print test page: {e}")



def cancel_print_jobs(printer_name):
    """
    Cancel all print jobs in the printer's queue.
    """
    try:
        printer_handle = win32print.OpenPrinter(printer_name)
        if not printer_handle:
            error_message("Printer Error", f"Failed to open printer: {printer_name}")
            log_message(f"ERROR - Failed to open printer: {printer_name}")
            return
        
        jobs = win32print.EnumJobs(printer_handle, 0, 10, 1)
        for job in jobs:
            print(f"Cancelling job ID {job['JobId']} on printer {printer_name}")
            win32print.SetJob(printer_handle, job['JobId'], 0, None, win32print.JOB_CONTROL_CANCEL)
        print(f"\nAll print jobs canceled on {printer_name}")
        log_message(f"All print jobs canceled on {printer_name}")
    except Exception as e:
        error_message("Printer Error", f"Failed to cancel print jobs: {e}")
        traceback.print_exc()
        log_message(f"ERROR - Failed to cancel print jobs: {e}")



def reboot_spool_service():
    """
    Run a reboot process on the printer spool service.
    """

    try:
        'Restarting Spooler...'
        subprocess.run(["net", "stop", "spooler"], check=True)
        subprocess.run(["net", "start", "spooler"], check=True)
        print("Print Spooler restarted!")

    except subprocess.CalledProcessError as z:
        print(f"Error restarting print spooler: {z}")


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
        printers = list_printers()
        if not printers:
            print("No printers found. Exiting.")
            log_message("No printers found. Exiting.")
            break

        try:
            choice = input("\nEnter the number of the printer you want to manage (or 'q' to quit): ").strip()
            if choice.lower() == 'q':
                print("Exiting.")
                log_message("Exiting.")
                break

            printer_index = int(choice) - 1
            if printer_index < 0 or printer_index >= len(printers):
                print("Invalid selection. Please try again.")
                log_message("Invalid selection.")
                continue

            printer_name = printers[printer_index]
            print(f"\nSelected Printer: {printer_name}")
            log_message(f"Selected Printer: {printer_name}")

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
                    reboot_spool_service(printer_name)
                elif action == '7':
                    print("Exiting.")
                    log_message("Exiting.")
                    return
                else:
                    print("Invalid choice. Please try again.")
                    log_message("Invalid choice selected.")
        except ValueError:
            print("Invalid input. Please enter a number.")
            log_message("Invalid input entered.")
        except Exception as e:
            print(f"An error occurred: {e}")
            traceback.print_exc()
            log_message(f"ERROR - An error occurred: {e}")



if __name__ == "__main__":
    main()   