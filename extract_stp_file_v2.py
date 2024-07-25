import os
import re
import sys
from OCP.STEPControl import STEPControl_Reader, STEPControl_Writer, STEPControl_AsIs
from OCP.IFSelect import IFSelect_RetDone
from OCP.TopExp import TopExp_Explorer
from OCP.TopAbs import TopAbs_SOLID
from tqdm import tqdm

def extract_shape_names(step_file_path):
    """Extract names from the STEP file."""
    shape_names = []
    with open(step_file_path, 'r') as file:
        content = file.read()
        pattern = re.compile(r"#\d+=MANIFOLD_SOLID_BREP\('([^']+)'\s*,\s*#\d+\)")
        matches = pattern.findall(content)
        shape_names.extend(matches)
    return shape_names

def save_shape_to_step(shape, filename):
    """Save a shape to a STEP file."""
    writer = STEPControl_Writer()
    writer.Transfer(shape, STEPControl_AsIs)
    writer.Write(filename)

def extract_and_save_unique_shapes(shape, output_dir, shape_names, original_file_name):
    """Extract unique solids and compounds and save with names."""
    unique_shapes = set()
    exp = TopExp_Explorer(shape, TopAbs_SOLID)
    
    shape_index = 0
    total_shapes = 0
    while exp.More():
        total_shapes += 1
        exp.Next()
    
    exp.ReInit()
    
    with tqdm(total=total_shapes, desc="Extracting shapes") as pbar:
        while exp.More():
            sub_shape = exp.Current()
            if sub_shape not in unique_shapes:
                unique_shapes.add(sub_shape)
                if shape_index < len(shape_names):
                    shape_name = shape_names[shape_index]
                    sub_shape_name = f"{shape_name}.stp"
                    sub_shape_path = os.path.join(output_dir, sub_shape_name)
                    save_shape_to_step(sub_shape, sub_shape_path)
                    print(f"Saved: {sub_shape_path}")
                else:
                    # Log the original file name if no shape name is found
                    log_path = os.path.join(output_dir, "no_name_log.txt")
                    with open(log_path, 'a') as log_file:
                        log_file.write(f"No name found for parts in: {original_file_name}\n")
                    print(f"No name found for parts in: {original_file_name}. Logged to {log_path}")
                    break
                shape_index += 1
            exp.Next()
            pbar.update(1)

def process_step_file(step_file_path, output_dir):
    """Process a single STEP file."""
    # Extract shape names from the STEP file
    shape_names = extract_shape_names(step_file_path)
    print(f"Extracted shape names: {shape_names}")

    # Load the STEP file
    reader = STEPControl_Reader()
    status = reader.ReadFile(step_file_path)
    if status != IFSelect_RetDone:  # IFSelect_RetDone indicates success
        raise Exception("Error: Cannot read the STEP file.")
    reader.TransferRoots()
    shape = reader.OneShape()

    # Extract and save unique shapes with names
    original_file_name = os.path.basename(step_file_path)
    extract_and_save_unique_shapes(shape, output_dir, shape_names, original_file_name)

    print("All unique constituent parts have been saved for", step_file_path)

def main(input_dir, output_dir):
    """Main function to process all STEP files in the input directory."""
    files = [f for f in os.listdir(input_dir) if f.endswith('.stp') or f.endswith('.step')]
    
    with tqdm(total=len(files), desc="Processing files") as pbar:
        for file_name in files:
            step_file_path = os.path.join(input_dir, file_name)
            process_step_file(step_file_path, output_dir)
            pbar.update(1)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python extract_shapes.py <input_dir> <output_dir>")
        sys.exit(1)

    input_dir = sys.argv[1]
    output_dir = sys.argv[2]

    if not os.path.isdir(input_dir):
        print(f"Error: The directory '{input_dir}' does not exist.")
        sys.exit(1)

    if not os.path.isdir(output_dir):
        print(f"Error: The directory '{output_dir}' does not exist.")
        sys.exit(1)

    main(input_dir, output_dir)
