import os
import re
import sys
from OCP.STEPControl import STEPControl_Reader, STEPControl_Writer, STEPControl_AsIs
from OCP.IFSelect import IFSelect_RetDone
from OCP.TopExp import TopExp_Explorer
from OCP.TopAbs import TopAbs_SOLID

def extract_shape_names(step_file_path):
    """Extract names from the STEP file."""
    shape_names = []
    with open(step_file_path, 'r') as file:
        content = file.read()
        pattern = re.compile(r'#(\d+)=ADVANCED_BREP_SHAPE_REPRESENTATION\(\'([^\']+)\'')
        matches = pattern.findall(content)
        for match in matches:
            shape_id, shape_name = match
            shape_names.append(shape_name)
    return shape_names

def save_shape_to_step(shape, filename):
    """Save a shape to a STEP file."""
    writer = STEPControl_Writer()
    writer.Transfer(shape, STEPControl_AsIs)
    writer.Write(filename)

def extract_and_save_unique_shapes(shape, output_dir, shape_names):
    """Extract unique solids and compounds and save with names."""
    unique_shapes = set()
    exp = TopExp_Explorer(shape, TopAbs_SOLID)
    
    shape_index = 0
    while exp.More():
        sub_shape = exp.Current()
        if sub_shape not in unique_shapes:
            unique_shapes.add(sub_shape)
            shape_name = shape_names[shape_index] if shape_index < len(shape_names) else f"constituent_{shape_index + 1}"
            sub_shape_name = f"{shape_name}.stp"
            sub_shape_path = os.path.join(output_dir, sub_shape_name)
            save_shape_to_step(sub_shape, sub_shape_path)
            print(f"Saved: {sub_shape_path}")
            shape_index += 1
        exp.Next()

def main(step_file_path, output_dir):
    """Main function to process the STEP file and extract shapes."""
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
    extract_and_save_unique_shapes(shape, output_dir, shape_names)

    print("All unique constituent parts have been saved.")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python extract_shapes.py <step_file_path> <output_dir>")
        sys.exit(1)

    step_file_path = sys.argv[1]
    output_dir = sys.argv[2]

    if not os.path.isfile(step_file_path):
        print(f"Error: The file '{step_file_path}' does not exist.")
        sys.exit(1)

    if not os.path.isdir(output_dir):
        print(f"Error: The directory '{output_dir}' does not exist.")
        sys.exit(1)

    main(step_file_path, output_dir)
