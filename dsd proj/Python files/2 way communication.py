import serial
import threading

# UART Configuration
UART_PORT = 'COM5'  # Replace with your port
BAUD_RATE = 9600
DATA_FILE = 'data.txt'  # File for transmission input
OUTPUT_FILE = 'received_data.txt'  # File for reception output
TRANSMISSION_LOG_FILE = 'transmission_log.txt'  # File to log transmitted decimal values

# Function to transmit data from a file
import time  # Import time module for delays

# Function to transmit data from a file with delay
def transmit_data(uart):
    try:
        with open(DATA_FILE, 'r') as file, open(TRANSMISSION_LOG_FILE, 'w') as log_file:
            for line in file:
                line = line.strip()  # Remove whitespace or newline characters
                if line.isdigit():  # Validate if it's a number
                    number = int(line)
                    if 0 <= number <= 255:  # Ensure it fits in 1 byte
                        binary_data = number.to_bytes(1, byteorder='little')  # Convert to binary
                        binary_string = format(number, '08b')  # 8-bit binary string

                        # Introduce a delay before transmitting the next byte
                        time.sleep(0.4)  # Delay of 1 second (adjust as needed)

                        uart.write(binary_data)  # Send data
                        print(f"Transmitted: {binary_string} (Decimal: {number})")

                        # Log the transmitted decimal value to the file
                        log_file.write(f"Transmitted Decimal: {number}\n")
                        log_file.flush()  # Ensure immediate write to the file
                    else:
                        print(f"Invalid number (out of range): {line}")
                elif line == ".":  # Special handling for period (transmit it as a byte)
                    binary_data = b"."  # Send period as a byte (ASCII value 46)
                    binary_string = format(ord("."), '08b')  # Get the binary representation
                    print(f"Transmitted: {binary_string} (ASCII: {ord('.')})")

                    uart.write(binary_data)  # Transmit period
                    time.sleep(2)  # Delay of 1 second
                    log_file.write(f"Transmitted Period: {ord('.')}\n")  # Log the period transmission
                    log_file.flush()  # Ensure immediate write to the file
                else:
                    print(f"Ignoring invalid input: {line}")
    except FileNotFoundError:
        print(f"Error: File '{DATA_FILE}' not found.")
    except Exception as e:
        print(f"Error during transmission: {e}")

# Function to receive data and save to a file
def receive_data(uart):
    try:
        with open(OUTPUT_FILE, 'w') as file:
            print(f"Listening for UART data...")
            while True:
                if uart.in_waiting > 0:  # Check for available data
                    binary_data = uart.read(1)  # Read 1 byte
                    decimal_value = int.from_bytes(binary_data, byteorder='big')  # Convert to integer
                    binary_string = format(decimal_value, '08b')  # 8-bit binary string
                    ascii_char = chr(decimal_value)  # Convert to ASCII character
                    print(f"Received Binary: {binary_string}, Decimal: {decimal_value}, ASCII: {ascii_char}")

                    # Write received binary, decimal, and ASCII character to file
                    file.write(f"Binary: {binary_string}, Decimal: {decimal_value}, ASCII: {ascii_char}\n")
                    file.flush()  # Ensure immediate write to file
                      # Introduce a delay of 1 second between receiving bytes
                    time.sleep(1)
    except Exception as e:
        print(f"Error during reception: {e}")  

# Main function to set up UART and threads
def main():



    try:
        uart = serial.Serial(UART_PORT, BAUD_RATE, timeout=1)
        print(f"UART connection established on {UART_PORT} at {BAUD_RATE} baud.")

        # Create threads for transmission and reception
        tx_thread = threading.Thread(target=transmit_data, args=(uart,))
        rx_thread = threading.Thread(target=receive_data, args=(uart,))

        # Start threads
        tx_thread.start()
        rx_thread.start()

        # Wait for threads to finish
        tx_thread.join()
        rx_thread.join()

    except serial.SerialException as e:
        print(f"Serial error: {e}")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if 'uart' in locals() and uart.is_open:
            uart.close()
            print("UART connection closed.")

if __name__ == "__main__":
    main()