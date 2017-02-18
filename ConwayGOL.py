import sys, argparse
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

ON = 255
OFF = 0
PERCON = 0.4
PERCOFF = 0.6
vals = [ON, OFF]

def randomGrid(N):
    """Returns a grid of NxN random values"""
    return np.random.choice(vals, N*N, p=[PERCON, PERCOFF]).reshape(N, N)

def addGlider(i, j, grid):
    """Adds a glider with top left cell at (i, j)"""
    glider = np.array([[0,  0,   255],
                      [255, 0,   255],
                      [0,   255, 255]])
    grid[i:i+3, j:j+3] = glider

def update(frameNum, img, grid, N):
    # Copy grid for 8 neighbors for calculation
    # go line by line
    newGrid = grid.copy()
    for i in range(N):
        for j in range(N):
            # Compute 8-neighbor sum using toroidal boundary conditions
            # x and y wrap around so the sim takes place on a toroidal surface
            total = int((grid[i,       (j-1)%N] + grid[(i),         (j+1)%N] +
                         grid[(i-1)%N,       j] + grid[(i+1)%N,         j] +
                         grid[(i-1)%N, (j-1)%N] + grid[(i-1)%N, (j + 1)%N] +
                         grid[(i+1)%N, (j-1)%N] + grid[(i+1)%N, (j+1)%N])/255)

            # Apply Conway's Rules
            if grid[i, j] == ON:
                if (total < 2) or (total > 3):
                    newGrid[i, j] = OFF
            else:
                if total == 3:
                    newGrid[i, j] = ON

    # Update Data
    img.set_data(newGrid)
    grid[:] = newGrid[:]
    return img

def main():
    # command line arguments are in sys.argv[1], sys.argv[2], ...
    # sys.argv[0] is the script name and can be ignored
    # parse arguments
    parser = argparse.ArgumentParser(description="Runs Conway's Game of Life simulation.")

    # add arguments
    parser.add_argument('--grid-size', dest='N',            required=False)
    parser.add_argument('--mov-file',  dest='movfile',      required=False)
    parser.add_argument('--interval',  dest='interval',     required=False)
    parser.add_argument('--glider',    action='store_true', required=False)
    parser.add_argument('--gosper',    action='store_true', required=False)
    args = parser.parse_args()

    # set grid size
    N = 100
    if args.N and int(args.N) > 8:
        N = int(args.N)

    # Set animation update interval
    updateInterval = 50
    if args.interval:
        updateInterval = int(args.interval)

    # Declare grid
    grid = np.array([])
    # Check if "glider" demo flag is called
    if args.glider:

        grid = np.zeros(N*N).reshape(N, N)
        addGlider(1, 1, grid)
    else:
        # Populate grid with random on/off
        grid = randomGrid(N)

    # Set up animation
    fig, ax = plt.subplots()
    img = ax.imshow(grid, interpolation='nearest')
    ani = animation.FuncAnimation(fig, update, fargs=(img, grid, N, ),
                                  frames=10,
                                  interval=updateInterval,
                                  save_count=50)
    # Number of frames?
    # Set output file
    if args.movfile:
        ani.save(args.movfile, fps=30, extra_args=['-vcodec', 'libx264'])

    plt.show()

if __name__ == '__main__':
    main()









