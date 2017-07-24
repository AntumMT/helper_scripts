#!/bin/bash

# Clears the local Minetest cache directory

# CC0 LICENSE BOILERPLATE
#
#  To the extent possible under law, the person who associated CC0 with
#  this file has waived all copyright and related or neighboring rights
#  to this file.
#
#  You should have received a copy of the CC0 legalcode along with this
#  work. If not, see <https://creativecommons.org/publicdomain/zero/1.0/>.


CACHEDIR=${HOME}/.cache/minetest

rm -vrf "${CACHEDIR}"
