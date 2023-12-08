#!/usr/bin/env python

import sys
from argparse import ArgumentParser
from elftools.elf.elffile import ELFFile
from elftools.common.exceptions import ELFError

import io
sys.path.insert(0, './ar')
from ar import Archive

def should_print(symbol):
  bind = symbol.entry.st_info.bind
  visibility = symbol.entry.st_other.visibility
  index = symbol.entry.st_shndx

  # TODO: do we need to handle binding other than local, global, or weak?
  # Error loundly if so.
  assert bind == 'STB_GLOBAL' or bind == 'STB_WEAK' or bind == 'STB_LOCAL'
  # TODO: do we need to handle non-default visibility?
  # Error loundly if so.
  if visibility == 'STV_HIDDEN':
    return False
  assert visibility == 'STV_DEFAULT'

  if index == 'SHN_ABS' or index == 'SHN_UNDEF':
    return False

  if symbol.name == '':
    return False

  return bind == 'STB_GLOBAL' or bind == 'STB_WEAK'


def foo(elf_file):
  sym_sec = elf_file.get_section_by_name('.dynsym') or elf_file.get_section_by_name('.symtab')
  if sym_sec == None:
    print("no .dynsym or .symtab found", file=sys.stderr)
    sys.exit(1)
  for symbol in sym_sec.iter_symbols():
    if should_print(symbol):
      yield symbol.name


def get_symbols(input_file):
    with open(input_file, 'rb') as f:
      elf_files = []

      try:
        elf_files.append(ELFFile(f))
        elf_file = ELFFile(f)
      except ELFError as e:
        print("non elf file", file=sys.stderr)

        f.seek(0)
        archive = Archive(f)

        for entry in archive:
          x = archive.open(entry, mode='b')

          try:
            elf_files.append(ELFFile(x))
          except ELFError as e:
            continue
      for elf_file in elf_files:
        yield from foo(elf_file)


if __name__ == "__main__":
  parser = ArgumentParser(description="dump external symbols with visible linkage")
  parser.add_argument('input_file')
  args = parser.parse_args()
  # TODO: since symbols are versioned, this will produce duplicates. Consumers
  # of this output can filter these bypiping output into `| sort -u` though
  # perhaps the version info is helpful.
  for sym in get_symbols(args.input_file):
    print(sym)
