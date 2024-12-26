import os 
  
file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'testfile.csv')

print(f'File path: {file_path}')

file_contents = open(file_path, 'r').read() 

rows = file_contents.split('\n')

for i, row in enumerate(rows):
    cells = row.split(',') 
    print(f'Row {i}: {cells}')
 

