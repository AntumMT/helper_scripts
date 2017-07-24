#!/bin/bash

# Launches the server using "main" parameters

# CC0 LICENSE BOILERPLATE
#
#  To the extent possible under law, the person who associated CC0 with
#  this file has waived all copyright and related or neighboring rights
#  to this file.
#
#  You should have received a copy of the CC0 legalcode along with this
#  work. If not, see <https://creativecommons.org/publicdomain/zero/1.0/>.


# Directory where this script & support scripts are located
BINDIR=$(dirname $0)

# Main game is named 'antum':
## Symlink is located in /usr/share/minetest/games
## Links to /home/jordan/Games/Minetest/games/antum
GAME=antum
GAME_ROOT="/home/jordan/Games/Minetest/games/antum"

# Main game uses port 30000
PORT="30000"

# Server settings
SERVER_ROOT="/home/jordan/Games/Minetest/server"
WORLD_ROOT="${SERVER_ROOT}/worlds"
WORLD_NAME="Antum"
DATA_ROOT="${SERVER_ROOT}/config/Antum"

# Check for new setting values to add to configuration
mtserver-update-config

# Import common variables & execute server
. "${BINDIR}/minetest-common"

echo -e "\nExit status: $?\n"

# Run a server backup after shutdown
. "${BINDIR}/mtserver-backup"
