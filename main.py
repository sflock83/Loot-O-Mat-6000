import os
import time
import pyautogui
import pydirectinput
import requests

"""
This script automates the process of looting legendary items in the game Enshrouded.

The script uses the pyautogui, pydirectinput, and requests libraries.

The script locates an image on the screen, 
verifies if the loot on the screen matches an item in the loot list,
and moves the character forward and interacts with a chest.

The script is not currently used in the main script.

The script can be run from the command line.

Example:
    $ python main.py

"""



def locate_image(image_path: str, region: tuple[int, int, int, int] | None = None) -> tuple[bool, tuple[int, int] | None]:
    """
    Locates an image on the screen.

    Args:
        image_path (str): The path to the image file.
        region (tuple[int, int, int, int] | None):
            The region of the screen to search for the image. Defaults to None.

    Returns:
        tuple[bool, tuple[int, int] | None]:
        A tuple containing a boolean indicating if the image was found and the location of the image.
    """
    screen_width, screen_height = pyautogui.size()
    pyautogui.moveTo(screen_width * 0.9, screen_height * 0.1, duration=0.15)
    try:
        location = pyautogui.locateOnScreen(image_path, confidence=0.7, region=region)
        location = pyautogui.center(location)
        img_found = True
    except Exception:
        img_found = False
        location = None
    return img_found, location


def verify_loot() -> tuple[bool, str | None]:
    """
    Verifies if the loot on the screen matches an item in the loot list.

    Returns:
        tuple[bool, str | None]: A tuple containing a boolean indicating
        if a loot item was found and the name of the loot item.
    """
    loot_list = os.listdir("./images/loot_list/")
    for loot in loot_list:
        img_found, _ = locate_image(f"./images/loot_list/{loot}")
        if img_found:
            return True, loot
    return False, None


def move_character() -> int:
    """
    Moves the character forward and interacts with a chest.

    Returns:
        int: The number of legendary items looted (0 or 1).
    """
    time.sleep(0.25)
    pydirectinput.keyDown("w")
    time.sleep(3.85)
    pydirectinput.keyUp("w")
    pydirectinput.press("e")
    time.sleep(0.5)
    img_found, _ = locate_image("./images/Loot_Legendary.png")
    if img_found:
        print("Looted a legendary item.")
        pydirectinput.press("f")
        return 1
    else:
        pydirectinput.press("esc")
        return 0


def reload_game() -> None:
    """
    Reloads the game and navigates through the main menu.

    This function is not currently used in the main script.
    """
    print("Reload Game...")
    img_return_to_main_menu = "./images/1_Return_To_Main_Menu.png"
    img_play = "./images/2_Play_Game.png"
    img_private = "./images/3_Private.png"
    img_play_save = "./images/5_Play_Save.png"
    img_list = [img_return_to_main_menu, img_play, img_private, img_play_save]
    img_selected = 0
    repeat = True
    emergency_exit = 0
    time.sleep(0.25)
    pydirectinput.press("esc")
    while repeat:
        emergency_exit += 1
        if emergency_exit > 15:
            print("Emergency Exit: Exiting the script")
            repeat = False
        img_found, location = locate_image(img_list[img_selected])
        if img_found:
            pyautogui.moveTo(location, duration=0.15)
            time.sleep(0.5)
            pyautogui.click(button="left")
            time.sleep(0.5)
            img_selected += 1
            if img_selected == len(img_list):
                repeat = False
    img_found = False
    while not img_found:
        emergency_exit += 1
        time.sleep(1)
        img_found, location = locate_image("./images/6_Healthbar.png")
        if img_found:
            break
        if emergency_exit > 15:
            print("Emergency Exit: Exiting the script")
            img_found = True
            break


def send_notification(attachment: str = None, capacity: int = None) -> None:
    """
    Sends a notification to the user using pushover.net API.

    Args:
        attachment (str): The path to the attachment image file. Defaults to None.
        capacity (int): The capacity of the inventory. Defaults to None.
    """
    user_key = "um9pyotuq7gu327x9632hyobx5dx4t"
    app_key = "ab7uhpcdxziujwj27pnet5dw4ddayv"
    message = "Item found."
    attachment = "./images/LootPurple.png"
    r = requests.post(
        "https://api.pushover.net/1/messages.json",
        data={
            "user": user_key,
            "token": app_key,
            "message": message,
        },
        files={"attachment": ("image.png", open(attachment, "rb"), "image/png")},
        timeout=15
    )
    print(r.text)


def main() -> None:
    """
    The main function of the script.

    This function is currently not called in the script.
    """
    if not os.listdir("./images/loot_list/"):
        print("No items in the loot list. Exiting the script.")
        exit(0)
    pyautogui.FAILSAFE = True
    found_items = 0
    while True:
        inventory_space = input("Enter the current inventory space: ")
        try:
            inventory_space = int(inventory_space)
            if 1 <= inventory_space <= 48:
                break
            else:
                print("Invalid input. Please enter a number between 1 and 48.")
        except ValueError:
            print("Invalid input. Please enter a number between 1 and 48.")
    for i in range(5, 0, -1):
        print(f"Waiting for {i} seconds")
        time.sleep(1)
    while found_items < inventory_space:
        print(f"Starting loop {i+1}")
        reload_game()
        found_items += move_character()
        print(f"Ending loop {i+1}")
        print("Exiting the script.")
    if found_items > 0:
        print("Found a legendary item.")
    exit(0)


if __name__ == "__main__":
    main()
