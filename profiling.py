import subprocess

# Run cProfile on your Python application
cprofiler_command = "python -m cProfile -o app.prof app.py"
subprocess.call(cprofiler_command, shell=True)

# Run SnakeViz to visualize the profile data
snakeviz_command = "snakeviz app.prof"
subprocess.call(snakeviz_command, shell=True)