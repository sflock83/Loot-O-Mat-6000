import os
import subprocess
import time

import pyautogui
import pydirectinput
import requests


def locate_image(image_path, region=tuple(int, int, int, int) | None):
    # move the mouse to the upper right corner 10% shy of the screen edge so menu items arent obstructed
    screenWidth, screenHeight = pyautogui.size()
    pyautogui.moveTo(screenWidth * 0.9, screenHeight * 0.1, duration=0.15)
    # pyautogui.locateOnScreen(image_path, confidence=0.7) thorws an exceptio if the image is not found
    try:
        # locate the image on the screen
        location = pyautogui.locateOnScreen(image_path, confidence=0.7, region=region)
        # center the location of the image
        location = pyautogui.center(location)
        imgFound = True
    except Exception:
        imgFound = False
        location = None
    # return if the image was found and the location of the image
    return imgFound, location


def verify_loot():
    # verify if the loot on screen matches an item in the loot list
    # ./images/loot_list/ contains images of all the loot items on the loot list

    # get the list of all the loot items in the loot_list directory
    loot_list = os.listdir("./images/loot_list/")
    # iterate through the loot list
    for loot in loot_list:
        # locate the image of the loot item on the screen
        imgFound, _ = locate_image(f"./images/loot_list/{loot}")
        if imgFound:
            # return the name of the loot item if the image is found
            return True, loot
    # return False if no loot item is found
    return False, None


def move_character():
    # move the character straight forward for 3.85 seconds until chest is reached. adjust time if needed
    time.sleep(0.25)
    pydirectinput.keyDown("w")
    time.sleep(3.85)
    pydirectinput.keyUp("w")
    # open the chest by pressing 'e' key and wait for 0.5 seconds for the chest to open
    pydirectinput.press("e")
    time.sleep(0.5)
    # check if a legendary item is found by locating the image Loot_Legendary.png
    imgFound, _ = locate_image("./images/Loot_Legendary.png")
    if imgFound:
        print("Looted a legendary item.")
        pydirectinput.press("f")
        return 1
    else:
        pydirectinput.press("esc")
        return 0


def Reload_Game():
    print("Reload Game...")
    imgReturnToMainMenu = "./images/1_Return_To_Main_Menu.png"
    imgPlay = "./images/2_Play_Game.png"
    imgPrivate = "./images/3_Private.png"
    imgPlaySave = "./images/5_Play_Save.png"
    imgList = [imgReturnToMainMenu, imgPlay, imgPrivate, imgPlaySave]
    imgSelected = 0
    repeat = True
    emergencyExit = 0
    # press 'esc' key to open menu
    time.sleep(0.25)
    pydirectinput.press("esc")
    while repeat:
        emergencyExit += 1
        if emergencyExit > 15:
            print("Emergency Exit: Exiting the script")
            repeat = False
        imgFound, location = locate_image(imgList[imgSelected])
        if imgFound:
            pyautogui.moveTo(location, duration=0.15)
            time.sleep(0.5)
            pyautogui.click(button="left")
            time.sleep(0.5)
            # print(f"Image {imgList[imgSelected]} found. imgSelected: {imgSelected}")
            imgSelected += 1

            if imgSelected == len(imgList):
                repeat = False
            # else:
            #    print(
            #        f"Looking for Image {imgList[imgSelected]} now. imgSelected: {imgSelected}"
            #    )
    # while not imgFound locate image 6_Healthbar.png
    imgFound = False
    while not imgFound:
        emergencyExit += 1
        time.sleep(1)
        imgFound, location = locate_image("./images/6_Healthbar.png")
        if imgFound:
            # print("Savegame loaded successfully. Moving on.")
            break
        if emergencyExit > 15:
            print("Emergency Exit: Exiting the script")
            imgFound = True
            break


def ocr(image):
    if ".png" in image:
        image = '"' + abspath(image) + '"'
        ofname = image.replace(".png", "")
        cmd = (
            "C:\\Program Files\\Tesseract-OCR\\tesseract.exe "
            + image
            + " "
            + ofname
            + " -c page_separator="
            " --psm 4 -l eng txt"
        )
        rc = subprocess.run(cmd, shell=True).returncode
        txtfname = ofname.strip('"') + ".txt"
        with open(txtfname, "rt", encoding="utf-8-sig", errors="ignore") as txtfile:
            pyperclip.copy(txtfile.read())


def send_notification(attachment=None, capacity=None):
    # send a notification to the user using pushover.net API
    # pushover.net API requires a user key and an application key
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
    )
    print(r.text)


def main():
    # check if there are any items in the loot list
    if not os.listdir("./images/loot_list/"):
        print("No items in the loot list. Exiting the script.")
        exit(0)
    # pyautogui failsafe to stop the script by moving the mouse to the upper left corner of the screen
    pyautogui.FAILSAFE = True
    # set foundItems to 0 at the start of the script
    foundItems = 0
    # ask the user to provide current inventory space repeatedly until a valid input (>=1 integer and <=48) is provided
    while True:
        inventorySpace = input("Enter the current inventory space: ")
        try:
            inventorySpace = int(inventorySpace)
            if 1 <= inventorySpace <= 48:
                break
            else:
                print("Invalid input. Please enter a number between 1 and 48.")
        except ValueError:
            print("Invalid input. Please enter a number between 1 and 48.")

    # wait for 5 seconds
    for i in range(5, 0, -1):
        print(f"Waiting for {i} seconds")
        time.sleep(1)
    while foundItems < inventorySpace:
        print(f"Starting loop {i+1}")
        Reload_Game()
        foundItems += move_character()
        print(f"Ending loop {i+1}")
        print("Exiting the script.")
    if foundItems > 0:
        print("Found a legendary item.")
    exit(0)


if __name__ == "__main__":
    # main()
    send_notification("Epic Item")

    # pusherover.net API send notification per found item
