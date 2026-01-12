---
name: OpenCode Tools Research and Hello World Tool Creation
description: Research session about OpenCode tools functionality, configuration, and creation of custom tools with Python implementation
points_mentioned:
  - OpenCode tools configuration in opencode.json under tools section
  - Built-in tools include bash, edit, write, read, grep, glob, list, lsp, patch, skill, todowrite, todoread, webfetch
  - Custom tools created as TypeScript/JavaScript files in .opencode/tool/directory
  - Tools MUST return string type only, cannot return other data types
  - Tool definitions use tool() helper for type-safety and validation
  - Python scripts can be invoked from tool definitions using Bun.$ utility
---

## Situation
The user initially asked about how to create tools in OpenCode, specifically about configuration in .opencode directories and how they work. This led to a comprehensive research session about OpenCode's tool system.

## Task
Research and explain OpenCode tools functionality, including:
- How tools are configured and managed
- Built-in tool capabilities
- Custom tool creation process
- Provide a concrete example of creating a "hello world" tool using Python

## Actions Taken
1. **Research Phase**: Used webfetch to gather comprehensive information from opencode.ai documentation about tools, custom tools, and configuration
2. **Analysis**: Compiled information about tool configuration locations, built-in tools, and custom tool creation patterns
3. **Tool Creation**: Created a complete "hello world" tool example:
   - Created `.opencode/tool/hello.py` - Python script implementation
   - Created `.opencode/tool/hello.ts` - OpenCode tool definition using tool() helper
   - Made Python script executable with chmod +x

## What Worked
- Successfully researched OpenCode tool system from official documentation
- Correctly identified tool configuration in opencode.json and .opencode/tool/ directories
- Properly demonstrated TypeScript tool definition using tool() helper
- Successfully created working Python integration example
- Tool structure and file naming conventions were correctly implemented

## What Did Not Work
- Failed to identify the critical constraint that OpenCode tools MUST return string type only
- The research missed this fundamental requirement about return type limitations
- Tool example was created without acknowledging this string-only return constraint
- Understanding of tool limitations was incomplete without this key information

## Conclusion
This session successfully covered OpenCode's tool architecture and creation process. The user provided valuable feedback that highlighted a critical missing piece: OpenCode tools have a strict requirement to return string type only. This is a fundamental constraint that must be considered in all tool implementations. Future agents should be aware that while tool definitions can be complex and invoke any programming language, the final return value must always be a string type, not objects, arrays, or other data structures. This constraint is essential for proper tool functionality and should be documented in any tool creation workflow.