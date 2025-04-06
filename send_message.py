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
    # TODO implement your own
  except Exception as e:
    print(e)

def image(path_name):
  try:
    msg = "Send image " + str(path_name) + " synchronously..."
    if debug:
      print(msg)
    # TODO implement your own
  except Exception as e:
    print(e)

def file(file_name):
  try:
    if debug:
      print("Send file: ")
      print(file_name)
    # TODO implement your own
  except Exception as e:
    print(e)
