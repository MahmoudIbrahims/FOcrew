from string import Template

analysis_prompt =Template("\n".join([
          "Perform an in-depth analysis on the cleaned dataset.\n\n"
                    "Steps:\n"
                    "The working directory is $working_dir.\n"
                    "1. Generate Python code for statistical summaries and feature correlations.\n"
                    "2. Execute code to compute metrics (mean, std, skew, etc.).\n"
                    "3. Identify key trends, anomalies, or interesting relationships.\n"
                    "4. Return analytical insights for the visualization stage."
                
            ]))


