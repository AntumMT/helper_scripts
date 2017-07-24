#!/bin/bash

# Backs up server (world) data to a local directory

# CC0 LICENSE BOILERPLATE
#
#  To the extent possible under law, the person who associated CC0 with
#  this file has waived all copyright and related or neighboring rights
#  to this file.
#
#  You should have received a copy of the CC0 legalcode along with this
#  work. If not, see <https://creativecommons.org/publicdomain/zero/1.0/>.


printf "\n\nRunning server backup ...\n"
printf "\nChecking for world data ..."

if [ -z ${WORLD_NAME+x} ]; then
    WORLD_NAME="Antum"
fi

if [ -z ${WORLD+x} ]; then
    SERVER_ROOT="/home/jordan/Games/Minetest/server"
    WORLD_ROOT="${SERVER_ROOT}/worlds"
    WORLD="${WORLD_ROOT}/${WORLD_NAME}"
fi

if [ -d "${WORLD}" ]; then
    printf "\t${WORLD}\n"
else
    printf "\tNOT FOUND!\n"
    exit 1
fi


BACKUP_DIR="/home/jordan/Backup/Minetest"
DATE=`show-date`
TARGET_NAME="minetest-server-antum_${DATE}"
TARGET_DIR="${BACKUP_DIR}/${TARGET_NAME}"
LOG="${BACKUP_DIR}/minetest-backup.log"

if [ -e "${TARGET_DIR}" ]; then
	echo "BACKUP ERROR: Backup already exists: ${TARGET_DIR}";
	exit 1;
fi

if [ ! -d "${TARGET_DIR}" ]; then
	mkdir -vp "${TARGET_DIR}";
fi

echo -e "\n\n\n---------------- `show-date` ----------------\n" >> "${LOG}"
cp -vRf "${WORLD}" "${TARGET_DIR}" >> "${LOG}"

echo "Compressing backup ..."
cd "${BACKUP_DIR}"
tar -vcJf "${TARGET_NAME}.tar.xz" "${TARGET_NAME}"

TAR_INFO=`file "${TARGET_NAME}.tar.xz"`

if [ $? -gt 0 ]; then
	echo "BACKUP ERROR: ${TARGET_NAME}.tar.xz archive was not created";
	exit 1;
fi

echo -e "\nCreated archive:\n${TAR_INFO}\n" >> "${LOG}"

echo "Deleting temp directory ..."
rm -vrf "${TARGET_DIR}"

echo "Backup complete"

