# Check if PHP is installed
# Adapted from the following StackOverflow response: https://stackoverflow.com/a/26759734
if ! [ -x "$(command -v php)" ]; then
  echo 'Error: PHP not found. Please install an up-to-date version of php.' >&2
  exit 1
fi


# Thanks to https://pretzelhands.com/posts/command-line-flags
for arg in "$@"
do
    case $arg in
        -n=*|--numcases=*)
        NUM_SAMPLES="${arg#*=}"
        shift # Remove --initialize from processing
        ;;
        OTHER_ARGUMENTS+=("$1")
        shift # Remove generic argument from processing
        ;;
    esac
done

echo "Number of samples to create:"
echo $NUM_SAMPLES

mkdir -p dataset

# Creating Datasets

echo "Creating dataset..."
i=1
while [ $i -le $TRAIN_SIZE ]
do
	php gotcha.php -o ./dataset/ -b blank.png - m 6 -x 7 &> ./php.log
	i=$[$i+1]
done
echo "Done."

echo "Generation of Dataset complete. Examples can be found in ./dataset/"