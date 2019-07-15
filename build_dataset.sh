
# Default value: Do not create evaluation set.
CREATE_EVAL=false

# Check if PHP is installed
if ! [ -x "$(command -v php)" ]; then
  echo 'Error: PHP not found. Please install an up-to-date version of php.' >&2
  exit 1
fi


for arg in "$@"
do
    case $arg in
        -n=*|--numcases=*)
        NUM_SAMPLES="${arg#*=}"
        shift # Remove --initialize from processing
        ;;
        -v|--valset)
        CREATE_EVAL=true
        shift # Remove --cache= from processing
        ;;
        -s=*|--trainsplit=*)
        TRAIN_SPLIT="${arg#*=}"
        shift # Remove argument value from processing
        ;;
        *)
        OTHER_ARGUMENTS+=("$1")
        shift # Remove generic argument from processing
        ;;
    esac
done

TEST_SPLIT=$((100-$TRAIN_SPLIT))
TRAIN_SIZE=$(($NUM_SAMPLES*$TRAIN_SPLIT/100))
TEST_SIZE=$(($NUM_SAMPLES-$TRAIN_SIZE))

echo "Number of samples to create:"
echo $NUM_SAMPLES
echo "Dataset split (Train:Test)"
echo "$TRAIN_SPLIT:$TEST_SPLIT"
echo "Creating validation set:"
echo $CREATE_EVAL
echo "Size of Training set:"
echo $TRAIN_SIZE
echo "Size of Test set:"
echo $TEST_SIZE

mkdir -p dataset
mkdir -p dataset/test
mkdir -p dataset/train


# Creating Datasets

echo "Create training set..."
i=1
while [ $i -le $TRAIN_SIZE ]
do
	php gotcha.php -o ./dataset/train -b blank.png - m 6 -x 7 &> ./php.log
	i=$[$i+1]
done
echo "Done."



echo "Create test set..."
i=1
while [ $i -le $TEST_SIZE ]
do
	php gotcha.php -o ./dataset/test -b blank.png - m 6 -x 7 &> ./php.log
	i=$[$i+1]
done
echo "Done."


if [ $CREATE_EVAL = true ] ; then
	echo "Create validation set of size $TEST_SIZE ..."
    mkdir -p dataset/val
	i=1
	while [ $i -le $TEST_SIZE ]
	do
		php gotcha.php -o ./dataset/val -b blank.png - m 6 -x 7 &> ./php.log
		i=$[$i+1]
	done
	echo "Done."
fi
echo "Generation of Dataset complete. Examples can be found in ./dataset/"