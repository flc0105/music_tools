#!/usr/bin/env python3
import subprocess

subprocess.Popen('metaflac --remove-all --dont-use-padding *.flac', shell=True)
