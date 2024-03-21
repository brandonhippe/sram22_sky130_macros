import os, re

if __name__ == "__main__":
    sram_dir = os.path.join(os.getcwd(), "sram22_sky130_macros")

    print("Renaming sram22_sky130_macros...")

    curr_name = r'\d+x\d+m\d+w\d+'
    
    for root, dirs, files in os.walk(sram_dir):
        for file in files:
            print(f"Checking {file}")
            new_name = file
            if new_name.endswith(".rc.lib"):
                new_name = new_name.replace(".rc.lib", ".lib")

            
            m = re.search(curr_name, new_name)
            if m and "sramgen" not in new_name:
                new_name = f"sramgen_sram_{m.group(0)}_replica_v1{new_name[m.end():]}"
                print(f"Renaming {file} to {new_name}")

            os.rename(os.path.join(root, file), os.path.join(root, new_name))

            if new_name.endswith(".v") or new_name.endswith(".spice") or new_name.endswith(".lib"):
                with open(os.path.join(root, new_name), "r") as f:
                    lines = f.readlines()
                    
                for ix in range(len(lines)):
                    line = lines[ix]
                    m = re.search(curr_name, line)
                    if m and "sramgen" not in line:
                        line = f"{line[:m.start()]}sramgen_sram_{m.group(0)}_replica_v1{line[m.end():]}"
                        line = line.replace("sram22_", "")
                        print(f"Renaming in {new_name}: {line}")

                    lines[ix] = line

                with open(os.path.join(root, new_name), "w") as f:
                    f.writelines(lines)

    for root, dirs, files in os.walk(sram_dir):
        for dir in dirs:
            print(f"Checking {dir}")
            new_name = dir
            m = re.search(curr_name, new_name)
            if m and "sramgen" not in new_name:
                new_name = f"sramgen_sram_{m.group(0)}_replica_v1{new_name[m.end():]}"
                print(f"Renaming {dir} to {new_name}")

            os.rename(os.path.join(root, dir), os.path.join(root, new_name))

    print("Done!")
