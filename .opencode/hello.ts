import { tool } from "@opencode-ai/plugin"

export default tool({
  description: "Say hello to someone using Python script",
  args: {
    name: tool.schema.string().optional().describe("Name to say hello to (defaults to 'World')"),
  },
  async execute(args) {
    // Call the Python script with the name argument
    const name = args.name || "World"
    const result = await Bun.$`python3 .opencode/tool/hello.py ${name}`.text()
    return result.trim()
  },
})