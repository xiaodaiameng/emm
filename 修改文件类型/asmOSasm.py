import os
directory_path = r"C:\Users\ass\Desktop\asmAsm"
for filename in os.listdir(directory_path):
    if filename.endswith(".asm"):
        new_filename = filename.replace(".asm", ".txt")
        src = os.path.join(directory_path, filename)
        dst = os.path.join(directory_path, new_filename)
        os.rename(src, dst)
