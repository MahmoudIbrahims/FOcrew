from string import Template

visualizations_prompt =Template("\n".join([
          "Generate visualizations based on the analytical insights.\n\n"
                    "Steps:\n"
                    "The working directory is $working_dir.\n"
                    "1. Create Python code using matplotlib/seaborn for relevant charts.\n"
                    "2. Execute visualization code using RunCommandTool.\n"
                    "3. Save the charts and summarize what each chart shows.\n"
                    "4. Return visualization paths and descriptions for report writing."
                
            ]))


