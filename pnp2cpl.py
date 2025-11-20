import os
import re

def convert_pnp_to_cpl():
    # Find the first .xy file in the current directory
    for filename in os.listdir('.'):
        if filename.endswith('_pnp.xy'):
            pnp_file = filename
            break
    else:
        print("No _pnp.xy file found in the current directory.")
        return

    cpl_file = filename.replace('_pnp.xy', '_cpl.csv')
    print(f"Converting '{pnp_file}' to '{cpl_file}'...")

    with open(pnp_file, 'r', encoding='UTF-8') as infile, open(cpl_file, 'w', encoding='UTF-8') as outfile:
        outfile.write("Variant: No variations\n")
        outfile.write("Units used: mil\n")
        outfile.write("\n")
        outfile.write("Designator, Comment, Layer, Footprint, Center-X, Center-Y, Rotation, Description\n")
        for line in infile:
            # Skip lines that start with Via or Pad or B1-B6 or comments
            # if not line.strip().startswith('Via') and not line.strip().startswith('Pad') \
            #    and not line.strip().startswith('B1') and not line.strip().startswith('B2') \
            #    and not line.strip().startswith('B3') and not line.strip().startswith('B4') \
            #    and not line.strip().startswith('B5') and not line.strip().startswith('B6') \
            if not line.strip().startswith('Via') and not line.strip().startswith('Pad') \
               and not re.match(r'^P[0-9]', line.strip()) \
               and not line.strip().startswith('#') and not line.strip().startswith('Description:'):
                clean_line = line.replace('"', '')
                for s in ['[SMD, multilayer]', '[SMD]', 'SandFlower', 'sandflower', '[SMD, electrolytic]']:
                    clean_line = clean_line.replace(s, '')
                parts = clean_line.strip().split(',')
                if len(parts) >= 6:
                    designator = parts[0]
                    comment = re.sub(r'\s+', ' ', parts[1].replace(';', ' ').replace('"', '')).strip()
                    comment = comment.replace(' 0.25W', 'Ω')
                    footprint = parts[2].replace('[', '').replace(']', '').strip()
                    center_x = parts[3]
                    center_y = parts[4]
                    layer = parts[6]
                    # 替换Layer名称
                    if layer == "Top":
                        layer = "TopLayer"
                    elif layer == "Bottom":
                        layer = "BottomLayer"
                    rotation = parts[5]
                    outfile.write(f"{designator},{comment},{layer},{footprint},{center_x},{center_y},{rotation}\n")
                else:
                    print(f"Invalid line in '{pnp_file}': {line}")

    print(f"Converted successfully.")

if __name__ == "__main__":
    print("Converting PNP to CPL...")
    convert_pnp_to_cpl()