from string import Template
from datetime import datetime


Data_processing_prompt =Template("\n".join([
    
            "Process the inventory data file:$file_path",
                "Process large inventory dataset in batches optimized for Gemini's context length. For each batch: ",
                "1. Read the file Excel or CSV and split it into manageable batches. The `Optimized Batch File Reader` tool_1 save the results inside **results/Mini_Batches**",
                "2. Read batch by batch to use `JsonBatchFileReader` tool_2",
                "3. Use the `Batch Processor` tool_3 to process ALL and save resuts for this tool inside path **results/Mini_reports**",
                "4. Use only real data from the batch. ",
                "5. Save intermediate results per batch. ",
                "6. Combine into a final report. ",
                "## save the final report inside path **results/inventory_management/Analysis_Report.md**"
            ]))
    
    
    
    