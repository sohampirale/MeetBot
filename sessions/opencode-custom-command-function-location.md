---
name : opencode-custom-command-function-location
filename : opencode-custom-command-function-location.md
description : Discussion about where to declare functions for custom commands in opencode so they can be found by agents across different project directories
points_mentioned: ["opencode","custom-commands","function-location","shared-libraries","~/.config/opencode","cross-project"]
---
## Situation
The user wanted to create a custom command inside `~/.config/opencode/command` that depended on a function (either Python or TypeScript). They were unsure where to declare this function so that coding agents could invoke it with the custom command, especially when opening opencode in different project directories where the function wouldn't be locally present.

## Task
Provide guidance on where to declare functions for custom commands in opencode so they are accessible across different project directories without being auto-loaded as tools in every agent session.

## Actions Taken
1. Created the `~/.config/opencode/lib/` directory structure for shared functions
2. Explained the naming convention and organization approach
3. Provided a concrete example showing how to reference the function using absolute paths
4. Outlined the workflow for agents to read and execute these functions when needed

## What Worked
- The solution provides a clear, organized structure for shared functions
- Functions remain available globally but don't auto-load into every agent session
- The approach allows agents to explicitly read and execute functions when instructed
- The absolute path reference ensures functions work regardless of the current project directory

## What Did Not Work
No issues encountered with this approach. The solution addresses the user's concern about function discoverability across different project directories while maintaining the desired separation from auto-loaded tools.

## Conclusion
The recommended approach is to place shared functions in `~/.config/opencode/lib/` with clear naming conventions. Custom commands can reference these functions using absolute paths, and agents can access them by reading the function files and executing them explicitly when needed. This provides the right balance of global availability without auto-loading behavior.