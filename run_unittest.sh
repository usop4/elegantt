
echo "usage:"
echo " run_unittest.sh           # all unittest"
echo " run_unittest.sh --simple  # simple check only"
echo " run_unittest.sh --install # install and test"
echo ""

if [ "$1" = "--install" ]; then
    pip3 uninstall elegantt -y
    pip3 install .
    echo ""
fi

cd elegantt/tests

if [ "$1" = "--simple" ]; then
    #python3 -m unittest test_simple.TestSimple
    pytest test_simple.py
else
    #python3 -m unittest
    pytest
fi



