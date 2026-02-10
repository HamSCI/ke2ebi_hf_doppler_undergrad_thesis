'''
import os
data_dir = 'w2naf_grape1'  # or whatever the full path should be
print(f"Directory exists: {os.path.exists(data_dir)}")
if os.path.exists(data_dir):
    print(f"Contents: {os.listdir(data_dir)}")
'''
'''
import os
# Look in current directory
print([d for d in os.listdir('.') if os.path.isdir(d) and 'w2naf' in d.lower()])
'''

import os

###
data_path = 'data/psws_grapeDRF/w2naf_grape1'
print(f"Contents of {data_path}:")
for item in os.listdir(data_path):
    item_path = os.path.join(data_path, item)
    if os.path.isdir(item_path):
        print(f"  [DIR] {item}")
        # Show subdirectory contents
        for subitem in os.listdir(item_path)[:5]:  # First 5 items
            print(f"        {subitem}")
    else:
        print(f"  [FILE] {item}")

data_path = 'data/psws_grapeDRF/w2naf'
print(f"\nContents of {data_path}:")
for item in os.listdir(data_path):
    item_path = os.path.join(data_path, item)
    if os.path.isdir(item_path):
        print(f"  [DIR] {item}")
####

data_path = 'data/psws_grapeDRF/w2naf_grape1'
props_file = os.path.join(data_path, 'ch0', 'drf_properties.h5')
print(f"Properties file exists: {os.path.exists(props_file)}")

# Also check what's in ch0
ch0_path = os.path.join(data_path, 'ch0')
print(f"\nAll files in ch0:")
for item in os.listdir(ch0_path):
    print(f"  {item}")