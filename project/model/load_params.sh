#!/bin/sh
LOC=$(pwd)
FILE=$LOC/params.py
if test -f "$FILE"; then
    rm $FILE
fi

printf "strategy_vote = '$1'\n" >> $FILE
printf "strategy_action = '$2'\n" >> $FILE
printf "infer = '$3'" >> $FILE