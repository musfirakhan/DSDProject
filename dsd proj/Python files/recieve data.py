import serial

# Open UART device (e.g., COM4 on Windows or /dev/ttyS0 on Linux)
uart = serial.Serial('COM5', 9600)


# Open the file containing numerical data
with open('data.txt', 'r') as file:
    for line in file:
        line = line.strip()  # Remove any extra whitespace or newline characters
        if line.isdigit():  # Check if the line is a valid number
            number = int(line)  # Convert string to integer
            if 0 <= number <= 255:  # Ensure the number fits in 1 byte
                binary_data = number.to_bytes(1, byteorder='little')  # Convert to 1-byte binary
                
                # Generate the 8-bit binary representation
                binary_string = format(number, '08b')  # Convert to binary string with leading zeros
                
                # Print the binary data and 8-bit binary representation
                print(f"Binary Data (8-bit): {binary_string}, Sent as: {binary_data.hex()}")
                
                uart.write(binary_data)  # Send binary data over UART
            else:
                print(f"Number out of range (0-255): {line}")
        else:
            print(f"Ignoring invalid data: {line}")

# Close the UART connection
uart.close()
