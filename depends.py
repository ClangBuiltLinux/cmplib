#!/usr/bin/env python

from argparse import ArgumentParser
from elftools.elf.elffile import ELFFile

def should_print(symbol):
  index = symbol.entry.st_shndx

  if symbol.name == '':
    return False
  if index != 'SHN_UNDEF':
    return False

  return True


def get_undefined_symbols(input_file):
  with open(input_file, 'rb') as f:
    elf_file = ELFFile(f)

    dynsym_sec = elf_file.get_section_by_name('.dynsym')
    if dynsym_sec != None:
      for symbol in dynsym_sec.iter_symbols():
        if should_print(symbol):
          # print(symbol.name, symbol.entry)
          yield symbol.name

    symtab = elf_file.get_section_by_name('.symtab')
    if symtab != None:
      for symbol in symtab.iter_symbols():
        yield symbol.name

if __name__ == "__main__":
  parser = ArgumentParser(description="dump undefined symbols")
  parser.add_argument('input_file')
  args = parser.parse_args()
  for sym in get_undefined_symbols(args.input_file):
    print(sym)
