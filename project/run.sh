MAFIA="MAFIA WINS!"
MAFIA_WINS=0
TOWN_WINS=0
for (( i=1; i <=$1; i++ ))
do
    RESULT=$(python3 /home/merkel/Documents/University/lamas/Town-Of-Salem/project/main.py)
    if [ "$RESULT"="$MAFIA" ]; then
        ((MAFIA_WINS=MAFIA_WINS+1))
        printf "Mafia wins: %d" $MAFIA_WINS > /home/merkel/Documents/University/lamas/Town-Of-Salem/project/results
        printf "\nTown wins: %d\n" $TOWN_WINS >> /home/merkel/Documents/University/lamas/Town-Of-Salem/project/results
    else
        ((TOWN_WINS=TOWN_WINS+1))
        printf "Mafia wins: %d" $MAFIA_WINS > /home/merkel/Documents/University/lamas/Town-Of-Salem/project/results
        printf "\nTown wins: %d\n" $TOWN_WINS >> /home/merkel/Documents/University/lamas/Town-Of-Salem/project/results
    fi
    echo $i
done


