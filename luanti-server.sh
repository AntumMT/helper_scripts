#!/usr/bin/env bash

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
BINDIR="$(dirname $0)"
cd "${BINDIR}"
BINDIR=$(pwd)

# Main game is named 'antum':
GAME="antum"
GAME_ROOT="~/Development/Luanti/games/antum"

# Main game uses port 30000
PORT="30000"

# Server settings
WORLD_NAME="Antum"

# Check for new setting values to add to configuration
"${BINDIR}/luanti-server-update-config.py"

# Import common variables & execute server
. "${BINDIR}/luanti-common"

echo -e "\nExit status: $?\n"

# Run a server backup after shutdown
. "${BINDIR}/luanti-server-backup.sh"
