#!/usr/bin/env python3
import logging
import os
from dockerized.ui import cli

if __name__ == '__main__':
    logging.basicConfig(level=os.environ.get("LOGLEVEL", "CRITICAL"))
    cli.main()
