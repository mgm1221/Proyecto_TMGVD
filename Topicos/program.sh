#!/bin/bash

# Path to your Python programs (adjust as needed)
program1="/Users/martingarces/Desktop/UdeC/2024-2/Topicos en manejos de grandes volumenes de datos/Proyecto_Semestral/spAPI2.py"
program2="/Users/martingarces/Desktop/UdeC/2024-2/Topicos en manejos de grandes volumenes de datos/Proyecto_Semestral/add_info_deezer.py"

# Python interpreter (use the correct python path)
python="/Users/martingarces/.pyenv/versions/3.13.0/bin/python3" # You can verify this path by running `which python3`

# Number of loops
loop_count=40

# Loop to run the programs
for ((i=1; i<=loop_count; i++))
do
    # Run the first program
    echo "Running program 1 (Spotify API), iteration $i..."
    $python "$program1"

    # Add a delay between executions
    sleep 300  # Adjust the time (in seconds) to your needs

    # Run the second program
    echo "Running program 2 (Deezer API), iteration $i..."
    $python "$program2"

    # Add a delay between executions
    sleep 750  # Adjust the time (in seconds) to your needs
done

echo "All loops completed."
