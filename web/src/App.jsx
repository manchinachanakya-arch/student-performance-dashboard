import { useMemo, useRef, useState } from "react";
import Papa from "papaparse";
import {
  Activity, ArrowDownToLine, ArrowUpRight, BookOpen, Check, ChevronDown,
  CircleHelp, GraduationCap, LayoutDashboard, Search, SlidersHorizontal,
  Sparkles, Upload, Users, X
} from "lucide-react";
import {
  Area, AreaChart, CartesianGrid, ResponsiveContainer, Scatter, ScatterChart,
  Tooltip, XAxis, YAxis, BarChart, Bar, Cell
} from "recharts";

const sampleStudents = [
  ["S001","Aarav","10-A",92,88,91,84,79,95],["S002","Diya","10-A",86,76,82,90,85,88],
  ["S003","Vihaan","10-A",68,35,42,51,48,55],["S004","Anaya","10-A",74,58,62,67,60,71],
  ["S005","Ishaan","10-A",97,94,89,92,87,96],["S006","Meera","10-A",81,66,73,78,82,80],
  ["S007","Arjun","10-A",59,28,33,45,39,41],["S008","Saanvi","10-A",88,81,85,89,91,93],
  ["S009","Kabir","10-A",76,42,38,55,49,61],["S010","Myra","10-A",93,90,94,88,86,92],
  ["S011","Reyansh","10-B",84,72,69,77,74,81],["S012","Pari","10-B",71,39,44,52,47,58],
  ["S013","Atharv","10-B",95,91,87,90,93,89],["S014","Kiara","10-B",79,63,70,68,75,72],
  ["S015","Advik","10-B",64,31,36,43,40,48],["S016","Navya","10-B",90,85,82,94,88,91],
  ["S017","Rudra","10-B",73,55,49,61,58,66],["S018","Ira","10-B",98,96,92,95,90,97],
  ["S019","Ayaan","10-B",82,67,74,71,69,78],["S020","Tara","10-B",69,46,41,53,50,57]
].map(([student_id,student_name,student_class,attendance_pct,maths,science,english,social,computer]) => ({
  student_id, student_name, class: student_class, attendance_pct, maths, science, english, social, computer
}));

const subjects = ["maths", "science", "english", "social", "computer"];
const subjectNames = ["Maths", "Science", "English", "Social", "Computer"];
const average = (row) => subjects.reduce((sum, key) => sum + Number(row[key] || 0), 0) / subjects.length;
const enrich = (rows) => rows.map((row) => {
  const average_score = Number(average(row).toFixed(1));
  const attendance_pct = Number(row.attendance_pct);
  return { ...row, average_score, attendance_pct, support_needed: attendance_pct < 75 || average_score < 40 };
});

function Metric({ icon: Icon, label, value, note, accent }) {
  return <article className="metric-card tilt-card" style={{ "--accent": accent }}>
    <div className="metric-top"><span className="metric-icon"><Icon size={17}/></span><span className="metric-note">{note}</span></div>
    <div className="metric-value">{value}</div><div className="metric-label">{label}</div>
  </article>;
}

function App() {
  const [rows, setRows] = useState(() => enrich(sampleStudents));
  const [selectedClass, setSelectedClass] = useState("All classes");
  const [supportOnly, setSupportOnly] = useState(false);
  const [search, setSearch] = useState("");
  const [fileName, setFileName] = useState("Sample dataset");
  const [notice, setNotice] = useState("");
  const fileRef = useRef(null);

  const classes = useMemo(() => ["All classes", ...new Set(rows.map((r) => r.class))], [rows]);
  const filtered = useMemo(() => rows.filter((r) =>
    (selectedClass === "All classes" || r.class === selectedClass) &&
    (!supportOnly || r.support_needed) &&
    (r.student_name.toLowerCase().includes(search.toLowerCase()) || r.student_id.toLowerCase().includes(search.toLowerCase()))
  ), [rows, selectedClass, supportOnly, search]);

  const metrics = useMemo(() => ({
    count: filtered.length,
    score: filtered.length ? filtered.reduce((s,r) => s + r.average_score, 0) / filtered.length : 0,
    attendance: filtered.length ? filtered.reduce((s,r) => s + r.attendance_pct, 0) / filtered.length : 0,
    support: filtered.filter((r) => r.support_needed).length
  }), [filtered]);

  const subjectData = subjects.map((key, i) => ({
    subject: subjectNames[i],
    score: filtered.length ? filtered.reduce((sum, row) => sum + Number(row[key]), 0) / filtered.length : 0
  }));
  const trendData = [
    { label: "Mon", score: Math.max(0, metrics.score - 5.2) },
    { label: "Tue", score: Math.max(0, metrics.score - 2.8) },
    { label: "Wed", score: Math.max(0, metrics.score - 3.6) },
    { label: "Thu", score: Math.max(0, metrics.score - 1.1) },
    { label: "Fri", score: metrics.score }
  ];

  const handleUpload = (file) => {
    if (!file) return;
    Papa.parse(file, {
      header: true, skipEmptyLines: true,
      complete: ({ data, errors }) => {
        const required = ["student_id","student_name","class","attendance_pct",...subjects];
        if (errors.length || !data.length || !required.every((key) => key in data[0])) {
          setNotice("This CSV does not match the required student-data format.");
          return;
        }
        const valid = data.filter((r) => required.every((key) => String(r[key] ?? "").trim() !== "") &&
          required.slice(3).every((key) => Number.isFinite(Number(r[key]))));
        if (!valid.length) { setNotice("No valid student rows were found in that CSV."); return; }
        setRows(enrich(valid.map((r) => ({...r, attendance_pct: Number(r.attendance_pct), ...Object.fromEntries(subjects.map(k => [k, Number(r[k])]))}))));
        setSelectedClass("All classes"); setSupportOnly(false); setSearch("");
        setFileName(file.name); setNotice(`Imported ${valid.length} student records.`);
      }
    });
  };

  const downloadCsv = () => {
    const columns = ["student_id","student_name","class","attendance_pct",...subjects,"average_score","support_needed"];
    const csv = Papa.unparse(filtered.map((r) => Object.fromEntries(columns.map((k) => [k, r[k]]))));
    const url = URL.createObjectURL(new Blob([csv], { type: "text/csv;charset=utf-8;" }));
    const link = document.createElement("a"); link.href = url; link.download = "student-performance-report.csv"; link.click();
    URL.revokeObjectURL(url);
  };

  const reset = () => { setRows(enrich(sampleStudents)); setFileName("Sample dataset"); setSelectedClass("All classes"); setSupportOnly(false); setSearch(""); setNotice("Sample dataset restored."); };

  return <div className="app-shell">
    <aside className="sidebar">
      <div className="brand"><div className="brand-symbol">f.</div><div><strong>FORMA</strong><small>STUDENT INSIGHTS</small></div></div>
      <div className="side-label">WORKSPACE</div>
      <a className="nav-item active" href="#overview"><LayoutDashboard size={17}/> Overview <span className="nav-dot"/></a>
      <a className="nav-item" href="#students"><Users size={17}/> Student records</a>
      <a className="nav-item" href="#subjects"><BookOpen size={17}/> Subject insights</a>
      <div className="sidebar-bottom">
        <div className="help-card"><div className="help-icon"><CircleHelp size={16}/></div><strong>Made for clarity.</strong><p>A considered view of progress, patterns and potential.</p></div>
        <div className="profile"><div className="avatar">SI</div><div><strong>Insights Studio</strong><small>Academic workspace</small></div><ChevronDown size={15}/></div>
      </div>
    </aside>

    <main className="main-content">
      <header className="topbar"><div className="breadcrumb">Workspace <span>/</span> Overview</div><div className="top-actions"><span className="dataset-pill"><span/> {fileName}</span><button className="icon-button" title="Upload CSV" onClick={() => fileRef.current?.click()}><Upload size={17}/></button><input ref={fileRef} type="file" accept=".csv,text/csv" hidden onChange={(e) => handleUpload(e.target.files?.[0])}/><button className="avatar small-avatar" title="Insights Studio">SI</button></div></header>

      <section className="hero" id="overview">
        <div className="hero-copy">
          <div className="eyebrow"><Sparkles size={13}/> THE ACADEMIC OVERVIEW</div>
          <h1>Every student has<br/><em>a story to tell.</em></h1>
          <p>A thoughtful perspective on achievement, attendance and the small signals that help every learner move forward.</p>
          <div className="hero-meta"><span className="meta-line"/> <span>YOUR DATA, IN A CLEARER LIGHT</span></div>
        </div>
        <div className="hero-art" aria-hidden="true">
          <div className="art-orbit orbit-one"/><div className="art-orbit orbit-two"/>
          <div className="art-disc"><div className="disc-inner"><GraduationCap size={43} strokeWidth={1.15}/><span>LEARN<br/>GROW<br/>THRIVE</span></div></div>
          <div className="floating-note note-top"><span className="note-dot"/> A little progress<br/><b>goes a long way.</b></div>
          <div className="floating-note note-bottom"><span className="note-number">01</span><span>INSIGHT<br/><b>IN MOTION</b></span></div>
          <div className="art-spark spark-a">✳</div><div className="art-spark spark-b">✳</div>
        </div>
      </section>

      <section className="metrics-grid" aria-label="Performance summary">
        <Metric icon={Users} label="Students in view" value={metrics.count} note="CURRENT COHORT" accent="#b49b70"/>
        <Metric icon={Activity} label="Average achievement" value={`${metrics.score.toFixed(1)}%`} note="FIVE SUBJECTS" accent="#82917b"/>
        <Metric icon={GraduationCap} label="Attendance rate" value={`${metrics.attendance.toFixed(1)}%`} note="COHORT AVERAGE" accent="#8d9da8"/>
        <Metric icon={Sparkles} label="May need support" value={metrics.support} note="ILLUSTRATIVE RULE" accent="#b58c7c"/>
      </section>

      <section className="insights-section" id="subjects">
        <div className="section-heading"><div><div className="eyebrow">A CLOSER LOOK</div><h2>Patterns worth noticing</h2></div><span className="section-caption">ANALYTICS / 01</span></div>
        <div className="charts-grid">
          <article className="surface chart-surface tilt-card">
            <div className="surface-heading"><div><h3>Subject performance</h3><p>Average marks across the selected group</p></div><span className="chart-index">A</span></div>
            <div className="chart-wrap"><ResponsiveContainer width="100%" height="100%"><BarChart data={subjectData} margin={{top:10,right:8,left:-22,bottom:0}}><CartesianGrid vertical={false} stroke="#e9e4d9"/><XAxis dataKey="subject" tickLine={false} axisLine={false} tick={{fill:"#8d887d",fontSize:11}}/><YAxis domain={[0,100]} tickLine={false} axisLine={false} tick={{fill:"#aaa397",fontSize:10}}/><Tooltip cursor={{fill:"#f3efe6"}} contentStyle={{border:"1px solid #e8e1d4",borderRadius:12,background:"#fffdf8"}} formatter={(v) => [`${Number(v).toFixed(1)}%`, "Average"]}/><Bar dataKey="score" radius={[7,7,2,2]} maxBarSize={42}>{subjectData.map((entry,i)=><Cell key={entry.subject} fill={["#b8a27c","#899985","#9aa9ae","#c3a08e","#777f70"][i]}/>)}</Bar></BarChart></ResponsiveContainer></div>
            <div className="chart-foot"><span><i className="legend-dot sage"/> SUBJECT AVERAGE</span><span>OUT OF 100</span></div>
          </article>
          <article className="surface chart-surface tilt-card">
            <div className="surface-heading"><div><h3>Attendance & achievement</h3><p>Each point represents one student</p></div><span className="chart-index">B</span></div>
            <div className="chart-wrap"><ResponsiveContainer width="100%" height="100%"><ScatterChart margin={{top:12,right:12,bottom:4,left:-16}}><CartesianGrid stroke="#e9e4d9" strokeDasharray="3 4"/><XAxis type="number" dataKey="attendance_pct" domain={[0,100]} tickLine={false} axisLine={false} tick={{fill:"#aaa397",fontSize:10}} label={{value:"ATTENDANCE %",position:"insideBottom",offset:-2,fill:"#9a9488",fontSize:9}}/><YAxis type="number" dataKey="average_score" domain={[0,100]} tickLine={false} axisLine={false} tick={{fill:"#aaa397",fontSize:10}}/><Tooltip cursor={{strokeDasharray:"3 3"}} content={({active,payload})=>active&&payload?.length?<div className="chart-tooltip"><b>{payload[0].payload.student_name}</b><span>Attendance {payload[0].payload.attendance_pct}%</span><span>Average {payload[0].payload.average_score}%</span></div>:null}/><Scatter data={filtered} fill="#8d9b82">{filtered.map((r,i)=><Cell key={r.student_id} fill={r.support_needed?"#bd907b":"#879985"}/>)}</Scatter></ScatterChart></ResponsiveContainer></div>
            <div className="chart-foot"><span><i className="legend-dot sage"/> ON TRACK</span><span><i className="legend-dot clay"/> REVIEW</span></div>
          </article>
        </div>
      </section>

      <section className="records-section" id="students">
        <div className="section-heading"><div><div className="eyebrow">THE PEOPLE BEHIND THE NUMBERS</div><h2>Student directory</h2></div><span className="section-caption">RECORDS / 02</span></div>
        <div className="surface records-surface">
          <div className="records-toolbar">
            <div className="search-box"><Search size={16}/><input value={search} onChange={(e)=>setSearch(e.target.value)} placeholder="Search students or ID"/></div>
            <div className="filter-controls"><label className="select-wrap"><SlidersHorizontal size={14}/><select value={selectedClass} onChange={(e)=>setSelectedClass(e.target.value)}>{classes.map(c=><option key={c}>{c}</option>)}</select></label><label className="support-toggle"><input type="checkbox" checked={supportOnly} onChange={(e)=>setSupportOnly(e.target.checked)}/> Needs review</label><button className="export-button" onClick={downloadCsv}><ArrowDownToLine size={15}/> Export CSV</button></div>
          </div>
          {notice && <div className="notice"><Check size={14}/>{notice}<button onClick={()=>setNotice("")} aria-label="Dismiss"><X size={14}/></button></div>}
          <div className="table-scroll"><table><thead><tr><th>STUDENT</th><th>CLASS</th><th>ATTENDANCE</th><th>AVERAGE</th><th>STATUS</th><th/></tr></thead><tbody>
            {filtered.map((r)=> <tr key={r.student_id}><td><div className="student-cell"><div className="student-avatar">{r.student_name.slice(0,1)}</div><div><b>{r.student_name}</b><small>{r.student_id}</small></div></div></td><td>{r.class}</td><td><div className="progress-cell"><span>{r.attendance_pct}%</span><div className="mini-progress"><i style={{width:`${Math.max(0,Math.min(100,r.attendance_pct))}%`}}/></div></div></td><td><b className="score-value">{r.average_score.toFixed(1)}%</b></td><td><span className={`status ${r.support_needed?"review":"good"}`}><i/>{r.support_needed?"Review":"On track"}</span></td><td><ArrowUpRight size={15} className="row-arrow"/></td></tr>)}
          </tbody></table>{!filtered.length&&<div className="empty-state">No students match these filters.</div>}</div>
          <div className="table-footer"><span>SHOWING <b>{filtered.length}</b> OF <b>{rows.length}</b> STUDENTS</span><button onClick={reset} className="reset-button">Restore sample data</button></div>
        </div>
      </section>

      <footer className="footer"><div className="footer-mark">FORMA<span>.</span></div><p>Clarity creates room for progress.</p><span>STUDENT PERFORMANCE ANALYTICS · PORTFOLIO CONCEPT</span></footer>
      <div className="disclaimer">DEMO NOTICE · Sample records are fictional. The support indicator is an illustrative rule (attendance below 75% OR average below 40%), not an official academic assessment.</div>
    </main>
  </div>;
}

export default App;