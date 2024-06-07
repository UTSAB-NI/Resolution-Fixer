import time
import win32api
import win32con

# Constants for display device state flags
DISPLAY_DEVICE_ACTIVE = 0x00000001
DISPLAY_DEVICE_PRIMARY_DEVICE = 0x00000004

def get_display_settings(device_name):
    return win32api.EnumDisplaySettings(device_name, win32con.ENUM_CURRENT_SETTINGS)

def set_display_settings(device_name, width, height, bits_per_pel, display_frequency):
    devmode = get_display_settings(device_name)
    devmode.PelsWidth = width
    devmode.PelsHeight = height
    devmode.BitsPerPel = bits_per_pel
    devmode.DisplayFrequency = display_frequency
    devmode.Fields = win32con.DM_PELSWIDTH | win32con.DM_PELSHEIGHT | win32con.DM_BITSPERPEL | win32con.DM_DISPLAYFREQUENCY
    win32api.ChangeDisplaySettingsEx(device_name, devmode, 0)

def find_secondary_display():
    i = 0
    while True:
        device = win32api.EnumDisplayDevices(None, i)
        if not device:
            break
        if device.StateFlags & DISPLAY_DEVICE_ACTIVE and not (device.StateFlags & DISPLAY_DEVICE_PRIMARY_DEVICE):
            return device.DeviceName
        i += 1
    return None

def main():
    # Find the secondary display
    secondary_display = find_secondary_display()
    if not secondary_display:
        print("No secondary display found.")
        return

    print(f"Secondary Display: {secondary_display}")
    
    # Save current display settings
    original_settings = get_display_settings(secondary_display)
    
    # Print original settings
    print(f"Original Resolution: {original_settings.PelsWidth}x{original_settings.PelsHeight}")
    
    # Define the new resolution settings
    new_width = 1680
    new_height = 1050
    new_bits_per_pel = original_settings.BitsPerPel
    new_display_frequency = original_settings.DisplayFrequency
    
    # Change to the new resolution
    set_display_settings(secondary_display, new_width, new_height, new_bits_per_pel, new_display_frequency)
    print(f"Changed Resolution to: {new_width}x{new_height}")
    
    # Wait for a few seconds (optional, for demonstration purposes)
    time.sleep(1)
    
    # Revert back to the original resolution
    set_display_settings(secondary_display, original_settings.PelsWidth, original_settings.PelsHeight, original_settings.BitsPerPel, original_settings.DisplayFrequency)
    print(f"Reverted Resolution to: {original_settings.PelsWidth}x{original_settings.PelsHeight}")

if __name__ == "__main__":
    main()
