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


def show_usage():
	usage = '\nUsage:\n\t{} [-h|-s] <source> <target>' \
		+ '\n\nOptions:' \
		+ '\n\t-t  Show this help message.' \
		+ '\n\t-s  Denotes that source file is settingtypes.txt formatted.'
	print(usage.format(os.path.basename(sys.argv[0])))

def message(mode, msg):
	sys.stdout.write('\n[{}] {}\n'.format(mode, msg))

def msgS(msg):
	message('MESSAGE', msg)

def msgW(msg):
	message('WARNING', msg)

def msgE(msg):
	message('ERROR', msg)

args = sys.argv[1:]

if len(sys.argv) < 2:
	msgE("Not enough arguments")
	show_usage()
	sys.exit(1)

if "-h" in args:
	show_usage()
	sys.exit(0)

settingtypes = False
if args[0] == "-s":
	settingtypes = True
	args.pop(0)

CFG_SOURCE = args[0]
CFG_TARGET = args[1]


# Check for existing source configuration
if not os.path.isfile(CFG_SOURCE):
	msgE('Source configuration does not exist, exiting ...')
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
	CFG_TEXT = codecs.open(CFG_TARGET, 'w', encoding='utf8')
	CFG_TEXT.close()

	if os.path.isfile(CFG_TARGET):
		msgS('Configuration file created.')
	else:
		msgE('Configuration file could not be created, please check the target directory:\n\t{}'.format(CFG_TARGET_DIR))
		sys.exit(1)

# Read source config
msgS('Reading source configuration file ...')

CFG_SRC_DATA = codecs.open(CFG_SOURCE, 'r', encoding='utf8')
src_lines = CFG_SRC_DATA.read().split('\n')
CFG_SRC_DATA.close()

msgS('Reading target configuration file ...')

CFG_TGT_DATA = codecs.open(CFG_TARGET, 'r', encoding='utf8')
tgt_lines = CFG_TGT_DATA.read().split('\n')
CFG_TGT_DATA.close()

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

deprecated = []
for line in tgt_lines:
	if '=' in line:
		key = line.split('=')[0].lstrip(' \t#').rstrip()
		if not key in deprecated:
			deprecated.append(key)

def updateDeprecated(line):
	key = line.lstrip('#').split('=')[0].strip()

	while key in deprecated:
		deprecated.pop(deprecated.index(key))

def parseConf(lines):
	msgS('Parsing config formatted source')

	ret = []

	for LINE in lines:
		# Comments are delimited by a hashtag followed with whitespace
		if LINE and '=' in LINE and not LINE.startswith('# ') and not LINE.startswith('#\t') \
				and not LINE.startswith('##'):
			if not targetContainsKey(LINE):
				ret.append(LINE)

			updateDeprecated(LINE)

	return tuple(ret)

def parseSetTypes(lines):
	msgS('Parsing settingtypes formatted source')

	ret = []

	for LINE in lines:
		LINE = LINE.strip()
		if len(LINE) > 0 and not LINE.startswith('#') and not LINE.startswith('['):
			key = LINE.split(' ')[0]
			value = LINE.split(') ')[-1].split(' ')
			if len(value) < 2:
				if value[0] == "string":
					value = ""
				else:
					msgW('Missing value for: {}'.format(key))
					continue
			else:
				value = value[1]

			new_line = '#{} = {}'.format(key, value)
			if not targetContainsKey(key):
				ret.append(new_line)

			updateDeprecated(new_line)

	return tuple(ret)

if settingtypes:
	src_lines = parseSetTypes(src_lines)
else:
	src_lines = parseConf(src_lines)


if deprecated:
	msgS('{} potentially deprecated settings:'.format(len(deprecated)))
	for set in deprecated:
		print('  {}'.format(set))


if src_lines:
	msgS('Writing new lines to target configuration ...')

	# Show message about new settings
	msgS('New settings:')
	for LS in src_lines:
		print('\t{}'.format(LS))

	tgt_text = '\n'.join(tgt_lines).strip(' \n\t')
	src_text = '\n'.join(src_lines).strip(' \n\t')

	CFG_TGT_DATA = codecs.open(CFG_TARGET, 'w', encoding='utf8')
	CFG_TGT_DATA.write('\n'.join([tgt_text, '\n# ----- NEWLY ADDED -----\n', src_text]).strip() + '\n')
	CFG_TGT_DATA.close()

else:
	msgS('Target configuration is unchanged.')
