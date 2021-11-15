
import unittest
import requests
import json
import sys
import os
import errno

test_results = '.\\test_results.txt'
website = "http://192.168.50.142"

class utilities():
    def logMessage(self, message):
        test_results_file = open(test_results, "a")  # append mode
        test_results_file.write(str(message) +"\n")
        test_results_file.close()
    def logger(self, message):
        test_results_file = open(test_results, "a")  # append mode
        test_results_file.write(" \t..." +str(message) + "\n")
        test_results_file.close()
    def server(self):
        return website
    def test_results_file(self):
        return test_results