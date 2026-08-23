import express from "express";
import path from "path";
import fs from "fs";
import { spawn } from "child_process";
import { createServer as createViteServer } from "vite";

async function startServer() {
  const app = express();
  const PORT = 3000;

  app.use(express.json());

  // API Route: Run eSim Tool Manager commands safely
  app.post("/api/run", (req, res) => {
    const { command, tool, dryRun, jsonMode } = req.body || {};

    let pyArgs: string[] = ["main.py"];

    if (command === "test") {
      pyArgs = ["-m", "unittest", "discover", "tests", "-v"];
    } else if (command === "check") {
      pyArgs.push("check");
      if (jsonMode) pyArgs.push("--json");
    } else if (command === "list") {
      pyArgs.push("list");
      if (jsonMode) pyArgs.push("--json");
    } else if (command === "doctor") {
      pyArgs.push("doctor");
      if (jsonMode) pyArgs.push("--json");
    } else if (command === "version" && typeof tool === "string") {
      pyArgs.push("version", tool.trim());
      if (jsonMode) pyArgs.push("--json");
    } else if (command === "info" && typeof tool === "string") {
      pyArgs.push("info", tool.trim());
      if (jsonMode) pyArgs.push("--json");
    } else if (command === "install" && typeof tool === "string") {
      pyArgs.push("install", tool.trim());
      if (dryRun !== false) pyArgs.push("--dry-run");
      if (jsonMode) pyArgs.push("--json");
    } else {
      res.status(400).json({ error: "Invalid or unsupported command parameter." });
      return;
    }

    const proc = spawn("python3", pyArgs, {
      cwd: process.cwd(),
      env: { ...process.env, PYTHONPATH: path.join(process.cwd(), "src") },
    });

    let stdout = "";
    let stderr = "";

    proc.stdout.on("data", (chunk) => {
      stdout += chunk.toString();
    });

    proc.stderr.on("data", (chunk) => {
      stderr += chunk.toString();
    });

    proc.on("close", (code) => {
      res.json({
        command: `python3 ${pyArgs.join(" ")}`,
        exitCode: code,
        stdout,
        stderr,
      });
    });

    proc.on("error", (err) => {
      res.status(500).json({
        error: `Failed to spawn Python process: ${err.message}`,
      });
    });
  });

  // API Route: Fetch log content
  app.get("/api/logs", (req, res) => {
    const logPath = path.join(process.cwd(), "logs", "esim_manager.log");
    if (fs.existsSync(logPath)) {
      const content = fs.readFileSync(logPath, "utf-8");
      res.json({ logs: content });
    } else {
      res.json({ logs: "No logs recorded yet." });
    }
  });

  // API Route: Download Design Document in DOCX format
  app.get("/api/download-docx", (req, res) => {
    const docxPath = path.join(process.cwd(), "docs", "eSim_Automated_Tool_Manager_Design_Document.docx");
    if (fs.existsSync(docxPath)) {
      res.setHeader("Content-Type", "application/vnd.openxmlformats-officedocument.wordprocessingml.document");
      res.setHeader("Content-Disposition", 'attachment; filename="eSim_Automated_Tool_Manager_Design_Document.docx"');
      res.sendFile(docxPath);
    } else {
      res.status(404).json({ error: "DOCX file not found. Run python3 generate_docx.py" });
    }
  });

  // API Route: Download Internship Proposal in DOCX format
  app.get("/api/download-proposal-docx", (req, res) => {
    const docxPath = path.join(process.cwd(), "docs", "eSim_Tool_Manager_Internship_Proposal.docx");
    if (fs.existsSync(docxPath)) {
      res.setHeader("Content-Type", "application/vnd.openxmlformats-officedocument.wordprocessingml.document");
      res.setHeader("Content-Disposition", 'attachment; filename="eSim_Tool_Manager_Internship_Proposal.docx"');
      res.sendFile(docxPath);
    } else {
      res.status(404).json({ error: "Proposal DOCX file not found. Run python3 generate_proposal_docx.py" });
    }
  });

  // API Route: Download Internship Proposal in PDF format
  app.get("/api/download-proposal-pdf", (req, res) => {
    const pdfPath = path.join(process.cwd(), "docs", "eSim_Tool_Manager_Internship_Proposal.pdf");
    if (fs.existsSync(pdfPath)) {
      res.setHeader("Content-Type", "application/pdf");
      res.setHeader("Content-Disposition", 'attachment; filename="eSim_Tool_Manager_Internship_Proposal.pdf"');
      res.sendFile(pdfPath);
    } else {
      res.status(404).json({ error: "PDF file not found. Run python3 generate_pdf.py" });
    }
  });

  // Vite middleware for development
  if (process.env.NODE_ENV !== "production") {
    const vite = await createViteServer({
      server: { middlewareMode: true },
      appType: "spa",
    });
    app.use(vite.middlewares);
  } else {
    const distPath = path.join(process.cwd(), "dist");
    app.use(express.static(distPath));
    app.get("*", (req, res) => {
      res.sendFile(path.join(distPath, "index.html"));
    });
  }

  app.listen(PORT, "0.0.0.0", () => {
    console.log(`eSim Tool Manager server listening on http://0.0.0.0:${PORT}`);
  });
}

startServer();
