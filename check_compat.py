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

  for unsatisfied_dependency in unsatisfied_dependencies:
    yield unsatisfied_dependency


if __name__ == "__main__":
  parser = ArgumentParser(description="check compatibility between depended on symbols from 2 libraries")
  parser.add_argument('dependent')
  parser.add_argument('existing')
  parser.add_argument('new')
  args = parser.parse_args()

  print(f"{args.existing} provides the following symbols (used by "
        f"{args.dependent}) BUT ARE MISSING from {args.new}:")
  for sym in check_compat(args.dependent, args.existing, args.new):
    print(sym)
