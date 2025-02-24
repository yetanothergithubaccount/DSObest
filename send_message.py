#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Send a message

@author: solveigh
"""

debug = False


def text(message):
  try:
    msg = "Send message " + str(message) + " synchronously..."
    if debug:
      print(msg)

    # TODO implement this on your own

  except Exception as e:
    print(e)
