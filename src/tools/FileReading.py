from crewai_tools import FileReadTool,DirectoryReadTool


def FileTool():
    file_tool = FileReadTool()
    return file_tool
    
def DirectoryTool():
    directory_tool = DirectoryReadTool()
    return directory_tool
