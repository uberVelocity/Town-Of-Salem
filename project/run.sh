SCRIPT="/main.py"
FILE=$(pwd)$SCRIPT
RESULTS_NAME="/results"
RESULTS=$(pwd)$RESULTS_NAME
MAFIA="MAFIA WINS!"
MAFIA_WINS=0
TOWN_WINS=0
for (( i=1; i <=$1; i++ ))
do
    RESULT=$(python3 $FILE)
    if [ "$RESULT"="$MAFIA" ]; then
        ((MAFIA_WINS=MAFIA_WINS+1))
        printf "Mafia wins: %d" $MAFIA_WINS > $RESULTS
        printf "\nTown wins: %d\n" $TOWN_WINS >> $RESULTS
    else
        ((TOWN_WINS=TOWN_WINS+1))
        printf "Mafia wins: %d" $MAFIA_WINS > $RESULTS
        printf "\nTown wins: %d\n" $TOWN_WINS >> $RESULTS
    fi
    echo $i
done


