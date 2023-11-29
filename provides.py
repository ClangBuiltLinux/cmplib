#!/usr/bin/env python

import sys
from argparse import ArgumentParser
from elftools.elf.elffile import ELFFile
from elftools.common.exceptions import ELFError

def should_print(symbol):
  bind = symbol.entry.st_info.bind
  visibility = symbol.entry.st_other.visibility
  index = symbol.entry.st_shndx

  # TODO: do we need to handle binding other than local, global, or weak?
  # Error loundly if so.
  assert bind == 'STB_GLOBAL' or bind == 'STB_WEAK' or bind == 'STB_LOCAL'
  # TODO: do we need to handle non-default visibility?
  # Error loundly if so.
  assert visibility == 'STV_DEFAULT'

  if index == 'SHN_ABS' or index == 'SHN_UNDEF':
    return False

  if symbol.name == '':
    return False

  return bind == 'STB_GLOBAL' or bind == 'STB_WEAK'

def get_symbols(input_file):
    with open(input_file, 'rb') as f:

      try:
        elf_file = ELFFile(f)
      except ELFError as e:
        print("non elf file", file=sys.stderr)
        sys.exit(1)

      dynsym_sec = elf_file.get_section_by_name('.dynsym')
      for symbol in dynsym_sec.iter_symbols():
        if should_print(symbol):
          # print(symbol.name, symbol.entry)
          yield symbol.name

if __name__ == "__main__":
  parser = ArgumentParser(description="dump external symbols with visible linkage")
  parser.add_argument('input_file')
  args = parser.parse_args()
  # TODO: since symbols are versioned, this will produce duplicates. Consumers
  # of this output can filter these bypiping output into `| sort -u` though
  # perhaps the version info is helpful.
  for sym in get_symbols(args.input_file):
    print(sym)
