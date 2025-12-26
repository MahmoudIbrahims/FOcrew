from string import Template

cleaning_prompt =Template("\n".join([
           "Clean and preprocess the dataset based on the summary provided by the Data Reader.\n\n"
                    "Steps:\n"
                    "The working directory is $working_dir.\n"
                    "1. Identify missing values, inconsistent data types, or outliers.\n"
                    "2. Generate Python code to clean the dataset.\n"
                    "3. Execute that code using the RunCommandTool.\n"
                    "4. Return a cleaned dataset summary and actions performed."
            ]))


