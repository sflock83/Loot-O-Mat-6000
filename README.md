# Loot-O-Mat-6000

Welcome to the Loot-O-Mat-6000 repository! This is a project that aims to create an auto-looter for the game Enshrouded.

## Features

- Asks player for their current inventory capacity
- Automatically exits back to the games main menu using image recognition.
- Loads back into the last save and walks straight forward from the spawn point which you should locate directly south from a loot chest.
- Opens the chest and decides to loot or not bases on image recognition. (Default: only Legendary Items. Rarity Icons must be enabled.)
- Repeats the process until inventory capacity is reached.
- Failsafe exit the script by bringin your mouse into the top left corner.

## Installation

To use the Loot-O-Mat-6000, follow these steps:

1. Clone this repository to your local machine.
2. Install the required dependencies by running the following command:

    ```bash
    $ pip install -r requirements.txt
    ```

## Usage

Either provide pictures of your wanted Items in loot_list folder or default which is legendary only loot.
Start Enshrouded, run the script, enter the amount of free slot in your inventory and go do something usefull.
