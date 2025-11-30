import os
import re

def convert_pnp_to_cpl(pnp_file, useMil=True, zh=True):
    cpl_file = pnp_file.replace('_pnp.xy', '_cpl.csv')
    print(f"Converting '{pnp_file}' to '{cpl_file}'...")

    with open(pnp_file, 'r', encoding='UTF-8') as infile, open(cpl_file, 'w', encoding='UTF-8') as outfile:
        if zh:
            outfile.write("变体: 没有变体\n")
            if useMil:
                outfile.write("长度单位：mil\n")
            else:
                outfile.write("长度单位：mm\n")
            outfile.write("\n")
            outfile.write("位号, 说明, 层, 规格, X中心座标, Y中心座标, 旋转度数\n")
        else:
            outfile.write("Variant: No variations\n")
            if useMil:
                outfile.write("Units used: mil\n")
            else:
                outfile.write("Units used: mm\n")
            outfile.write("\n")
            outfile.write("Designator, Comment, Layer, Package, Center-X, Center-Y, Rotation\n")
        for line in infile:
            # Skip lines that start with Via or Pad or comments
            if not line.strip().startswith('Via') and not line.strip().startswith('Pad') \
               and not re.match(r'^P[0-9]', line.strip()) \
               and not line.strip().startswith('#') and not line.strip().startswith('Description:') \
               and not line.strip().startswith('RefDes,Description,Package,X,Y,Rotation,Side,Mount'):
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
                    if not useMil:
                        center_x = str(round(float(center_x) * 25.4 / 1000, 4))
                        center_y = str(round(float(center_y) * 25.4 / 1000, 4))
                    layer = parts[6]
                    # 替换Layer名称
                    if layer == "Top":
                        if zh:
                            layer = "顶层"
                        else:
                            layer = "TopLayer"
                    elif layer == "Bottom":
                        if zh:
                            layer = "底层"
                        else:
                            layer = "BottomLayer"
                    rotation = parts[5]
                    outfile.write(f"{designator},{comment},{layer},{footprint},{center_x},{center_y},{rotation}\n")
                else:
                    print(f"Invalid line in '{pnp_file}': {line}")

    print(f"Converted successfully.")

if __name__ == "__main__":
    print("Converting PNP to CPL...")
    # Convert all _pnp.xy files in the current directory
    found = False
    for filename in os.listdir('.'):
        if filename.endswith('_pnp.xy'):
            convert_pnp_to_cpl(filename, False)
            found = True
    if not found:
        print("No _pnp.xy file found in the current directory.")
