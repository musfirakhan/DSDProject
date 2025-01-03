import serial

try:
    

    # Open UART device (e.g., COM4 on Windows)
    uart = serial.Serial('COM5', 9600, timeout=1)  # Adjust timeout as needed

    # Open the file to save the received ASCII characters (explicitly in UTF-8)
    with open('received_data.txt', 'w', encoding='utf-8') as file:
        print("Listening for UART data on COM4...")
        while True:
            if uart.in_waiting > 0:  # Check if data is available to read
                # Read one byte at a time
                binary_data = uart.read(1)  # Read 1 byte (8 bits)
                
                # Convert binary data to integer
                ascii_value = int.from_bytes(binary_data, byteorder='big')

                # Convert the integer to an 8-bit binary string
                binary_string = format(ascii_value, '08b')  # Always 8 bits
                ascii_character = chr(ascii_value)  # Convert to ASCII character

                # Display the received binary, ASCII character, and binary string for debugging
                print(f"Received Binary (Hex): {binary_data.hex()}")
                print(f"Received Binary (8-bit): {binary_string}")
                print(f"ASCII: {ascii_character}")

                # Write the ASCII character to the file
                file.write(ascii_character)
                file.write('\n')  # Optional: Write each character on a new line
                file.flush()  # Ensure immediate write to the file

except KeyboardInterrupt:
    print("\nTerminated by user.")
except serial.SerialException as e:
    print(f"Serial Error: {e}")
finally:
    # Close the UART connection
    if 'uart' in locals() and uart.is_open:
        uart.close()
        print("UART connection closed.")
