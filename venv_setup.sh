if [ -d "venv" ]; then
    echo "Activating virtual environment..."
    source venv/bin/activate
else
    echo "venv directory not found!"
    echo "Creating venv ..."
    mkdir venv
    virtualenv venv

    if [ -d "venv" ]; then
        echo "Activating virtual environment..."    
        source venv/bin/activate
    else
        echo "Failed to make venv directory"
    fi
fi
