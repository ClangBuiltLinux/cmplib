#!/usr/bin/env python

from argparse import ArgumentParser
from depends import get_undefined_symbols
from provides import get_symbols
import sys

def check_compat(dependent, existing, new):
  undef = set(get_undefined_symbols(dependent))
  old_def = set(get_symbols(existing))
  new_def = set(get_symbols(new))
  dependencies_on_old = undef & old_def
  unsatisfied_dependencies = dependencies_on_old - new_def

  print(f"{existing} provides the following symbols (used by {dependent}) BUT ARE MISSING from {new}:")
  for unsatisfied_dependency in unsatisfied_dependencies:
    print(unsatisfied_dependency)

  return len(unsatisfied_dependencies)


if __name__ == "__main__":
  parser = ArgumentParser(description="check compatibility between depended on symbols from 2 libraries")
  parser.add_argument('dependent')
  parser.add_argument('existing')
  parser.add_argument('new')
  args = parser.parse_args()
  if check_compat(args.dependent, args.existing, args.new) != 0:
    sys.exit(1)
