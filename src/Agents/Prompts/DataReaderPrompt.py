from string import Template

data_reader_prompt = Template("\n".join([
    "**ABSOLUTELY MUST**Read and summarize the dataset file provided at $file_path.\n"
    "",
    "Steps:.\n"
    "The working directory is $working_dir .\n"
    "1. Detect the file type (CSV, Excel, or JSON).\n"
    "2. Load the dataset into a pandas DataFrame.\n"
    "3. Display the first few rows and dataset structure (columns, types, shape).\n"
    "4. Return a summary that will be passed to the next agent.\n"
]))
