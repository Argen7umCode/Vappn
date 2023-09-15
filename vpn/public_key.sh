#!/usr/bin/bash

VAR=$( echo $1 | wg pubkey )
echo $VAR