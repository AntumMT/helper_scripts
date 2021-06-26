#!/usr/bin/env python

# Updates server config (minetest.conf) from source file

# CC0 LICENSE BOILERPLATE
#
#  To the extent possible under law, the person who associated CC0 with
#  this file has waived all copyright and related or neighboring rights
#  to this file.
#
#  You should have received a copy of the CC0 legalcode along with this
#  work. If not, see <https://creativecommons.org/publicdomain/zero/1.0/>.


import codecs, os, sys

CFG_SOURCE = '{}/Games/Minetest/games/antum/minetest.conf.example'.format(os.getenv('HOME'))
CFG_TARGET = '{}/Games/Minetest/server/config/Antum/minetest.conf'.format(os.getenv('HOME'))

def message(mode, msg):
	sys.stdout.write('\n[{}] {}\n'.format(mode, msg))

def msgS(msg):
	message('MESSAGE', msg)

def msgW(msg):
	message('WARNING', msg)

def msgE(msg):
	message('ERROR', msg)


# Check for existing source configuration
if not os.path.isfile(CFG_SOURCE):
	msgE('Source configuration does not exits, exiting ...')
	print('\t{}'.format(CFG_SOURCE))
	sys.exit(1)
else:
	msgS('Found source configuration:\n\t{}'.format(CFG_SOURCE))

# Check for non-existing target configuration
CFG_TARGET_DIR = os.path.dirname(CFG_TARGET)
if not os.path.isdir(CFG_TARGET_DIR):
	msgW('Target configuration directory does not exist, a new directory will be created.\n\t{}'.format(CFG_TARGET_DIR))

	# Create the target directory
	os.makedirs(CFG_TARGET_DIR)

# Check for non-existing target configuration
if not os.path.isfile(CFG_TARGET):
	msgW('Target configuration file not found, a new file will be created:\n\t{}'.format(CFG_TARGET))

	# Create a new, empty configuration file
	CFG_TEXT = codecs.open(CFG_TARGET, 'wt')
	CFG_TEXT.close()

	if os.path.isfile(CFG_TARGET):
		msgS('Configuration file created.')
	else:
		msgE('Configuration file could not be created, please check the target directory:\n\t{}'.format(CFG_TARGET_DIR))
		sys.exit(1)

# Read source config
msgS('Reading source configuration file ...')

CFG_SRC_DATA = codecs.open(CFG_SOURCE, 'rt')
src_lines = CFG_SRC_DATA.read().split('\n')
CFG_SRC_DATA.close()

msgS('Reading target configuration file ...')

CFG_TGT_DATA = codecs.open(CFG_TARGET, 'rt')
tgt_lines = CFG_TGT_DATA.read().split('\n')
CFG_TGT_DATA.close()

src_lines_copy = tuple(src_lines)
# Clear the original list
src_lines = []

msgS('Comparing target against source configuration ...')

def targetContainsKey(line):
	if line in tgt_lines:
		return True

	else:
		src_key = line
		if '=' in src_key:
			src_key = src_key.split('=')[0].lstrip(' #\t').rstrip()

			for TLINE in tgt_lines:
				tgt_key = TLINE
				if '=' in tgt_key:
					tgt_key = tgt_key.split('=')[0].lstrip(' #\t').rstrip()

					if src_key == tgt_key:
						return True

	return False

l = 0
for LINE in src_lines_copy:
	l += 1

	# Comments are delimited by a hashtag followed with whitespace
	if LINE and '=' in LINE and not LINE.startswith('# ') and not LINE.startswith('#\t'):
		if not targetContainsKey(LINE):
			src_lines.append(LINE)

if src_lines:
	msgS('Writing new lines to target configuration ...')
	'''
	t_index = 0
	for LT in tgt_lines:
		# Skip empty lines
		if LT:
			key = LT.lstrip('#').split('=')[0].strip()

			s_index = 0
			s_removes = []
			for LS in src_lines:
				if key in LS:
					msgS('Not replacing old setting:\n\t{} -> {}'.format(LT, LS))
					#tgt_lines[t_index] = LS
					s_removes.append(s_index)

					break

				s_index += 1

			t_index += 1

			# Remove lines that are already in config with differenc value
			for INDEX in reversed(s_removes):
				src_lines.pop(INDEX)
	'''

	# Show message about new settings
	msgS('New settings:')
	for LS in src_lines:
		print('\t{}'.format(LS))

	tgt_text = '\n'.join(tgt_lines).strip(' \n\t')
	src_text = '\n'.join(src_lines).strip(' \n\t')

	CFG_TGT_DATA = codecs.open(CFG_TARGET, 'wt')
	CFG_TGT_DATA.write('\n'.join([tgt_text, '\n# ----- NEWLY ADDED -----\n', src_text]).strip() + '\n\n')
	CFG_TGT_DATA.close()

else:
	msgS('Target configuration is unchanged.')
