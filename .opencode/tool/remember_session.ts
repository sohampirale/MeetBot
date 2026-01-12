import { tool } from "@opencode-ai/plugin"
import dotenv from "dotenv"
dotenv.config()
import fs from "fs"
import path from "path"
import { CohereClient } from "cohere-ai";
import { spawn } from "child_process";

const cohere = new CohereClient({
  token: process.env.COHERE_API_KEY!,
});

export default tool({
  description: "Retrive past sessions info related to task given to you,using RAG",
  args: {
    rag_queries: tool.schema.string().describe("String of all the queries for RAG ex 'fastapi,backend,jwt' this entire string"),
  },
  async execute(args) {
    const rag_queries = args.rag_queries;
    
    const indexPath = path.join("sessions", "faiss_data", "sessions.index");
    const topK = 2;
    const response = await cohere.embed({
      model: "embed-english-v3.0",
      texts: [
        rag_queries
      ],
      inputType: "search_document",
    });

    const embeddings = response.embeddings[0];
    const embeddingDim=1024

    const result = await new Promise<string>((resolve, reject) => {
      const py = spawn("uv", [
        "run",
        ".opencode/tool/rag_p.py",
        indexPath,
        String(embeddingDim),
        String(topK),
      ]);

      let output = "";
      let error = "";

      py.stdout.on("data", (data) => {
        output += data.toString();
      });

      py.stderr.on("data", (data) => {
        error += data.toString();
      });

      py.on("close", (code) => {
        if (code !== 0 || error) {
          reject(error);
        } else {
          resolve(output);
        }
      });

      py.stdin.write(
        Buffer.from(new Float32Array(embeddings).buffer)
      );
      py.stdin.end();
    })

    const parsed = JSON.parse(result);

    // INSERT_YOUR_CODE
    const metaPath = path.join("sessions", "faiss_data", "sessions.meta.json");
    const metaRaw = fs.readFileSync(metaPath, "utf8");
    let metaList;
    try {
      metaList = JSON.parse(metaRaw);
      if (!Array.isArray(metaList)) metaList = [];
    } catch (e) {
      metaList = [];
    }
    // Use indices from parsed.indices to look up meta entries (by position)
    const accumulatedResults = parsed.indices.map((idx: number) => metaList[idx]).filter(Boolean);
    const ret={
      results:accumulatedResults,
      ...parsed
    }

    return JSON.stringify(ret)

  },
})
