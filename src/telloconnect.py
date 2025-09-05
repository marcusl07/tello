from djitellopy import Tello

def set_tello_to_ap_mode(ssid, password):
    """
    Set the Tello drone to access point (AP) mode with the specified SSID and password.

    :param ssid: The SSID (name) for the Tello's new Wi-Fi network.
    :param password: The password for the Tello's new Wi-Fi network.
    """
    # Create a Tello instance
    tello = Tello()

    try:
        print("Connecting to Tello's default Wi-Fi...")
        tello.connect()  # Connect to the Tello's default Wi-Fi network
        print("Successfully connected to Tello.")

        # Construct the AP configuration command
        ap_command = f"ap {ssid} {password}"
        print(f"Sending AP configuration command: {ap_command}")

        # Send the AP configuration command
        response = tello.send_control_command(ap_command)
        if response == "ok":
            print(f"The Tello is now set to AP mode with SSID='{ssid}' and PASSWORD='{password}'.")
        else:
            print(f"Command failed with response: {response}")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        tello.end()


if __name__ == "__main__":
    # Predefined SSID and Password for AP mode
    ap_ssid = "dlink7A56"  # Replace with your desired SSID
    ap_password = "83543906"  # Replace with your desired password

    # Set the Tello to AP mode with the given credentials
    set_tello_to_ap_mode(ap_ssid, ap_password)