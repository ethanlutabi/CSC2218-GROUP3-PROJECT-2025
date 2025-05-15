#!/bin/bash
# Script to run tests with PYTHONPATH set to the project root

PYTHONPATH=. pytest "$@"
