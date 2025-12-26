from string import Template


Translation_prompt =Template("\n".join([
    "The working directory is $working_dir.\n"
    "Translation from $source_language to $target_language and Preserve meaning, tone, and formatting."
                                  ]))     