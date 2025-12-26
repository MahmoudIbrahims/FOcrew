from string import Template


SendEmail_prompt =Template("\n".join([
                "The working directory is $working_dir.\n"
                "Take the pdf analysis this file path $file_path.\n"
                "1. Use the `Send Report via Gmail` tool.\n"
                "2. Pass a suitable subject (like 'Inventory Report').\n"
                "3. Pass the report body pdf or text or summary.\n"
                "4. sent to $managers"
                                  ]))     