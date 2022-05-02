# !FINISH BY MONDAY
import copy

# We have a gray scale image with size of (W, H, 1), which is split into several pieces. Those split
# lines or curves are all 1s, while the rest of the image are all 0s. Implement a function to label
# those split regions, which means all four-way connects 0s are relabeled as a same number (>1)
# and all unconnected regions should not have same id. For example, in python if we have an
# input image like              # Your output should be like:
# [0, 0, 1, 0, 0]               # [2, 2, 1, 3, 3]
# [0, 1, 0, 0, 1]               # [2, 1, 3, 3, 1]
# [1, 0, 0, 1, 0]               # [1, 3, 3, 1, 4]
# [0, 1, 0, 1, 1]               # [5, 1, 3, 1, 1]


""""
FUNCTION:       group_connections

INTERFACE:      grid:list ([[],[],[]]), - 2d array consisting of integer >= 0
                group_id:int - current gourp_id
                
RETURNS:        list grid: modified array
                int group_id: modified ground_id
NOTES:
This function takes a 2d array and groups of 0's separated by 1's. once a group is created
it will increment the group id. This will return the modified grid and updated grid id
""" 
def group_connections(grid:list, group_id:int):
    if not grid:
        return 0
    
    h = len(grid)
    w = len(grid[0])
    
    # Depth First Search Algorithm
    # Recursive Function that look around the index and changes the value to id if value is 0
    def dfs(row, col):
        # if col or row out of bounds, or value of is not 0, return
        if row<0 or col<0 or row>=h or col>=w or grid[row][col] != 0:
            return
        
        # Change value to group_id
        grid[row][col] = group_id       

        dfs(row, col+1) # go right
        dfs(row, col-1) # go left 
        dfs(row+1, col) # go down
        dfs(row-1, col) # go up    
    
    # Go through the rows and col of the grid
    for row in range(h):
        for col in range(w):
            # if 0 is found run dfs search
            if grid[row][col] == 0:
                dfs(row, col)
                group_id +=  1
    # Return modified group and new group_id
    return grid, group_id


"""
FUNCTION:       merge_groups

INTERFACE:      group1:int - 1st group name
                group2:int - 2nd group name
                grid:list ([[],[],[]]) - 2d array consisting of integer >= 0
                group_id:int - current gourp_id

RETURNS:        grid:list - modified array
                group_id:int - modified ground_id
NOTES:
This function takes 2 group names and merge them including the "1" border. Then returns 
the merged grid
"""
def merge_groups(group1:int, group2:int, grid:list, group_id:int):
    if not grid:
        return 0
    
    h = len(grid)
    w = len(grid[0])
    
    grid_cpy = copy.deepcopy(grid)
    has_border = False
    
    # Depth First Search Algorithm
    # Recursively go through the grid if it is 1, group1 or group2
    # then changes its value to the new group_id if there is a border
    # found in between groups
    def dfs(row, col):
        nonlocal has_border 
        
        # Check if within bounds of the array
        if (row<0 or col<0 or row>=h or col>=w): 
            return 
        
        #  Check if the value is not 1, group1, or group2
        if (grid_cpy[row][col] != 1 and grid_cpy[row][col] != group1 and grid_cpy[row][col] != group2):
            return
        
        # Check if value is 1, change value to group_id if it is between group1 and 2
        if grid_cpy[row][col] == 1:
            # row edges, only check for col changes
            if (row-1) < 0 or (row+1) >= h:
                if (grid_cpy[row][col-1] in {group1,group2,group_id} and grid_cpy[row][col+1] in {group1,group2,group_id}):
                    grid_cpy[row][col] = group_id
                    has_border = True
                return 
            
            # column edge, only check for row changes
            if (col-1) < 0 or (col+1) >= w:
                if (grid_cpy[(row-1)][col] in {group1,group2,group_id} and grid_cpy[(row+1)][col] in {group1,group2,group_id}):
                    grid_cpy[row][col] = group_id
                    has_border = True
                return
            
            # everything else in the grid
            if ((grid_cpy[row-1][col] in {group1,group2,group_id} and grid_cpy[row+1][col] in {group1,group2,group_id}) or 
                (grid_cpy[row][col-1] in {group1,group2,group_id} and grid_cpy[row][col+1] in {group1,group2,group_id})):
                grid_cpy[row][col] = group_id
                has_border = True                                 

        # Change value to group_id
        else:
            grid_cpy[row][col] = group_id
            dfs(row, col+1) # go right
            dfs(row, col-1) # go left 
            dfs(row+1, col) # go down
            dfs(row-1, col) # go up    
            
    # go through the item in the grid
    for row in range(h):
        for col in range(w):
            if grid_cpy[row][col] == group1 or grid_cpy[row][col] == group2:
                dfs(row,col)
    
    # If it found a border, increment group_id and return the modified array
    if has_border:
        group_id +=  1
        return grid_cpy, group_id
    
    # Border not found, return original grid and id
    return grid, group_id


# --------------------------------------------------------------

# [0, 0, 1, 0, 0]
# [0, 1, 0, 0, 1]
# [1, 0, 0, 1, 0]
# [0, 1, 0, 1, 1]

original_grid = [[0, 0, 1, 0, 0],[0, 1, 0, 0, 1],[1, 0, 0, 1, 0],[0, 1, 0, 1, 1]]
group_id = 2

print("Original")
for i in original_grid:
    print(i)
print("")

# [2, 2, 1, 3, 3]
# [2, 1, 3, 3, 1]
# [1, 3, 3, 1, 4]
# [5, 1, 3, 1, 1]
print("Group Connection")
grid,group_id  = group_connections(original_grid, group_id)
for i in grid:
    print(i)
print("")


# [2, 2, 1, 3, 3]
# [2, 1, 3, 3, 1]
# [1, 3, 3, 1, 4]
# [5, 1, 3, 1, 1]
print("Merge Grouped Connection \n2,4")
grid_2_4,_ = merge_groups(2,4, grid, group_id)
for i in grid_2_4:
    print(i)
print("")

# [2, 2, 1, 6, 6]
# [2, 1, 6, 6, 1]
# [1, 6, 6, 1, 4]
# [6, 6, 6, 1, 1]
print("Merge Grouped Connection \n3,5")
grid_3_5,_ = merge_groups(3,5, grid, group_id)
for i in grid_3_5:
    print(i)
print("")

# [6, 6, 1, 3, 3]
# [6, 1, 3, 3, 1]
# [6, 3, 3, 1, 4]
# [6, 1, 3, 1, 1]
print("Merge Grouped Connection \n2,5")
grid_2_5,group_id = merge_groups(2,5, grid, group_id)
for i in grid_2_5:
    print(i)
print("")

# [7, 7, 7, 7, 7]
# [7, 7, 7, 7, 1]
# [7, 7, 7, 1, 4]
# [7, 7, 7, 1, 1]
print("Merge Grouped Connection \n3,6 from 2,5 merged grid")
grid_3_6,group_id = merge_groups(3,6, grid_2_5, group_id)
for i in grid_3_6:
    print(i)
print("")
    