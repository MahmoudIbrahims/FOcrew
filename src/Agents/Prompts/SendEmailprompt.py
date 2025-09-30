from string import Template


SendEmail_prompt =Template("\n".join([
                "Take the pdf analysis this file path (default: results/inventory_management/report.pdf).",
                "1. Use the `Send Report via Gmail` tool.",
                "2. Pass a suitable subject (like 'Inventory Report').",
                "3. Pass the report body pdf or text or summary.",
                "4. sent to $manager"
                                  ]))     