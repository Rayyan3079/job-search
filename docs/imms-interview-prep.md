# IMMS interview prep – Netlist Carpentry circuit viewer

**Interview:** Friday 27 Nov 2026, 10:00, MS Teams, with Eric Schäfer (Head of Microelectronics, Erfurt branch).
**Role:** Student research assistant, topic IMMS_STUD_ME_1226 – extend the interactive circuit viewer of Netlist Carpentry
with a search bar, signal-path tracing and node marking/highlighting; test and document everything.
**What you sent:** [CV](../output/2026-10-31/imms-student-netlist-carpentry-circuit-viewer/CV-Muhammad-Rayyan-Ahmed.pdf),
[cover letter](../output/2026-10-31/imms-student-netlist-carpentry-circuit-viewer/Cover-Letter-Muhammad-Rayyan-Ahmed.pdf),
[posting](../jds/2026-10-31-imms-student-netlist-carpentry-circuit-viewer.md).

## 1. What the project actually is (from the official docs)

- Docs: https://imms-ilmenau.github.io/netlist-carpentry/ · GitHub: IMMS-Ilmenau/netlist-carpentry · `pip install netlist-carpentry`
- Python library to **read a digital circuit (Verilog), analyse/modify it in Python, and write Verilog back**.
  Uses **Yosys** to synthesise Verilog into a JSON netlist first. Python ≥ 3.9 (tested on 3.12). Dev tools: uv, ruff, mypy, pytest.
- Structure: `core` (data model: Circuit, Module, Instance, Port, Wire + `graph`), `io` (read/write), `routines`
  (optimization, scan-chain insertion, ...), `scripts`, `utils` (cfg, gate library, logging). Hexagonal architecture: the core has no I/O.
- **Module graph** = `module.graph()` → a NetworkX **MultiDiGraph** (directed: driver → load; multi-edges: several wires between two instances).
  Nodes = ports + instances; edges = wires. Node data: `ntype` (port/instance), `nsubtype` (gate type or port direction), `ndata` (the object).
- **The viewer you would extend:** `netlist_carpentry.vis.CytoscapeGraph`, built on **ipycytoscape** (interactive graphs in Jupyter).
  The older Dash Cytoscape viewer (`core.graph.visualization.Plotting`) is deprecated. Today, clicking a node shows a basic info box only.

## 2. How you would build the three features (have this ready to explain)

| Feature | Idea | NetworkX / Cytoscape pieces |
|---|---|---|
| **Search bar** | Text box (ipywidgets `Text`/`Combobox`); match node name, `nsubtype` (e.g. all `$and` gates) or port names; highlight matches and centre/zoom on them | `[n for n, d in G.nodes(data=True) if q in n or q in str(d['nsubtype'])]`; set a CSS class / style on matching Cytoscape nodes |
| **Signal-path tracing** | "Where does this signal come from / go to?" = **fan-in cone** (all predecessors) and **fan-out cone** (all successors) of a node; optionally the concrete path between two nodes | `nx.ancestors(G, n)`, `nx.descendants(G, n)`, `nx.shortest_path(G, a, b)` / `nx.all_simple_paths`; colour nodes and edges on the path |
| **Marking / highlighting** | Click or select instances to mark them, keep a set of marked nodes, clear/reset button, maybe different colours per mark group | ipycytoscape node classes + style rules; an observer on node click events |
| **Info box** | Show more data on click: type, ports, connected wires, bit widths, fan-in/fan-out counts | read from `G.nodes[n]['ndata']` (the Instance/Port object) |
| **Tests & docs** | pytest on small example circuits with known answers (e.g. the docs' `decentral_mux.v`): search returns the right nodes, the cone of output X contains inputs A and B; add a user-guide notebook like the existing ones | pytest, docs notebooks (mkdocs) |

Edge cases worth mentioning: multi-bit wires and multi-edges (MultiDiGraph), very large graphs (performance: compute cones once, cache),
constant/unconnected nodes, cycles (registers can create loops; `ancestors` still works on cyclic graphs).

## 3. Plan for the next 8 days

| Day | Do |
|---|---|
| 1 | Install Python 3.12 + Yosys (Windows: easiest via WSL Ubuntu `sudo apt install yosys`, or the OSS CAD Suite; Mac: `brew install yosys`). `pip install netlist-carpentry jupyter ipycytoscape`. |
| 2 | Work through the official user-guide notebooks: 01 Getting started, 02 Access circuit data, 05 Module graphs, 06 Graph visualization, Visualization 01 Plotting. Load `decentral_mux.v`, print ports/instances/wires, draw the graph. |
| 3–4 | **Mini prototype (your biggest advantage):** in one notebook, write `search_nodes(G, query)`, `fan_in(G, node)`, `fan_out(G, node)` and highlight the results in an ipycytoscape view of `decentral_mux`. Add 3–4 pytest tests. Push it to your GitHub as `netlist-viewer-experiments` with a short README. You must write and understand every line yourself – they will ask. |
| 5 | Basics so you can follow the conversation: what Verilog is, what synthesis (Yosys) does, netlist = cells/instances + ports + wires/nets, primitive gates (AND/OR/MUX/flip-flop), fan-in/fan-out, DAG. 1–2 hours of YouTube/articles is enough. |
| 6 | Prepare your answers (section 4) out loud, 1–2 minutes each, in English. |
| 7 | Mock interview (ask me) + Teams test call (camera, mic, quiet room, neutral background). |
| 8 | Rest; re-read this file and the job posting. |

## 4. Likely questions and what to say

- **"Tell us about yourself."** 60 seconds: Data Science M.Sc. at TU Ilmenau, B.S. AI; SAP data/analytics work in Pakistan
  (dashboards, data models, validation); recently built DocuMind; you enjoy building tools other people use and making sure they are tested.
- **"Why this topic?"** Concrete, well-scoped Python task on graphs; you like making complex structures understandable; open-source,
  research institute next to your university; you live in Ilmenau.
- **"Your Python experience?"** DocuMind: package structure, FastAPI, Streamlit, 37 pytest tests with mocks, GitHub Actions, Docker.
  Knowledge-graph project: NetworkX graphs, embeddings, clustering. Then: "I also tried Netlist Carpentry myself – may I show you?"
- **"Git?"** Commit history and CI on DocuMind; branches/pull requests: be honest about how much you have used them.
- **"How would you implement signal-path tracing?"** Section 2: ancestors/descendants on the MultiDiGraph, colour the cone, tests on a small circuit.
- **"How do you test a UI feature?"** Separate logic (search, cones) from display; unit-test the logic with pytest on example circuits; keep the widget layer thin.
- **"You have no microelectronics background."** True – you said so in the letter. You learned the basics (netlist, gates, synthesis)
  for this interview, the task is mostly Python/graphs, and you learn domains quickly (SAP BW → Datasphere, OCT images, cricket video).
- **"A problem you got stuck on?"** DocuMind's two wrong answers → you built evaluation, traced them to chunk boundaries, explained trade-offs.
- **"Hours / start / duration?"** Up to 20 h/week during semester, start immediately, as long as possible (whole Master's).
- **German?** Work language here can be English; say you are learning German (A1) and attending classes.

## 5. Your questions for them (pick 3)
1. Which parts of the viewer are most important to the team first – search, tracing or marking?
2. Who uses the viewer day to day (researchers, external partners)? How large are typical circuits?
3. Is the work mostly remote or in Erfurt/Ilmenau? How many hours per week and for how long?
4. Is it a student assistant contract (hourly rate)? *(near the end)*
5. Could this grow into other topics (e.g. constant propagation, SDF annotation) or a Master's thesis later?

## 6. On the day
- Join 5 minutes early, laptop charged, Teams updated, CV + cover letter + posting open, GitHub tab with DocuMind (and the prototype) ready to screen-share.
- A short German opening is a nice touch: "Guten Morgen, Herr Schäfer, vielen Dank für die Einladung." Then switch to English.
- Afterwards (same day): short thank-you email, mention one thing you discussed and that you are looking forward to hearing from them.
