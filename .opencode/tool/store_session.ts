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
  description: "Store front matter of session summary in a vector DB",
  args: {
    filename: tool.schema.string().describe("filename of the session summary stored inside `sessions/` folder"),
  },
  async execute(args) {
    
    const filename = args.filename;
    const filePath = path.join('sessions', filename);

    const content = fs.readFileSync(filePath, 'utf8');
    const frontMatterMatch = content.match(/^(-{3,})\s*\n([\s\S]*?)\n\1/m);
    let frontMatter;

    if (frontMatterMatch) {
      frontMatter = `${frontMatterMatch[1]}\n${frontMatterMatch[2]}\n${frontMatterMatch[1]}`;
      const response = await cohere.embed({
        model: "embed-english-v3.0",
        texts: [
          content
        ],
        inputType: "search_document",
      });

      const embeddings = response.embeddings;
      // INSERT_YOUR_CODE
      console.log("Embeddings length:", embeddings[0].length);
      // One faiss and one meta file for ALL session summaries
      const faissDir = path.join('sessions', 'faiss_data');
      if (!fs.existsSync(faissDir)) {
        fs.mkdirSync(faissDir, { recursive: true });
      }

      const allFaissFile = path.join(faissDir, `sessions.faiss`);
      const allMetaFile = path.join(faissDir, `sessions.meta.json`);

      // ------ METADATA (JSON LIST) HANDLING ------
      // Meta is a JSON list of session meta objects: {filename, frontmatter, embedding_shape}
      let existingMeta: any[] = [];
      if (fs.existsSync(allMetaFile)) {
        try {
          const raw = fs.readFileSync(allMetaFile, 'utf8');
          existingMeta = JSON.parse(raw);
          if (!Array.isArray(existingMeta)) existingMeta = [];
        } catch (e) {
          console.log('error : ',e);
          existingMeta = [];
        }
      }

      const embedding_shape = embeddings && embeddings[0] ? embeddings[0].length : 0;
      const metadata = {
        filename,
        extracted_frontmatter: frontMatter,
        embedding_shape: embedding_shape
      };

      // Just append to meta (no duplicate checks, no remove/overwrite for now)
      existingMeta.push(metadata);

      fs.writeFileSync(allMetaFile, JSON.stringify(existingMeta, null, 2), 'utf8');

      // ------ FAISS VECTOR BLOB COLLECTION ------
      // Just append this embedding to faiss binary file in order
      const vector = new Float32Array(embeddings[0]);
      if (fs.existsSync(allFaissFile)) {
        // Existing file: append new vector
        const fd = fs.openSync(allFaissFile, 'a');
        fs.writeSync(fd, Buffer.from(vector.buffer));
        fs.closeSync(fd);
      } else {
        // First vector, create new file
        fs.writeFileSync(allFaissFile, Buffer.from(vector.buffer));
      }

      const result = {
        faissFile: allFaissFile,
        metaFile: allMetaFile,
        totalSessions: existingMeta.length,
        status: 'written'
      };

      spawn("uv", ["run",".opencode/tool/rebuild_index.py"], {
        stdio: "inherit"
      });

      return "session stored successfully for file " + filename + JSON.stringify(result);
    }

    return "session not stored!";
  },
})
