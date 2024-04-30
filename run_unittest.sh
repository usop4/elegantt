
if [ "$1" = "--install" ]; then
    pip3 uninstall elegantt -y
    pip3 install .
    echo ""
else
    echo "usage:"
    echo " run_unittest.sh           # test only"
    echo " run_unittest.sh --install # install and test"
    echo ""
fi

cd elegantt/tests
python3 -m unittest
