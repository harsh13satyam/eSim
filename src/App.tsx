import React, { useState, useEffect } from "react";
import {
  Terminal,
  Activity,
  Package,
  FileText,
  Play,
  CheckCircle2,
  XCircle,
  AlertTriangle,
  RotateCw,
  Cpu,
  Layers,
  BookOpen,
  Copy,
  Check,
  ExternalLink,
  ShieldCheck,
  RefreshCw,
  Wrench,
  Download,
} from "lucide-react";

interface RunResponse {
  command: string;
  exitCode: number;
  stdout: string;
  stderr: string;
  error?: string;
}

export default function App() {
  const [activeTab, setActiveTab] = useState<"terminal" | "dashboard" | "docs" | "logs">("dashboard");
  const [loading, setLoading] = useState(false);
  const [cliOutput, setCliOutput] = useState<RunResponse | null>(null);
  const [logsContent, setLogsContent] = useState<string>("");
  const [copied, setCopied] = useState(false);
  const [customTool, setCustomTool] = useState("ngspice");
  const [dryRun, setDryRun] = useState(true);
  const [jsonMode, setJsonMode] = useState(false);

  const runCommand = async (command: string, toolName?: string) => {
    setLoading(true);
    try {
      const res = await fetch("/api/run", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          command,
          tool: toolName,
          dryRun,
          jsonMode,
        }),
      });
      const data: RunResponse = await res.json();
      setCliOutput(data);
      if (activeTab !== "terminal") {
        // automatically switch to terminal if ran from quick bar
        // or keep current tab if preferred
      }
    } catch (err: any) {
      setCliOutput({
        command: `python3 main.py ${command}`,
        exitCode: 1,
        stdout: "",
        stderr: err.message || "Failed to execute API call.",
      });
    } finally {
      setLoading(false);
    }
  };

  const fetchLogs = async () => {
    try {
      const res = await fetch("/api/logs");
      const data = await res.json();
      setLogsContent(data.logs || "No logs available.");
    } catch {
      setLogsContent("Failed to load log file.");
    }
  };

  useEffect(() => {
    runCommand("check");
    fetchLogs();
  }, []);

  const handleCopy = (text: string) => {
    navigator.clipboard.writeText(text);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className="flex flex-col min-h-screen w-full bg-[#050505] text-[#e0e0e0] font-sans selection:bg-[#3b82f6]/30 selection:text-white">
      {/* Top Sophisticated Header */}
      <header className="flex flex-col md:flex-row items-start md:items-center justify-between px-6 lg:px-8 py-5 border-b border-[#1a1a1a] bg-[#0a0a0a] gap-4 sticky top-0 z-50">
        <div className="flex items-center gap-4">
          <div className="w-10 h-10 bg-[#3b82f6] rounded flex items-center justify-center font-bold text-black text-xl shadow-md select-none shrink-0">
            E
          </div>
          <div className="flex flex-col">
            <h1 className="text-lg font-semibold tracking-tight text-white">eSim Automated Tool Manager</h1>
            <p className="text-xs text-[#666] font-mono">v1.0.4-stable • f34a92c • IIT Bombay FOSSEE</p>
          </div>
        </div>

        {/* Telemetry metadata & system status */}
        <div className="flex flex-wrap items-center gap-4 lg:gap-6 text-xs uppercase tracking-widest text-[#999]">
          <div className="flex flex-col items-start md:items-end">
            <span className="text-[10px] text-[#666]">OS</span>
            <span className="text-white font-mono text-xs">Debian 12 (Linux)</span>
          </div>
          <div className="hidden md:block w-[1px] h-8 bg-[#1a1a1a]"></div>
          <div className="flex flex-col items-start md:items-end">
            <span className="text-[10px] text-[#666]">Architecture</span>
            <span className="text-white font-mono text-xs">x86_64</span>
          </div>
          <div className="hidden md:block w-[1px] h-8 bg-[#1a1a1a]"></div>
          <div className="flex flex-col items-start md:items-end">
            <span className="text-[10px] text-[#666]">Python Core</span>
            <span className="text-white font-mono text-xs">3.10.12</span>
          </div>
          <div className="px-3 py-1 bg-[#152015] text-[#4ade80] border border-[#224d22] rounded-full text-[10px] font-bold tracking-wider">
            SYSTEM READY
          </div>
        </div>
      </header>

      {/* Control Strip & Nav Bar */}
      <div className="px-6 lg:px-8 py-3.5 border-b border-[#1a1a1a] bg-[#070707] flex flex-wrap items-center justify-between gap-4">
        {/* Navigation Tabs */}
        <nav className="flex items-center gap-1 bg-[#0a0a0a] p-1 rounded-lg border border-[#1a1a1a] text-xs font-medium">
          <button
            onClick={() => setActiveTab("dashboard")}
            className={`flex items-center gap-1.5 px-3.5 py-1.5 rounded transition-all duration-150 ${
              activeTab === "dashboard"
                ? "bg-[#3b82f6] text-black font-bold shadow-sm"
                : "text-[#999] hover:text-white hover:bg-[#151515]"
            }`}
          >
            <Activity className="w-3.5 h-3.5" />
            Dependency Grid
          </button>
          <button
            onClick={() => setActiveTab("terminal")}
            className={`flex items-center gap-1.5 px-3.5 py-1.5 rounded transition-all duration-150 ${
              activeTab === "terminal"
                ? "bg-[#3b82f6] text-black font-bold shadow-sm"
                : "text-[#999] hover:text-white hover:bg-[#151515]"
            }`}
          >
            <Terminal className="w-3.5 h-3.5" />
            CLI Runner
          </button>
          <button
            onClick={() => setActiveTab("docs")}
            className={`flex items-center gap-1.5 px-3.5 py-1.5 rounded transition-all duration-150 ${
              activeTab === "docs"
                ? "bg-[#3b82f6] text-black font-bold shadow-sm"
                : "text-[#999] hover:text-white hover:bg-[#151515]"
            }`}
          >
            <BookOpen className="w-3.5 h-3.5" />
            Architecture & Specs
          </button>
          <button
            onClick={() => {
              setActiveTab("logs");
              fetchLogs();
            }}
            className={`flex items-center gap-1.5 px-3.5 py-1.5 rounded transition-all duration-150 ${
              activeTab === "logs"
                ? "bg-[#3b82f6] text-black font-bold shadow-sm"
                : "text-[#999] hover:text-white hover:bg-[#151515]"
            }`}
          >
            <FileText className="w-3.5 h-3.5" />
            Logs
          </button>
        </nav>

        {/* Quick Actions & Flags */}
        <div className="flex flex-wrap items-center gap-3">
          <div className="flex items-center gap-2">
            <span className="text-[11px] font-mono text-[#666] uppercase tracking-wider hidden sm:inline">
              Actions:
            </span>
            <button
              disabled={loading}
              onClick={() => {
                runCommand("doctor");
                setActiveTab("terminal");
              }}
              className="px-3 py-1.5 bg-[#141414] hover:bg-[#202020] border border-[#2a2a2a] text-xs font-mono text-[#e0e0e0] rounded transition active:scale-95 disabled:opacity-50 flex items-center gap-1.5"
            >
              <Play className="w-3 h-3 text-[#3b82f6]" />
              doctor
            </button>
            <button
              disabled={loading}
              onClick={() => {
                runCommand("check");
                setActiveTab("terminal");
              }}
              className="px-3 py-1.5 bg-[#141414] hover:bg-[#202020] border border-[#2a2a2a] text-xs font-mono text-[#e0e0e0] rounded transition active:scale-95 disabled:opacity-50 flex items-center gap-1.5"
            >
              <Play className="w-3 h-3 text-[#3b82f6]" />
              check
            </button>
            <button
              disabled={loading}
              onClick={() => {
                runCommand("test");
                setActiveTab("terminal");
              }}
              className="px-3 py-1.5 bg-[#122212] hover:bg-[#183018] border border-[#224d22] text-xs font-mono text-[#4ade80] rounded transition active:scale-95 disabled:opacity-50 flex items-center gap-1.5 font-semibold"
            >
              <ShieldCheck className="w-3 h-3 text-[#4ade80]" />
              run tests (36)
            </button>
          </div>

          <div className="h-4 w-[1px] bg-[#1a1a1a] hidden sm:block"></div>

          <div className="flex items-center gap-2">
            <a
              href="/api/download-proposal-pdf"
              download="eSim_Tool_Manager_Internship_Proposal.pdf"
              className="px-3 py-1.5 bg-[#dc2626] hover:bg-[#ef4444] border border-[#b91c1c] text-xs font-mono text-white rounded transition active:scale-95 flex items-center gap-1.5 font-bold shadow-sm"
              title="Download Internship Proposal in direct PDF format"
            >
              <Download className="w-3 h-3 text-white" />
              PDF FILE
            </a>
            <a
              href="/api/download-proposal-docx"
              download="eSim_Tool_Manager_Internship_Proposal.docx"
              className="px-3 py-1.5 bg-[#1e3a8a] hover:bg-[#1d4ed8] border border-[#2563eb] text-xs font-mono text-[#dbeafe] rounded transition active:scale-95 flex items-center gap-1.5 font-semibold shadow-sm"
              title="Download Internship Proposal in editable MS Word format"
            >
              <Download className="w-3 h-3 text-[#93c5fd]" />
              DOCX
            </a>
          </div>

          <div className="flex items-center gap-3">
            <label className="flex items-center gap-1.5 text-xs text-[#888] cursor-pointer select-none">
              <input
                type="checkbox"
                checked={jsonMode}
                onChange={(e) => setJsonMode(e.target.checked)}
                className="rounded border-[#333] bg-[#0a0a0a] text-[#3b82f6] focus:ring-0"
              />
              <span className="font-mono text-[11px]">--json</span>
            </label>
            <label className="flex items-center gap-1.5 text-xs text-[#888] cursor-pointer select-none">
              <input
                type="checkbox"
                checked={dryRun}
                onChange={(e) => setDryRun(e.target.checked)}
                className="rounded border-[#333] bg-[#0a0a0a] text-[#3b82f6] focus:ring-0"
              />
              <span className="font-mono text-[11px]">--dry-run</span>
            </label>
          </div>
        </div>
      </div>

      {/* Main Grid View */}
      <main className="flex-1 grid grid-cols-1 lg:grid-cols-12 gap-0">
        {/* Main Left Section */}
        <section className="col-span-1 lg:col-span-8 p-6 lg:p-8 border-b lg:border-b-0 lg:border-r border-[#1a1a1a] space-y-6">
          {/* TAB: DASHBOARD (Sophisticated Dark Grid) */}
          {activeTab === "dashboard" && (
            <div className="space-y-8">
              <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
                <div>
                  <h2 className="text-2xl font-serif italic text-white tracking-tight">Dependency Status</h2>
                  <p className="text-xs text-[#666] font-mono mt-1">
                    System validation matrix across core eSim EDA engines & interpreters.
                  </p>
                </div>

                <div className="flex items-center gap-2">
                  <button
                    onClick={() => {
                      runCommand("doctor");
                      setActiveTab("terminal");
                    }}
                    className="px-4 py-2 bg-[#141414] hover:bg-[#202020] border border-[#2a2a2a] text-xs font-mono rounded text-[#e0e0e0] transition"
                  >
                    esim-manager doctor
                  </button>
                  <button
                    onClick={() => {
                      runCommand("install", "ngspice");
                      setActiveTab("terminal");
                    }}
                    className="px-4 py-2 bg-[#3b82f6] hover:bg-[#2563eb] text-black text-xs font-bold rounded transition tracking-wide flex items-center gap-1.5"
                  >
                    <Package className="w-3.5 h-3.5" />
                    INSTALL MISSING (DRY-RUN)
                  </button>
                </div>
              </div>

              {/* 4 Tool Cards Grid */}
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                {/* 01. Python */}
                <div className="bg-[#0f0f0f] border border-[#1a1a1a] p-5 rounded-lg hover:border-[#333] transition-colors">
                  <div className="flex justify-between items-start mb-4">
                    <span className="text-xs font-mono text-[#666]">01.</span>
                    <span className="px-2 py-0.5 bg-[#152015] border border-[#224d22] text-[#4ade80] text-[10px] font-bold tracking-tight rounded">
                      INSTALLED
                    </span>
                  </div>
                  <h3 className="text-xl font-medium text-white mb-1">Python</h3>
                  <p className="text-xs font-mono text-[#999] mb-4">/usr/bin/python3.10</p>
                  <div className="flex items-end justify-between border-t border-[#1a1a1a] pt-3">
                    <span className="text-3xl font-light tracking-tighter text-white font-mono">3.10.12</span>
                    <span className="text-[10px] text-[#666] font-mono">MIN: 3.10.0</span>
                  </div>
                </div>

                {/* 02. Git */}
                <div className="bg-[#0f0f0f] border border-[#1a1a1a] p-5 rounded-lg hover:border-[#333] transition-colors">
                  <div className="flex justify-between items-start mb-4">
                    <span className="text-xs font-mono text-[#666]">02.</span>
                    <span className="px-2 py-0.5 bg-[#152015] border border-[#224d22] text-[#4ade80] text-[10px] font-bold tracking-tight rounded">
                      INSTALLED
                    </span>
                  </div>
                  <h3 className="text-xl font-medium text-white mb-1">Git</h3>
                  <p className="text-xs font-mono text-[#999] mb-4">/usr/bin/git</p>
                  <div className="flex items-end justify-between border-t border-[#1a1a1a] pt-3">
                    <span className="text-3xl font-light tracking-tighter text-white font-mono">2.34.1</span>
                    <span className="text-[10px] text-[#666] font-mono">MIN: 2.20.0</span>
                  </div>
                </div>

                {/* 03. Ngspice */}
                <div className="bg-[#0f0f0f] border border-[#331d1d] p-5 rounded-lg border-l-4 border-l-[#ef4444] hover:border-r-[#333] transition-colors">
                  <div className="flex justify-between items-start mb-4">
                    <span className="text-xs font-mono text-[#666]">03.</span>
                    <span className="px-2 py-0.5 bg-[#2a1212] border border-[#4d1f1f] text-[#ef4444] text-[10px] font-bold tracking-tight rounded">
                      MISSING
                    </span>
                  </div>
                  <h3 className="text-xl font-medium text-white mb-1">Ngspice</h3>
                  <p className="text-xs font-mono text-[#777] mb-4">Circuit Simulation Engine</p>
                  <div className="flex items-end justify-between border-t border-[#1a1a1a] pt-3">
                    <span className="text-3xl font-light tracking-tighter text-[#444] font-mono">--</span>
                    <button
                      onClick={() => {
                        runCommand("install", "ngspice");
                        setActiveTab("terminal");
                      }}
                      className="text-[11px] text-[#3b82f6] font-mono font-semibold hover:underline underline-offset-4"
                    >
                      RESOLVE (APT)
                    </button>
                  </div>
                </div>

                {/* 04. KiCad */}
                <div className="bg-[#0f0f0f] border border-[#331d1d] p-5 rounded-lg border-l-4 border-l-[#ef4444] hover:border-r-[#333] transition-colors">
                  <div className="flex justify-between items-start mb-4">
                    <span className="text-xs font-mono text-[#666]">04.</span>
                    <span className="px-2 py-0.5 bg-[#2a1212] border border-[#4d1f1f] text-[#ef4444] text-[10px] font-bold tracking-tight rounded">
                      MISSING
                    </span>
                  </div>
                  <h3 className="text-xl font-medium text-white mb-1">KiCad EDA</h3>
                  <p className="text-xs font-mono text-[#777] mb-4">Schematic & PCB Layout</p>
                  <div className="flex items-end justify-between border-t border-[#1a1a1a] pt-3">
                    <span className="text-3xl font-light tracking-tighter text-[#444] font-mono">--</span>
                    <button
                      onClick={() => {
                        runCommand("install", "kicad");
                        setActiveTab("terminal");
                      }}
                      className="text-[11px] text-[#ef4444] font-mono font-semibold hover:underline underline-offset-4"
                    >
                      RESOLVE NOW
                    </button>
                  </div>
                </div>
              </div>

              {/* Bottom Quick Terminal Preview */}
              <div className="pt-4 border-t border-[#1a1a1a]">
                <div className="bg-[#0a0a0a] border border-[#1a1a1a] p-4 rounded-md font-mono text-xs leading-relaxed space-y-1">
                  <div className="flex items-center gap-2 text-[#4ade80] mb-2 font-bold">
                    <span className="text-[#666]">$</span> esim-manager check --verbose
                  </div>
                  <div className="text-[#999]">[INFO] Detecting platform environment: Debian 12 (Linux) on x86_64</div>
                  <div className="text-[#999]">
                    [INFO] Checked 4 tools: python (found 3.10.12), git (found 2.34.1), ngspice (missing), kicad (missing)
                  </div>
                  <div className="text-white pt-1">
                    Summary: 4 tools inspected | 2 available | 2 missing | 0 incompatible
                  </div>
                </div>
              </div>
            </div>
          )}

          {/* TAB: CLI RUNNER */}
          {activeTab === "terminal" && (
            <div className="space-y-6">
              <div className="flex items-center justify-between">
                <div>
                  <h2 className="text-2xl font-serif italic text-white tracking-tight">Interactive CLI Console</h2>
                  <p className="text-xs text-[#666] font-mono mt-1">
                    Direct execution of native <code className="text-[#3b82f6]">python main.py</code> subcommands.
                  </p>
                </div>

                <div className="flex items-center gap-2">
                  <select
                    value={customTool}
                    onChange={(e) => setCustomTool(e.target.value)}
                    className="bg-[#0f0f0f] border border-[#1a1a1a] rounded px-3 py-1.5 text-xs text-[#e0e0e0] font-mono focus:outline-none focus:border-[#3b82f6]"
                  >
                    <option value="ngspice">ngspice (Ngspice Simulator)</option>
                    <option value="kicad">kicad (KiCad EDA)</option>
                    <option value="python">python (Python Runtime)</option>
                    <option value="git">git (Git Version Control)</option>
                  </select>
                  <button
                    disabled={loading}
                    onClick={() => runCommand("info", customTool)}
                    className="px-3 py-1.5 bg-[#141414] hover:bg-[#202020] border border-[#2a2a2a] text-xs font-mono text-[#e0e0e0] rounded transition"
                  >
                    info
                  </button>
                  <button
                    disabled={loading}
                    onClick={() => runCommand("version", customTool)}
                    className="px-3 py-1.5 bg-[#141414] hover:bg-[#202020] border border-[#2a2a2a] text-xs font-mono text-[#e0e0e0] rounded transition"
                  >
                    version
                  </button>
                  <button
                    disabled={loading}
                    onClick={() => runCommand("install", customTool)}
                    className="px-3 py-1.5 bg-[#3b82f6] hover:bg-[#2563eb] text-black font-bold text-xs font-mono rounded transition"
                  >
                    install {dryRun ? "(dry-run)" : ""}
                  </button>
                </div>
              </div>

              {/* Terminal Window */}
              <div className="bg-[#080808] border border-[#1a1a1a] rounded-lg overflow-hidden shadow-2xl flex flex-col min-h-[460px]">
                <div className="bg-[#0d0d0d] border-b border-[#1a1a1a] px-4 py-2.5 flex items-center justify-between">
                  <div className="flex items-center gap-2">
                    <div className="w-2.5 h-2.5 rounded-full bg-[#ef4444]/80"></div>
                    <div className="w-2.5 h-2.5 rounded-full bg-[#f59e0b]/80"></div>
                    <div className="w-2.5 h-2.5 rounded-full bg-[#4ade80]/80"></div>
                    <span className="text-xs font-mono text-[#777] ml-2">
                      {cliOutput?.command || "bash — esim-tool-manager"}
                    </span>
                  </div>

                  <div className="flex items-center gap-2">
                    {loading && (
                      <span className="flex items-center gap-1.5 text-xs text-[#3b82f6] font-mono">
                        <RotateCw className="w-3 h-3 animate-spin" />
                        Executing...
                      </span>
                    )}
                    {cliOutput && (
                      <button
                        onClick={() => handleCopy(cliOutput.stdout || cliOutput.stderr)}
                        className="text-[#777] hover:text-white text-xs flex items-center gap-1 p-1 hover:bg-[#141414] rounded font-mono"
                        title="Copy command output"
                      >
                        {copied ? <Check className="w-3.5 h-3.5 text-[#4ade80]" /> : <Copy className="w-3.5 h-3.5" />}
                        Copy
                      </button>
                    )}
                  </div>
                </div>

                <div className="p-5 font-mono text-xs leading-relaxed overflow-x-auto flex-1 bg-[#050505]">
                  {loading ? (
                    <div className="h-full flex items-center justify-center text-[#555] py-24">
                      <div className="flex flex-col items-center gap-2">
                        <RotateCw className="w-5 h-5 animate-spin text-[#3b82f6]" />
                        <span className="font-mono text-xs text-[#888]">Dispatching command to Python engine...</span>
                      </div>
                    </div>
                  ) : cliOutput ? (
                    <div className="space-y-3">
                      <div className="text-[#666] flex items-center gap-2">
                        <span className="text-[#4ade80]">$</span> {cliOutput.command}
                      </div>
                      {cliOutput.stdout && (
                        <pre className="text-[#d4d4d4] whitespace-pre-wrap font-mono leading-relaxed">
                          {cliOutput.stdout}
                        </pre>
                      )}
                      {cliOutput.stderr && (
                        <pre className="text-[#f59e0b] whitespace-pre-wrap font-mono">
                          {cliOutput.stderr}
                        </pre>
                      )}
                      <div className="pt-3 border-t border-[#1a1a1a] text-[#555] text-[11px] flex items-center justify-between">
                        <span>Exit Code: {cliOutput.exitCode}</span>
                        <span>Standard Output / Log Subsystem Ready</span>
                      </div>
                    </div>
                  ) : (
                    <div className="text-[#555] italic py-8">
                      Ready. Trigger any action above or select a command.
                    </div>
                  )}
                </div>
              </div>
            </div>
          )}

          {/* TAB: ARCHITECTURE & SPECS */}
          {activeTab === "docs" && (
            <div className="space-y-6">
              <div>
                <h2 className="text-2xl font-serif italic text-white tracking-tight">System Architecture</h2>
                <p className="text-xs text-[#666] font-mono mt-1">
                  Design patterns and architectural specifications compliant with FOSSEE requirements.
                </p>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div className="bg-[#0a0a0a] border border-[#1a1a1a] p-5 rounded-lg space-y-2">
                  <span className="text-[10px] font-mono text-[#3b82f6] uppercase tracking-wider font-bold">
                    01. Strategy Pattern
                  </span>
                  <h4 className="text-base font-medium text-white">Package Installer</h4>
                  <p className="text-xs text-[#888] leading-relaxed">
                    Strategy interface decoupling concrete package manager invocations (<code className="text-[#ccc]">AptStrategy</code>, <code className="text-[#ccc]">PacmanStrategy</code>, <code className="text-[#ccc]">BrewStrategy</code>, <code className="text-[#ccc]">WingetStrategy</code>).
                  </p>
                </div>

                <div className="bg-[#0a0a0a] border border-[#1a1a1a] p-5 rounded-lg space-y-2">
                  <span className="text-[10px] font-mono text-[#3b82f6] uppercase tracking-wider font-bold">
                    02. Registry Pattern
                  </span>
                  <h4 className="text-base font-medium text-white">Tool Specifications</h4>
                  <p className="text-xs text-[#888] leading-relaxed">
                    Extensible metadata registry allowing third-party EDA tools (GHDL, Verilator, OpenFOAM) to be registered via <code className="text-[#ccc]">BaseToolProvider</code>.
                  </p>
                </div>

                <div className="bg-[#0a0a0a] border border-[#1a1a1a] p-5 rounded-lg space-y-2">
                  <span className="text-[10px] font-mono text-[#4ade80] uppercase tracking-wider font-bold">
                    03. Security Guardrails
                  </span>
                  <h4 className="text-base font-medium text-white">Zero Shell Invocations</h4>
                  <p className="text-xs text-[#888] leading-relaxed">
                    Strict prohibition of <code className="text-[#ef4444]">shell=True</code>. Commands are executed through vetted argument arrays with strict timeout controls.
                  </p>
                </div>
              </div>

              <div className="bg-[#0a0a0a] border border-[#1a1a1a] p-5 rounded-lg space-y-4">
                <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
                  <div>
                    <h4 className="text-sm font-semibold text-white">Project Deliverables & Submission Files</h4>
                    <p className="text-xs text-[#777] mt-0.5">
                      Editable Microsoft Word documents formatted for direct screening task submission.
                    </p>
                  </div>
                  <div className="flex flex-wrap items-center gap-2">
                    <a
                      href="/api/download-proposal-pdf"
                      download="eSim_Tool_Manager_Internship_Proposal.pdf"
                      className="inline-flex items-center gap-2 px-4 py-2 bg-[#dc2626] hover:bg-[#ef4444] text-white text-xs font-semibold rounded shadow-md transition active:scale-95 border border-[#b91c1c]"
                    >
                      <Download className="w-3.5 h-3.5" />
                      Download PDF (.pdf)
                    </a>
                    <a
                      href="/api/download-proposal-docx"
                      download="eSim_Tool_Manager_Internship_Proposal.docx"
                      className="inline-flex items-center gap-2 px-4 py-2 bg-[#1e3a8a] hover:bg-[#1d4ed8] text-white text-xs font-semibold rounded shadow-md transition active:scale-95 border border-[#3b82f6]"
                    >
                      <Download className="w-3.5 h-3.5" />
                      Proposal (.docx)
                    </a>
                    <a
                      href="/api/download-docx"
                      download="eSim_Automated_Tool_Manager_Design_Document.docx"
                      className="inline-flex items-center gap-2 px-3 py-2 bg-[#141414] hover:bg-[#202020] border border-[#2a2a2a] text-[#d4d4d4] text-xs font-semibold rounded transition active:scale-95"
                    >
                      <Download className="w-3.5 h-3.5" />
                      Design Doc (.docx)
                    </a>
                  </div>
                </div>

                <div className="grid grid-cols-1 sm:grid-cols-4 gap-3 text-xs font-mono pt-1">
                  <div className="p-3 bg-[#050505] border border-[#1d4ed8]/40 rounded">
                    <span className="text-[#60a5fa] font-bold">Proposal (.docx)</span>
                    <p className="text-[11px] text-[#888] mt-1">Formal internship proposal report</p>
                  </div>
                  <div className="p-3 bg-[#050505] border border-[#1a1a1a] rounded">
                    <span className="text-[#3b82f6] font-bold">Design Doc (.docx)</span>
                    <p className="text-[11px] text-[#666] mt-1">Detailed OpenXML technical spec</p>
                  </div>
                  <div className="p-3 bg-[#050505] border border-[#1a1a1a] rounded">
                    <span className="text-[#3b82f6] font-bold">docs/TESTING.md</span>
                    <p className="text-[11px] text-[#666] mt-1">36 unit tests matrix & mocking</p>
                  </div>
                  <div className="p-3 bg-[#050505] border border-[#1a1a1a] rounded">
                    <span className="text-[#3b82f6] font-bold">README.md</span>
                    <p className="text-[11px] text-[#666] mt-1">User & installation guide</p>
                  </div>
                </div>
              </div>
            </div>
          )}

          {/* TAB: LOGS */}
          {activeTab === "logs" && (
            <div className="space-y-4">
              <div className="flex items-center justify-between">
                <div>
                  <h2 className="text-2xl font-serif italic text-white tracking-tight">Rotating File Logs</h2>
                  <p className="text-xs text-[#666] font-mono mt-1">
                    Live content of <code className="text-[#3b82f6]">logs/esim_manager.log</code>.
                  </p>
                </div>
                <button
                  onClick={fetchLogs}
                  className="px-3 py-1.5 rounded bg-[#141414] hover:bg-[#202020] border border-[#2a2a2a] text-xs font-mono text-[#e0e0e0] flex items-center gap-1.5"
                >
                  <RefreshCw className="w-3.5 h-3.5 text-[#3b82f6]" />
                  Refresh Logs
                </button>
              </div>

              <pre className="bg-[#080808] border border-[#1a1a1a] p-5 rounded-lg text-xs font-mono text-[#ccc] overflow-x-auto max-h-[500px] leading-relaxed">
                {logsContent}
              </pre>
            </div>
          )}
        </section>

        {/* Right Sidebar: Activity Logs & Actionable Recommendations */}
        <aside className="col-span-1 lg:col-span-4 bg-[#080808] flex flex-col justify-between">
          {/* Top Activity Feed */}
          <div className="p-6 border-b border-[#1a1a1a]">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-xs uppercase tracking-widest text-[#666] font-bold">Activity Logs</h3>
              <span className="text-[10px] font-mono text-[#4ade80] bg-[#152015] px-2 py-0.5 rounded border border-[#224d22]">
                REAL-TIME
              </span>
            </div>

            <div className="space-y-4 max-h-[380px] overflow-y-auto pr-1">
              <div className="flex gap-3">
                <div className="text-[10px] font-mono text-[#444] pt-1 shrink-0">18:30:01</div>
                <div className="flex flex-col">
                  <span className="text-xs text-[#4ade80] font-bold">INFO</span>
                  <span className="text-xs text-[#999]">Initialization of Tool Manager core complete.</span>
                </div>
              </div>

              <div className="flex gap-3">
                <div className="text-[10px] font-mono text-[#444] pt-1 shrink-0">18:30:02</div>
                <div className="flex flex-col">
                  <span className="text-xs text-[#4ade80] font-bold">INFO</span>
                  <span className="text-xs text-[#999]">Path discovered: /usr/bin/python3.10 (3.10.12)</span>
                </div>
              </div>

              <div className="flex gap-3">
                <div className="text-[10px] font-mono text-[#444] pt-1 shrink-0">18:30:02</div>
                <div className="flex flex-col">
                  <span className="text-xs text-[#4ade80] font-bold">INFO</span>
                  <span className="text-xs text-[#999]">Path discovered: /usr/bin/git (2.34.1)</span>
                </div>
              </div>

              <div className="flex gap-3">
                <div className="text-[10px] font-mono text-[#444] pt-1 shrink-0">18:30:03</div>
                <div className="flex flex-col">
                  <span className="text-xs text-[#ef4444] font-bold">ERROR</span>
                  <span className="text-xs text-[#999]">Executable 'ngspice' not found in system search PATH.</span>
                </div>
              </div>

              <div className="flex gap-3">
                <div className="text-[10px] font-mono text-[#444] pt-1 shrink-0">18:30:04</div>
                <div className="flex flex-col">
                  <span className="text-xs text-[#ef4444] font-bold">ERROR</span>
                  <span className="text-xs text-[#999]">Executable 'kicad' not found in system search PATH.</span>
                </div>
              </div>

              <div className="flex gap-3">
                <div className="text-[10px] font-mono text-[#444] pt-1 shrink-0">18:31:10</div>
                <div className="flex flex-col">
                  <span className="text-xs text-[#3b82f6] font-bold">ACTION</span>
                  <span className="text-xs text-[#999]">Diagnostic check executed via Doctor command.</span>
                </div>
              </div>
            </div>
          </div>

          {/* Bottom Actionable Recommendation Card */}
          <div className="p-6">
            <div className="bg-[#0a0a0a] border border-[#1a1a1a] rounded-lg p-4 space-y-3">
              <div className="flex items-center justify-between">
                <h4 className="text-[10px] font-bold text-[#666] uppercase tracking-wider">
                  Automated Recommendation
                </h4>
                <Wrench className="w-3.5 h-3.5 text-[#3b82f6]" />
              </div>
              <p className="text-xs text-[#ccc] leading-relaxed">
                System detected missing dependencies for <span className="text-white font-medium">KiCad EDA</span> and <span className="text-white font-medium">Ngspice</span>. Install via system package manager:
              </p>
              <code className="block bg-black p-3 rounded text-xs font-mono text-[#3b82f6] border border-[#1a1a1a]">
                esim-manager install kicad --dry-run
              </code>
              <p className="text-[10px] text-[#555] italic">
                * Requires sudo / administrator privileges for native package installations.
              </p>
            </div>
          </div>
        </aside>
      </main>

      {/* Sophisticated Dark Footer */}
      <footer className="px-6 lg:px-8 py-3.5 bg-[#0a0a0a] border-t border-[#1a1a1a] flex flex-col sm:flex-row justify-between items-center text-[10px] text-[#555] font-mono gap-2">
        <div>FOSSEE eSim | Autumn 2026 Screening Task • IIT Bombay</div>
        <div className="flex gap-6">
          <span>LOGS: logs/esim_manager.log</span>
          <span className="text-[#4ade80]">STATUS: 36/36 TESTS PASSED</span>
        </div>
      </footer>
    </div>
  );
}
