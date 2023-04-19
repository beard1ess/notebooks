import os
import re

def find_tf_files(directory):
    tf_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".tf"):
                tf_files.append(os.path.join(root, file))
    return tf_files

def extract_variable_usages(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
        regex = r'var\.(\w+)'
        matches = re.findall(regex, content)
        return set(matches)

def generate_variables_tf(variables, output_file):
    with open(output_file, 'w') as file:
        for variable in variables:
            file.write(f'variable "{variable}" {{\n')
            file.write(f'  description = "Description for {variable}"\n')
            file.write(f'  type        = any\n')
            file.write(f'  default     = null\n')
            file.write(f'}}\n\n')

def main():
    directory = '.'  # Change this to the directory with your Terraform files
    output_file = 'variables.tf'
    
    tf_files = find_tf_files(directory)
    all_variables = set()

    for tf_file in tf_files:
        variables = extract_variable_usages(tf_file)
        all_variables.update(variables)

    generate_variables_tf(all_variables, output_file)
    print(f'Successfully generated {output_file} with {len(all_variables)} variables.')

if __name__ == "__main__":
    main()
