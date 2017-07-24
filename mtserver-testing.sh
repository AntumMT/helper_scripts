#!/bin/bash

# Launches the server using "testing" parameters

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

# Test game is named 'antum-testing'
## Symlink is located in /usr/share/minetest/games
## Links to /home/jordan/Development/Minetest/games/antum
GAME=antum-testing
GAME_ROOT="/home/jordan/Development/Minetest/games/antum"

# Test game uses port 30001
PORT="30001"

# Server settings
SERVER_ROOT="/home/jordan/Games/Minetest/server"
WORLD_ROOT="${SERVER_ROOT}/worlds"
WORLD_NAME="Antum_Testing"
DATA_ROOT="${GAME_ROOT}"

# Import common variables
. "${BINDIR}/minetest-common"

