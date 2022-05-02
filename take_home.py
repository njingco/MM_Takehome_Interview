# !FINISH BY MONDAY
import copy

#  We have a gray scale image with size of (W, H, 1), which is split into several pieces. Those split
# lines or curves are all 1s, while the rest of the image are all 0s. Implement a function to label
# those split regions, which means all four-way connects 0s are relabeled as a same number (>1)
# and all unconnected regions should not have same id. For example, in python if we have an
# input image like              # Your output should be like:
# [0, 0, 1, 0, 0]               # [2, 2, 1, 3, 3]
# [0, 1, 0, 0, 1]               # [2, 1, 3, 3, 1]
# [1, 0, 0, 1, 0]               # [1, 3, 3, 1, 4]
# [0, 1, 0, 1, 1]               # [5, 1, 3, 1, 1]

 
# w: width (size of array in grid array)
# h: height (size of grid array)
# grid: [[],[],[]]
def group_connections_recursive(grid:list, group_id:int):
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
        
        grid[row][col] = group_id       # Change group id

        dfs(row, col+1) # right
        dfs(row, col-1) # left (can be commented out)
        dfs(row+1, col) # down
        dfs(row-1, col) # up    
    
    # Go through the rows and col of the grid
    for row in range(h):
        for col in range(w):
            # if 0 is found run dfs search
            if grid[row][col] == 0:
                dfs(row, col)
                group_id +=  1
                
    return grid, group_id


# After we get the output from the above question, implement a function that if we give any two
# integers (greater than 1, and must be present in the image), we would connect those two
# regions and labels as another integer which is not in the image. For example, if we have above
# 
# image, and two integers as 3 and 5,               # Another example would be the image with two            
# the output should be like:                          integers as 2 and 4, the output should be   
# [2, 2, 1, 6, 6]                                     # [2, 2, 1, 3, 3]    
# [2, 1, 6, 6, 1]                                     # [2, 1, 3, 3, 1]
# [1, 6, 6, 1, 4]                                     # [1, 3, 3, 1, 4]
# [6, 6, 6, 1, 1]                                     # [5, 1, 3, 1, 1]
#
# if groups are 1 space away horizontal and vertical merge the two groups

def merge_groups(group1:int, group2:int, grid:list, group_id:int):
    if not grid:
        return 0
    
    h = len(grid)
    w = len(grid[0])
    
    grid_cpy = copy.deepcopy(grid)
    has_border = False
    
    def dfs(row, col):
        nonlocal has_border 
        
        if (row<0 or col<0 or row>=h or col>=w): 
            return 
             
        if (grid_cpy[row][col] != 1 and 
            grid_cpy[row][col] != group1 and 
            grid_cpy[row][col] != group2):
            return
        
        if grid_cpy[row][col] == 1:
            # row edges, only check for col changes
            if (row-1) < 0 or (row+1) >= h:
                if (grid_cpy[row][col-1] in {group1,group2,group_id} and 
                    grid_cpy[row][col+1] in {group1,group2,group_id}):
                    grid_cpy[row][col] = group_id
                    has_border = True
                return 
            
            # column edge, only check for row changes
            if (col-1) < 0 or (col+1) >= w:
                if (grid_cpy[(row-1)][col] in {group1,group2,group_id} and 
                    grid_cpy[(row+1)][col] in {group1,group2,group_id}):
                    grid_cpy[row][col] = group_id
                    has_border = True
                return
            
            # everything else in the grid
            if ((grid_cpy[row-1][col] in {group1,group2,group_id} and 
                 grid_cpy[row+1][col] in {group1,group2,group_id}) or 
                (grid_cpy[row][col-1] in {group1,group2,group_id} and 
                 grid_cpy[row][col+1] in {group1,group2,group_id})):
                grid_cpy[row][col] = group_id
                has_border = True                                 

        else:
            grid_cpy[row][col] = group_id
            
            dfs(row, col+1) # go right
            dfs(row, col-1) # go left 
            dfs(row+1, col) # go down
            dfs(row-1, col) # go up    
            
            
    for row in range(h):
        for col in range(w):
            if grid_cpy[row][col] == group1 or grid_cpy[row][col] == group2:
                dfs(row,col)
    
    if has_border:
        group_id +=  1
        return grid_cpy, group_id
    
    return grid, group_id

original_grid = [[0, 0, 1, 0, 0],[0, 1, 0, 0, 1],[1, 0, 0, 1, 0],[0, 1, 0, 1, 1]]
group_id = 2

print("Original")
for i in original_grid:
    print(i)
print("")

print("Group Connection")
grid,group_id  = group_connections_recursive(original_grid, group_id)
for i in grid:
    print(i)
print("")


print("Merge Grouped Connection 2,4")
grid_2_4,_ = merge_groups(2,4, grid, group_id)
for i in grid_2_4:
    print(i)
print("")

print("Merge Grouped Connection 3,5")
grid_3_5,_ = merge_groups(3,5, grid, group_id)
for i in grid_3_5:
    print(i)
print("")

print("Merge Grouped Connection 2,5")
grid_2_5,group_id = merge_groups(2,5, grid, group_id)
for i in grid_2_5:
    print(i)
print("")

print("Merge Grouped Connection 3,6 from 2,5 merged grid")
grid_3_6,group_id = merge_groups(3,6, grid_2_5, group_id)
for i in grid_3_6:
    print(i)
print("")
    